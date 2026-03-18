from generator import Maze, Direction
import curses


#print(wall * (maze.width * 2 + 1))
#print(hex(maze.grid[i][j])[2:], end="")

def draw_maze(screen, grid) -> None:
    IN = 0x10
    FRONTIER = 0x20
    screen.move(0, 0)
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            cell = grid[i][j]
            screen.addch("+")
            if cell & Direction.NORTH:
                screen.addstr("--")
            else:
                screen.addstr("  ")
        screen.addch("\n")
        for j in range(len(grid[i])):
            cell = grid[i][j]
            screen.addstr("|" if cell & Direction.WEST else " ")
            if cell & IN and False:
                screen.attron(curses.color_pair(2))
            if cell & FRONTIER and not cell & IN:
                screen.attron(curses.color_pair(1))
            if 1:
                screen.addstr("  ")
            else:
                hex_num = hex(grid[i][j] & 0b00001111)[1:]
                #hex_num = hex(grid[i][j])[1:]
                screen.addstr(hex_num.replace("x", " "))
            screen.attroff(curses.color_pair(1))
            screen.attroff(curses.color_pair(2))
        screen.addch("\n")
        screen.refresh()

    screen.timeout(10)
    if screen.getch() == ord("q"):
        exit()
