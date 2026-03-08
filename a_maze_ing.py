#!/usr/bin/env python3

import sys
import os
import time
import termios
import tty
import random
from typing import Callable, TypedDict, Any, cast
from mazegen import Maze, Box
from generator import generator
from display import display
from parsing import parsing


class ParamDict(TypedDict, total=False):
    """Typed dictionary for maze configuration parameters.

    Attributes:
        width: Maze width in number of cells.
        height: Maze height in number of cells.
        entry: Entry coordinates as [x, y].
        exit: Exit coordinates as [x, y].
        output_file: Output filename.
        perfect: Whether to generate a perfect maze.
        seed: Random seed for reproducibility.
        animation: Whether to display generation animation.
    """

    width: int
    height: int
    entry: list[int]
    exit: list[int]
    output_file: str
    perfect: bool
    seed: int
    animation: bool


class ScoreDict(TypedDict):
    """Typed dictionary for a completed game score.

    Attributes:
        name: 3-letter player name entered after completing the maze.
        seed: The maze seed used.
        size: The maze dimensions as 'WxH' string.
        time: Elapsed time in seconds.
        steps: Number of steps taken by the player.
        optimal: Length of the optimal path.
        stars: Star rating string.
    """

    name: str
    seed: int
    size: str
    time: float
    steps: int
    optimal: int
    stars: str


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
                 color: str, cursor: str = '█'
                 ) -> ScoreDict | None:
    """Run the interactive play mode where the user navigates the maze.

    Puts the terminal into cbreak mode to capture arrow key inputs directly
    without requiring Enter. The player moves with arrow keys and wins when
    reaching the exit cell. Press 'q' to quit early.
    Displays a live timer and step counter.
    Returns a score dict if the player reaches the exit, else None.

    Args:
        maze: The current Maze object to navigate.
        entry: Starting position as [x, y].
        exit: Target position as [x, y].
        path: Current shortest path set (displayed as overlay if non-empty).
        color: Wall color name for the display.
        cursor: Character displayed on the player's cell.

    Returns:
        A dict with keys 'time', 'steps', 'optimal', 'stars' on success,
        or None if the player quit early.
    """
    pos = entry[:]
    steps = 0
    optimal = len(maze.dir)
    start_time = time.time()
    fd = 0
    stt = termios.tcgetattr(fd)

    # os.system('clear')
    # display(maze.m, maze.ft, path, color, False, pos, maze.s, maze.e, cursor)
    # print('up down right left or q')

    def redraw() -> None:
        elapsed = time.time() - start_time
        os.system('clear')
        print(f'⏱  {elapsed:6.1f}s   🐾 steps: {steps}'
              f'   🎯 optimal: {optimal}')
        display(maze.m, maze.ft, path, color, False, pos, maze.s, maze.e,
                cursor)
        print('arrow keys to move  |  q to quit')

    redraw()

    try:
        tty.setcbreak(fd)
        moved = False

        while pos != exit:
            c1 = sys.stdin.read(1)
            if c1 == 'q':
                break
            elif c1 == '\x1b':
                c2 = sys.stdin.read(1)
                c3 = sys.stdin.read(1)
                moved = False
                if c2 == '[':
                    if c3 == 'A' and up(pos, maze.m) == 1:  # up
                        pos[1] -= 1
                        # os.system('clear')
                        # display(maze.m, maze.ft, path, color,
                        #         False, pos, maze.s, maze.e, cursor)
                        moved = True
                        # print('up down right left or q')
                    elif c3 == 'B' and down(pos, maze.m) == 1:  # down
                        pos[1] += 1
                        # os.system('clear')
                        # display(maze.m, maze.ft, path, color,
                        #         False, pos, maze.s, maze.e, cursor)
                        moved = True
                        # print('up down right left or q')
                    elif c3 == 'C' and right(pos, maze.m) == 1:  # right
                        pos[0] += 1
                        # os.system('clear')
                        # display(maze.m, maze.ft, path, color,
                        #         False, pos, maze.s, maze.e, cursor)
                        moved = True
                        # print('up down right left or q')
                    elif c3 == 'D' and left(pos, maze.m) == 1:  # left
                        pos[0] -= 1
                        # os.system('clear')
                        # display(maze.m, maze.ft, path, color,
                        #         False, pos, maze.s, maze.e, cursor)
                        moved = True
                        # print('up down right left or q')
                if moved:
                    steps += 1
                    redraw()

        # if pos == exit:
        #     print('Congratulations !')
        elapsed = time.time() - start_time
        if pos == exit:
            ratio = steps / optimal if optimal > 0 else 1
            if ratio <= 1.2:
                stars = '⭐⭐⭐'
            elif ratio <= 1.5:
                stars = ' ⭐⭐ '
            elif ratio <= 2.0:
                stars = '  ⭐  '
            else:
                stars = '  🫠  '
            os.system('clear')
            print(f'⏱  {elapsed:6.1f}s   🐾 steps: {steps}'
                  f'   🎯 optimal: {optimal}')
            display(maze.m, maze.ft, path, color, False, pos, maze.s, maze.e,
                    cursor)
            print(f'\n  💪 Congratulations!  {stars}')
            print(f'  Time: {elapsed:.1f}s  |  Steps: {steps}'
                  f'  |  Optimal: {optimal}')
            termios.tcsetattr(fd, termios.TCSADRAIN, stt)
            name = ''
            while len(name) != 3 or not name.isalpha():
                raw = input('  Enter your name (3 letters): ').strip().upper()
                if len(raw) == 3 and raw.isalpha():
                    name = raw
                else:
                    print('  Please enter exactly 3 letters.')
            return ScoreDict(
                name=name,
                seed=int(maze.d),
                size=f'{maze.w}x{maze.h}',
                time=elapsed,
                steps=steps,
                optimal=optimal,
                stars=stars,
            )
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, stt)
    print("Exited")
    return None


