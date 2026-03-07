#!/usr/bin/env python3

from random import choice, seed
from typing import Callable, Optional


class Box:
    """Represents a single cell in the maze grid.
    Each Box has a position, a bitmask of walls, and fields for pathfinding.

    Walls bitmask: N=1, E=2, S=4, W=8.
    Initially all walls are present (0b1111).

    Attributes:
        pos: Tuple (x, y) coordinates of the cell.
        walls: Integer bitmask representing which walls are present.
        prev: List of coordinates of the previous cell in the path (for BFS).
        dir: Direction taken to reach this cell from prev (for BFS).

    Methods:
        remove_wall(dir, reverse=False): Remove a wall in the given direction.
        dead_end(width, height): Check if the cell is a dead end and return
                                 the open direction.
        has_wall(): Return a set of directions where walls are present.
    """
    def __init__(self, x: int, y: int):
        """Initialize a maze cell at position (x, y) with all walls closed.

        Args:
            x: Column index of the cell.
            y: Row index of the cell.

        Returns:
            None.
        """
        self.pos = (x, y)
        self.walls = 0b1111
        self.prev = list[int]()
        self.dir = str()

    def remove_wall(self, dir: str, reverse: bool = False) -> None:
        """Remove a wall on the given direction.

        Args:
            dir: Direction of the wall to remove ('N', 'E', 'S', 'W').
            reverse: If True, remove the opposite wall (used for the
            neighbour).

        Returns:
            None.
        """
        if reverse is True:
            if dir == 'N':
                dir = 'S'
            elif dir == 'S':
                dir = 'N'
            elif dir == 'E':
                dir = 'W'
            elif dir == 'W':
                dir = 'E'
        walls = self.has_wall()

        if dir == 'N' and 'N' in walls:
            self.walls -= 0b0001
        elif dir == 'E' and 'E' in walls:
            self.walls -= 0b0010
        elif dir == 'S' and 'S' in walls:
            self.walls -= 0b0100
        elif dir == 'W' and 'W' in walls:
            self.walls -= 0b1000

    def dead_end(self, width: int, height: int) -> str | None:
        """Return the open direction if the cell is a dead end, else None.

        A dead end has exactly 3 walls closed. Returns the one open direction
        only if moving that way stays within the maze bounds.

        Args:
            width: Total width of the maze.
            height: Total height of the maze.

        Returns:
            Direction string ('N', 'E', 'S', 'W') or None.
        """
        if self.walls == 0b0111 and self.pos[0] < width - 1:  # east
            return 'E'
        elif self.walls == 0b1011 and self.pos[1] > 0:  # north
            return 'N'
        elif self.walls == 0b1101 and self.pos[0] > 0:  # west
            return 'W'
        elif self.walls == 0b1110 and self.pos[1] < height - 1:  # south
            return 'S'
        return None

    def has_wall(self) -> set[str]:
        """Return the set of directions where a wall is present.

        Returns:
            A set containing any of 'N', 'E', 'S', 'W'.
        """
        m = set()
        if self.walls in {1, 3, 5, 7, 9, 11, 13, 15}:
            m.add('N')
        if self.walls in {2, 3, 6, 7, 10, 11, 14, 15}:
            m.add('E')
        if self.walls in {4, 5, 6, 7, 12, 13, 14, 15}:
            m.add('S')
        if self.walls in {8, 9, 10, 11, 12, 13, 14, 15}:
            m.add('W')
        return m


