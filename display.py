#!/usr/bin/env python3
from generator import Box, generator, print_maze


class DisplayMaze:
    def __init__(self, maze: list[list[Box]], color: int):
        self.w = len(maze)
        self.l = len(maze[0])
        self.maze = maze
        self.display = []
        self.color = color
        self.pos = [0, 0]
    
    def createdisp(self):
        self.toprow()
        return self.display

    def toprow(self):
        tr = '▄︎▄︎▄︎' * self.l + '▄︎'
        self.display.append(tr)
    
    def eachrow(self):
        ...
    
    def lastrow(self):
        tr = '▀︎▀︎▀︎' * self.l + '▀︎'
        self.display.append(tr)


def display(maze: list[list[Box]]):
    # print_maze(maze)
    temp = maze[:][:]
    for i in range(len(maze)):
        for j in range(len(maze[0])):
            if temp[i][j].walls < 10:
                temp[i][j].walls = int(hex(temp[i][j].walls).split('x')[-1])
            else:
                temp[i][j].walls = hex(temp[i][j].walls).split('x')[-1].capitalize()
    print_maze(temp)
    
    display = DisplayMaze(maze, 0)
    for r in display.createdisp():
        print(r)

    # c = Console()
    # c.print("┏━┳━┓")
    # c.print("║   ║")
    # c.print("╚═══╝")
    # print()
    # print("┏━┳━┓")
    # print("┣━╋━┫")
    # print("┗━┻━┛")
    # maze2 = [
    #     ['┏', '━', '━', '━', '━', '━','┓'],
    #     ['┣', '━', '━', '━', '━', '┓', '┃'],
    #     ['┣', '━', '━', ' ', '━', '┛', '┫'],
    #     ['┗', '━', '━', '┻', '━', '━', '┛'],
    # ]
    # print()


if __name__ == "__main__":
    display(generator())
