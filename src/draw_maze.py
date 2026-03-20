from generator import Maze, Direction
import curses
from enum import IntEnum, auto


#print(wall * (maze.width * 2 + 1))
#print(hex(maze.grid[i][j])[2:], end="")

#if 1:
#    screen.addstr("  ")
#else:
#    hex_num = hex(grid[i][j] & 0b00001111)[1:]
#    #hex_num = hex(grid[i][j])[1:]
#    screen.addstr(hex_num.replace("x", " "))


class Colors(IntEnum):
    BLUE_WALLS = auto()
    RED_WALLS = auto()
    GREEN_WALLS = auto()
    RED_FRONTIER = auto()
    BLUE_FRONTIER = auto()
    PURPLE_BLOCK = auto()
    YELLOW_BLOCK = auto()
    _BLOCK = auto()


def draw_maze(screen, grid, palette, wait: bool = True) -> None:
    IN = 0x10
    FRONTIER = 0x20
    BLOCK = 0x40
    NODE = "██"
    WALL = "██"
    #WALL = "▓▓"
    EMPTY = "  "

    screen.move(0, 0)
    screen.scrollok(True)
    walls, fronts, blocks = palette
    screen.attron(curses.color_pair(walls))
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            cell = grid[i][j]
            screen.addstr(NODE)
            if cell & Direction.NORTH:
                screen.addstr(WALL)
            else:
                screen.addstr("  ")
        screen.addstr(NODE)
        screen.addch("\n")
        for j in range(len(grid[i])):
            cell = grid[i][j]
            screen.addstr(WALL if cell & Direction.WEST else EMPTY)
            if cell & FRONTIER and not cell & IN:
                screen.attron(curses.color_pair(fronts))
            if cell & BLOCK:
                screen.attron(curses.color_pair(blocks))
            screen.addstr("  ")
            screen.attroff(curses.color_pair(fronts))
            screen.attroff(curses.color_pair(blocks))
            screen.attron(curses.color_pair(walls))
        screen.addstr(WALL if cell & Direction.EAST else EMPTY)
        screen.addch("\n")

    for j in range(len(grid[i])):
        cell = grid[i][j]
        screen.addstr(WALL)
        if cell & Direction.SOUTH:
            screen.addstr(WALL)
    screen.addstr(WALL)
    screen.addstr("\n\n")
    screen.attroff(curses.color_pair(3))
    screen.refresh()

    if not wait:
        return
    ch = screen.getch()
    if ch == ord("q"):
        exit()
    elif ch == ord("\n") or ch == ord(" "):
        screen.timeout(0)
