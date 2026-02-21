#!/usr/bin/env python3
import sys
import curses
import os
from generator import Box, generator
from display import display
from parsing import parsing


def play(stdscr):
    curses.curs_set(0)
    stdscr.keypad(True)
    while True:
        stdscr.clear()
        stdscr.addstr("Use arrows, press q to quit\n")
        stdscr.refresh()

        key = stdscr.getch()

        if key == ord('q'):
            break
        elif key == curses.KEY_UP:
            stdscr.addstr("UP pressed\n")
        elif key == curses.KEY_DOWN:
            stdscr.addstr("DOWN pressed\n")
        elif key == curses.KEY_RIGHT:
            print("RIGHT pressed\n")
        elif key == curses.KEY_LEFT:
            stdscr.addstr("LEFT pressed\n")
        else:
            stdscr.addstr("Other key\n")

        stdscr.refresh()
        curses.napms(100)


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


def ft_interface(maze):
    entry = [0, 0]
    exit = [15, 15]
    pos = entry[:]

    os.system('clear')
    display(maze)
    print()
    print('up down right left or q')
    for line in sys.stdin:
        os.system('clear')
        display(maze)
        print()
        print('up down right left or q')
        if line.rstrip() == 'q':
            break
        elif line.rstrip() == 'play':
            curses.wrapper(play)
        elif line.rstrip() == 'print':
            print(pos)

        elif line.rstrip() == '\x1b[A': #up
            if up(pos, maze) == 0:
                print('not this way!')
            else:
                pos[1] -= 1
                print(pos)

        elif line.rstrip() == '\x1b[B': #down
            if down(pos, maze) == 0:
                print('not this way!')
            else:
                pos[1] += 1
                print(pos)

        elif line.rstrip() == '\x1b[C': #right
            if right(pos, maze) == 0:
                print('not this way!')
            else:
                pos[0] += 1
                print(pos)

        elif line.rstrip() == '\x1b[D': #left
            if left(pos, maze) == 0:
                print('not this way!')
            else:
                pos[0] -= 1
                print(pos)

        if exit == pos:
            print('maze completed!')
            break
        else:
            print('please select another key...')

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
    interaction()
    for line in sys.stdin:
        os.system('clear')
        display(maze)
        interaction()
        if line.rstrip() == 'q':
            break
        elif line.rstrip() == '1':
            maze = generator(param)
        elif line.rstrip() == '2':
            ...
        elif line.rstrip() == '3':
            ...
        elif line.rstrip() == '4':
            ft_interface(maze)
        else :
            print('please select another key...')
    
    print("Exit")


if __name__ == "__main__":
    main()
