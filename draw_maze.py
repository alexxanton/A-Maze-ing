from generator import Maze, Direction


#print(wall * (maze.width * 2 + 1))
#print(hex(maze.grid[i][j])[2:], end="")

def draw_maze(maze: Maze) -> None:
    for i in range(len(maze.grid)):
        for j in range(len(maze.grid[i])):
            cell = maze.grid[i][j]
            print("+", end="")
            if cell & Direction.NORTH:
                print("--", end="")
            else:
                print("  ", end="")
        print()
        for j in range(len(maze.grid[i])):
            cell = maze.grid[i][j]
            print("|" if cell & Direction.WEST else " ", end="")
            #print("  ", end="")
            hex_num = hex(maze.grid[i][j] & 0b00001111)[1:]
            print(hex_num.replace("x", " "), end="")
        print()
