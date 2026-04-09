import sys
from src.parser import ConfigParser, ParsingError
import curses
from src.interactive_menu import InteractiveMenu


def main(stdscr: curses.window) -> None:
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
    try:
        curses.wrapper(main)
    except KeyboardInterrupt:
        print("Program halted!")
