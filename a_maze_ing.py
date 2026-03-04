#!/usr/bin/env python3
import sys
import os
import termios
import tty
import random
from MazeGenerator import Maze, Box
from generator import generator
from display import display
from parsing import parsing


def up(pos: list[int], maze: list[list[Box]]) -> int:
    n = {1, 3, 5, 7, 9, 11, 13, 15}
    if maze[pos[1]][pos[0]].walls in n:
        return 0
    return 1


def down(pos: list[int], maze: list[list[Box]]) -> int:
    n = (4, 5, 6, 7, 12, 13, 14, 15)
    if maze[pos[1]][pos[0]].walls in n:
        return 0
    return 1


def left(pos: list[int], maze: list[list[Box]]) -> int:
    n = (8, 9, 10, 11, 12, 13, 14, 15)
    if maze[pos[1]][pos[0]].walls in n:
        return 0
    return 1


def right(pos: list[int], maze: list[list[Box]]) -> int:
    n = (2, 3, 6, 7, 10, 11, 14, 15)
    if maze[pos[1]][pos[0]].walls in n:
        return 0
    return 1


def ft_interface(maze: Maze, entry: list[int],
                 exit: list[int], path: set[tuple[int]]):
    pos = entry[:]
    fd = 0
    stt = termios.tcgetattr(fd)

    os.system('clear')
    display(maze.m, maze.ft, path, False, pos, maze.s, maze.e)
    print('up down right left or q')
    
    try:
        tty.setcbreak(fd)
    
        while pos != exit:
            ch1 = sys.stdin.read(1)
            if ch1 == 'q':
                break
            elif ch1 == '\x1b':
                ch2 = sys.stdin.read(1)
                ch3 = sys.stdin.read(1)
    
                if ch2 == '[':
                    if ch3 == 'A': #up
                        if up(pos, maze.m) == 1:
                            pos[1] -= 1
                            os.system('clear')
                            display(maze.m, maze.ft, path, False, pos, maze.s, maze.e)
                            print('up down right left or q')
                    elif ch3 == 'B': #down
                        if down(pos, maze.m) == 1:
                            pos[1] += 1
                            os.system('clear')
                            display(maze.m, maze.ft, path, False, pos, maze.s, maze.e)
                            print('up down right left or q')
                    elif ch3 == 'C': #right
                        if right(pos, maze.m) == 1:
                            pos[0] += 1
                            os.system('clear')
                            display(maze.m, maze.ft, path, False, pos, maze.s, maze.e)
                            print('up down right left or q')
                    elif ch3 == 'D': #left
                        if left(pos, maze.m) == 1:
                            pos[0] -= 1
                            os.system('clear')
                            display(maze.m, maze.ft, path, False, pos, maze.s, maze.e)
                            print('up down right left or q')
        if pos == exit:
            print('congratulation !')
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, stt)
    print("Exited")


def interaction():
    print()
    print('1 = generate new maze')
    print('2 = show/hide the shortest path')
    print('3 = change wall colours')
    print('4 = play the maze')
    print('q = quit')
    print()


def main() -> None:
    args = sys.argv
    if len(args) != 2:
        print('expected execution> python3 a_maze_ing.py config.txt')
        return
    param = parsing(args[1])
    if param == {}:
        return
    maze = generator(param)
    if 'animation' in param.keys():
        anim = True if param['animation'] else False
    else:
        anim = False
    path = set()

    os.system('clear')
    display(maze.m, maze.ft, path, anim)
    print(f'seed: {maze.d}')
    interaction()
    for line in sys.stdin:
        if line.rstrip() == 'q':
            break
        elif line.rstrip() == '1': #regenerate random maze
            param['seed'] = random.randint(0, 2147483647)
            maze = generator(param)
            if path:
                path = maze.sv
        elif line.rstrip() == '2': #show/hide shortest path
            if path:
                path = set()
            else:
                path = maze.sv
        elif line.rstrip() == '3': #change wall color
            ...
        elif line.rstrip() == '4': #play the maze
            ft_interface(maze, param['entry'], param['exit'], path)
        else :
            print('please select another key...')
        os.system('clear')
        display(maze.m, maze.ft, path, anim)
        print(f'seed: {maze.d}')
        interaction()
    
    print("Exit")


if __name__ == "__main__":
    main()
