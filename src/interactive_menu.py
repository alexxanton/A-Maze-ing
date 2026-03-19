from generator import MazeGenerator, Maze
from dataclasses import astuple
from draw_maze import draw_maze, Colors
from random import seed, randint
from sys import stdout
import curses
from utils import generate_name


class InteractiveMenu:
    BLUE_MAZE = (Colors.BLUE_WALLS, Colors.RED_FRONTIER, Colors.PURPLE_BLOCK)
    RED_MAZE = (Colors.RED_WALLS, Colors.BLUE_FRONTIER, Colors._BLOCK)
    GREEN_MAZE = (Colors.GREEN_WALLS, Colors.RED_FRONTIER, Colors.RED_BLOCK)

    def __init__(self, config) -> None:
        self.config = config
        self.screen = None

    def init(self):
        self.screen = curses.initscr()
        curses.curs_set(0)
        curses.raw()

        if curses.has_colors():
            curses.start_color()
            curses.init_pair(self.BLUE_MAZE[0], 4, 6)
            curses.init_pair(self.RED_MAZE[0], 1, 9)
            curses.init_pair(self.GREEN_MAZE[0], 2, 10)
            curses.init_pair(Colors.RED_FRONTIER, 0, 9)
            curses.init_pair(Colors.BLUE_FRONTIER, 0, 6)
            curses.init_pair(Colors.PURPLE_BLOCK, 0, 13)
            curses.init_pair(Colors.RED_BLOCK, 0, 1)


    def start(self):
        gen_seed = randint(0, 1_000_000)
        seed(gen_seed)
        maze_gen = MazeGenerator(*astuple(self.config))
        maze = maze_gen.create()
        variations = [self.BLUE_MAZE, self.RED_MAZE, self.GREEN_MAZE]
        color = 0
        #self.screen.timeout(10)
        while True:
            seed(gen_seed)
            draw_maze(self.screen, maze.grid, variations[color], wait=False)
            self.screen.addstr("Seed: " + "{:<9d}".format(gen_seed))
            self.screen.addstr(generate_name(str(gen_seed)))
            self.screen.addch("\n")
            self.screen.addstr(
                "(r): Regenerate (t): Toggle Path (c): Change Color\n"
                "(a): Play Animations (g): Play Game (q): Quit"
            )
            self.screen.refresh()
            #self.screen.timeout(-1)
            ch = self.screen.getch()
            if ch == ord("q"):
                break
            elif ch == ord("r"):
                #self.screen.timeout(0)
                gen_seed = randint(0, 1_000_000)
                seed(gen_seed)
                maze = maze_gen.create()
            elif ch == ord("a"):
                seed(gen_seed)
                self.screen.timeout(20)
                maze = self.generate_maze(gen_seed, variations[color])
            elif ch == ord("c"):
                color += 1
                if color > len(variations) - 1:
                    color = 0
            elif ch == ord("t"):
                pass
            elif ch == ord("\n"):
                pass

        curses.curs_set(1)

    def generate_maze(self, gen_seed: int, palette) -> Maze:
        def draw_wrapper(grid):
            return draw_maze(self.screen, grid, palette)

        maze_gen = MazeGenerator(*astuple(self.config), draw_wrapper)
        maze = maze_gen.create()
        #self.screen.timeout(-1)
        return maze
