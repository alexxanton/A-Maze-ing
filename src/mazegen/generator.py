from enum import IntFlag, auto
from random import randrange, choice, seed, randint, shuffle
from typing import List, Tuple, Callable, Optional
from dataclasses import dataclass


@dataclass
class MazeConfig:
    """Data class for storing the maze config"""
    width: int
    height: int
    entry: Tuple[int, int]
    m_exit: Tuple[int, int]
    output_file: str
    perfect: bool
    seed: Optional[int] = randint(0, 1_000_000)
    algorithm: Optional[str] = "prim"


class Direction(IntFlag):
    """Enum for cardinal directions represented as bits"""
    NORTH = auto()  # 0001
    EAST = auto()  # 0010
    SOUTH = auto()  # 0100
    WEST = auto()  # 1000
    NONE = 0  # used for type checkers


class MazeEntity:
    def __init__(self, name: str, pos: Tuple[int, int], **kwargs) -> None:
        self.name = name
        self.pos: Tuple[int, int] = pos
        self.half_x = 0
        self.half_y = 0
        super().__init__(**kwargs)


class Maze:
    """Maze containing a grid and its attributes"""
    def __init__(self, width: int, height: int,
                 entry: Tuple[int, int], m_exit: Tuple[int, int]) -> None:
        self.width = width
        self.height = height
        self.entry = entry
        self.m_exit = m_exit
        self.grid = [[15] * self.width for _ in range(self.height)]
        self.entities: List[MazeEntity] = []
        self.logo: bool = True

    def init(self) -> None:
        self.add_entity(MazeEntity("entry", self.entry))
        self.add_entity(MazeEntity("exit", self.m_exit))

    def add_entity(self, entity: MazeEntity) -> None:
        if isinstance(entity, MazeEntity):
            self.entities.append(entity)

    def generate_output_file(self) -> None:
        with open("output.txt", "w") as file:
            for row in self.grid:
                line = "".join(format(col & 0b1111, "X") for col in row)
                file.write(line + "\n")
            file.write("\n")
            file.write(",".join(map(str, self.entry)) + "\n")
            file.write(",".join(map(str, self.m_exit)) + "\n")
            file.write("SWE")
            file.write("\n")


