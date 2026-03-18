from utils import MazeConfig
from enum import IntFlag, auto
from random import randrange, choice, seed
from typing import List, Tuple


class Direction(IntFlag):
    NORTH = auto() # 0001
    EAST = auto() # 0010
    SOUTH = auto() # 0100
    WEST = auto() # 1000


class Maze:
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
        draw = None
    ) -> None:
        self.width: int = width
        self.height: int = height
        self.entry: tuple[int, int] = entry
        self.exit: tuple[int, int] = exit
        self.output_file: str = output_file
        self.perfect: bool = perfect
        self.draw = draw

    def create(self) -> Maze:
        maze = Maze(self.width, self.height)
        self._prim(maze.grid)
        return maze

    def _prim(self, grid) -> None:
        IN = 0x10
        FRONTIER = 0x20
        frontiers = []
        width = self.width
        height = self.height
        opposite = {
            Direction.NORTH: Direction.SOUTH,
            Direction.SOUTH: Direction.NORTH,
            Direction.WEST: Direction.EAST,
            Direction.EAST: Direction.WEST,
        }
        seed(4242)
        
        def add_frontier(x: int, y: int) -> None:
            if 0 <= x < width and 0 <= y < height and grid[y][x] == 0xF:
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
            if x > nx:
                return Direction.WEST
            if x < nx:
                return Direction.EAST
            if y > ny:
                return Direction.NORTH
            if y < ny:
                return Direction.SOUTH

        mark_cell(*self.entry)
        self.draw(grid)
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

            if self.draw:
                self.draw(grid)
