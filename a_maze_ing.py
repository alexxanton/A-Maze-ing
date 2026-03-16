import sys
from parse import parse, ParsingError
from generator import MazeGenerator
from dataclasses import astuple
from draw_maze import draw_maze


def main() -> None:
    if len(sys.argv) < 2:
        print("No config file provided!")
        return
    try:
        config = parse(sys.argv[1])
    except ParsingError as e:
        print("Error while parsing file:", e)
        return

    maze_gen = MazeGenerator(*astuple(config))
    maze = maze_gen.create()
    draw_maze(maze)


if __name__ == "__main__":
    main()
