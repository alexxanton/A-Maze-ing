from dataclasses import dataclass


@dataclass
class MazeConfig:
    """Data class for storing the maze config"""
    width: int
    height: int
    entry: tuple[int, int]
    exit: tuple[int, int]
    output_file: str
    perfect: bool


def parse(file: str) -> MazeConfig:
    """Parse file to generate maze"""
    with open(file, "r") as f:
        for line in f:
            line = line.strip()
            print(line)
