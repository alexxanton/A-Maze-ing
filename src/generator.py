from enum import IntFlag, auto
from random import randrange, choice, seed
from typing import List, Tuple, Callable, Optional
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


class Direction(IntFlag):
    """Enum for cardinal directions represented as bits"""
    NORTH = auto()  # 0001
    EAST = auto()  # 0010
    SOUTH = auto()  # 0100
    WEST = auto()  # 1000


class Maze:
    """Maze containing a grid and its attributes"""
    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height
        self.grid = [[15] * self.width for _ in range(self.height)]


class MazeGenerator:
    """Generate a maze with various configurations"""
    def __init__(
        self,
        width: int,
        height: int,
        entry: tuple[int, int],
        exit: tuple[int, int],
        output_file: str,
        perfect: bool,
    ) -> None:
        self.width: int = width
        self.height: int = height
        self.entry: tuple[int, int] = entry
        self.exit: tuple[int, int] = exit
        self.output_file: str = output_file
        self.perfect: bool = perfect
        self.draw_method: Optional[Callable[[List[List[int]]], None]] = None

    def _place_42(self, grid: List[List[int]]) -> None:
        WIDTH = 7
        HEIGHT = 5
        BLOCK = 0x40

        shape = [
            (0, 0), (0, 1), (0, 2),
            (1, 2), (2, 2),
            (2, 3), (2, 4),

            (4, 0), (5, 0), (6, 0),
                            (6, 1),
            (4, 2), (5, 2), (6, 2),
            (4, 3),
            (4, 4), (5, 4), (6, 4)
        ]

        start_x = self.width // 2 - WIDTH // 2
        start_y = self.height // 2 - HEIGHT // 2
        if self.height <= HEIGHT + 1 or self.width <= WIDTH + 1:
            return
        for x, y in shape:
            block_pos = (x + start_x, y + start_y)
            if self.entry == block_pos or self.exit == block_pos:
                raise ValueError(
                    "Cant't place an entry or exit on the '42' blocks"
                )
            grid[y + start_y][x + start_x] |= BLOCK

    def create(self) -> Maze | None:
        maze = Maze(self.width, self.height)
        self._place_42(maze.grid)
        self._prim(maze.grid)
        return maze

    def _prim(self, grid: List[List[int]]) -> None:
        IN = 0x10
        FRONTIER = 0x20
        BLOCK = 0x40
        frontiers = []
        width = self.width
        height = self.height
        opposite = {
            Direction.NORTH: Direction.SOUTH,
            Direction.SOUTH: Direction.NORTH,
            Direction.WEST: Direction.EAST,
            Direction.EAST: Direction.WEST,
        }
        
        def add_frontier(x: int, y: int) -> None:
            if 0 <= x < width and 0 <= y < height and grid[y][x] == 0xF:
                if grid[y][x] & BLOCK:
                    return
                grid[y][x] |= FRONTIER
                frontiers.append((x, y))

        def mark_cell(x: int, y: int) -> None:
            grid[y][x] |= IN
            add_frontier(x + 1, y)
            add_frontier(x - 1, y)
            add_frontier(x, y + 1)
            add_frontier(x, y - 1)

        def get_neighbors(x: int, y: int) -> List[Tuple[int, int]]:
            nbs = []
            if x > 0 and grid[y][x - 1] & IN:
                nbs.append((x - 1, y))
            if x + 1 < width and grid[y][x + 1] & IN:
                nbs.append((x + 1, y))
            if y > 0 and grid[y - 1][x] & IN:
                nbs.append((x, y - 1))
            if y + 1 < height and grid[y + 1][x] & IN:
                nbs.append((x, y + 1))

            return nbs

        def get_direction(x: int, y: int, nx: int, ny: int) -> Direction:
            """Get the direction between two cells"""
            if x > nx:
                return Direction.WEST
            if x < nx:
                return Direction.EAST
            if y > ny:
                return Direction.NORTH
            if y < ny:
                return Direction.SOUTH

        mark_cell(*self.entry)
        if self.draw_method:
            self.draw_method(grid)

        while frontiers:
            index = randrange(len(frontiers))
            x, y = frontiers.pop(index)
            nbs = get_neighbors(x, y)
            nx, ny = choice(nbs)

            # carve walls
            direction = get_direction(x, y, nx, ny)
            grid[y][x] &= ~direction
            grid[ny][nx] &= ~opposite[direction]
            grid[y][x] |= IN
            grid[ny][nx] |= IN

            mark_cell(x, y)

            if self.draw_method:
                self.draw_method(grid)
