from generator import MazeGenerator
from dataclasses import astuple
from draw_maze import draw_maze
from random import seed, randint
from sys import stdout
import curses


class InteractiveMenu:
    def __init__(self, config) -> None:
        self.config = config
        self.screen = None

    def init(self):
        self.screen = curses.initscr()
        curses.curs_set(0)
        curses.raw()
        #stdout.write("\033[38;2;150;80;200m")
        #("\033[0m")
        #stdout.flush()

        if curses.has_colors():
            curses.start_color()
            curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_RED)
            curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_CYAN)

    def start(self):
        gen_seed = randint(0, 1_000_000)
        seed(gen_seed)
        maze_gen = MazeGenerator(*astuple(self.config))
        maze = maze_gen.create()
        self.screen.timeout(0)
        while True:
            seed(gen_seed)
            draw_maze(self.screen, maze.grid)
            self.screen.addstr(
                "(r): Regenerate (t): Toggle Path (c): Change Color\n"
                "(a): Play Animations (g): Play Game (q): Quit"
            )
            self.screen.refresh()
            ch = self.screen.getch()
            if ch == ord("q"):
                break
            elif ch == ord("r"):
                gen_seed = randint(0, 1_000_000)
                #self.screen.timeout(100)
                maze = maze_gen.create()
                #maze = self.generate_maze(gen_seed)
            elif ch == ord("t"):
                pass
            elif ch == ord("\n"):
                pass

        curses.curs_set(1)

    def generate_maze(self, gen_seed: int) -> None:
        def draw_wrapper(grid):
            return draw_maze(self.screen, grid)

        maze_gen = MazeGenerator(*astuple(self.config), draw_wrapper)
        maze = maze_gen.create()
        self.screen.timeout(-1)
        self.screen.addstr(str(gen_seed))
