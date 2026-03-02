#!/usr/bin/env python3
from generator import Box
import time


class Color:
    def __init__(self):
        self.white = '\033[47m  \0'
        self.lightcyan = '\033[106m  \0'
        self.cyan = '\033[46m  \0'
        self.lightpurple = '\033[105m  \0'
        self.purple = '\033[45m  \0'
        self.lightblue = '\033[104m  \0'
        self.blue = '\033[44m  \0'
        self.lightyellow = '\033[103m  \0'
        self.yellow = '\033[43m  \0'
        self.lightgreen = '\033[102m  \0'
        self.green = '\033[42m  \0'
        self.lightred = '\033[101m  \0'
        self.red = '\033[41m  \0'
        self.black = '\033[100m  \0'
        self.cell = '\033[0m  \0'
        self.void = '\033[0m'


def display(maze: list[list[Box]],
            forty_two: list | list[list[int]],
            path: list | list[list[int]],
            animation: bool = False,
            pos: None | list[int] = None,
            start: None | list[int] = None,
            end: None | list[int] = None) -> None:

    c = Color()
    color = c.red
    top = color * (len(maze[0]) * 2 + 1) + c.void
    if animation:
        time.sleep(0.05)
    print(top)

    for y in range(len(maze)):
        line = color
        bottom = color
        for x in range(len(maze[0])):
            cell = maze[y][x]
            if pos and pos[0] == x and pos[1] == y:
                line += c.black + color if 'E' in cell.has_wall() else c.black + c.cell
            elif start and start[0] == x and start[1] == y:
                line += c.lightpurple + color if 'E' in cell.has_wall() else c.green + c.cell
            elif end and end[0] == x and end[1] == y:
                line += c.purple + color if 'E' in cell.has_wall() else c.purple + c.cell
            elif path and any(cell.pos == tuple(c) for c in path):
                line += c.lightgreen + color if 'E' in cell.has_wall() else c.lightgreen + c.cell
            elif forty_two and any(cell.pos == tuple(c) for c in forty_two):
                line += c.lightred + color
            else:
                line += c.cell + color if 'E' in cell.has_wall() else c.cell * 2
            bottom += color * 2 if 'S' in cell.has_wall() else c.cell + color

        if animation:
            time.sleep(0.05)
        print(line, c.void, sep='')
        if animation:
            time.sleep(0.05)
        print(bottom, c.void, sep='')


if __name__ == '__main__':
    ...
