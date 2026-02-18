#!/usr/bin/env python3

n = 0b1111
r = 0b1111 / 2
r = int(r)
print(r)

pos = 0
if pos:
    print(0)

pos = (0, 1)
next_pos = [0, 1]
print(pos[0] == next_pos[0], pos[1] == next_pos[1])