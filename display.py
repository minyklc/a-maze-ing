#!/usr/bin/env python3
# from turtle import st
from generator import Box
# from display import print_maze


class Color:
    def __init__(self):
        self.white = '\033[107m  \0'
        self.cyan = '\033[106m  \0'
        self.purple = '\033[105m  \0'
        self.blue = '\033[104m  \0'
        self.yellow = '\033[103m  \0'
        self.green = '\033[102m  \0'
        self.red = '\033[101m  \0'
        self.black = '\033[100m  \0'
        # self.pos = '\033[100m  \0'
        self.cell = '\033[0m  \0'
        self.void = '\033[0m'


def display(maze: list[list[Box]], 
            forty_two: list | list[list[int]] = [None],
            pos: None | list[int] = None, 
            start: None | tuple[int, int] = None,
            end: None | tuple[int, int] = None) -> None:
    c = Color()
    color = c.red
    top = color * (len(maze[0]) * 2 + 1) + c.void
    print(top)
    for y in range(len(maze)):
        line = color
        bottom = color
        for x in range(len(maze[0])):
            cell = maze[y][x]
            if pos is not None and pos[0] == x and pos[1] == y:
                line += c.black + color if 'E' not in cell.not_wall() else c.black + c.cell
            elif start is not None and start[0] == x and start[1] == y:
                line += c.green + color if 'E' not in cell.not_wall() else c.green + c.cell
            elif end is not None and end[0] == x and end[1] == y:
                line += c.purple + color if 'E' not in cell.not_wall() else c.purple + c.cell
            elif forty_two != [None] and any(cell.pos == tuple(c) for c in forty_two if c is not None):
                line += c.white + color if 'E' not in cell.not_wall() else c.cell * 2
            else:
                line += c.cell + color if 'E' not in cell.not_wall() else c.cell * 2
            bottom += color * 2 if 'S' not in cell.not_wall() else c.cell + color
        print(line, c.void, sep='')
        print(bottom, c.void, sep='')


if __name__ == '__main__':
    ...
    # maze = generator()
    # temp = maze[:][:]
    # with open('output.txt', 'w') as f:
    #     for i in range(len(temp)):
    #         for j in range(len(temp[0])):
    #             if temp[i][j].walls < 10:
    #                 f.write(f'{int(hex(temp[i][j].walls).split('x')[-1])} ')
    #             else:
    #                 f.write(f'{hex(temp[i][j].walls).split('x')[-1].capitalize()} ')
    #         f.write('\n')
    # # print_maze(temp)
    # display(maze)
