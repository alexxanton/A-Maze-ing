from generator import MazeGenerator, Maze
from dataclasses import astuple
from draw_maze import draw_maze, Colors
from random import seed, randint
from sys import stdout
import curses
from utils import generate_name


class InteractiveMenu:
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

    def __init__(self, config) -> None:
        self.config = config
        self.screen = None
        self.maze_gen = MazeGenerator(*astuple(self.config))
        self.variations = [self.BLUE_MAZE, self.RED_MAZE, self.GREEN_MAZE]
        self.color = 0

    def init(self):
        self.screen = curses.initscr()
        curses.curs_set(0)
        #curses.raw()

        if curses.has_colors():
            curses.start_color()
            curses.init_pair(self.BLUE_MAZE[0], 4, 6)
            curses.init_pair(self.RED_MAZE[0], 1, 9)
            curses.init_pair(self.GREEN_MAZE[0], 2, 10)
            curses.init_pair(Colors.RED_FRONTIER, 0, 9)
            curses.init_pair(Colors.BLUE_FRONTIER, 0, 6)
            curses.init_pair(Colors.PURPLE_BLOCK, 0, 13)
            curses.init_pair(Colors.YELLOW_BLOCK, 0, 3)

            curses.init_pair(Colors.BLUE_ENTRY, 5, 6)
            curses.init_pair(Colors.BLUE_EXIT, 1, 6)
            curses.init_pair(Colors.RED_ENTRY, 5, 9)
            curses.init_pair(Colors.RED_EXIT, 0, 9)
            curses.init_pair(Colors.GREEN_ENTRY, 5, 10)
            curses.init_pair(Colors.GREEN_EXIT, 1, 10)


    def start(self):
        gen_seed = randint(0, 1_000_000)
        maze = self.generate_maze(gen_seed)
        while True:
            seed(gen_seed)
            draw_maze(
                self.screen,
                maze.grid,
                self.variations[self.color],
                maze.entities,
                wait=False
            )
            self.screen.addstr("Seed: " + "{:<10d}".format(gen_seed))
            self.screen.addstr(generate_name(str(gen_seed)))
            self.screen.addch("\n")
            self.screen.addstr(
                "(r): Regenerate \t\t(t): Toggle Path\t\t(c): Change Color\n"
                "(a): Play Animations\t\t(g): Play Game\t\t\t(q): Quit"
            )
            self.screen.refresh()
            self.screen.timeout(-1)
            ch = self.screen.getch()
            if ch <= ord("Z"):
                ch += ord("a") - ord("A")
            if ch == ord("q"):
                break
            elif ch == ord("r"):
                gen_seed = randint(0, 1_000_000)
                maze = self.generate_maze(gen_seed)
            elif ch == ord("a"):
                self.screen.timeout(20)
                maze = self.generate_maze(gen_seed, draw=True)
            elif ch == ord("c"):
                self.color += 1
                if self.color > len(self.variations) - 1:
                    self.color = 0
            elif ch == ord("t"):
                pass
            elif ch == ord("\n"):
                pass

        curses.curs_set(1)

    def generate_maze(self, gen_seed: int, draw: bool = False) -> Maze:
        palette = self.variations[self.color]
        def draw_wrapper(grid):
            return draw_maze(self.screen, grid, palette)

        if draw:
            self.maze_gen.draw_method = draw_wrapper
        else:
            self.maze_gen.draw_method = None

        try:
            seed(gen_seed)
            maze = self.maze_gen.create()
        except ValueError as e:
            exit(e)
        return maze
