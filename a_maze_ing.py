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
    """Check if the player can move north from the current position.

    Args:
        pos: Current player position as [x, y].
        maze: 2D grid of Box objects.

    Returns:
        1 if no north wall, 0 if blocked.
    """
    n = {1, 3, 5, 7, 9, 11, 13, 15}
    if maze[pos[1]][pos[0]].walls in n:
        return 0
    return 1


def down(pos: list[int], maze: list[list[Box]]) -> int:
    """Check if the player can move south from the current position.

    Args:
        pos: Current player position as [x, y].
        maze: 2D grid of Box objects.

    Returns:
        1 if no south wall, 0 if blocked.
    """
    n = {4, 5, 6, 7, 12, 13, 14, 15}
    if maze[pos[1]][pos[0]].walls in n:
        return 0
    return 1


def left(pos: list[int], maze: list[list[Box]]) -> int:
    """Check if the player can move west from the current position.

    Args:
        pos: Current player position as [x, y].
        maze: 2D grid of Box objects.

    Returns:
        1 if no west wall, 0 if blocked.
    """
    n = {8, 9, 10, 11, 12, 13, 14, 15}
    if maze[pos[1]][pos[0]].walls in n:
        return 0
    return 1


def right(pos: list[int], maze: list[list[Box]]) -> int:
    """Check if the player can move east from the current position.

    Args:
        pos: Current player position as [x, y].
        maze: 2D grid of Box objects.

    Returns:
        1 if no east wall, 0 if blocked.
    """
    n = {2, 3, 6, 7, 10, 11, 14, 15}
    if maze[pos[1]][pos[0]].walls in n:
        return 0
    return 1


def ft_interface(maze: Maze, entry: list[int],
                 exit: list[int], path: set[tuple[int, int]],
                 color: str) -> None:
    """Run the interactive play mode where the user navigates the maze.

    Puts the terminal into cbreak mode to capture arrow key inputs directly
    without requiring Enter. The player moves with arrow keys and wins when
    reaching the exit cell. Press 'q' to quit early.

    Args:
        maze: The current Maze object to navigate.
        entry: Starting position as [x, y].
        exit: Target position as [x, y].
        path: Current shortest path set (displayed as overlay if non-empty).
        color: Wall color name for the display.

    Returns:
        None.
    """
    pos = entry[:]
    fd = 0
    stt = termios.tcgetattr(fd)

    os.system('clear')
    display(maze.m, maze.ft, path, color, False, pos, maze.s, maze.e)
    print('up down right left or q')

    try:
        tty.setcbreak(fd)

        while pos != exit:
            c1 = sys.stdin.read(1)
            if c1 == 'q':
                break
            elif c1 == '\x1b':
                c2 = sys.stdin.read(1)
                c3 = sys.stdin.read(1)

                if c2 == '[':
                    if c3 == 'A':  # up
                        if up(pos, maze.m) == 1:
                            pos[1] -= 1
                            os.system('clear')
                            display(maze.m, maze.ft, path, color,
                                    False, pos, maze.s, maze.e)
                            print('up down right left or q')
                    elif c3 == 'B':  # down
                        if down(pos, maze.m) == 1:
                            pos[1] += 1
                            os.system('clear')
                            display(maze.m, maze.ft, path, color,
                                    False, pos, maze.s, maze.e)
                            print('up down right left or q')
                    elif c3 == 'C':  # right
                        if right(pos, maze.m) == 1:
                            pos[0] += 1
                            os.system('clear')
                            display(maze.m, maze.ft, path, color,
                                    False, pos, maze.s, maze.e)
                            print('up down right left or q')
                    elif c3 == 'D':  # left
                        if left(pos, maze.m) == 1:
                            pos[0] -= 1
                            os.system('clear')
                            display(maze.m, maze.ft, path, color,
                                    False, pos, maze.s, maze.e)
                            print('up down right left or q')
        if pos == exit:
            print('congratulation !')
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, stt)
    print("Exited")


def interaction() -> None:
    """Print the list of available user commands to the terminal.

    This function is called after displaying the maze to show the user what
    actions they can take. The user can refresh the maze, generate a new one,
    toggle the shortest path display, change wall colors, or enter play mode.

    Returns:
        None.
    """
    print()
    print('1 = refresh')
    print('2 = generate new maze')
    print('3 = show/hide the shortest path')
    print('4 = change wall colours')
    print('5 = play the maze')
    print('q = quit')
    print()


def main() -> None:
    """Entry point: parse config, generate maze, and run the interaction loop.

    Reads the config file path from sys.argv, generates the maze, displays it,
    then waits for user input to refresh, regenerate, toggle the path,
    change colors, or enter play mode.

    Returns:
        None.
    """
    args = sys.argv
    if len(args) != 2:
        print('expected execution> python3 a_maze_ing.py config.txt')
        return
    param = parsing(args[1])
    if param == {}:
        return
    if 'animation' in param.keys():
        anim = True if param['animation'] else False
    else:
        anim = False
    path = set[tuple[int, int]]()
    colors = [
        'red',
        'yellow',
        'purple',
        'blue',
        'cyan',
        'green'
    ]
    i = 0
    color = colors[i]

    try:
        maze = generator(param)
    except ValueError:
        print('error: entry or exit in 42 pattern '
              '(please choose other coordinates..)')
        return

    os.system('clear')
    display(maze.m, maze.ft, path, color, anim)
    print(f'seed: {maze.d}')
    if not maze.ft:
        print("warning: 42 pattern couldn't be reseolved "
              "(must be at least 9x7)")
    interaction()
    for line in sys.stdin:
        if line.rstrip() == 'q':
            break
        elif line.rstrip() == '1':  # refresh
            ...
        elif line.rstrip() == '2':  # generate new random maze
            param['seed'] = random.randint(0, 2147483647)
            maze = generator(param)
            if path:
                path = maze.sv
        elif line.rstrip() == '3':  # show/hide shortest path
            if path:
                path = set()
            else:
                path = maze.sv
        elif line.rstrip() == '4':  # change wall color
            i += 1
            if i == len(colors):
                i = 0
            color = colors[i]
        elif line.rstrip() == '5':  # play the maze
            ft_interface(maze, param['entry'], param['exit'], path, color)
        else:
            print('please select another key...')
        os.system('clear')
        display(maze.m, maze.ft, path, color, anim)
        print(f'seed: {maze.d}')
        interaction()

    print("Exit")


if __name__ == "__main__":
    main()
