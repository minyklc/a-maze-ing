#!/usr/bin/env python3


class Box:
    def __init__(self, x: int, y: int):
        self.pos = (x, y)
        self.walls = [1, 1, 0, 0]
    
    def add_wall(self, dir):
        ...
    
    def remove_wall(self, dir):
        ...


class Maze:
    def __init__(self, width: int, length: int, perfect: bool):
        # self.w = width
        # self.l = length
        self.p = perfect
        self.m = self.blank_maze(width, length)
    
    def blank_maze(self, width: int, length: int) -> list[list[int]]:
        maze = []
        for n in range(width + 1):
            maze.append([])
            for b in range(length + 1):
                maze[n].append(Box(b, n))
        return maze


def print_maze(maze):
    for n in maze:
        print(n)
        # for b in n:
        #     print(b.pos)
    print()


def generator():
    # maze = [
    #     [13, 5, 3],
    #     [5, 3, 10],
    #     [13, 4, 6],
    # ]
    exit = [0, 1] # x, y
    pos = [0, 0]
    width = 3
    length = 3
    maze = Maze(width, length, True)
    print_maze(maze.m)


if __name__ == "__main__":
    generator()