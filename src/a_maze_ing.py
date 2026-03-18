import sys
from parse import parse, ParsingError
import curses
from interactive_menu import InteractiveMenu


def main(stdscr=None) -> None:
    if len(sys.argv) < 2:
        print("No config file provided!")
        return
    try:
        config = parse(sys.argv[1])
    except ParsingError as e:
        print("Error while parsing file:", e)
        return

    menu = InteractiveMenu(config)
    menu.init()
    menu.start()


if __name__ == "__main__":
    curses.wrapper(main)
