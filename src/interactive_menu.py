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
        self.maze = self.maze_gen.create()
        self.color = 0
        self.show_path = False

    def init(self) -> None:
        curses.curs_set(0)
        self.renderer.init()
        #curses.raw()

    def screen_resized(self, size = {}):
        current = self.screen.getmaxyx()
        last = getattr(self, "_last_size", None)

        self._last_size = current
        return last is not None and current != last

    def display_menu_info(self) -> None:
        options = ["(r): Regenerate", "(t): Toggle Path", "(c): Change Color",
                   "(a): Play Animations", "(g): Play Game", "(q): Quit"]
        self.screen.scrollok(True)
        self.screen.addstr(f"Seed: {self.maze_gen.seed:<10}")
        self.screen.addstr(
            generate_name(
                str(self.maze_gen.seed + self.maze.width + self.maze.height)
            )
        )
        if not self.maze.logo:
            self.screen.addstr("Warning: 42 logo doesn't fit")
        self.screen.addstr("\n" + ("─" * 81) + "\n")
        offset = 0
        padding = 20
        screen_width = self.screen.getmaxyx()[1]
        if screen_width < 45:
            rows = 6
            cols = 1
            offset_amount = 0
        elif screen_width < 60:
            rows = 3
            cols = 2
            offset_amount = 1
        else:
            rows = 2
            cols = 3
            offset_amount = 2
            padding = 22

        for row in range(rows):
            x = 0
            for col in range(cols):
                option = options[row + col + offset]
                self.screen.addstr(f"{option:{padding}}")
            offset += offset_amount
            self.screen.addch("\n")
        self.screen.scrollok(False)

    def start(self) -> None:
        #maze = self.generate_maze(gen_seed)
        while True:
            seed(self.maze_gen.seed)
            if self.screen_resized():
                self.screen.clear()
            self.renderer.draw_maze(
                self.maze.grid,
                self.color,
                self.maze.entities,
                wait=False
            )
            self.display_menu_info()
            self.screen.refresh()
            self.screen.timeout(-1)

            ch = self.screen.getch()
            if ch <= ord("Z"):
                ch += ord("a") - ord("A")
            if ch == ord("q"):
                break
            elif ch == ord("r"):
                self.maze_gen.seed = randint(0, 1_000_000)
                self.maze = self.generate_maze()
            elif ch == ord("a"):
                #self.screen.timeout(20)
                #maze = self.generate_maze(draw=True)
                self.screen.timeout(10)
                def wrap(grid):
                    self.renderer.draw_maze(
                        grid, self.color, self.maze.entities, wait=True)
                solution = solve_maze(self.maze, wrap, self.screen)
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

    def generate_maze(self, draw: bool = False) -> Maze:
        def draw_wrapper(grid: List[List[int]]) -> None:
            self.renderer.draw_maze(grid, self.color)

        if draw:
            self.maze_gen.draw_method = draw_wrapper
        else:
            self.maze_gen.draw_method = None

        try:
            maze = self.maze_gen.create()
        except ValueError as e:
            exit(f"Error: {e}")
        return maze
