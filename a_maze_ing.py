#!/usr/bin/env python3
import sys


def interaction():
    print('1 = regenerate new maze')
    print('2 = show/hide the shortest path')
    print('3 = change wall colours')
    print('4 = play the maze')
    print('q = quit')
    print()


def main():
    
    interaction()
    for line in sys.stdin:
        interaction()
        if line.rstrip() == 'q':
            break
        elif line.rstrip() == '1':
            ...
        elif line.rstrip() == '2':
            ...
        elif line.rstrip() == '3':
            ...
        elif line.rstrip() == '4':
            ...
        else :
            print('please select another key...')
    
    print("Exit")


if __name__ == '__main__':
    main()
