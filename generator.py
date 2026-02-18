#!/usr/bin/env python3
from random import random, randint


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
        pos = (randint(0, self.l), randint(0, self.w))
        while len(stack) < self.l * self.w:
            ...
        

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
    maze.p
    maze.m[0][2].remove_wall(['W', 'N', 'E', 'S'])
    maze.m[0][2].add_wall(['W', 'E', 'S'])
    print(maze.m[0][2].not_wall())
    maze.generate()


if __name__ == "__main__":
    generator()