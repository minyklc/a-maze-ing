#!/usr/bin/env python3
from generator import generator, Box
from display import print_maze


def affichage(maze: list[list[Box]]):

    print(f"{'█' * (len(maze[0]) * 4 + 2)}")
    for y in range(len(maze)):
        line = "██"
        bottom = "██"
        for x in range(len(maze[0])):
            cell = maze[y][x]
            line   += "  ██" if 'E' not in cell.not_wall() else "    "
            bottom += "████" if 'S' not in cell.not_wall() else "    "
        print(line)
        print(bottom)
    # print(f"{RESET}")


if __name__ == '__main__':
    
    temp = generator()[:][:]
    for i in range(len(temp)):
        for j in range(len(temp[0])):
            if temp[i][j].walls < 10:
                temp[i][j].walls = int(hex(temp[i][j].walls).split('x')[-1])
            else:
                temp[i][j].walls = hex(temp[i][j].walls).split('x')[-1].capitalize()
    print_maze(temp)
    affichage(generator())