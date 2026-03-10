from dataclasses import dataclass
from enum import StrEnum
from typing import Any, Dict, Tuple


class RequiredSettings(StrEnum):
    WIDTH = "WIDTH"
    HEIGHT = "HEIGHT"
    ENTRY = "ENTRY"
    EXIT = "EXIT"
    OUTPUT_FILE = "OUTPUT_FILE"
    PERFECT = "PERFECT"


class ParsingError(Exception):
    def __init__(self, msg: str):
        super().__init__(msg)


@dataclass
class MazeConfig:
    """Data class for storing the maze config"""
    width: int
    height: int
    entry: tuple[int, int]
    exit: tuple[int, int]
    output_file: str
    perfect: bool


def process_values(settings: Dict[str, Any]) -> MazeConfig:
    try:
        width: int = int(settings["WIDTH"])
        height: int = int(settings["HEIGHT"])
    except ValueError:
        raise ParsingError("(ValueError): invalid values for width and height")

    def parse_coord(coord: str) -> Tuple[int, int]:
        parts = coord.split(",")
        if len(parts) != 2:
            raise ParsingError("")
        try:
            return int(parts[0]), int(parts[1])
        except ValueError:
            raise ParsingError("(ValueError): invalid values for coordinates")

    entry = parse_coord(settings["ENTRY"])
    m_exit = parse_coord(settings["EXIT"])

    output_file = settings["OUTPUT_FILE"]
    if not output_file:
        raise ParsingError("OUTPUT_FILE must not be empty")
    if settings["PERFECT"] not in ["True", "False"]:
        raise ParsingError("PERFECT must be either 'True' or 'False'")
    perfect = settings["PERFECT"] == "True"

    return MazeConfig(width, height, entry, m_exit, output_file, perfect)


def parse(file: str) -> MazeConfig:
    """Parse file to generate maze"""
    settings = {}
    required = [str(item) for item in list(RequiredSettings)]
    with open(file, "r") as f:
        for line in f:
            line = line.strip()

            if not line:
                continue

            if line.count("=") != 1:
                raise ParsingError("Only one '=' needed for each line")

            key, value = line.split("=", 1)
            if key not in required:
                raise ParsingError(f"Unknown key: '{key}'")
            settings[key] = value

        missing = set(required).difference(settings.keys())
        if missing:
            raise ParsingError(f"Missing settings: {missing}")

    return process_values(settings)
