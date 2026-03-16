from generator import Maze, Directions


def draw_maze(maze: Maze) -> None:
    wall = "█"
    for x in range(len(maze.grid)):
        print(wall * (maze.width * 2 + 1))
        for y in range(len(maze.grid[x])):
            print(wall, end="")
            print(hex(maze.grid[x][y])[2:], end="")
        print(wall)
    print(wall * (maze.width * 2 + 1))
