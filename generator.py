#!/usr/bin/env python3


class Box:
    def __init__(self, x: int, y: int):
        self.pos = (x, y)
        self.walls = 0b1111

    def add_wall(self, dir) -> None:
        if dir == 'north':
            self.walls += 0b0001
        elif dir == 'east':
            self.walls += 0b0010
        elif dir == 'south':
            self.walls += 0b0100
        elif dir == 'west':
            self.walls += 0b1000

    def remove_wall(self, dir) -> None:
        if dir == 'north':
            self.walls -= 0b0001
        elif dir == 'east':
            self.walls -= 0b0010
        elif dir == 'south':
            self.walls -= 0b0100
        elif dir == 'west':
            self.walls -= 0b1000


class Maze:
    def __init__(self, width: int, length: int,
                 start: tuple, end: tuple, perfect: bool):
        # self.w = width
        # self.l = length
        self.p = perfect
        self.s = start
        self.e = end
        self.m = self.blank_maze(width, length)
        

    def blank_maze(self, width: int, length: int) -> list[list[int]]:
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
        # stack = []
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


if __name__ == "__main__":
    generator()