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
        self.solution: List[Tuple[int, int]] = solve_maze(self.maze)
        self.color = 0
        self.show_path = False
        self.run = True

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
        options = [
            "(r): Regenerate", "(t): Toggle Path", "(c): Change Color",
            "(s): See Solving", "(z): See Generation", "(g): Play Game",
            "(a): Adjust to screen", "(q): Quit"
        ]
        self.screen.scrollok(True)
        self.screen.addstr(f"Seed: {self.maze_gen.seed:<10}")
        maze_name = generate_name(
            str(self.maze_gen.seed + self.maze.width + self.maze.height)
        )
        self.screen.addstr(f"Maze name: {maze_name:20}")
        if not self.maze.logo:
            self.screen.addstr("Warning: 42 logo doesn't fit")
        screen_width = self.screen.getmaxyx()[1]
        self.screen.addnstr("\n" + ("─" * 80), screen_width)
        self.screen.addch("\n")
        offset = 0
        padding = 20
        if screen_width < 50:
            cols = 1
        elif screen_width < 70:
            cols = 2
        else:
            cols = 3

        for i in range(len(options)):
            padding = 25
            option = options[i]
            if i % cols == cols - 1:
                padding = 0
                option += "\n"
            self.screen.addstr(f"{option:{padding}}")
        self.screen.scrollok(False)

    def handle_options(self) -> None:
        self.screen.timeout(-1)
        ch = self.screen.getch()
        if ch >= ord("A") and ch <= ord("Z"):
            ch += ord("a") - ord("A")

        match chr(ch):
            case "q":
                self.run = False
            case "r":
                self.maze_gen.seed = randint(0, 1_000_000)
                self.maze = self.generate_maze()
                self.solution = solve_maze(self.maze)
                self.show_path = False
            case "z":
                self.screen.timeout(20)
                self.generate_maze(draw=True)
                self.show_path = False
            case "s":
                self.screen.timeout(10)
                def wrap(grid):
                    self.renderer.draw_maze(
                        grid, self.color, self.maze.entities, wait=True)
                solve_maze(self.maze, wrap)
                self.show_path = True
            case "c":
                self.color += 1
                if self.color > 2:
                    self.color = 0
            case "t":
                self.show_path = not self.show_path
            case "\n" | " ":
                self.show_path = False

    def start(self) -> None:
        while self.run:
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
            if self.show_path:
                self.renderer.draw_path(self.solution)
            self.screen.refresh()
            self.handle_options()

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