class MazeGenerator:
    """Generate a maze with various configurations"""
    width: int
    height: int
    entry: tuple[int, int]
    m_exit: tuple[int, int]
    output_file: str
    perfect: bool
    seed: int
    algorithm: str
    draw_method: Optional[Callable[[List[List[int]]], None]]

    def __init__(
        self,
        width: int,
        height: int,
        entry: tuple[int, int],
        m_exit: tuple[int, int],
        output_file: str,
        perfect: bool,
        seed: int,
        algorithm: str,
        draw_method: Optional[Callable[[List[List[int]]], None]] = None
    ) -> None:
        self.width = width
        self.height = height
        self.entry = entry
        self.m_exit = m_exit
        self.output_file = output_file
        self.perfect = perfect
        self.seed = seed
        self.algorithm = algorithm
        self.draw_method = draw_method

    def _place_42(self, grid: List[List[int]]) -> bool:
        WIDTH = 7
        HEIGHT = 5
        BLOCK = 0x40

        shape = [
            (0, 0),                     (4, 0), (5, 0), (6, 0),
            (0, 1),                                     (6, 1),
            (0, 2), (1, 2), (2, 2),     (4, 2), (5, 2), (6, 2),
                            (2, 3),     (4, 3),
                            (2, 4),     (4, 4), (5, 4), (6, 4)
        ]

        start_x = self.width // 2 - WIDTH // 2
        start_y = self.height // 2 - HEIGHT // 2
        if self.height <= HEIGHT + 1 or self.width <= WIDTH + 1:
            return False
        for x, y in shape:
            block_pos = (x + start_x, y + start_y)
            if self.entry == block_pos or self.m_exit == block_pos:
                raise ValueError(
                    "Cant't place an entry or exit on the '42' blocks"
                )
            grid[y + start_y][x + start_x] |= BLOCK
        return True

    def _get_valid_coords(
        self, grid: List[List[int]]
    ) -> List[Tuple[int, int]]:
        return [
            (x, y) for y in range(self.height)
            for x in range(self.width)
            if not grid[y][x] & 0x40
        ]

    def _remove_dead_ends(self, grid: List[List[int]]) -> None:
        opposite = {
            Direction.NORTH: Direction.SOUTH,
            Direction.SOUTH: Direction.NORTH,
            Direction.WEST: Direction.EAST,
            Direction.EAST: Direction.WEST,
        }

        def get_neighbor(x: int, y: int) -> Tuple[int, int] | None:
            if (
                x >= 0 and x <= self.width - 1 and
                y >= 0 and y <= self.height - 1 and
                not grid[y][x] & 0x40
            ):
                return x, y
            return None

        valid_coords = self._get_valid_coords(grid)
        dead_ends = [
            (x, y) for x, y in valid_coords
            if (grid[y][x] & 0xF).bit_count() == 3
        ]

        length = len(dead_ends)
        if self.algorithm == "prim":
            length //= 3
            shuffle(dead_ends)

        for x, y in dead_ends[:length]:
            walls = grid[y][x] & 0xF
            open_wall = ~walls
            dx, dy = 0, 0
            if open_wall & Direction.WEST:
                dx = 1
            elif open_wall & Direction.EAST:
                dx = -1
            elif open_wall & Direction.NORTH:
                dy = 1
            elif open_wall & Direction.SOUTH:
                dy = -1

            if (grid[y][x] & 0xF).bit_count() != 3:
                continue

            neighbor = get_neighbor(x + dx, y + dy)
            if neighbor:
                nx, ny = neighbor
                direction = self._get_direction(x, y, nx, ny)
                grid[y][x] &= ~direction
                grid[ny][nx] &= ~opposite[direction]

    def create(self) -> Maze:
        seed(self.seed)
        maze = Maze(self.width, self.height, self.entry, self.m_exit)
        maze.init()
        maze.logo = self._place_42(maze.grid)
        if self.algorithm == "prim":
            self._prim(maze.grid)
        else:
            self._backtracking(maze.grid)
        if not self.perfect:
            self._remove_dead_ends(maze.grid)
        maze.generate_output_file()
        return maze

    def _get_direction(self, x: int, y: int, nx: int, ny: int) -> Direction:
        """Get the direction between two cells"""
        if x > nx:
            return Direction.WEST
        if x < nx:
            return Direction.EAST
        if y > ny:
            return Direction.NORTH
        if y < ny:
            return Direction.SOUTH
        return Direction.NONE

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

        mark_cell(*choice(self._get_valid_coords(grid)))
        if self.draw_method:
            self.draw_method(grid)

        while frontiers:
            index = randrange(len(frontiers))
            x, y = frontiers.pop(index)
            nbs = get_neighbors(x, y)
            nx, ny = choice(nbs)

            # carve walls
            direction = self._get_direction(x, y, nx, ny)
            grid[y][x] &= ~direction
            grid[ny][nx] &= ~opposite[direction]
            grid[ny][nx] |= IN

            mark_cell(x, y)

            if self.draw_method:
                self.draw_method(grid)

    def _backtracking(self, grid: List[List[int]]) -> None:
        IN = 0x10
        BLOCK = 0x40
        stack: List[Tuple[int, int]] = [self.entry]
        grid[self.entry[1]][self.entry[0]] |= IN
        opposite = {
            Direction.NORTH: Direction.SOUTH,
            Direction.SOUTH: Direction.NORTH,
            Direction.WEST: Direction.EAST,
            Direction.EAST: Direction.WEST,
        }
        if self.draw_method:
            self.draw_method(grid)

        while stack:
            x, y = stack[-1]
            neighbors = []
            for dx, dy, direction in [
                    (0, -1, Direction.NORTH),
                    (0, 1, Direction.SOUTH),
                    (1, 0, Direction.EAST),
                    (-1, 0, Direction.WEST)
            ]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.width and 0 <= ny < self.height:
                    if not (grid[ny][nx] & IN) and not (grid[ny][nx] & BLOCK):
                        neighbors.append((nx, ny, direction))

            if neighbors:
                nx, ny, direction = choice(neighbors)
                d = int(direction)
                od = int(opposite[direction])
                grid[y][x] &= ~d
                grid[ny][nx] &= ~od
                grid[ny][nx] |= IN
                # grid[ny][nx] |= 0x20
                stack.append((nx, ny))

            else:
                stack.pop()

            if self.draw_method:
                self.draw_method(grid)
