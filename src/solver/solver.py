from __future__ import annotations
from typing import List, Tuple, Callable, Any, Optional
from copy import deepcopy
from mazegen import Maze, MazeEntity, Direction


class Node:
    """Represent a node in pathfinding with position and parent link."""
    def __init__(self, pos: Tuple[int, int], prev: Node | None = None) -> None:
        """Initialize node with position and optional previous node."""
        self.pos = pos
        self.prev = prev

    def get_path(self) -> List[Tuple[int, int]]:
        """Return path from start node to current node."""
        path: List[Tuple[int, int]] = []
        node: Node | None = self
        while node is not None:
            path.append(node.pos)
            node = node.prev
        path.reverse()
        return path


class PathFind:
    """Find path in a maze using BFS or DFS."""
    def __init__(
        self, target: MazeEntity, solver: str = "bfs", **kwargs: Any
    ) -> None:
        """Initialize solver with target entity and algorithm type."""
        self.target = target
        self.solver = solver
        super().__init__(**kwargs)

    def find_path(
            self,
            maze: Maze,
            start_from: Tuple[int, int],
            draw: Optional[Callable[[List[List[int]]], None]] = None
    ) -> List[Tuple[int, int]]:
        """Compute path from start to target, optionally visualizing steps."""
        def get_neighbors(node: Node) -> List[Node]:
            """Return reachable neighbor nodes from current node."""
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

        def get_pop_method() -> Callable[[List[Node]], Node]:
            """Return node retrieval method based on solver type."""
            def pop_dfs(nodes: List[Node]) -> Node:
                """Pop last node"""
                return nodes.pop()

            def pop_bfs(nodes: List[Node]) -> Node:
                """Pop first node"""
                return nodes.pop(0)

            if getattr(self, "solver", "bfs") == "dfs":
                return pop_dfs
            else:
                return pop_bfs

        if not start_from or not self.target:
            raise ValueError("Must provide a start position and a target")

        VISITED = 0x80
        start = Node(start_from)
        end = self.target.pos
        grid: List[List[int]] = deepcopy(maze.grid)
        nodes: List[Node] = [start]
        pop_method = get_pop_method()

        while nodes:
            node = pop_method(nodes)
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
