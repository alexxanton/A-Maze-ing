from dataclasses import astuple
from random import seed, randint
import curses
from typing import List, Tuple
from mazegen import MazeGenerator, Maze, MazeConfig
from .utils import generate_name
from .renderer import MazeRenderer
from .video_game import VideoGame
from .solver import PathFind


class InteractiveMenu:

    def __init__(self, config: MazeConfig, screen: curses.window) -> None:
        self.config = config
        self.screen = screen
        self.renderer = MazeRenderer(self.screen)
        self.maze_gen = MazeGenerator(*astuple(self.config))
        self.solution: List[Tuple[int, int]] = []
        self.color = 0
        self.show_path = False
        self.run = True

    def _init(self) -> None:
        curses.curs_set(0)
        self.renderer.init()
        self.generate_new_maze()

    def display_menu_info(self) -> None:
        screen_height, screen_width = self.screen.getmaxyx()
        menu_options = [
            "(r): Regenerate", "(t): Toggle Path", "(c): Change Color",
            "(s): See Solving", "(g): See Generation", "(f): Play Game",
            "(a): Adjust to screen", "(q): Quit"
        ]

        game_options = [
            "(wasd): Move", "(q): Quit"
        ]

        options = game_options if self.game.run else menu_options
        if screen_width < 50:
            cols = 1
        elif screen_width < 70:
            cols = 2
        else:
            cols = 3

        self.screen.scrollok(True)
        self.screen.addstr(f"Seed: {self.maze_gen.seed:<10}")
        maze_name = generate_name(
            str(self.maze_gen.seed + self.maze.width + self.maze.height)
        )
        self.screen.addstr(f"Maze name: {maze_name:20}")
        if not self.maze.logo:
            self.screen.addstr("Warning: 42 logo doesn't fit")

        self.screen.addnstr("\n" + ("─" * 80), screen_width)
        self.screen.addch("\n")

        for i in range(len(options)):
            padding = 25
            option = options[i]
            if i % cols == cols - 1:
                padding = 0
                option += "\n"
            self.screen.addstr(f"{option:{padding}}")
        self.screen.clrtobot()

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
                self.generate_new_maze()
            case "g":
                self.screen.timeout(20)
                self.generate_new_maze(draw=True)
                self.show_path = False
            case "s":
                def wrap(grid: List[List[int]]) -> None:
                    self.renderer.draw_maze(
                        grid, self.color, self.maze.entities, wait=True
                    )
                self.screen.timeout(10)
                self.solver.find_path(self.maze, self.maze.entry, wrap)
                self.show_path = True
            case "c":
                self.color += 1
                if self.color > 2:
                    self.color = 0
            case "t":
                self.show_path = not self.show_path
            case "f":
                self.game.start()
                self.game.run = True
                self.show_path = False
            case "\n" | " ":
                self.show_path = False

    def start(self) -> None:
        self._init()
        while self.run:
            seed(self.maze_gen.seed)
            self.renderer.draw_maze(
                self.maze.grid,
                self.color,
                self.maze.entities,
                wait=False
            )
            self.screen.clrtobot()
            if self.show_path:
                self.renderer.draw_path(self.solution)
            self.display_menu_info()
            self.screen.refresh()

            if self.game.run:
                self.game.update()
            else:
                self.handle_options()

        curses.curs_set(1)

    def generate_new_maze(self, draw: bool = False) -> Maze:
        def draw_wrapper(grid: List[List[int]]) -> None:
            self.renderer.draw_maze(grid, self.color)

        if draw:
            self.maze_gen.draw_method = draw_wrapper
        else:
            self.maze_gen.draw_method = None

        try:
            self.maze = self.maze_gen.create()
            ex = next(e for e in self.maze.entities if e.name == "exit")
            self.solver = PathFind(ex)
            self.solution = self.solver.find_path(self.maze, self.maze.entry)
            self.show_path = False
            self.game = VideoGame(self.maze, self.screen)
        except Exception as e:
            exit(f"Error: {e}")
