from __future__ import annotations
from typing import List, Tuple
from copy import deepcopy
from mazegen import Maze, MazeEntity, Direction


class Node:
    def __init__(self, pos: Tuple[int, int], prev: Node | None = None) -> None:
        self.pos = pos
        self.prev = prev

    def get_path(self) -> List[Tuple[int, int]]:
        path: List[Tuple[int, int]] = []
        node: Node | None = self
        while node is not None:
            path.append(node.pos)
            node = node.prev
        path.reverse()
        return path


class PathFind:
    def __init__(self, target: MazeEntity, **kwargs) -> None:
        self.target = target
        super().__init__(**kwargs)

    def find_path(self, maze: Maze, start_from: Tuple[int, int], draw = None) -> List[Tuple[int, int]]:
        def get_neighbors(node: Node) -> List[Node]:
            nbs = []
            x, y = node.pos

            if (
                x + 1 < maze.width and not grid[y][x + 1] & VISITED
                and not grid[y][x + 1] & Direction.WEST
            ):
                nbs.append(Node((x + 1, y), node))
            if (
                x > 0 and not grid[y][x - 1] & VISITED
                and not grid[y][x - 1] & Direction.EAST
            ):
                nbs.append(Node((x - 1, y), node))
            if (
                y + 1 < maze.height and not grid[y + 1][x] & VISITED
                and not grid[y + 1][x] & Direction.NORTH
            ):
                nbs.append(Node((x, y + 1), node))
            if (
                y > 0 and not grid[y - 1][x] & VISITED
                and not grid[y - 1][x] & Direction.SOUTH
            ):
                nbs.append(Node((x, y - 1), node))
            return nbs
        VISITED = 0x80
        nodes: List[Node] = []

        if not start_from or not self.target:
            raise ValueError("Must provide a start position and a target")

        start = Node(start_from)
        end = self.target.pos
        nodes.append(start)

        grid: List[List[int]] = deepcopy(maze.grid)
        while nodes:
            node = nodes.pop(0)
            x, y = node.pos

            grid[y][x] |= VISITED

            if node.pos == end:
                return node.get_path()

            nbs = get_neighbors(node)
            for nb in nbs:
                nx, ny = nb.pos
                nodes.append(nb)
                grid[ny][nx] |= VISITED

            if draw:
                draw(grid)

        return []
