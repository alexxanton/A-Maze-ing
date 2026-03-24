from generator import Maze, MazeEntity, Direction
from typing import List, Tuple
from copy import deepcopy


def solve_maze(maze: Maze, draw, screen) -> List[Tuple[int, int]]:
    def get_entity(name: str) -> MazeEntity | None:
        return next((e for e in maze.entities if e.name == name), None)

    def get_neighbors(x: int, y: int) -> List[Tuple[int, int]]:
        nbs = []

        if (
            x + 1 < maze.width and not grid[y][x + 1] & VISITED
            and not grid[y][x + 1] & Direction.WEST
        ):
            nbs.append((x + 1, y))
        if (
            x > 0 and not grid[y][x - 1] & VISITED
            and not grid[y][x - 1] & Direction.EAST
        ):
            nbs.append((x - 1, y))
        if (
            y + 1 < maze.height and not grid[y + 1][x] & VISITED
            and not grid[y + 1][x] & Direction.NORTH
        ):
            nbs.append((x, y + 1))
        if (
            y > 0 and not grid[y - 1][x] & VISITED
            and not grid[y - 1][x] & Direction.SOUTH
        ):
            nbs.append((x, y - 1))
        return nbs

    VISITED = 0x80
    frontiers: List[Tuple[int, int]] = []

    entry = get_entity("entry")
    m_exit = get_entity("exit")

    if not entry or not m_exit:
        raise ValueError("Must provide an entry and an exit")

    start = entry.pos
    end = m_exit.pos
    frontiers.append(start)

    grid = deepcopy(maze.grid)
    while frontiers:
        node = frontiers.pop(0)
        x, y = node

        #grid[y][x] |= VISITED

        if node == end:
            screen.timeout(-1)
            screen.getch()
            break

        nbs = get_neighbors(x, y)
        for nb in nbs:
            nx, ny = nb
            frontiers.append(nb)
            grid[ny][nx] |= VISITED

        draw(grid)
        #screen.addstr(str(node))

    return []
