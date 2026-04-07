from generator import Maze, MazeEntity, Direction
from typing import Tuple
import curses
from solver import PathFind


class Player(MazeEntity):
    def __init__(self, name: str, pos: Tuple[int, int]) -> None:
        super().__init__(name, pos)
        self.direction = Direction.NONE


class Enemy(MazeEntity, PathFind):
    def __init__(
        self, name: str, pos: Tuple[int, int], target: MazeEntity
    ) -> None:
        super().__init__(name=name, pos=pos, target=target)
        self.direction = Direction.NONE
        self.frame = 5


class VideoGame:
    def __init__(self, maze: Maze, screen: curses.window) -> None:
        self.maze = maze
        self.player = Player("player", self.maze.entry)
        self.enemy = Enemy("enemy", self.maze.m_exit, self.player)
        self.screen = screen
        self.run = False

    def update(self) -> None:
        self._update_player()
        self._update_enemy()

    def init(self):
        self.maze.add_entity(self.player)
        self.maze.add_entity(self.enemy)

    def _get_input(self) -> int:
        self.screen.timeout(50)
        ch = self.screen.getch()
        if ch < 0:
            return 0
        return ch

    def _exit_game(self) -> None:
        self.player.pos = self.maze.entry
        self.player.direction = Direction.NONE
        self.player.half_x = 0
        self.player.half_y = 0
        self.run = False

    def _update_enemy(self) -> None:
        self.enemy.frame -= 1
        if self.enemy.frame < 1:
            path = self.enemy.find_path(self.maze, self.enemy.pos)
            if len(path) > 2:
                self.enemy.pos = path[1]
            self.enemy.frame = 5

    def _update_player(self) -> None:
        x, y = self.player.pos
        if self.player.half_x or self.player.half_y:
            self.player.half_x = 0
            self.player.half_y = 0
        if (x, y) == self.maze.m_exit:
            self.screen.timeout(100)
            self._exit_game()
            return

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
                self._exit_game()
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
                self.player.half_x = -1
            case Direction.EAST:
                x += 1
                self.player.half_x = 1
            case Direction.NORTH:
                y -= 1
                self.player.half_y = -1
            case Direction.SOUTH:
                y += 1
                self.player.half_y = 1

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
