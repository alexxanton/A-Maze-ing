from generator import Maze, MazeEntity, Direction
from typing import Tuple
import curses


class Player(MazeEntity):
    def __init__(self, name: str, pos: Tuple[int, int]) -> None:
        super().__init__(name, pos)
        self.direction = Direction.NONE


class VideoGame:
    def __init__(self, maze: Maze, screen: curses.window) -> None:
        self.maze = maze
        self.player = Player("player", self.maze.entry)
        self.screen = screen
        self.run = False

    def update(self) -> None:
        self._update_player()

    def init(self):
        self.maze.add_entity(self.player)

    def _get_input(self) -> int:
        self.screen.timeout(100)
        ch = self.screen.getch()
        if ch < 0:
            return 0
        return ch

    def _update_player(self) -> None:
        x, y = self.player.pos
        match chr(self._get_input()):
            case "a" | "A":
                self.player.direction = Direction.WEST
            case "d" | "D":
                self.player.direction = Direction.EAST
            case "w" | "W":
                self.player.direction = Direction.NORTH
            case "s" | "S":
                self.player.direction = Direction.SOUTH
            case "q" | "Q":
                self.player.pos = self.maze.entry
                self.run = False
                return

        direction = self.player.direction
        cell = self.maze.grid[y][x]
        if (
            (direction & Direction.NORTH and cell & Direction.NORTH) or
            (direction & Direction.SOUTH and cell & Direction.SOUTH) or
            (direction & Direction.WEST and cell & Direction.WEST) or
            (direction & Direction.EAST and cell & Direction.EAST)
        ):
            direction = Direction.NONE

        match direction:
            case Direction.WEST:
                x -= 1
            case Direction.EAST:
                x += 1
            case Direction.NORTH:
                y -= 1
            case Direction.SOUTH:
                y += 1

        self.player.pos = (x, y)
        self.player.direction = direction

        cell = self.maze.grid[y][x]
        left_right = Direction.WEST | Direction.EAST
        up_down = Direction.NORTH | Direction.SOUTH

        def is_open(d: Direction):
            return (cell & d) == 0

        if direction & left_right:
            if is_open(Direction.NORTH) or is_open(Direction.SOUTH):
                self.player.direction = Direction.NONE

        if direction & up_down:
            if is_open(Direction.EAST) or is_open(Direction.WEST):
                self.player.direction = Direction.NONE
