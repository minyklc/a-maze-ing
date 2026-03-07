#!/usr/bin/env python3

from MazeGenerator import Box, Maze
from typing import Any, Callable, Optional


def maze_output(maze: Maze, file: str) -> None:
    """Write the maze to a file in hexadecimal format.

    Each cell is encoded as one hex digit (walls bitmask: N=1,E=2,S=4,W=8).
    After the grid, writes entry coords, exit coords, and shortest path.

    Args:
        maze: The generated Maze object.
        file: Output file path.

    Returns:
        None.
    """
    with open(file, 'w') as f:
        for i in range(len(maze.m)):
            for j in range(len(maze.m[0])):
                # if maze.m[i][j].walls < 10:
                #   f.write(f'{int(hex(maze.m[i][j].walls).split("x")[-1])}')
                # else:
                #  nalc = hex(maze.m[i][j].walls).split("x")[-1].capitalize()
                #     f.write(f'{nalc}')
                f.write(f'{maze.m[i][j].walls:X}')  # No espace in hex coords
            f.write('\n')
        f.write('\n')
        f.write(f"{maze.s[0]},{maze.s[1]}\n")
        f.write(f"{maze.e[0]},{maze.e[1]}\n")
        for d in maze.dir:
            f.write(d[0])
        f.write('\n')  # add \n at the end of the file


def generator(param: dict[str, Any],
              callback: Optional[Callable[[list[list['Box']]], None]] = None
              ) -> Maze:
    """Build and return a Maze from parsed config parameters.

    Args:
        param: Dictionary from parsing(), containing width, height,
               entry, exit, perfect, seed, and output_file keys.
        callback: Optional animation callback passed to maze.generate().


    Returns:
        The generated and solved Maze object.
    """
    start = param['entry']  # x, y
    end = param['exit']
    width = param['width']
    height = param['height']
    perfect = param['perfect']
    seed = param['seed']
    maze = Maze(height, width, start, end, perfect, seed)
    maze.generate(callback)
    maze_output(maze, param['output_file'])
    return maze


if __name__ == "__main__":
    ...
