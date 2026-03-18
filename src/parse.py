from enum import StrEnum
from typing import Any, Dict, Tuple
from generator import MazeConfig


class RequiredSettings(StrEnum):
    """List of required settings"""
    WIDTH = "WIDTH"
    HEIGHT = "HEIGHT"
    ENTRY = "ENTRY"
    EXIT = "EXIT"
    OUTPUT_FILE = "OUTPUT_FILE"
    PERFECT = "PERFECT"


class ParsingError(Exception):
    """Exception for parsing errors"""
    def __init__(self, msg: str):
        super().__init__(msg)


def process_values(settings: Dict[str, Any]) -> MazeConfig:
    """Validate and store config values"""
    try:
        width: int = int(settings["WIDTH"])
        height: int = int(settings["HEIGHT"])
        if width < 0 or height < 0:
            raise ValueError
    except ValueError:
        raise ParsingError(
            "(ValueError): WIDTH and HEIGHT must be non-negative integers"
        )

    def parse_coord(coord: str) -> Tuple[int, int]:
        """Validate and parse coordinates"""
        parts = coord.split(",")
        if len(parts) != 2:
            raise ParsingError(
                "Coords must contain 2 values separated with a comma"
            )
        try:
            coords = int(parts[0]), int(parts[1])
            if coords[0] < 0 or coords[1] < 0:
                raise ValueError
            return coords
        except ValueError:
            raise ParsingError(
                f"(ValueError): {parts} Coords must be non-negative integers"
            )

    entry = parse_coord(settings["ENTRY"])
    m_exit = parse_coord(settings["EXIT"])

    output_file = settings["OUTPUT_FILE"]
    if not output_file:
        raise ParsingError("OUTPUT_FILE must not be empty")
    if settings["PERFECT"] not in ["True", "False"]:
        raise ParsingError("PERFECT must be either 'True' or 'False'")
    perfect = settings["PERFECT"] == "True"

    return MazeConfig(width, height, entry, m_exit, output_file, perfect)


def read_and_parse_file(file: str) -> MazeConfig:
    """Attempts to read a file and parse its contents"""
    settings = {}
    required = [str(item) for item in list(RequiredSettings)]
    with open(file, "r") as f:
        for line in f:
            line = line.strip()

            if not line or line[0] == "#":
                continue

            if line.count("=") != 1:
                raise ParsingError("Only one '=' needed for each line")

            key, value = line.split("=")
            if key not in required:
                raise ParsingError(f"Unknown key: '{key}'")
            if key in settings:
                raise ParsingError(f"Repeated key: '{key}'")
            settings[key] = value

        missing = set(required).difference(settings.keys())
        if missing:
            raise ParsingError(f"Missing settings: {missing}")

    return process_values(settings)


def parse(file: str) -> MazeConfig:
    """Parse file to generate maze"""
    try:
        return read_and_parse_file(file)
    except FileNotFoundError:
        raise ParsingError(f"File {file} not found")
    except PermissionError as e:
        raise ParsingError(f"(PermissionError): {e}")
