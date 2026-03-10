import sys
from parse import parse, ParsingError


def main() -> None:
    if len(sys.argv) < 2:
        print("No config file provided!")
        return
    try:
        parse(sys.argv[1])
    except ParsingError as e:
        print("Error while parsing file:", e)


if __name__ == "__main__":
    main()
