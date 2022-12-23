#!/usr/bin/env python3

import re
import sys

board = []
           #R       D       L        U
facings = ((1, 0), (0, 1), (-1, 0), (0, -1))

maxlen = -1
with open("day22.txt") as infile:
    for line in infile:
        if len(line.rstrip()) == 0:
            # this is the blank line ending the board, so skip it
            # and then read in the instructions
            line = next(infile)
            instructions = re.split(r"([LR])", line.rstrip())
            break
            
        board.append(list(line.rstrip()))
        if len(board[-1]) > maxlen:
            maxlen = len(board[-1])

# Make sure all lines have the same length
for b in board:
    if len(b) < maxlen:
        b.extend([" "]*(maxlen-len(b)))

board_width = len(board[0])
board_height = len(board)
cur_y = 0
cur_x = board[0].index(".")
cur_facing = 0

# Nextly, execute the instructions.
for i in instructions:
    if (i == 'R'):
        cur_facing = (cur_facing + 1) % len(facings)
    elif (i == 'L'):
        cur_facing = (cur_facing - 1) % len(facings)
    else:
        for n in range(int(i)):
            new_x = (cur_x + facings[cur_facing][0]) % board_width
            new_y = (cur_y + facings[cur_facing][1]) % board_height
            if board[new_y][new_x] == '#':
                # we are blocked, so stop moving
                break
            elif board[new_y][new_x] == '.':
                # this is ok, move here
                cur_y = new_y
                cur_x = new_x
            else:
                # this space doesn't exist, wrap around
                while board[new_y][new_x] == ' ':
                    new_x = (new_x + facings[cur_facing][0]) % board_width
                    new_y = (new_y + facings[cur_facing][1]) % board_height
                # check to see if we were blocked
                if board[new_y][new_x] == '.':
                    # ok, move here
                    cur_y = new_y
                    cur_x = new_x
                elif board[new_y][new_x] == '#':
                    # we got blocked, no movement happens
                    break
                else:
                    print("unexpected board content")

print("We are at",cur_x,cur_y,"facing",cur_facing)
print("Final value is",1000*(cur_y+1)+4*(cur_x+1)+cur_facing)
