import sys
from dataclasses import astuple
from random import seed, randint, randrange, choice
import curses
from typing import List
from mazegen import MazeGenerator, Maze, MazeConfig
from src.utils import generate_name
from src.renderer import MazeRenderer
from src.video_game import VideoGame
from src.solver import PathFind


class InteractiveMenu:
    """Handles interactive maze UI, rendering, input, and gameplay."""

    def __init__(self, config: MazeConfig, screen: curses.window) -> None:
        """Initialize menu with configuration and curses screen."""
        self.config = config
        self.screen = screen
        self.renderer = MazeRenderer(self.screen)
        self.maze_gen = MazeGenerator(*astuple(self.config))
        self.color = 0
        self.show_path = False
        self.show_menu = True
        self.run = True

    def _init(self) -> None:
        """Set up curses environment and generate initial maze."""
        curses.curs_set(0)
        self.renderer.init()
        self.generate_new_maze()

    def display_menu_info(self) -> None:
        """Render menu, controls, and options."""
        screen_height, screen_width = self.screen.getmaxyx()
        menu_options = [
            "(r): Regenerate", "(t): Toggle Path", "(c): Change Color",
            "(s): See Solving", "(g): See Generation", "(f): Play Game",
            "(a): Adjust to screen", "(x): Hide menu", "(q): Quit"
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
        if self.maze.repositioned:
            self.screen.addstr("Warning: Overlapping wih a 42 block prevented")

        self.screen.addnstr("\n" + ("─" * 80), screen_width)
        self.screen.addch("\n")
        if not self.show_menu:
            return

        for i in range(len(options)):
            padding = 25
            option = options[i]
            if i % cols == cols - 1:
                padding = 0
                option += "\n"
            self.screen.addstr(f"{option:{padding}}")
        self.screen.clrtobot()

    def handle_options(self) -> None:
        """Process user input and execute corresponding actions."""
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
            case "a":
                y, x = self.screen.getmaxyx()
                height, width = y // 2 - 5, x // 4 - 1
                if width <= 0 or height <= 0:
                    return
                entry = (randrange(width), randrange(height))
                exit_x = [x for x in range(width) if x != entry[0]]
                exit_y = [x for x in range(height) if x != entry[1]]
                if len(exit_x) < 2 or len(exit_y) < 2:
                    return
                m_exit = (
                    choice(exit_x),
                    choice(exit_y)
                )
                self.maze_gen = MazeGenerator(
                    width, height, entry, m_exit,
                    self.config.output_file, self.config.perfect,
                    randrange(1_000_000), self.config.algorithm
                )
                self.generate_new_maze()
            case "x":
                self.show_menu = not self.show_menu
            case "\n" | " ":
                self.show_path = False

    def start(self) -> None:
        """Run the main loop for rendering, input handling, and gameplay."""
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
                self.renderer.draw_path(self.maze.solution)
            self.display_menu_info()
            self.screen.refresh()

            if self.game.run:
                self.game.update()
            else:
                self.handle_options()

        curses.curs_set(1)

    def generate_new_maze(self, draw: bool = False) -> Maze:
        """Create a new maze and initialize solver with optional animation."""
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
            self.maze.solution = self.solver.find_path(
                self.maze, self.maze.entry
            )
            self.maze.generate_output_file()
            self.show_path = False
            self.game = VideoGame(self.maze, self.screen)
        except OSError:
            sys.exit("Error opening file, check for permissions")
        except Exception as e:
            sys.exit(f"Error: {e}")
