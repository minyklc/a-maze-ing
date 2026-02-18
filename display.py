#!/usr/bin/env python3
from rich.console import Console


def print_maze(maze):
    for n in maze:
        print("".join(n))
    print()


def maze():
    maze = [
        [2, 11, 6],
        [3, 7, 13],
        [6, 10, 15],
        [12, 7, 9],
    ]
    # print_maze(maze)
    for i in range(len(maze)):
        for j in range(len(maze[0])):
            if maze[i][j] < 10:
                maze[i][j] = int(hex(maze[i][j]).split('x')[-1])
            else:
                maze[i][j] = hex(maze[i][j]).split('x')[-1].capitalize()
    # print_maze(maze)

    c = Console()
    c.print("┏━┳━┓")
    c.print("║   ║")
    c.print("╚═══╝")
    print()
    print("┏━┳━┓")
    print("┣━╋━┫")
    print("┗━┻━┛")
    maze2 = [
        ['┏', '━', '━', '━', '━', '━','┓'],
        ['┣', '━', '━', '━', '━', '┓', '┃'],
        ['┣', '━', '━', ' ', '━', '┛', '┫'],
        ['┗', '━', '━', '┻', '━', '━', '┛'],
    ]
    print()
    print_maze(maze2)
    print( '▄︎▄︎▄︎▄︎▄︎▄︎▄︎▄︎▄︎▄︎▄︎▄︎▄︎▄︎▄︎▄︎▄︎▄︎▄︎▄︎▄︎▄︎▄︎▄︎▄︎')
    print( '█', '  ', '█  █  █  █  █  █  █  █', sep='')
    print( '█▀︎▀︎█  █  █  █  █  █  █  █')
    print( '█▄︎▄︎█  █  █  █  █  █  █  █')
    print( '█  █  █  █  █  █  █  █  █')
    print( '█▀︎▀︎█  █  █  █  █  █  █  █')
    print( '█▄︎▄︎█  █  █  █  █  █  █  █')
    print( '█  █  █  █  █  █  █  █  █')
    print( '█▀︎▀︎█  █  █  █  █  █  █  █')
    print( '█▄︎▄︎█  █  █  █  █  █  █  █')
    print( '█  █  █  █  █  █  █  █  █')
    print( '▀︎▀︎▀︎▀︎▀︎▀︎▀︎▀︎▀︎▀︎▀︎▀︎▀︎▀︎▀︎▀︎▀︎▀︎▀︎▀︎▀︎▀︎▀︎▀︎▀︎')
    # print( '█▄︎▄︎█▄︎▄︎█▄︎▄︎█▄︎▄︎█▄︎▄︎█▄︎▄︎█▄︎▄︎█▄︎▄︎█')

    # maze = [
    #     [1, 0, 1],
    #     [0, 1, 0],
    #     [1, 1, 1],
    # ]
    
    # for row in maze:
    #     print("".join("█" if n else " " for n in row))


if __name__ == "__main__":
    maze()
