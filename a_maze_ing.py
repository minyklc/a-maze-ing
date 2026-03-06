#!/usr/bin/env python3

import sys
import os
import time
import termios
import tty
import random
from typing import Callable
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
                 color: str, cursor: str = '█') -> None:
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
        cursor: Character displayed on the player's cell.

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
                                    False, pos, maze.s, maze.e, cursor)
                            print('up down right left or q')
                    elif c3 == 'B':  # down
                        if down(pos, maze.m) == 1:
                            pos[1] += 1
                            os.system('clear')
                            display(maze.m, maze.ft, path, color,
                                    False, pos, maze.s, maze.e, cursor)
                            print('up down right left or q')
                    elif c3 == 'C':  # right
                        if right(pos, maze.m) == 1:
                            pos[0] += 1
                            os.system('clear')
                            display(maze.m, maze.ft, path, color,
                                    False, pos, maze.s, maze.e, cursor)
                            print('up down right left or q')
                    elif c3 == 'D':  # left
                        if left(pos, maze.m) == 1:
                            pos[0] -= 1
                            os.system('clear')
                            display(maze.m, maze.ft, path, color,
                                    False, pos, maze.s, maze.e, cursor)
                            print('up down right left or q')
        if pos == exit:
            print('Congratulations !')
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, stt)
    print("Exited")


def make_callback(ft: set[tuple[int, int]],
                  color: str) -> Callable[[list[list[Box]]], None]:
    """Return an animation callback that clears and redraws the maze grid.

    The returned function can be passed to maze.generate() so the maze
    is displayed live as each wall is removed during generation.

    Args:
        ft: The '42' pattern cell positions for correct display.
        color: Wall color name used for the display.

    Returns:
        A callback function accepting the current grid as argument.
    """
    def callback(grid: list[list[Box]]) -> None:
        os.system('clear')
        display(grid, ft, set(), color, False)
        time.sleep(0.01)
    return callback


def choose_cursor() -> str:
    """Prompt the user to pick a cursor character for the play mode.

    Displays a numbered list of available cursors (emojis and ASCII).
    The user enters the corresponding number, or presses Enter to keep
    the current cursor. Returns the chosen character, or an empty string
    if the input is invalid (caller keeps the current cursor).

    Returns:
        The chosen cursor string, or '' on invalid input.
    """
    cursors = [
        ('🧑', 'person'),
        ('👩', 'girl'),
        ('👦', 'boy'),
        ('🐱', 'cat'),
        ('🐶', 'dog'),
        ('🐭', 'mouse'),
        ('🐸', 'frog'),
        ('👾', 'alien'),
        ('🔥', 'fire'),
        ('🪨', 'rock'),
        ('🌪️', 'air'),
        ('💧', 'water'),
        ('⭐', 'star'),
        ('💎', 'gem'),
        ('👻', 'ghost'),
        ('🤖', 'robot'),
        ('💩', 'poop'),
        ('@', 'at'),
        ('$', 'dollar'),
        ('&', 'ampersand'),
        ('*', 'star ascii'),
    ]
    print()
    print('Choose your cursor:')
    for idx, (char, label) in enumerate(cursors, 1):
        print(f'  {idx} = {char}  ({label})')
    print('  Enter = keep current')
    print()
    print('Choice: ', end='', flush=True)
    raw = sys.stdin.readline().rstrip()
    if not raw:
        return ''
    try:
        choice = int(raw)
        if 1 <= choice <= len(cursors):
            return cursors[choice - 1][0]
        print('error: invalid choice')
        return ''
    except ValueError:
        print('error: please enter a number')
        return ''


