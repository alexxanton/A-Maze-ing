import sys
from parse import parse, ParsingError
from generator import MazeGenerator
#from flimsy_generator import MazeGenerator
from dataclasses import astuple
from draw_maze import draw_maze
import curses


def main(stdscr=None) -> None:
    if len(sys.argv) < 2:
        print("No config file provided!")
        return
    try:
        config = parse(sys.argv[1])
    except ParsingError as e:
        print("Error while parsing file:", e)
        return

    screen = curses.initscr()

    curses.curs_set(0)
    if curses.has_colors():
        curses.start_color()
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_RED)

    def draw_wrapper(grid):
        return draw_maze(screen, grid)
    maze_gen = MazeGenerator(*astuple(config), draw_wrapper)
    maze = maze_gen.create()

    screen.timeout(-1)
    screen.getch()
    curses.curs_set(1)
    curses.echo()


if __name__ == "__main__":
    try:
        curses.wrapper(main)
    except KeyboardInterrupt:
        print("Program stoped")
