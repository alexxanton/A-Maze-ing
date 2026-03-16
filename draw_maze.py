from generator import Maze, Direction


#print(wall * (maze.width * 2 + 1))
def draw_maze(maze: Maze) -> None:
    wall = "██"
    empty = "  "
    maze.grid[5][5] = 0
    for i in range(len(maze.grid)):
        for j in range(len(maze.grid[i])):
            cell = maze.grid[i][j]
            print(wall if cell & Direction.NORTH else empty, end="")
            print(wall, end="")
            #print(hex(maze.grid[i][j])[2:], end="")
        print()
        for j in range(len(maze.grid[i])):
            print(empty, end="")
            print(wall if cell & Direction.SOUTH else empty, end="")
        print(wall)
