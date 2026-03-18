from generator import Maze, Direction
import curses


#print(wall * (maze.width * 2 + 1))
#print(hex(maze.grid[i][j])[2:], end="")

#if 1:
#    screen.addstr("  ")
#else:
#    hex_num = hex(grid[i][j] & 0b00001111)[1:]
#    #hex_num = hex(grid[i][j])[1:]
#    screen.addstr(hex_num.replace("x", " "))

def draw_maze(screen, grid) -> None:
    IN = 0x10
    FRONTIER = 0x20
    screen.move(0, 0)
    screen.scrollok(True)
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            cell = grid[i][j]
            screen.addch("+")
            if cell & Direction.NORTH:
                screen.addstr("--")
            else:
                screen.addstr("  ")
        screen.addch("+")
        screen.addch("\n")
        for j in range(len(grid[i])):
            cell = grid[i][j]
            screen.addstr("|" if cell & Direction.WEST else " ")
            if cell & FRONTIER and not cell & IN:
                screen.attron(curses.color_pair(1))
            if cell == 79:
                screen.attron(curses.color_pair(2))
            screen.addstr("  ")
            screen.attroff(curses.color_pair(1))
            screen.attroff(curses.color_pair(2))
        screen.addstr("|" if cell & Direction.EAST else " ")
        screen.addch("\n")

    for j in range(len(grid[i])):
        cell = grid[i][j]
        screen.addch("+")
        if cell & Direction.SOUTH:
            screen.addstr("--")
    screen.addch("+")
    screen.addch("\n")
    screen.refresh()

    return
    ch = screen.getch()
    if ch == ord("q"):
        exit()
    elif ch == ord("\n"):
        screen.timeout(0)
