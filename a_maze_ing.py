import sys
import os
from src.parser import ConfigParser, ParsingError
import curses
from src.interactive_menu import InteractiveMenu


def main(stdscr: curses.window) -> None:
    """Parse the config file and initialize the interactive menu with curses"""
    if len(sys.argv) < 2:
        exit("No config file provided!")

    try:
        config_parser = ConfigParser()
        config = config_parser.parse(sys.argv[1])
    except ParsingError as e:
        exit(f"Error while parsing file: {e}")
        return

    menu = InteractiveMenu(config, stdscr)
    menu.start()


if __name__ == "__main__":
    os.environ["PYTHONBREAKPOINT"] = "0"

    if sys.gettrace() is not None:
        print("pdb not compatible with curses")
        sys.exit(1)

    try:
        curses.wrapper(main)
    except KeyboardInterrupt:
        print("Program halted!")
