#!/usr/bin/env python3
from random import choice, seed
import time


class Box:
    def __init__(self, x: int, y: int):
        self.pos = (x, y)
        self.walls = 0b1111

    def add_wall(self, dir: list | str) -> None:
        if 'N' in dir and 'N' not in self.has_wall():
            self.walls += 0b0001
        if 'E' in dir and 'E' not in self.has_wall():
            self.walls += 0b0010
        if 'S' in dir and 'S' not in self.has_wall():
            self.walls += 0b0100
        if 'W' in dir and 'W' not in self.has_wall():
            self.walls += 0b1000

    def remove_wall(self, dir: str, reverse: bool = False) -> None:
        if reverse is True:
            if dir == 'N':
                dir = 'S'
            elif dir == 'S':
                dir = 'N'
            elif dir == 'E':
                dir = 'W'
            elif dir == 'W':
                dir = 'E'

        if dir == 'N' and 'N' in self.has_wall():
            self.walls -= 0b0001
        elif dir == 'E' and 'E' in self.has_wall():
            self.walls -= 0b0010
        elif dir == 'S' and 'S' in self.has_wall():
            self.walls -= 0b0100
        elif dir == 'W' and 'W' in self.has_wall():
            self.walls -= 0b1000

    def has_wall(self) -> set[str | None]:
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
    def __init__(self, height: int, width: int,
                 start: list, end: list,
                 perfect: bool,
                 seed: str | int):
        self.h = height
        self.w = width
        self.p = perfect
        self.s = start
        self.e = end
        self.d = seed

    def blank_maze(self, height: int, width: int) -> list[list[Box]]:
        maze = []
        for n in range(height):
            maze.append([])
            for b in range(width):
                maze[n].append(Box(b, n))
        return maze

    def forty_two(self, height, width) -> set[tuple[int]] | set:
        total = set()

        if height >= 7 and width >= 9:
            pos_x = int((width - 7) / 2)
            pos_y = int((height - 5) / 2)
            x = pos_x
            y = pos_y
            menu = [
                [0, 4, 1, 1],
                [0, 6],
                [0, 1, 1, 2, 1, 1],
                [2, 2],
                [2, 2, 1, 1]
            ]
            for m in menu:
                for i in m:
                    x += i
                    total.add(tuple([x, y]))
                x = pos_x
                y += 1
        return total

    def generate(self):
        self.m = self.blank_maze(self.h, self.w)
        self.ft = self.forty_two(self.h, self.w)
        if self.p is True:
            self.perfect_maze()
        else:
            self.imperfect_maze()
        self.sv, self.dir = self.solver()

    def perfect_maze(self): #dfs
        stack = []
        visited = set()
        pos = [0, 0]

        stack.append(pos[:]) # stack of list of positions -> actual way
        visited.add(tuple(pos)) # all visited positions
        if self.ft != []:
            for p in self.ft:
                if p is not None:
                    visited.add(tuple(p))

        seed(self.d)
        s = time.time()
        r1 = int()
        while stack:
            pos = stack[-1][:]
            s1 = time.time()
            dir = self.can_pass_through(pos, visited)
            e1 = time.time()
            r1 += e1 - s1
            if dir:
                next = choice(dir)
                self.m[pos[1]][pos[0]].remove_wall(next)
                new = self.update_pos(pos, next)
                self.m[new[1]][new[0]].remove_wall(next, True)
                stack.append(new[:])
                visited.add(tuple(new[:]))
            else:
                stack.pop(-1)
            # os.system('clear')
            # display(self.m, self.ft, [], False, pos, self.s, self.e)
            # time.sleep(0.05)
        e = time.time()
        print(e-s)
        print(r1)

    def update_pos(self, pos: list, dir: str) -> list:
        if dir == 'N':
            pos[1] -= 1
        elif dir == 'E':
            pos[0] += 1
        elif dir == 'S':
            pos[1] += 1
        elif dir == 'W':
            pos[0] -= 1
        return pos

    def can_pass_through(self, pos: list, visited: set) -> list:
        r = []
        n = ()
        if pos[1] > 0:
            n = self.m[pos[1] - 1][pos[0]].pos
        e = ()
        if pos[0] < self.w - 1:
            e = self.m[pos[1]][pos[0] + 1].pos
        s = ()
        if pos[1] < self.h - 1:
            s = self.m[pos[1] + 1][pos[0]].pos
        w = ()
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

    # @staticmethod
    # def is_same(pos: list, pos2: tuple) -> bool:
    #     if pos[0] == pos2[0] and pos[1] == pos2[1]:
    #         return True
    #     return False
        
    def imperfect_maze(self):
        ...
    
    def solver(self) -> tuple[set, list]: #bfs
        stack = []
        visited = set()
        pos = list(self.s)[:]
        print(pos, '\n')

        stack.append(pos[:]) # stack of list of positions on the same level
        visited.add(tuple(pos)) # all visited positions
        if self.ft:
            for p in self.ft:
                visited.add(tuple(p))

        while any(p == self.e for p in stack) is False:
            t_stack = []
            while stack:
                p = stack[0]
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
        pos = self.m[end[1]][end[0]]
        while list(pos.pos) != self.s:
            path.add(pos.pos[:])
            directions.append(pos.dir)
            pos = self.m[pos.prev[1]][pos.prev[0]]
        path.add(tuple(self.s))
        # directions.reverse()
        # path.reverse()
        return path, directions
        
    def check_pass(self, pos: list[int], visited: set):
        dir = []
        c = ['N', 'E', 'W', 'S']
        for i in c:
            if i not in self.m[pos[1]][pos[0]].has_wall() and \
                tuple(self.update_pos(pos[:], i)) not in visited:
                    dir.append(i)
        return dir
