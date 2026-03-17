from utils import MazeConfig
from enum import IntFlag, auto
from random import randrange, choice, seed
from time import sleep


class Direction(IntFlag):
    NORTH = auto() # 0001
    EAST = auto() # 0010
    SOUTH = auto() # 0100
    WEST = auto() # 1000


class Maze:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.grid = [[0] * self.width for _ in range(self.height)]


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
        self.prim(maze.grid)
        return maze

    def prim(self, grid):
        FRONTIER = 0x20
        IN = 0x10
        frontier = []
        width = self.width
        height = self.height
        seed(1234)

        def add_frontier(x, y, grid, frontier):
            if (x >= 0 and y >= 0 and x < width
            and y < height and grid[y][x] == 0):
                grid[y][x] |= FRONTIER
                frontier.append((x, y))

        def mark(x, y, grid, frontier):
            grid[y][x] |= IN
            add_frontier(x - 1, y, grid, frontier)
            add_frontier(x + 1, y, grid, frontier)
            add_frontier(x, y - 1, grid, frontier)
            add_frontier(x, y + 1, grid, frontier)

        def neighbors(x, y, grid):
            nbs = []

            if x > 0 and grid[y][x - 1] & IN != 0:
                nbs.append((x - 1, y))
            if x + 1 < width and grid[y][x + 1] & IN != 0:
                nbs.append((x + 1, y))
            if y > 0 and grid[y - 1][x] & IN != 0:
                nbs.append((x, y - 1))
            if y + 1 < height and grid[y + 1][x] & IN != 0:
                nbs.append((x, y + 1))

            return nbs

        def direction(fx, fy, tx, ty):
            if fx < tx:
                return Direction.EAST
            if fx > tx:
                return Direction.WEST
            if fy < ty:
                return Direction.SOUTH
            if fy > ty:
                return Direction.NORTH

        def empty(cell):
            return cell == 0 or cell == FRONTIER

        def get_opposite(dir_: Direction):
            if dir_ == Direction.NORTH: return Direction.SOUTH
            if dir_ == Direction.SOUTH: return Direction.NORTH
            if dir_ == Direction.WEST: return Direction.EAST
            if dir_ == Direction.EAST: return Direction.WEST

        mark(0, 0, grid, frontier)
        while frontier:
            x, y = frontier.pop(randrange(len(frontier)))
            nb = neighbors(x, y, grid)
            nx, ny = choice(nb)

            dir_ = direction(x, y, nx, ny)
            grid[y][x] |= dir_
            grid[ny][nx] |= get_opposite(dir_)

            mark(x, y, grid, frontier)
            #m = Maze(0, 0)
            #m.grid = grid
            #from draw_maze import draw_maze
            #print("\033[H", end="")
            #draw_maze(m)
            #sleep(0.1)
