from generator import MazeGenerator, Maze
from dataclasses import astuple
from draw_maze import draw_maze, Colors
from random import seed, randint
from sys import stdout
import curses


class InteractiveMenu:
    BLUE_MAZE = (Colors.BLUE_WALLS, Colors.FRONTIER, Colors.BLOCK)
    RED_MAZE = (Colors.RED_WALLS, Colors.FRONTIER, Colors.BLOCK)
    GREEN_MAZE = (Colors.GREEN_WALLS, Colors.FRONTIER, Colors.BLOCK)

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
            curses.init_pair(Colors.FRONTIER, 0, 9)
            curses.init_pair(Colors.BLOCK, 0, 14)

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
                maze = maze_gen.create()
            elif ch == ord("a"):
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
        #self.screen.addstr(str(gen_seed))
        return maze
