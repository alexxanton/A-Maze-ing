from generator import Direction, MazeEntity
import curses
from enum import IntEnum, auto
from typing import List, Optional, Tuple


class Colors(IntEnum):
    BLUE_WALLS = auto()
    RED_WALLS = auto()
    GREEN_WALLS = auto()

    BLUE_ENTRY = auto()
    RED_ENTRY = auto()
    GREEN_ENTRY = auto()

    BLUE_EXIT = auto()
    RED_EXIT = auto()
    GREEN_EXIT = auto()

    RED_FRONTIER = auto()
    BLUE_FRONTIER = auto()
    PURPLE_BLOCK = auto()
    YELLOW_BLOCK = auto()
    BLACK_BLOCK = auto()


class CellFlags(IntEnum):
    IN = 0x10
    FRONTIER = 0x20
    BLOCK = 0x40


class MazeRenderer:
    NODE = "██"
    WALL = "██"
    #WALL = "▓▓"
    EMPTY = "  "

    BLUE_MAZE = (
        Colors.BLUE_WALLS,
        Colors.RED_FRONTIER,
        Colors.PURPLE_BLOCK,
        Colors.BLUE_ENTRY,
        Colors.BLUE_EXIT
    )
    RED_MAZE = (
        Colors.RED_WALLS,
        Colors.BLUE_FRONTIER,
        Colors.BLACK_BLOCK,
        Colors.RED_ENTRY,
        Colors.RED_EXIT
    )
    GREEN_MAZE = (
        Colors.GREEN_WALLS,
        Colors.RED_FRONTIER,
        Colors.YELLOW_BLOCK,
        Colors.GREEN_ENTRY,
        Colors.GREEN_EXIT
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

        curses.init_pair(Colors.BLUE_ENTRY, 5, 6)
        curses.init_pair(Colors.BLUE_EXIT, 1, 6)
        curses.init_pair(Colors.RED_ENTRY, 5, 9)
        curses.init_pair(Colors.RED_EXIT, 2, 9)
        curses.init_pair(Colors.GREEN_ENTRY, 5, 10)
        curses.init_pair(Colors.GREEN_EXIT, 1, 10)

    def _draw_entities(self, entities: List[MazeEntity]) -> None:
        walls, fronts, blocks, entry, m_exit = self.palette

        for entity in entities:
            og_x, og_y = self.screen.getyx()
            x, y = entity.pos
            x = x * 2 + (2 if x % 2 == 0 else 4)
            y = y * 2 + 1
            #screen.addstr(y, x, ".." + str(x))
            pair = 0
            if entity.name == "entry":
                pair = entry
            elif entity.name == "exit":
                pair = m_exit
            self.screen.addstr(y, x, self.WALL, curses.color_pair(pair))
            self.screen.move(og_y, og_x)

    def _draw_top_line(self, row: List[int]) -> None:
        walls, fronts, blocks, entry, m_exit = self.palette
        for i in range(len(row)):
            cell = row[i]
            self.screen.addstr(self.NODE)
            if cell & Direction.NORTH:
                self.screen.addstr(self.WALL)
            else:
                self.screen.addstr("  ")
        self.screen.addstr(self.NODE)
        self.screen.addch("\n")

    def _draw_row(self, row: List[int]) -> None:
        walls, fronts, blocks, entry, m_exit = self.palette

        def enable_colors(cell: int) -> None:
            self.screen.addstr(
                self.WALL if cell & Direction.WEST else self.EMPTY
            )
            if cell & CellFlags.FRONTIER and not cell & CellFlags.IN:
                self.screen.attron(curses.color_pair(fronts))
            if cell & CellFlags.BLOCK:
                self.screen.attron(curses.color_pair(blocks))

        def disable_colors() -> None:
            self.screen.attroff(curses.color_pair(fronts))
            self.screen.attroff(curses.color_pair(blocks))
            self.screen.attron(curses.color_pair(walls))

        for i in range(len(row)):
            cell = row[i]
            enable_colors(cell)
            self.screen.addstr("  ")
            disable_colors()

        self.screen.addstr(self.WALL if cell & Direction.EAST else self.EMPTY)
        self.screen.addch("\n")

    def _draw_bottom(self, row: List[int]) -> None:
        for i in range(len(row)):
            cell = row[i]
            self.screen.addstr(self.WALL)
            if cell & Direction.SOUTH:
                self.screen.addstr(self.WALL)

    def draw_maze(
        self,
        grid: List[List[int]],
        color: int,
        entities: Optional[List[MazeEntity]] = None,
        wait: bool = True
    ) -> None:
        self.palette = self.variations[color]
        walls, fronts, blocks, entry, m_exit = self.palette

        self.screen.move(0, 0)
        self.screen.scrollok(True)
        self.screen.attron(curses.color_pair(walls))

        for i in range(len(grid)):
            self._draw_top_line(grid[i])
            self._draw_row(grid[i])
        self._draw_bottom(grid[-1])

        self.screen.addstr(self.WALL)
        self.screen.addstr("\n\n")
        self.screen.attroff(curses.color_pair(3))

        if entities:
            self._draw_entities(entities)
        self.screen.refresh()

        if not wait:
            return
        ch = self.screen.getch()
        if ch == ord("q"):
            exit()
        elif ch == ord("\n") or ch == ord(" "):
            self.screen.timeout(0)
