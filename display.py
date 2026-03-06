#!/usr/bin/env python3

from MazeGenerator import Box
import time


class Color:
    """Container for ANSI terminal background color escape sequences.

    Provides colored block strings used to render maze cells and walls,
    and a helper method to select a wall/highlight color pair by name.

    Attributes:
        white, lightcyan, cyan, lightpurple, purple, lightblue, blue,
        lightyellow, yellow, lightgreen, green, lightred, red, grey,
        black: Strings representing ANSI escape sequences for bg colors.
        cell: String representing the default cell color (no background).
        void: String representing the default void color (no background).

    Methods:
        which_color(color: str) -> tuple[str, str]:
            Returns a tuple of (wall_color, highlight_color) based on
            the input color name.
    """
    def __init__(self) -> None:
        """Initialize ANSI escape color strings for terminal rendering.

        Each attribute is a background color code followed by two spaces,
        ready to be printed as a colored cell block in the terminal.
        """
        self.white = '\033[47m  '
        self.lightcyan = '\033[106m  '
        self.cyan = '\033[46m  '
        self.lightpurple = '\033[105m  '
        self.purple = '\033[45m  '
        self.lightblue = '\033[104m  '
        self.blue = '\033[44m  '
        self.lightyellow = '\033[103m  '
        self.yellow = '\033[43m  '
        self.lightgreen = '\033[102m  '
        self.green = '\033[42m  '
        self.lightred = '\033[101m  '
        self.red = '\033[41m  '
        self.grey = '\033[100m  '
        self.black = '\033[40m  '
        self.cell = '\033[0m  '
        self.void = '\033[0m'

    def which_color(self, color: str) -> tuple[str, str]:
        """Return the wall color and highlight color for the given color name.

        Args:
            color: Color name ('purple', 'yellow', 'blue', 'cyan', 'green',
                   or any other string which defaults to red).

        Returns:
            A tuple (wall_color, highlight_color) as ANSI escape strings.
        """
        if color == 'purple':
            return self.lightblue, self.lightpurple
        elif color == 'yellow':
            return self.yellow, self.lightred
        elif color == 'blue':
            return self.blue, self.lightcyan
        elif color == 'cyan':
            return self.cyan, self.lightgreen
        elif color == 'green':
            return self.green, self.purple
        else:
            return self.red, self.lightyellow


def display(maze: list[list[Box]],
            forty_two: set[None] | set[tuple[int, int]],
            path: set[None] | set[tuple[int, int]],
            color: str,
            animation: bool = False,
            pos: None | list[int] = None,
            start: None | list[int] = None,
            end: None | list[int] = None) -> None:
    """Render the maze in the terminal using ANSI background colors.

    Each cell is drawn as a 2-character block. Walls are shown as colored
    blocks, open passages as blank cells. Special cells are highlighted:
    the player position in white, entry in purple, exit in light purple,
    the shortest path in grey, and the '42' pattern in the highlight color.

    Args:
        maze: 2D grid of Box objects indexed as maze[row][col].
        forty_two: Set of (x, y) tuples forming the '42' pattern.
        path: Set of (x, y) tuples on the shortest path to highlight.
        color: Wall color name passed to Color.which_color().
        animation: If True, adds a short sleep between rows for visual effect.
        pos: Current player position as [x, y], or None if not in play mode.
        start: Entry cell coordinates as [x, y], or None.
        end: Exit cell coordinates as [x, y], or None.

    Returns:
        None. Prints the maze directly to the terminal.
    """

    c = Color()
    cwall, clight = c.which_color(color)
    top = cwall * (len(maze[0]) * 2 + 1) + c.void
    if animation:
        time.sleep(0.05)
    print(top)

    for y in range(len(maze)):
        line = cwall
        bottom = cwall
        for x in range(len(maze[0])):
            cell = maze[y][x]
            walls = cell.has_wall()
            if pos and pos[0] == x and pos[1] == y:
                line += c.white + cwall if 'E' in walls else c.white + c.cell
            elif start and start[0] == x and start[1] == y:
                line += c.purple + cwall if 'E' in walls else c.purple + c.cell
            elif end and end[0] == x and end[1] == y:
                line += c.lightpurple + cwall if 'E' in walls \
                    else c.lightpurple + c.cell
            elif path and cell.pos in path:
                line += c.grey + cwall if 'E' in walls else c.grey + c.cell
            elif forty_two and cell.pos in forty_two:
                line += clight + cwall
            else:
                line += c.cell + cwall if 'E' in walls else c.cell * 2
            bottom += cwall * 2 if 'S' in walls else c.cell + cwall

        if animation:
            time.sleep(0.05)
        print(f"{line+c.void}")
        if animation:
            time.sleep(0.05)
        print(f"{bottom+c.void}")


if __name__ == '__main__':
    ...
