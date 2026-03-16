from utils import MazeConfig
from enum import IntEnum


class Directions(IntEnum):
    NORTH = 0b0001
    EAST = 0b0010
    SOUTH = 0b0100
    WEST = 0b1000


class Maze:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.grid = [[15] * self.width] * self.height


class MazeGenerator:
    """Generate a maze with various configurations"""
    def __init__(
        self,
        width: int,
        height: int,
        entry: tuple[int, int],
        exit: tuple[int, int],
        output_file: str,
        perfect: bool
    ) -> None:
        self.width: int = width
        self.height: int = height
        self.entry: tuple[int, int] = entry
        self.exit: tuple[int, int] = exit
        self.output_file: str = output_file
        self.perfect: bool = perfect

    def create(self) -> Maze:
        maze = Maze(self.width, self.height)
        return maze