def ask_dimensions(param: dict) -> bool:  # type: ignore[type-arg]
    """Prompt the user for new maze dimensions and new entry/exit coordinates.

    Reads width and height from stdin, then always asks for new entry and
    exit coordinates. If the current coordinates are still valid for the
    new dimensions, they are shown as defaults.
    Updates param in place on success.

    Args:
        param: The current config dict, modified in place on success.

    Returns:
        True if dimensions were updated, False if the user cancelled
        or entered invalid values.
    """
    print('Enter new width (>= 2): ', end='', flush=True)
    raw_w = sys.stdin.readline().rstrip()
    print('Enter new height (>= 2): ', end='', flush=True)
    raw_h = sys.stdin.readline().rstrip()

    try:
        new_w = int(raw_w)
        new_h = int(raw_h)
        if new_w < 2 or new_h < 2:
            raise ValueError
    except ValueError:
        print('error: width and height must be integers >= 2')
        return False

    cur_entry = param['entry']
    cur_exit = param['exit']
    default_entry = cur_entry if (cur_entry[0] < new_w
                                  and cur_entry[1] < new_h) else [0, 0]
    default_exit = cur_exit if (cur_exit[0] < new_w and
                                cur_exit[1] < new_h) else [new_w-1, new_h-1]

    print(f'Enter new entry x,y (0-{new_w-1}, 0-{new_h-1})'
          f' [default: {default_entry[0]},{default_entry[1]}]: ',
          end='', flush=True)
    raw_entry = sys.stdin.readline().rstrip()
    print(f'Enter new exit  x,y (0-{new_w-1}, 0-{new_h-1})'
          f' [default: {default_exit[0]},{default_exit[1]}]: ',
          end='', flush=True)
    raw_exit = sys.stdin.readline().rstrip()

    try:
        entry = ([int(v) for v in raw_entry.split(',')]
                 if raw_entry else default_entry)
        exit_ = ([int(v) for v in raw_exit.split(',')]
                 if raw_exit else default_exit)
        ex, ey = entry
        ox, oy = exit_
        if ex < 0 or ex >= new_w or ey < 0 or ey >= new_h:
            raise ValueError('entry out of bounds')
        if ox < 0 or ox >= new_w or oy < 0 or oy >= new_h:
            raise ValueError('exit out of bounds')
        if [ex, ey] == [ox, oy]:
            raise ValueError('entry and exit must differ')
    except ValueError as v:
        print(f'error: {v}')
        return False

    param['width'] = new_w
    param['height'] = new_h
    param['entry'] = entry
    param['exit'] = exit_
    return True


def interaction(anim: bool, cursor: str) -> None:
    """Print the list of available user commands to the terminal.

    This function is called after displaying the maze to show the user what
    actions they can take. The user can refresh the maze, generate a new one,
    toggle the shortest path display, change wall colors, or enter play mode.

    Args:
        anim: Current animation state, shown next to option 6.
        cursor: Current cursor character, shown next to option 8.

    Returns:
        None.
    """
    anim_status = 'ON' if anim else 'OFF'
    print()
    print('1 = refresh')
    print('2 = generate new maze')
    print('3 = show/hide the shortest path')
    print('4 = change wall colours')
    print('5 = play the maze')
    print(f'6 = enable/disable generation animation (currently {anim_status})')
    print('7 = change maze dimensions')
    print(f'8 = change cursor (currently {cursor})')
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
    cursor = '█'

    try:
        cb = make_callback(set(), color) if anim else None
        maze = generator(param)
    except ValueError:
        print('error: entry or exit in 42 pattern '
              '(please choose other coordinates..)')
        return

    os.system('clear')
    display(maze.m, maze.ft, path, color, False)
    print(f'seed: {maze.d}')
    if not maze.ft:
        print("warning: 42 pattern couldn't be reseolved "
              "(must be at least 9x7)")
    interaction(anim, cursor)
    for line in sys.stdin:
        if line.rstrip() == 'q':
            break
        elif line.rstrip() == '1':  # refresh
            ...
        elif line.rstrip() == '2':  # generate new random maze
            param['seed'] = random.randint(0, 2147483647)
            cb = make_callback(set(), color) if anim else None
            maze = generator(param, cb)
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
            ft_interface(maze, param['entry'], param['exit'],
                         path, color, cursor)
        elif line.rstrip() == '6':  # toggle animation
            anim = not anim
        elif line.rstrip() == '7':  # change maze dimensions
            if ask_dimensions(param):
                param['seed'] = random.randint(0, 2147483647)
                path = set()
                try:
                    cb = make_callback(set(), color) if anim else None
                    maze = generator(param, cb)
                except ValueError:
                    print('error: entry or exit in 42 pattern '
                          '(please choose other coordinates...)')
                    print('\nPress Enter to continue...')
                    sys.stdin.readline()
            else:
                print('\nPress Enter to continue...')
                sys.stdin.readline()
        elif line.rstrip() == '8':  # change cursor
            new_cursor = choose_cursor()
            if new_cursor:
                cursor = new_cursor
            else:
                print('\nPress Enter to continue...')
                sys.stdin.readline()
        else:
            print('please select another key...')
        os.system('clear')
        display(maze.m, maze.ft, path, color, anim)
        print(f'seed: {maze.d}')
        interaction(anim, cursor)

    print("Exit")


if __name__ == "__main__":
    main()
