from mazegen import Direction, MazeEntity
import curses
from enum import IntEnum, auto
from typing import List, Optional, Tuple


class Colors(IntEnum):
    BLUE_WALLS = auto()
    RED_WALLS = auto()
    GREEN_WALLS = auto()

    BLUE_MAZE_ENTRY = auto()
    RED_MAZE_ENTRY = auto()
    GREEN_MAZE_ENTRY = auto()

    BLUE_MAZE_EXIT = auto()
    RED_MAZE_EXIT = auto()
    GREEN_MAZE_EXIT = auto()

    RED_FRONTIER = auto()
    BLUE_FRONTIER = auto()
    PURPLE_BLOCK = auto()
    YELLOW_BLOCK = auto()
    BLACK_BLOCK = auto()

    GREEN_SOLVE = auto()
    BLUE_SOLVE = auto()
    ENEMY = auto()
    COIN = auto()


class CellFlags(IntEnum):
    IN = 0x10
    FRONTIER = 0x20
    BLOCK = 0x40
    VISITED = 0x80


class MazeRenderer:
    NODE = "██"
    WALL = "██"
    EMPTY = "  "

    BLUE_MAZE = (
        Colors.BLUE_WALLS,
        Colors.RED_FRONTIER,
        Colors.PURPLE_BLOCK,
        Colors.BLUE_MAZE_ENTRY,
        Colors.BLUE_MAZE_EXIT,
        Colors.GREEN_SOLVE
    )
    RED_MAZE = (
        Colors.RED_WALLS,
        Colors.BLUE_FRONTIER,
        Colors.BLACK_BLOCK,
        Colors.RED_MAZE_ENTRY,
        Colors.RED_MAZE_EXIT,
        Colors.GREEN_SOLVE
    )
    GREEN_MAZE = (
        Colors.GREEN_WALLS,
        Colors.RED_FRONTIER,
        Colors.YELLOW_BLOCK,
        Colors.GREEN_MAZE_ENTRY,
        Colors.GREEN_MAZE_EXIT,
        Colors.BLUE_SOLVE
    )
    variations = [BLUE_MAZE, RED_MAZE, GREEN_MAZE]

    def __init__(self, screen: curses.window) -> None:
        self.screen = screen
        self.palette: Tuple[Colors, ...]

    def init(self) -> None:
        if not curses.has_colors():
            return

        curses.start_color()
        curses.init_pair(self.BLUE_MAZE[0], 4, 6)
        curses.init_pair(self.RED_MAZE[0], 1, 9)
        curses.init_pair(self.GREEN_MAZE[0], 2, 10)
        curses.init_pair(Colors.RED_FRONTIER, 0, 9)
        curses.init_pair(Colors.BLUE_FRONTIER, 0, 6)
        curses.init_pair(Colors.PURPLE_BLOCK, 0, 13)
        curses.init_pair(Colors.YELLOW_BLOCK, 0, 3)
        curses.init_pair(Colors.BLACK_BLOCK, 15, 0)

        curses.init_pair(Colors.BLUE_MAZE_ENTRY, 5, 6)
        curses.init_pair(Colors.BLUE_MAZE_EXIT, 1, 6)
        curses.init_pair(Colors.RED_MAZE_ENTRY, 5, 9)
        curses.init_pair(Colors.RED_MAZE_EXIT, 2, 9)
        curses.init_pair(Colors.GREEN_MAZE_ENTRY, 5, 10)
        curses.init_pair(Colors.GREEN_MAZE_EXIT, 1, 10)

        curses.init_pair(Colors.GREEN_SOLVE, 0, 10)
        curses.init_pair(Colors.BLUE_SOLVE, 0, 6)
        curses.init_pair(Colors.ENEMY, 0, 0)
        curses.init_pair(Colors.COIN, 3, 0)

    def _draw_entities(self, entities: List[MazeEntity]) -> None:
        walls, fronts, blocks, entry, m_exit, solve = self.palette

        screen_height, screen_width = self.screen.getmaxyx()
        og_y, og_x = self.screen.getyx()
        for entity in entities:
            x, y = entity.pos
            half_x = 2
            half_y = 1
            if entity.half_x:
                half_x = 0 if entity.half_x == 1 else 4
            if entity.half_y:
                half_y = 0 if entity.half_y == 1 else 2
            x = x * 4 + half_x
            y = y * 2 + half_y

            if (
                x < 0 or x >= screen_width - 1 or
                y < 0 or y >= screen_height - 1
            ):
                continue

            pair = 0
            if entity.name == "player":
                pair = entry
            elif entity.name == "exit":
                pair = m_exit
            elif entity.name == "enemy":
                pair = Colors.ENEMY
            elif entity.name.startswith("coin"):
                pair = Colors.COIN

            self.screen.addstr(y, x, self.WALL, curses.color_pair(pair))

        self.screen.move(og_y, og_x)

    def _draw_top_line(self, row: List[int]) -> None:
        walls, fronts, blocks, entry, m_exit, solve = self.palette

        def enable_color() -> None:
            if cell & CellFlags.VISITED:
                self.screen.attron(curses.color_pair(solve))

        def disable_color() -> None:
            self.screen.attroff(curses.color_pair(solve))
            self.screen.attron(curses.color_pair(walls))

        for i in range(len(row)):
            cell = row[i]
            self.screen.addstr(self.NODE)
            if cell & Direction.NORTH:
                self.screen.addstr(self.WALL)
            else:
                enable_color()
                self.screen.addstr(self.EMPTY)
                disable_color()
        self.screen.addstr(self.NODE)
        self.screen.addch("\n")

    def _draw_row(self, row: List[int]) -> None:
        walls, fronts, blocks, entry, m_exit, solve = self.palette

        def enable_colors(cell: int) -> None:
            if cell & CellFlags.FRONTIER and not cell & CellFlags.IN:
                self.screen.attron(curses.color_pair(fronts))
            if cell & CellFlags.BLOCK:
                self.screen.attron(curses.color_pair(blocks))
            if cell & CellFlags.VISITED:
                self.screen.attron(curses.color_pair(solve))

        def disable_colors() -> None:
            self.screen.attroff(curses.color_pair(fronts))
            self.screen.attroff(curses.color_pair(blocks))
            self.screen.attron(curses.color_pair(walls))

        for i in range(len(row)):
            qty = 1
            cell = row[i]
            if cell & Direction.WEST:
                self.screen.addstr(self.WALL)
            else:
                qty = 2
            enable_colors(cell)
            self.screen.addstr(self.EMPTY * qty)
            disable_colors()

        self.screen.addstr(self.WALL if cell & Direction.EAST else self.EMPTY)
        self.screen.addch("\n")

    def _draw_bottom(self, row: List[int]) -> None:
        for i in range(len(row)):
            cell = row[i]
            self.screen.addstr(self.WALL)
            if cell & Direction.SOUTH:
                self.screen.addstr(self.WALL)
        self.screen.addstr(self.WALL)

    def draw_maze(
        self,
        grid: List[List[int]],
        color: int,
        entities: Optional[List[MazeEntity]] = None,
        wait: bool = True
    ) -> None:
        self.palette = self.variations[color]
        walls, fronts, blocks, entry, m_exit, solve = self.palette

        screen_height = self.screen.getmaxyx()[0]
        if screen_height <= 3:
            return

        max_y = screen_height // 2 - 2
        self.screen.move(0, 0)
        self.screen.attron(curses.color_pair(walls))

        for i in range(len(grid[:max_y])):
            screen_width = self.screen.getmaxyx()[1]
            max_x = screen_width // 4 - 1
            self._draw_top_line(grid[i][:max_x])
            self._draw_row(grid[i][:max_x])

        if len(grid[:max_y]) < max_y:
            self._draw_bottom(grid[-1][:max_x])

        self.screen.attroff(curses.color_pair(3))

        if entities:
            self._draw_entities(entities)
        self.screen.clrtobot()
        self.screen.addstr("\n\n")

        if not wait:
            return
        ch = self.screen.getch()
        if ch == ord("q"):
            exit()
        elif ch == ord("\n") or ch == ord(" "):
            self.screen.timeout(0)

    def draw_path(self, solution: List[Tuple[int, int]]) -> None:
        og_y, og_x = self.screen.getyx()
        self.screen.attron(curses.color_pair(Colors.PURPLE_BLOCK))
        for (x, y), (x2, y2) in zip(solution, solution[1:]):
            x_pos = x * 4 + 2
            y_pos = y * 2 + 1
            x_dir = x2 - x  # -1, 0 or 1
            y_dir = y2 - y  # -1, 0 or 1

            screen_height, screen_width = self.screen.getmaxyx()
            if (
                x < 0 or x > screen_width // 4 - 2 or
                y < 0 or y > screen_height // 2 - 4
            ):
                continue

            self.screen.addstr(y_pos, x_pos, self.EMPTY)
            self.screen.addstr(y_pos + y_dir, x_pos + (x_dir * 2), self.EMPTY)

        self.screen.attroff(curses.color_pair(Colors.PURPLE_BLOCK))
        self.screen.move(og_y, og_x)