def print_scores(scores: list[ScoreDict]) -> None:
    """Display the leaderboard of all completed runs.

    Args:
        scores: A list of scores dicts returned by ft_interface,
                each containing 'name', 'seed', 'size', 'time', 'steps',
                'optimal', and 'stars' keys.

    Returns:
        None.
    """
    if not scores:
        print('  No scores yet.')
        return
    print()
    print('  ╔═══════════════════════════════════════════════════════╗')
    print('  ║                      🏆  SCORES                       ║')
    print('  ╠══════╦════════╦══════════╦════════╦══════════╦════════╣')
    print('  ║ Name ║  Size  ║   Seed   ║  Time  ║  Steps   ║   🌟   ║')
    print('  ╠══════╬════════╬══════════╬════════╬══════════╬════════╣')
    for s in scores:
        seed_str = str(s['seed'])[:8]
        steps_str = f"{s['steps']}/{s['optimal']}"
        print(f"  ║ {s['name']:<4} ║ {s['size']:<6} ║ {seed_str:<8} ║"
              f" {s['time']:5.1f}s ║ {steps_str:<8} ║ {s['stars']} ║")
    print('  ╚══════╩════════╩══════════╩════════╩══════════╩════════╝')
    print()


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


def choose_cursor() -> Any:
    """Prompt the user to pick a cursor character for the play mode.

    Displays a numbered list of available cursors (emojis and ASCII).
    The user enters the corresponding number, or presses Enter to keep
    the current cursor. Returns the chosen character, or an empty string
    if the input is invalid (caller keeps the current cursor).

    Returns:
        The chosen cursor string, or '' on invalid input.
    """
    cursors = [
        ('\033[47m  \033[0m', 'white cursor'),
        ('\033[40m  \033[0m', 'black cursor'),
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
        ('🍆', 'eggplant'),
        ('🍑', 'peach'),
        ('🍔', 'burger'),
        ('💩', 'poop (again, because it is funny)'),
        ('💀', 'skull'),
        ('👑', 'crown'),
        ('🧙', 'wizard'),
        ('🧟', 'zombie'),
    ]
    print()
    print('Choose your cursor:')
    for idx, (char, label) in enumerate(cursors, 1):
        print(f'  {idx} = {char}  ({label})')
    print('  Enter = keep current')
    print()
    raw = input('Choice: ')
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


