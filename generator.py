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

    def remove_wall(self, dir: list | str) -> None:
        if 'N' in dir and 'N' not in self.not_wall():
            self.walls -= 0b0001
        if 'E' in dir and 'E' not in self.not_wall():
            self.walls -= 0b0010
        if 'S' in dir and 'S' not in self.not_wall():
            self.walls -= 0b0100
        if 'W' in dir and 'W' not in self.not_wall():
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
        initial = (randint(0, self.l - 1), randint(0, self.w - 1))
        pos = [initial[0], initial[1]]
        stack.append(pos) # stack of lists of position
        while pos:
            # temp = (pos[0], pos[1])
            try:
                next = choice(self.can_pass_through(pos, stack))
            # if next:
                self.m[pos[1]][pos[0]].remove_wall(next)
                pos = self.update_pos(pos, next)
                stack.append(pos)
            except IndexError:
                stack.pop(-1)
                pos = stack[-1]
            if self.is_same(pos, initial):
                pos = []
                
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

    def can_pass_through(self, pos: list, stack: list) -> list:
        r = []
        n = []
        if pos[1] > 0:
            n = self.m[pos[1] - 1][pos[0]].pos
        e = []
        if pos[0] < self.l - 1:
            e = self.m[pos[1]][pos[0] + 1].pos
        s = []
        if pos[1] < self.w - 1:
            s = self.m[pos[1] + 1][pos[0]].pos
        w = []
        if pos[0] > 0:
            w = self.m[pos[1]][pos[0] - 1].pos

        if n and not any(p for p in stack if self.is_same(p, n)):
            r.append('N')
        if e and not any(p for p in stack if self.is_same(p, e)):
            r.append('E')
        if s and not any(p for p in stack if self.is_same(p, s)):
            r.append('S')
        if w and not any(p for p in stack if self.is_same(p, w)):
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


def generator():
    # maze = [
    #     [13, 5, 3],
    #     [5, 3, 10],
    #     [13, 4, 6],
    # ]
    end = (0, 1) # x, y
    start = (0, 0)
    width = 3
    length = 3
    maze = Maze(width, length, start, end, True)
    maze.generate()
    print_maze(maze.m)
    maze.generate()
    print_maze(maze.m)


if __name__ == "__main__":
    generator()