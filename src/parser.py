from typing import Any, List, Dict, Tuple, get_type_hints, get_origin
from generator import MazeConfig


class ParsingError(Exception):
    """Exception for parsing errors"""
    def __init__(self, msg: str):
        super().__init__(msg)


class ConfigParser:
    def __init__(self) -> None:
        self.required = []
        self.types = {}

    def _get_required_fields(self) -> None:
        for name, t in get_type_hints(MazeConfig).items():
            if name.startswith("m_"):
                name = name.removeprefix("m_")
            self.required.append(name.upper())
            self.types[name.upper()] = t

    def _process_values(self, settings: Dict[str, Any]) -> MazeConfig:
        """Validate and store config values"""

        def parse_num(num: str) -> None:
            try:
                value = int(settings[num])
                if value < 0:
                    raise ValueError
                settings[num] = value
            except ValueError:
                raise ParsingError(
                    f"(ValueError): {num} must be a non-negative integer"
                )

        def parse_coord(coord: str) -> None:
            """Validate and parse coordinates"""
            parts = settings[coord].split(",")
            if len(parts) != 2:
                raise ParsingError(
                    "Coords must contain 2 values separated with a comma"
                )
            try:
                coords = int(parts[0]), int(parts[1])
                if coords[0] < 0 or coords[1] < 0:
                    raise ValueError
                if coords[0] >= settings["WIDTH"] or coords[1] >= settings["HEIGHT"]:
                    raise ParsingError(
                        f"{coord}'s coordinates are out of bounds {coords}\n"
                        f"Limit: ({settings['WIDTH']}, {settings['HEIGHT']})"
                    )
                settings[coord] = coords
            except ValueError:
                raise ParsingError(
                    f"(ValueError): {parts} Coords must be non-negative integers"
                )

        def parse_bool(b: str) -> None:
            if settings[b] not in ["True", "False"]:
                raise ParsingError(f"{b} must be either 'True' or 'False'")
            settings[b] = settings[b] == "True"

        def get_nums() -> List[str]:
            return [
                item for item in self.required
                if self.types[item] is int
            ]

        def get_coords() -> List[str]:
            return [
                item for item in self.required
                if get_origin(self.types[item]) is tuple
            ]

        def get_bools() -> List[str]:
            return [item for item in self.required if self.types[item] is bool]

        for num in get_nums():
            parse_num(num)

        for coord in get_coords():
            parse_coord(coord)

        for b in get_bools():
            parse_bool(b)

        if not settings["OUTPUT_FILE"]:
            raise ParsingError("OUTPUT_FILE must not be empty")

        config = [item for item in settings.values()]
        return MazeConfig(*config)


    def _read_and_parse_file(self, file: str) -> MazeConfig:
        """Attempts to read a file and parse its contents"""
        self._get_required_fields()
        settings = {}
        required = [str(item) for item in list(self.required)]
        with open(file, "r") as f:
            for line in f:
                line = line.strip()

                if not line or line[0] == "#":
                    continue

                if line.count("=") != 1:
                    raise ParsingError("Only one '=' needed for each line")

                key, value = [item.strip() for item in line.split("=", 1)]
                if key not in required:
                    raise ParsingError(f"Unknown key: '{key}'")
                if key in settings:
                    raise ParsingError(f"Repeated key: '{key}'")
                settings[key] = value

            missing = set(required).difference(settings.keys())
            if missing:
                raise ParsingError(f"Missing settings: {missing}")

        return self._process_values(settings)


    def parse(self, file: str) -> MazeConfig:
        """Parse file to generate maze"""
        try:
            return self._read_and_parse_file(file)
        except FileNotFoundError:
            raise ParsingError(f"File {file} not found")
        except PermissionError as e:
            raise ParsingError(f"(PermissionError): {e}")
