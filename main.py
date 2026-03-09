import sys
from parse import parse


def main() -> None:
    if len(sys.argv) < 2:
        print("No config file provided!")
        return
    parse(sys.argv[1])


if __name__ == "__main__":
    main()
