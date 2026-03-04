#!/usr/bin/env python3
from MazeGenerator import Box
import time


class Color:
    def __init__(self):
        self.white = '\033[47m  '
        self.lightcyan = '\033[106m  '
        self.cyan = '\033[46m  '
        self.lightpurple = '\033[105m  '
        self.purple = '\033[45m  '
        self.lightblue = '\033[104m  '
        self.blue = '\033[44m  '
        self.lightyellow = '\033[103m  '
        self.yellow = '\033[43m  '
        self.lightgreen = '\033[102m  '
        self.green = '\033[42m  '
        self.lightred = '\033[101m  '
        self.red = '\033[41m  '
        self.grey = '\033[100m  '
        self.black = '\033[40m  '
        self.cell = '\033[0m  '
        self.void = '\033[0m'


def display(maze: list[list[Box]],
            forty_two: set | set[tuple[int]],
            path: set | set[tuple[int]],
            animation: bool = False,
            pos: None | list[int] = None,
            start: None | list[int] = None,
            end: None | list[int] = None) -> None:

    c = Color()
    color = c.red
    # s = time.time()
    top = color * (len(maze[0]) * 2 + 1) + c.void
    if animation:
        time.sleep(0.05)
    print(top)

    for y in range(len(maze)):
        line = color
        bottom = color
        for x in range(len(maze[0])):
            cell = maze[y][x]
            walls = cell.has_wall()
            if pos and pos[0] == x and pos[1] == y:
                line += c.black + color if 'E' in walls else c.black + c.cell
            elif start and start[0] == x and start[1] == y:
                line += c.purple + color if 'E' in walls else c.purple + c.cell
            elif end and end[0] == x and end[1] == y:
                line += c.lightpurple + color if 'E' in walls else c.lightpurple + c.cell
            elif path and cell.pos in path:
                line += c.grey + color if 'E' in walls else c.grey + c.cell
            elif forty_two and cell.pos in forty_two:
                line += c.lightred + color
            else:
                line += c.cell + color if 'E' in walls else c.cell * 2
            bottom += color * 2 if 'S' in walls else c.cell + color

        if animation:
            time.sleep(0.05)
        print(f"{line+c.void}")
        # print(line, c.void, sep='')
        if animation:
            time.sleep(0.05)
        # print(bottom, c.void, sep='')
        print(f"{bottom+c.void}")
    # e = time.time()
    # print(e - s)


if __name__ == '__main__':
    ...