class Maze:
    """Represents the maze grid and contains methods to generate and solve it.

    Attributes:
        h: Height of the maze (number of rows).
        w: Width of the maze (number of columns).
        p: If True, generate a perfect maze (unique path).
        s: Entry coordinates as [x, y].
        e: Exit coordinates as [x, y].
        d: Random seed for maze generation.
        m: 2D list of Box objects representing the maze grid.
        ft: Set of (x, y) tuples for the '42' pattern cells.
        sv: Set of (x, y) tuples on the shortest path from entry to exit.
        dir: List of directions ('N', 'E', 'S', 'W') from entry to exit.

    Methods:
        blank_maze(height, width): Create a grid of Box cells with all walls.
        forty_two(height, width): Compute the cell positions forming
                                  the '42' pattern.
        generate(): Generate the maze grid, the '42' pattern, and solve it.
        perfect_maze(): Generate a perfect maze using depth-first search
                        (DFS).
        update_pos(pos, dir): Return the new position after moving
                              in the given direction.
        can_pass_through(pos, visited): Return the list of directions
                                        accessible from pos not yet visited.
        imperfect_maze(): Generate an imperfect maze using DFS
                          with extra wall openings.
        solver(): Find the shortest path from entry to exit using BFS.
        check_pass(pos, visited): Return directions passable from pos
                                  (no wall, not visited).
    """
    def __init__(self, height: int, width: int,
                 start: list[int], end: list[int],
                 perfect: bool,
                 seed: str | int,
                 pattern: str = '42'):
        """Initialize the maze with its dimensions and parameters.

        Args:
            height: Number of rows.
            width: Number of columns.
            start: Entry coordinates as [x, y].
            end: Exit coordinates as [x, y].
            perfect: If True, generate a perfect maze (unique path).
            seed: Random seed for reproducibility.
            pattern: Name of the pattern to embed ('42', 'PA', 'MINA').
                     Defaults to '42'.

        Returns:
            None.
        """
        self.h = height
        self.w = width
        self.p = perfect
        self.s = start
        self.e = end
        self.d = seed
        self.pattern = pattern

    def blank_maze(self, height: int, width: int) -> list[list[Box]]:
        """Create a grid of Box cells with all walls closed.

        Args:
            height: Number of rows.
            width: Number of columns.

        Returns:
            2D list of Box objects indexed as grid[row][col].
        """
        maze = list[list[Box]]()
        for n in range(height):
            maze.append([])
            for b in range(width):
                maze[n].append(Box(b, n))
        return maze

    # Patterns for '42', 'PA', 'MINA' (height = 5, adapted width).
    # Each string uses '#' for filled cells, ' ' for empty.
    # Look at this Mina, flood-filled is finally useful XD
    PATTERNS: dict[str, list[str]] = {
        '42': [
            "#   ###",
            "#     #",
            "### ###",
            "  # #  ",
            "  # ###",
        ],
        'PA': [
            "### ###",
            "# # # #",
            "### ###",
            "#   # #",
            "#   # #",
        ],
        'MINA': [
            "# # # #  # ###",
            "### # ## # # #",
            "# # # ## # ###",
            "# # # # ## # #",
            "# # # #  # # #",
        ],
        'POOP': [
            "### ### ### ###",
            "# # # # # # # #",
            "### # # # # ###",
            "#   # # # # #  ",
            "#   ### ### #  ",
        ],
        'OLI': [
            "### #   ###",
            "# # #    # ",
            "# # #    # ",
            "# # #    # ",
            "### ### ###",
        ],
    }

    def forty_two(self, height: int, width: int,
                  pattern: str = '42') -> set[tuple[int, int]]:
        """Compute the cell positions for the given named pattern.

        The pattern is centered in the maze. Returns an empty set if the
        maze is too small to fit the pattern and prints an error in that
        case.

        Args:
            height: Number of rows.
            width: Number of columns.
            pattern: Name of the pattern ('42', 'PA', 'MINA').
                     Unknown names fall back to '42'.

        Returns:
            Set of (x, y) tuples for cells belonging to the pattern.
        """
        # total = set()

        # if height >= 7 and width >= 9:
        #     pos_x = int((width - 7) / 2)
        #     pos_y = int((height - 5) / 2)
        #     x = pos_x
        #     y = pos_y
        #     menu = [
        #         [0, 4, 1, 1],
        #         [0, 6],
        #         [0, 1, 1, 2, 1, 1],
        #         [2, 2],
        #         [2, 2, 1, 1]
        #     ]
        #     for m in menu:
        #         for i in m:
        #             x += i
        #             total.add((x, y))
        #         x = pos_x
        #         y += 1
        # return total
        rows = self.PATTERNS.get(pattern, self.PATTERNS['42'])
        pat_w = len(rows[0])
        pat_h = len(rows)
        if height < pat_h + 2 or width < pat_w + 2:
            print(f'error: maze too small to display "{pattern}" pattern'
                  f' (need {pat_w + 2} width x {pat_h + 2} height)')
            return set()
        pos_x = (width - pat_w) // 2
        pos_y = (height - pat_h) // 2
        total: set[tuple[int, int]] = set()
        for dy, row in enumerate(rows):
            for dx, cell in enumerate(row):
                if cell == '#':
                    total.add((pos_x + dx, pos_y + dy))
        return total

    def generate(self,
                 callback: Optional[Callable[[list[list['Box']]], None]]
                 = None) -> None:
        """Generate the maze grid, the '42' pattern, and solve it.

        Args:
            callback: Optional function called after each wall removal during
                      generation, receiving the current grid for live display.

        Returns:
            None.

        Raises:
            ValueError: If entry or exit falls inside the '42' pattern.
        """
        self.m = self.blank_maze(self.h, self.w)
        self.ft = self.forty_two(self.h, self.w, self.pattern)
        if tuple(self.s) in self.ft or tuple(self.e) in self.ft:
            raise ValueError()
        if self.p:
            self.perfect_maze(callback)
        else:
            self.imperfect_maze(callback)
        self.sv, self.dir = self.solver()

    def perfect_maze(self,
                     callback: Optional[Callable[[list[list['Box']]], None]]
                     = None) -> None:  # dfs
        """Generate a perfect maze using depth-first search (DFS).

        A perfect maze has exactly one path between any two cells.
        The '42' pattern cells are pre-marked as visited so they stay closed.

        Args:
            callback: Optional function called after each wall removal,
                      receiving the current grid for live animation.

        Returns:
             None.
        """
        stack = []
        visited = set()
        pos = [0, 0]

        stack.append(pos[:])  # stack of list of positions -> actual way
        visited.add(tuple(pos))  # all visited positions
        if self.ft:
            for p in self.ft:
                if p is not None:
                    visited.add(tuple(p))

        seed(self.d)
        while stack:
            pos = stack[-1][:]
            dir = self.can_pass_through(pos, visited)
            if dir:
                next = choice(dir)
                self.m[pos[1]][pos[0]].remove_wall(next)
                new = self.update_pos(pos, next)
                self.m[new[1]][new[0]].remove_wall(next, True)
                stack.append(new[:])
                visited.add(tuple(new[:]))
                if callback:
                    callback(self.m)
            else:
                stack.pop(-1)

    def update_pos(self, pos: list[int], dir: str) -> list[int]:
        """Return the new position after moving in the given direction.

        Args:
            pos: Current [x, y] position.
            dir: Direction to move ('N', 'E', 'S', 'W').

        Returns:
            Updated [x, y] position.
        """
        if dir == 'N':
            pos[1] -= 1
        elif dir == 'E':
            pos[0] += 1
        elif dir == 'S':
            pos[1] += 1
        elif dir == 'W':
            pos[0] -= 1
        return pos

    def can_pass_through(self, pos: list[int],
                         visited: set[tuple[int, ...]]) -> list[str]:
        """Return the list of directions accessible from pos not yet visited.

        Args:
            pos: Current [x, y] position.
            visited: Set of already visited (x, y) tuples.

        Returns:
            List of direction strings among 'N', 'E', 'S', 'W'.
        """
        r = list[str]()
        n = tuple[int, ...]()
        if pos[1] > 0:
            n = self.m[pos[1] - 1][pos[0]].pos
        e = tuple[int, ...]()
        if pos[0] < self.w - 1:
            e = self.m[pos[1]][pos[0] + 1].pos
        s = tuple[int, ...]()
        if pos[1] < self.h - 1:
            s = self.m[pos[1] + 1][pos[0]].pos
        w = tuple[int, ...]()
        if pos[0] > 0:
            w = self.m[pos[1]][pos[0] - 1].pos

        if n and n not in visited:
            r.append('N')
        if e and e not in visited:
            r.append('E')
        if s and s not in visited:
            r.append('S')
        if w and w not in visited:
            r.append('W')
        return r

    def imperfect_maze(self,
                       callback: Optional[Callable[[list[list['Box']]], None]]
                       = None) -> None:
        """Generate an imperfect maze using DFS with extra wall openings.

        Based on DFS like perfect_maze, but dead-end cells get an additional
        wall removed to create loops and multiple paths.

        Args:
            callback: Optional function called after each wall removal,
                      receiving the current grid for live animation.

        Returns:
            None.
        """
        stack = []
        visited = set()
        pos = [0, 0]
        state = 0

        stack.append(pos[:])  # stack of list of positions -> actual way
        visited.add(tuple(pos))  # all visited positions
        if self.ft:
            for p in self.ft:
                if p is not None:
                    visited.add(tuple(p))

        seed(self.d)
        while stack:
            pos = stack[-1][:]
            dir = self.can_pass_through(pos, visited)
            if dir:
                state = 0
                next = choice(dir)
                self.m[pos[1]][pos[0]].remove_wall(next)
                new = self.update_pos(pos, next)
                self.m[new[1]][new[0]].remove_wall(next, True)
                stack.append(new[:])
                visited.add(tuple(new[:]))
                if callback:
                    callback(self.m)
            elif state == 0:
                state = 1
                last = stack.pop(-1)
                last_d: Optional[str] = \
                    self.m[last[1]][last[0]].dead_end(self.w, self.h)
                if last_d is None:
                    continue  # to avoid to call update_pos with None
                last2: list[int] = self.update_pos(pos, str(last_d))
                if last != [0, 0] and tuple(last2) not in self.ft:
                    self.m[last[1]][last[0]].remove_wall(str(last_d))
                    self.m[last2[1]][last2[0]].remove_wall(str(last_d), True)
                    if callback:
                        callback(self.m)
            else:
                stack.pop(-1)

    def solver(self) -> tuple[set[tuple[int, int]], list[str]]:  # bfs
        """Find the shortest path from entry to exit using BFS.

        Returns:
            A tuple of (path, directions) where:
            - path is a set of (x, y) tuples on the shortest path.
            - directions is the ordered list of moves ('N','E','S','W')
              from entry to exit.
        """
        stack = []
        visited = set[tuple[int, ...]]()
        pos = self.s[:]

        stack.append(pos[:])  # stack of list of positions on the same level
        visited.add(tuple(pos))  # all visited positions
        if self.ft:
            for q in self.ft:
                visited.add(tuple(q))

        while self.e not in stack:
            t_stack = []
            while stack:
                p: list[int] = stack[0]
                dir = self.check_pass(p, visited)
                if dir:
                    for d in dir:
                        tmp = self.update_pos(p[:], d)
                        t_stack.append(tmp[:])
                        self.m[tmp[1]][tmp[0]].prev = p[:]
                        self.m[tmp[1]][tmp[0]].dir = d
                visited.add(tuple(p[:]))
                stack.remove(p[:])
            stack = t_stack

        path = set()
        directions = list()
        end = list(self.e)[:]
        position = self.m[end[1]][end[0]]
        while list(position.pos) != self.s:
            path.add(position.pos[:])
            directions.append(position.dir)
            position = self.m[position.prev[1]][position.prev[0]]
        path.add((self.s[0], self.s[1]))
        directions.reverse()
        # reverse the directions to get the path from entry to exit!
        return path, directions

    def check_pass(self, pos: list[int], visited: set[tuple[int, ...]]
                   ) -> list[str]:
        """Return directions passable from pos (no wall, not visited).

        Args:
            pos: Current [x, y] position.
            visited: Set of already visited (x, y) tuples.

        Returns:
            List of direction strings among 'N', 'E', 'S', 'W'.
        """
        dir = []
        c = ['N', 'E', 'W', 'S']
        for i in c:
            if i not in self.m[pos[1]][pos[0]].has_wall() and \
             tuple(self.update_pos(pos[:], i)) not in visited:
                dir.append(i)
        return dir
