#!/usr/bin/env python3
from MazeGenerator import Maze
from typing import Any


def maze_output(maze: Maze, file: str) -> None:
    with open(file, 'w') as f:
        for i in range(len(maze.m)):
            for j in range(len(maze.m[0])):
                if maze.m[i][j].walls < 10:
                    f.write(f'{int(hex(maze.m[i][j].walls).split("x")[-1])}')
                else:
                    nalc = hex(maze.m[i][j].walls).split("x")[-1].capitalize()
                    f.write(f'{nalc}')
            f.write('\n')
        f.write('\n')
        f.write(f"{maze.s[0]}, {maze.s[1]}\n")
        f.write(f"{maze.e[0]}, {maze.e[1]}\n")
        for d in maze.dir:
            f.write(d[0])


def generator(param: dict[str, Any]) -> Maze:
    start = param['entry']  # x, y
    end = param['exit']
    width = param['width']
    height = param['height']
    perfect = param['perfect']
    seed = param['seed']
    maze = Maze(height, width, start, end, perfect, seed)
    maze.generate()
    maze_output(maze, param['output_file'])
    return maze


if __name__ == "__main__":
    ...
