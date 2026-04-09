from typing import Tuple, List
from random import shuffle
import curses
from mazegen import Maze, MazeEntity, Direction
from src.solver import PathFind
from src.utils import get_direction


class Player(MazeEntity):
    def __init__(self, name: str, pos: Tuple[int, int]) -> None:
        super().__init__(name, pos)
        self.direction = Direction.NONE


class Coin(MazeEntity):
    def __init__(
        self, name: str, pos: Tuple[int, int], collide_with: MazeEntity
    ) -> None:
        super().__init__(name, pos)
        self.direction = Direction.NONE
        self.collide_with = collide_with


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
        self.enemy = Enemy("enemy", (-1, -1), self.player)
        self.screen = screen
        self.run = False
        self.coins: List[Coin] = []

    def start(self) -> None:
        self.maze.add_entity(self.player)
        self.enemy.pos = self.maze.m_exit
        for i, coord in enumerate(self._get_valid_coords()):
            coin = Coin(f"coin{i}", coord, self.player)
            self.coins.append(coin)
            self.maze.add_entity(coin)
        self.maze.add_entity(self.enemy)

    def update(self) -> None:
        self._update_player()
        self._update_enemy()
        for coin in self.coins:
            if self.player.pos == coin.pos:
                self.coins.remove(coin)
                self.maze.entities.remove(coin)
                self.player.direction = Direction.NONE
                break

    def _get_valid_coords(self) -> List[Tuple[int, int]]:
        coords = [
            (x, y) for y in range(self.maze.height)
            for x in range(self.maze.width)
            if not self.maze.grid[y][x] & 0x40 and
            not (x, y) == self.maze.entry and
            not (x, y) == self.maze.m_exit
        ]
        shuffle(coords)
        return coords[:len(coords) // 10]

    def _get_input(self) -> int:
        self.screen.timeout(50)
        ch = self.screen.getch()
        if ch < 0:
            return 0
        return ch

    def _exit_game(self) -> None:
        self.coins.clear()
        for entity in list(self.maze.entities):
            if entity.name.startswith("coin"):
                self.maze.entities.remove(entity)
        self.player.pos = self.maze.entry
        self.enemy.pos = (-1, -1)
        self.player.direction = Direction.NONE
        self.player.half_x = 0
        self.player.half_y = 0
        self.run = False

    def _update_enemy(self) -> None:
        self.enemy.frame -= 1
        if self.enemy.frame == 3:
            self.enemy.half_x = 0
            self.enemy.half_y = 0

        if self.enemy.frame < 1:
            path = self.enemy.find_path(self.maze, self.enemy.pos)
            if len(path) >= 2:
                new_pos = path[1]
                x, y = self.enemy.pos
                nx, ny = new_pos
                match get_direction(x, y, nx, ny):
                    case Direction.WEST:
                        self.enemy.half_x = -1
                    case Direction.EAST:
                        self.enemy.half_x = 1
                    case Direction.NORTH:
                        self.enemy.half_y = -1
                    case Direction.SOUTH:
                        self.enemy.half_y = 1
                self.enemy.pos = new_pos
            else:
                self._exit_game()
            self.enemy.frame = 5

    def _update_player(self) -> None:
        left_right = Direction.WEST | Direction.EAST
        up_down = Direction.NORTH | Direction.SOUTH
        x, y = self.player.pos

        if self.player.half_x or self.player.half_y:
            self.player.half_x = 0
            self.player.half_y = 0

        if (x, y) == self.maze.m_exit and not self.coins:
            self._exit_game()
            return

        cell = self.maze.grid[y][x]
        match chr(self._get_input()):
            case "a" | "A":
                if not cell & Direction.WEST:
                    self.player.direction = Direction.WEST
            case "d" | "D":
                if not cell & Direction.EAST:
                    self.player.direction = Direction.EAST
            case "w" | "W":
                if not cell & Direction.NORTH:
                    self.player.direction = Direction.NORTH
            case "s" | "S":
                if not cell & Direction.SOUTH:
                    self.player.direction = Direction.SOUTH
            case "q" | "Q":
                self._exit_game()
                return

        direction = self.player.direction
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

        def is_open(cell: int, d: Direction) -> bool:
            return (cell & int(d)) == 0

        if direction & left_right:
            if (
                is_open(cell, Direction.NORTH)
                or is_open(cell, Direction.SOUTH)
            ):
                self.player.direction = Direction.NONE

        if direction & up_down:
            if (
                is_open(cell, Direction.EAST)
                or is_open(cell, Direction.WEST)
            ):
                self.player.direction = Direction.NONE
