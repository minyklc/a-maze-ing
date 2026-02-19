#!/usr/bin/env python3
from random import random, randint, choice


class Box:
    def __init__(self, x: int, y: int):
        self.pos = (x, y)
        self.walls = 0b1111

    def add_wall(self, dir: list | str) -> None:
        if 'N' in dir and 'N' in self.not_wall():
            self.walls += 0b0001
        if 'E' in dir and 'E' in self.not_wall():
            self.walls += 0b0010
        if 'S' in dir and 'S' in self.not_wall():
            self.walls += 0b0100
        if 'W' in dir and 'W' in self.not_wall():
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

        if dir == 'N' and 'N' not in self.not_wall():
            self.walls -= 0b0001
        elif dir == 'E' and 'E' not in self.not_wall():
            self.walls -= 0b0010
        elif dir == 'S' and 'S' not in self.not_wall():
            self.walls -= 0b0100
        elif dir == 'W' and 'W' not in self.not_wall():
            self.walls -= 0b1000
    
    def not_wall(self) -> list[str | None]:
        m = []
        if self.walls % 2 == 0:
            m.append('N')
        if int(self.walls / 2) % 2 == 0:
            m.append('E')
        if int(self.walls / 4) % 2 == 0:
            m.append('S')
        if int(self.walls / 8) % 2 == 0:
            m.append('W')
        return m


class Maze:
    def __init__(self, width: int, length: int,
                 start: tuple, end: tuple, perfect: bool):
        self.w = width
        self.l = length
        self.p = perfect
        self.s = start
        self.e = end
        self.m = self.blank_maze(width, length)

    def blank_maze(self, width: int, length: int) -> list[list[Box]]:
        maze = []
        for n in range(width):
            maze.append([])
            for b in range(length):
                maze[n].append(Box(b, n))
        return maze

    def generate(self):
        if self.p is True:
            self.perfect_maze()
        else:
            self.imperfect_maze()

    def perfect_maze(self):
        stack = []
        visited = set()

        initial = (randint(0, self.l - 1), randint(0, self.w - 1))
        pos = [initial[0], initial[1]]

        stack.append(pos[:]) # stack of lists of position
        visited.add(tuple(pos))

        while stack:
            pos = stack[-1][:]
            print(pos)
            print(stack)
            print_maze(self.m)
            dir = self.can_pass_through(pos, visited)
            if dir:
                next = choice(dir)
                self.m[pos[1]][pos[0]].remove_wall(next)
                new = self.update_pos(pos, next)
                self.m[new[1]][new[0]].remove_wall(next, reverse=True)
                stack.append(new[:])
                visited.add(tuple(new[:]))
            else:
                stack.pop(-1)
                
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

    def can_pass_through(self, pos: list, stack: set) -> list:
        r = []
        n = ()
        if pos[1] > 0:
            n = self.m[pos[1] - 1][pos[0]].pos
        e = ()
        if pos[0] < self.l - 1:
            e = self.m[pos[1]][pos[0] + 1].pos
        s = ()
        if pos[1] < self.w - 1:
            s = self.m[pos[1] + 1][pos[0]].pos
        w = ()
        if pos[0] > 0:
            w = self.m[pos[1]][pos[0] - 1].pos

        # print(n, e, s, w)
        # print(stack)
        if n and not any(p == n for p in stack):
            print('je peux aller au nord!')
            r.append('N')
        # print(any(p for p in stack if self.is_same(p, e)))
        if e and not any(p == e for p in stack):
            print('et a l est!')
            r.append('E')
        # print(any(p for p in stack if self.is_same(p, s)))
        if s and not any(p == s for p in stack):
            print('et au sud!')
            r.append('S')
        # print(any(p for p in stack if self.is_same(p, w)))
        if w and not any(p == w for p in stack):
            print('et a l ouest!')
            r.append('W')
        return r

    @staticmethod
    def is_same(pos: list, pos2: tuple) -> bool:
        if pos[0] == pos2[0] and pos[1] == pos2[1]:
            return True
        return False
        
    def imperfect_maze(self):
        ...


def print_maze(maze):
    for n in maze:
        # print(n)
        for b in n:
            print(b.walls, end=' ')
        print()
    print()


def generator() -> list[list[Box]]:
    # maze = [
    #     [13, 5, 3],
    #     [5, 3, 10],
    #     [13, 4, 6],
    # ]
    end = (0, 1) # x, y
    start = (0, 0)
    width = 4
    length = 4
    maze = Maze(width, length, start, end, True)
    print_maze(maze.m)
    maze.generate()
    print_maze(maze.m)
    return maze.m


if __name__ == "__main__":
    generator()
