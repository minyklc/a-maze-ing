#!/usr/bin/env python3
from generator import generator, Box
# from display import print_maze


class Color:
    def __init__(self):
        self.magenta = '\033[105m  \0'
        self.cell = '\033[0m  \0'
        self.void = '\033[0m'


def affichage(maze: list[list[Box]]):
    c = Color()
    # print(f"{c.green * (len(maze[0]) * 2 + 1)}")
    top = c.magenta * (len(maze[0]) * 2 + 1) + c.void
    print(top)
    for y in range(len(maze)):
        line = c.magenta
        bottom = c.magenta
        for x in range(len(maze[0])):
            cell = maze[y][x]
            line += c.cell + c.magenta if 'E' not in cell.not_wall() else c.cell * 2
            bottom += c.magenta * 2 if 'S' not in cell.not_wall() else c.cell + c.magenta
            # print(cell.walls, cell.not_wall())
        print(line, c.void, sep='')
        print(bottom, c.void, sep='')
    # top = c.magenta * (len(maze[0]) * 2 + 1) + c.void
    # print(top)


if __name__ == '__main__':
    
    maze = generator()
    temp = maze[:][:]
    with open('output.txt', 'w') as f:
        for i in range(len(temp)):
            for j in range(len(temp[0])):
                if temp[i][j].walls < 10:
                    f.write(f'{int(hex(temp[i][j].walls).split('x')[-1])} ')
                else:
                    f.write(f'{hex(temp[i][j].walls).split('x')[-1].capitalize()} ')
            f.write('\n')
    # print_maze(temp)
    affichage(maze)