from generator import MazeGenerator, Maze, MazeConfig
from dataclasses import astuple
from random import seed, randint
import curses
from utils import generate_name
from renderer import MazeRenderer
from typing import List
from solver import solve_maze


class InteractiveMenu:

    def __init__(self, config: MazeConfig, screen: curses.window) -> None:
        self.config = config
        self.screen = screen
        self.renderer = MazeRenderer(self.screen)
        self.maze_gen = MazeGenerator(*astuple(self.config))
        self.color = 0

    def init(self) -> None:
        curses.curs_set(0)
        self.renderer.init()
        #curses.raw()

    def screen_resized(self, size = {}):
        current = self.screen.getmaxyx()
        last = getattr(self, "_last_size", None)

        self._last_size = current
        return last is not None and current != last

    def start(self) -> None:
        gen_seed = randint(0, 1_000_000)
        maze = self.generate_maze(gen_seed)
        while True:
            seed(gen_seed)
            if self.screen_resized():
                self.screen.clear()
            self.renderer.draw_maze(
                maze.grid,
                self.color,
                maze.entities,
                wait=False
            )
            self.screen.addstr("Seed: " + "{:<10d}".format(gen_seed))
            self.screen.addstr(
                generate_name(str(gen_seed + maze.width + maze.height))
            )
            if not maze.logo:
                self.screen.addstr("Warning: 42 logo doesn't fit")
            self.screen.addstr("\n" + ("─" * 81) + "\n")
            self.screen.addstr(
                "(r): Regenerate\t\t\t(t): Toggle Path\t\t(c): Change Color\n"
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
                #self.screen.timeout(20)
                #maze = self.generate_maze(gen_seed, draw=True)
                self.screen.timeout(10)
                def wrap(grid):
                    self.renderer.draw_maze(
                        grid, self.color, maze.entities, wait=True)
                solution = solve_maze(maze, wrap, self.screen)
                self.renderer.draw_path(solution)
                self.screen.timeout(-1)
                self.screen.getch()
            elif ch == ord("c"):
                self.color += 1
                if self.color > 2:
                    self.color = 0
            elif ch == ord("t"):
                pass
            elif ch == ord("\n"):
                pass

        curses.curs_set(1)

    def generate_maze(self, gen_seed: int, draw: bool = False) -> Maze:
        def draw_wrapper(grid: List[List[int]]) -> None:
            self.renderer.draw_maze(grid, self.color)

        if draw:
            self.maze_gen.draw_method = draw_wrapper
        else:
            self.maze_gen.draw_method = None

        try:
            seed(gen_seed)
            maze = self.maze_gen.create()
        except ValueError as e:
            exit(f"Error: {e}")
        return maze
