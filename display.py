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
    
    def which_color(self, color: str) -> tuple[str, str]:
        if color == 'purple':
            return self.purple, self.lightpurple
        elif color == 'yellow':
            return self.yellow, self.lightyellow
        elif color == 'blue':
            return self.blue, self.lightblue
        elif color == 'cyan':
            return self.cyan, self.lightcyan
        elif color == 'green':
            return self.green, self.lightgreen
        elif color == 'black':
            return self.black, self.white
        elif color == 'white':
            return self.white, self.grey
        else:
            return self.red, self.lightred


def display(maze: list[list[Box]],
            forty_two: set | set[tuple[int]],
            path: set | set[tuple[int]],
            color: str,
            animation: bool = False,
            pos: None | list[int] = None,
            start: None | list[int] = None,
            end: None | list[int] = None) -> None:

    c = Color()
    cwall, clight = c.which_color(color)
    top = cwall * (len(maze[0]) * 2 + 1) + c.void
    if animation:
        time.sleep(0.05)
    print(top)

    for y in range(len(maze)):
        line = cwall
        bottom = cwall
        for x in range(len(maze[0])):
            cell = maze[y][x]
            walls = cell.has_wall()
            if pos and pos[0] == x and pos[1] == y:
                line += c.black + cwall if 'E' in walls else c.black + c.cell
            elif start and start[0] == x and start[1] == y:
                line += c.purple + cwall if 'E' in walls else c.purple + c.cell
            elif end and end[0] == x and end[1] == y:
                line += c.lightpurple + cwall if 'E' in walls else c.lightpurple + c.cell
            elif path and cell.pos in path:
                line += c.grey + cwall if 'E' in walls else c.grey + c.cell
            elif forty_two and cell.pos in forty_two:
                line += clight + cwall
            else:
                line += c.cell + cwall if 'E' in walls else c.cell * 2
            bottom += cwall * 2 if 'S' in walls else c.cell + cwall

        if animation:
            time.sleep(0.05)
        print(f"{line+c.void}")
        if animation:
            time.sleep(0.05)
        print(f"{bottom+c.void}")


if __name__ == '__main__':
    ...
