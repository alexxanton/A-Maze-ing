from typing import get_type_hints, get_origin, get_args
from typing import Any, Union, Dict, List
from mazegen import MazeConfig


class ParsingError(Exception):
    """Exception for parsing errors"""
    def __init__(self, msg: str):
        super().__init__(msg)


class ConfigParser:
    def __init__(self) -> None:
        self.required: List[str] = []
        self.optional: List[str] = []
        self.types: Dict[str, type] = {}

    def _get_settings(self) -> None:
        def is_optional(t: type) -> bool:
            return get_origin(t) is Union and type(None) in get_args(t)

        for name, t in get_type_hints(MazeConfig).items():
            name = name.removeprefix("m_").upper()
            if is_optional(t):
                self.optional.append(name)
                self.types[name] = get_args(t)[0]
            else:
                self.types[name] = t
                self.required.append(name)

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
                settings[coord] = coords
            except ValueError:
                raise ParsingError(
                    f"(ValueError): {parts} "
                    "Coords must be non-negative integers"
                )

        def parse_bool(b: str) -> None:
            if settings[b] not in ["True", "False"]:
                raise ParsingError(f"{b} must be either 'True' or 'False'")
            settings[b] = settings[b] == "True"

        def check_out_of_bounds(name: str) -> None:
            if name not in settings:
                raise ParsingError(f"Unknown coord '{name}'")
            coords = settings[name]
            if (
                coords[0] >= settings["WIDTH"]
                or coords[1] >= settings["HEIGHT"]
            ):
                raise ParsingError(
                    f"{name}'s coordinates are out of bounds {coords}\n"
                    f"Limit: ({settings['WIDTH']}, {settings['HEIGHT']})"
                )

        for key in settings.keys():
            t = self.types[key]

            if t is int:
                parse_num(key)
            elif get_origin(t) is tuple:
                parse_coord(key)
            elif t is bool:
                parse_bool(key)

        check_out_of_bounds("ENTRY")
        check_out_of_bounds("EXIT")

        if not settings["OUTPUT_FILE"]:
            raise ParsingError("OUTPUT_FILE must not be empty")

        if (
            "ALGORITHM" in settings and
            settings["ALGORITHM"] not in ["prim", "backtracking"]
        ):
            raise ParsingError(
                "ALGORITHM must be either 'prim' or 'backtracking'"
            )

        if settings["ENTRY"] == settings["EXIT"]:
            raise ParsingError("ENTRY and EXIT overlap")

        settings = {
            key.lower() if key != "EXIT" else "m_exit": value
            for key, value in settings.items()
        }
        return MazeConfig(**settings)

    def _read_and_parse_file(self, file: str) -> MazeConfig:
        """Attempts to read a file and parse its contents"""
        self._get_settings()
        settings = {}
        with open(file, "r") as f:
            for line in f:
                line = line.strip()

                if not line or line[0] == "#":
                    continue

                if line.count("=") != 1:
                    raise ParsingError("Only one '=' needed for each line")

                key, value = [item.strip() for item in line.split("=", 1)]
                if key not in self.required and key not in self.optional:
                    raise ParsingError(f"Unknown key: '{key}'")
                if key in settings:
                    raise ParsingError(f"Repeated key: '{key}'")
                settings[key] = value

            missing = set(self.required).difference(settings.keys())
            if missing:
                raise ParsingError(f"Missing settings: {missing}")

        return self._process_values(settings)

    def parse(self, file: str) -> MazeConfig:
        """Parse file to generate maze"""
        try:
            return self._read_and_parse_file(file)
        except FileNotFoundError:
            raise ParsingError(f"File {file} not found")
        except OSError:
            raise ParsingError("Error opening file, check for permissions")