def choose_pattern() -> str:
    """Prompt the user to pick a pattern to embed in the maze.

    Displays the available named patterns with a small ASCII preview.
    The user enters the corresponding number, or presses Enter to keep
    the current pattern. Returns the chosen pattern name, or '' on
    invalid/empty input (caller keeps the current pattern).

    Returns:
        The chosen pattern name string ('42', 'PA', 'MINA'), or ''.
    """
    from mazegen import Maze
    patterns = list(Maze.PATTERNS.keys())
    print("\nChoose a pattern:")
    for idx, name in enumerate(patterns, 1):
        rows = Maze.PATTERNS[name]
        w = len(rows[0]) + 2
        h = len(rows) + 2
        print(f'  {idx} = {name}  (needs maze >= {w} width x {h} height)')
        for row in rows:
            print('      ' + row.replace('#', '█').replace(' ', '·'))
    print("  Enter = keep current\n")
    raw = input('Choice: ')
    if not raw:
        return ''
    try:
        choice = int(raw)
        if 1 <= choice <= len(patterns):
            return patterns[choice - 1]
        print('error: invalid choice')
        return ''
    except ValueError:
        print('error: please enter a number')
        return ''


def ask_dimensions(param: ParamDict) -> bool:
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
    try:
        new_w = int(input('Enter new width (>= 2): '))
        new_h = int(input('Enter new height (>= 2): '))
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

    raw_entry = input(f'Enter new entry x,y (0-{new_w-1}, 0-{new_h-1})'
                      f' [default: {cur_entry[0]},{cur_entry[1]}]: ')
    raw_exit = input(f'Enter new exit  x,y (0-{new_w-1}, 0-{new_h-1})'
                     f' [default: {cur_exit[0]},{cur_exit[1]}]: ')

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


def interaction(anim: bool, anim2: bool, cursor: str,
                pattern: str = '42') -> None:
    """Print the list of available user commands to the terminal.

    This function is called after displaying the maze to show the user what
    actions they can take. The user can refresh the maze, generate a new one,
    toggle the shortest path display, change wall colors, or enter play mode.

    Args:
        anim: Current animation state, shown next to option 6.
        anim2: Secondary animation state (generate-only).
        cursor: Current cursor character, shown next to option 8.
        pattern: Current pattern name, shown next to option 9.

    Returns:
        None.
    """
    anim_status = 'ON' if anim else 'OFF'
    anim_status = 'ON while generating' if anim2 else anim_status
    print()
    print('1 = refresh')
    print('2 = generate new maze')
    print('3 = show/hide the shortest path')
    print('4 = change wall colours')
    print('5 = play the maze')
    print(f'6 = enable/disable generation animation (currently {anim_status})')
    print('7 = change maze dimensions')
    print(f'8 = change cursor (currently {cursor})')
    print(f'9 = change pattern (currently {pattern})')
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
    cursor = '\033[47m  \033[0m'
    anim2 = False
    pattern = '42'
    scores: list[ScoreDict] = []

    try:
        cb = make_callback(set(), color) if anim2 else None
        param['pattern'] = pattern
        maze = generator(param, cb)
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
    interaction(anim, anim2, cursor, pattern)
    for line in sys.stdin:
        if line.rstrip() == 'q':
            break
        elif line.rstrip() == '1':  # refresh
            ...
        elif line.rstrip() == '2':  # generate new random maze
            param['seed'] = random.randint(0, 2147483647)
            cb = make_callback(set(), color) if anim2 else None
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
            score = ft_interface(maze, param['entry'], param['exit'],
                                 path, color, cursor)
            if score:
                scores.append(score)
                print_scores(scores)
                print('\nPress Enter to continue...')
                sys.stdin.readline()
        elif line.rstrip() == '6':  # toggle animation
            if anim and not anim2:
                anim2 = True
                anim = False
            elif not anim and anim2:
                anim2 = False
            else:
                anim = True
        elif line.rstrip() == '7':  # change maze dimensions
            if ask_dimensions(cast(ParamDict, param)):
                param['seed'] = random.randint(0, 2147483647)
                path = set()
                try:
                    cb = make_callback(set(), color) if anim2 else None
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
        elif line.rstrip() == '9':  # change pattern
            new_pattern = choose_pattern()
            if new_pattern and new_pattern != pattern:
                pattern = new_pattern
                param['pattern'] = pattern
                path = set()
                try:
                    cb = make_callback(maze.ft, color) if anim2 else None
                    maze = generator(param, cb)
                except ValueError:
                    print('error: entry or exit inside pattern, '
                          'please choose other coordinates.')
                    sys.stdin.readline()
            else:
                print('\nPress Enter to continue...')
                sys.stdin.readline()
        else:
            print('please select another key...')
        os.system('clear')
        display(maze.m, maze.ft, path, color, anim)
        print(f'seed: {maze.d}')
        interaction(anim, anim2, cursor, pattern)

    if scores:
        print_scores(scores)
    print("Exit")


if __name__ == "__main__":
    main()
