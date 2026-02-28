#!/usr/bin/env python3
from random import randint, choice


class Box:
    def __init__(self, x: int, y: int):
        self.pos = (x, y)
        self.walls = 0b1111

    def add_wall(self, dir: list | str) -> None:
        if 'N' in dir and 'N' in self.not_wall():
            self.walls += 0b0001
        if 'E' in dir and 'E' in self.not_wall():
            self.walls += 0b0010
        if 'S' in dir and 'S' in self.not_wall():
            self.walls += 0b0100
        if 'W' in dir and 'W' in self.not_wall():
            self.walls += 0b1000

    def remove_wall(self, dir: str, reverse: bool = False) -> None:
        if reverse is True:
            if dir == 'N':
                dir = 'S'
            elif dir == 'S':
                dir = 'N'
            elif dir == 'E':
                dir = 'W'
            elif dir == 'W':
                dir = 'E'

        if dir == 'N' and 'N' not in self.not_wall():
            self.walls -= 0b0001
        elif dir == 'E' and 'E' not in self.not_wall():
            self.walls -= 0b0010
        elif dir == 'S' and 'S' not in self.not_wall():
            self.walls -= 0b0100
        elif dir == 'W' and 'W' not in self.not_wall():
            self.walls -= 0b1000

    def not_wall(self) -> list[str | None]:
        m = []
        if int(self.walls % 2) == 0:
            m.append('N')
        if int(self.walls / 2 % 2) == 0:
            m.append('E')
        if int(self.walls / 4 % 2) == 0:
            m.append('S')
        if int(self.walls / 8 % 2) == 0:
            m.append('W')
        return m


class Maze:
    def __init__(self, width: int, length: int,
                 start: tuple, end: tuple, perfect: bool):
        self.w = width
        self.l = length
        self.p = perfect
        self.s = start
        self.e = end
        self.m = self.blank_maze(width, length)
        self.ft = self.forty_two(width, length)

    def blank_maze(self, width: int, length: int) -> list[list[Box]]:
        maze = []
        for n in range(width):
            maze.append([])
            for b in range(length):
                maze[n].append(Box(b, n))
        return maze

    def forty_two(self, width, length) -> list[list[int]] | list:
        total = []

        if width >= 7 and length >= 9:
            pos_x = int((length - 7) / 2)
            pos_y = int((width - 5) / 2)
            x = pos_x
            y = pos_y
            menu = [
                [0, 4, 1, 1],
                [0, 6],
                [0, 1, 1, 2, 1, 1],
                [2, 2],
                [2, 2, 1, 1]
            ]
            for m in menu:
                for i in m:
                    x += i
                    total.append([x, y])
                x = pos_x
                y += 1
        return total

    def generate(self):
        if self.p is True:
            self.perfect_maze()
        else:
            self.imperfect_maze()

    def perfect_maze(self):
        stack = []
        visited = set()

        initial = (randint(0, self.l - 1), randint(0, self.w - 1))
        pos = [initial[0], initial[1]]

        stack.append(pos[:]) # stack of list of positions -> actual way
        visited.add(tuple(pos)) # all visited positions
        if self.ft != []:
            for p in self.ft:
                if p is not None:
                    visited.add(tuple(p))

        while stack:
            pos = stack[-1][:]
            dir = self.can_pass_through(pos, visited)
            if dir:
                next = choice(dir)
                self.m[pos[1]][pos[0]].remove_wall(next)
                new = self.update_pos(pos, next)
                self.m[new[1]][new[0]].remove_wall(next, reverse=True)
                stack.append(new[:])
                visited.add(tuple(new[:]))
            else:
                stack.pop(-1)
                
    def update_pos(self, pos: list, dir: str) -> list:
        if dir == 'N':
            pos[1] -= 1
        elif dir == 'E':
            pos[0] += 1
        elif dir == 'S':
            pos[1] += 1
        elif dir == 'W':
            pos[0] -= 1
        return pos

    def can_pass_through(self, pos: list, stack: set) -> list:
        r = []
        n = ()
        if pos[1] > 0:
            n = self.m[pos[1] - 1][pos[0]].pos
        e = ()
        if pos[0] < self.l - 1:
            e = self.m[pos[1]][pos[0] + 1].pos
        s = ()
        if pos[1] < self.w - 1:
            s = self.m[pos[1] + 1][pos[0]].pos
        w = ()
        if pos[0] > 0:
            w = self.m[pos[1]][pos[0] - 1].pos

        if n and not any(p == n for p in stack):
            r.append('N')
        if e and not any(p == e for p in stack):
            r.append('E')
        if s and not any(p == s for p in stack):
            r.append('S')
        if w and not any(p == w for p in stack):
            r.append('W')
        return r

    @staticmethod
    def is_same(pos: list, pos2: tuple) -> bool:
        if pos[0] == pos2[0] and pos[1] == pos2[1]:
            return True
        return False
        
    def imperfect_maze(self):
        ...


def print_maze(maze: list[list[Box]]):
    for n in maze:
        for b in n:
            print(b.walls, end=' ')
        print()
    print()


def maze_output(maze: Maze, file: str):
    with open(file, 'w') as f:
        for i in range(len(maze.m)):
            for j in range(len(maze.m[0])):
                if maze.m[i][j].walls < 10:
                    f.write(f'{int(hex(maze.m[i][j].walls).split('x')[-1])} ')
                else:
                    f.write(f'{hex(maze.m[i][j].walls).split('x')[-1].capitalize()} ')
            f.write('\n')
        f.write(f"{maze.w}")


def generator(param: dict) -> Maze:
    start = param['entry'] # x, y
    end = param['exit']
    width = param['width']
    height = param['height']
    state = param['perfect']
    maze = Maze(height, width, start, end, state)
    maze.generate()
    maze_output(maze, param['output_file'])
    return maze


if __name__ == "__main__":
    ...