#!/usr/bin/env python3
import sys
import os
import termios
import tty
from generator import Box, generator
from display import display
from parsing import parsing


def up(pos: list[int], maze: list[list[Box]]) -> int:
    n = [1, 3, 5, 7, 9, 11, 13, 15]
    if any(n == maze[pos[1]][pos[0]].walls for n in n):
        return 0
    return 1


def down(pos: list[int], maze: list[list[Box]]) -> int:
    n = [4, 5, 6, 7, 12, 13, 14, 15]
    if any(n == maze[pos[1]][pos[0]].walls for n in n):
        return 0
    return 1


def left(pos: list[int], maze: list[list[Box]]) -> int:
    n = [8, 9, 10, 11, 12, 13, 14, 15]
    if any(n == maze[pos[1]][pos[0]].walls for n in n):
        return 0
    return 1


def right(pos: list[int], maze: list[list[Box]]) -> int:
    n = [2, 3, 6, 7, 10, 11, 14, 15]
    if any(n == maze[pos[1]][pos[0]].walls for n in n):
        return 0
    return 1


def ft_interface(maze: list[list[Box]], entry: list[int], exit: list[int]):
    pos = entry[:]
    fd = 0
    stt = termios.tcgetattr(fd)

    os.system('clear')
    display(maze, pos)
    # print(pos)
    print()
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
                        if up(pos, maze) == 1:
                            pos[1] -= 1
                            # print(pos)
                    elif ch3 == 'B': #down
                        if down(pos, maze) == 1:
                            pos[1] += 1
                            # print(pos)
                    elif ch3 == 'C': #right
                        if right(pos, maze) == 1:
                            pos[0] += 1
                            # print(pos)
                    elif ch3 == 'D': #left
                        if left(pos, maze) == 1:
                            pos[0] -= 1
                            # print(pos)
            os.system('clear')
            display(maze, pos)
            # print(pos)
            print()
            print('up down right left or q')

        if pos == exit:
            print('congratulation !')
    
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, stt)

    # os.system('clear')
    # display(maze)
    # print()
    # print('up down right left or q')
    
    # for line in sys.stdin:
    #     os.system('clear')
    #     display(maze)
    #     print()
    #     print('up down right left or q')
    #     if line.rstrip() == 'q':
    #         break
    #     elif line.rstrip() == 'play':
    #         curses.wrapper(play)
    #     elif line.rstrip() == 'print':
    #         print(pos)

    #     elif line.rstrip() == '\x1b[A': #up
    #         if up(pos, maze) == 0:
    #             print('not this way!')
    #         else:
    #             pos[1] -= 1
    #             print(pos)

    #     elif line.rstrip() == '\x1b[B': #down
    #         if down(pos, maze) == 0:
    #             print('not this way!')
    #         else:
    #             pos[1] += 1
    #             print(pos)

    #     elif line.rstrip() == '\x1b[C': #right
    #         if right(pos, maze) == 0:
    #             print('not this way!')
    #         else:
    #             pos[0] += 1
    #             print(pos)

    #     elif line.rstrip() == '\x1b[D': #left
    #         if left(pos, maze) == 0:
    #             print('not this way!')
    #         else:
    #             pos[0] -= 1
    #             print(pos)

    #     if exit == pos:
    #         print('maze completed!')
    #         break
    #     else:
    #         print('please select another key...')

    print("Exited")


def interaction():
    print('1 = regenerate new maze')
    print('2 = show/hide the shortest path')
    print('3 = change wall colours')
    print('4 = play the maze')
    print('q = quit')
    print()


def main():

    param = parsing()
    maze = generator(param)
    os.system('clear')
    display(maze)
    print()
    interaction()
    for line in sys.stdin:
        if line.rstrip() == 'q':
            break
        elif line.rstrip() == '1': #regenerate maze
            maze = generator(param)
        elif line.rstrip() == '2': #show/hide shortest path
            ...
        elif line.rstrip() == '3': #change wall color
            ...
        elif line.rstrip() == '4': #play the maze
            ft_interface(maze, param['entry'], param['exit'])
        else :
            print('please select another key...')
        os.system('clear')
        display(maze)
        print()
        interaction()
    
    print("Exit")


if __name__ == "__main__":
    main()
