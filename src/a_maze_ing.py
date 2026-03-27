import sys
from parser import ConfigParser, ParsingError
import curses
from interactive_menu import InteractiveMenu


def main(stdscr: curses.window) -> None:
    if len(sys.argv) < 2:
        print("No config file provided!")
        return
    try:
        config_parser = ConfigParser()
        config = config_parser.parse(sys.argv[1])
    except ParsingError as e:
        exit(f"Error while parsing file: {e}")
        return

    menu = InteractiveMenu(config, stdscr)
    menu.init()
    menu.start()


if __name__ == "__main__":
    curses.wrapper(main)
