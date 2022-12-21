#!/usr/bin/env python3

# Note: the rocks are upside-down to make the math simpler (this only affects the 3rd one)
# However, both the rocks and the board should be accessed as rocks[y][x]

rocks = [
    [[1, 1, 1, 1]],

    [[0, 1, 0],
     [1, 1, 1],
     [0, 1, 0]],

    [[1, 1, 1],
     [0, 0, 1],
     [0, 0, 1]],

    [[1], [1], [1], [1]],

    [[1, 1],
     [1, 1]]
]

cur_rock = 0

with open("day17.txt") as infile:
    jets = list(infile.read().rstrip())

cur_jet = 0

board_width = 7
board = []
board.append([1]*board_width)
cur_max_height = 0

for i in range(2022):
    # Spawn rock
    cur_bottom_pos = cur_max_height+4
    cur_left_pos = 2
    cur_height = len(rocks[cur_rock])
    cur_width = len(rocks[cur_rock][0])

    # Add rows as necessary
    while (cur_bottom_pos+cur_height) > len(board):
        board.append([0]*board_width)

    # Move rock according to the rules until it comes to rest
    while True:
        # First apply the jet.
        if jets[cur_jet] == '<':
            jet_dir = -1
        else:
            jet_dir = 1
        cur_jet = (cur_jet + 1) % len(jets)

        # First check to see if this is even in bounds.
        if (cur_left_pos + jet_dir >= 0 and cur_left_pos + cur_width - 1 + jet_dir < board_width):
            # Now check each item in the rock to see if it actually works.
            move_is_valid = True
            for rx in range(0, cur_width):
                for ry in range(0, cur_height):
                    if rocks[cur_rock][ry][rx] == 1 and board[cur_bottom_pos+ry][cur_left_pos+rx+jet_dir] == 1:
                        move_is_valid = False

            # If the move was not blocked, move! Otherwise nothing happens.
            if move_is_valid:
                cur_left_pos += jet_dir
                
        # Next, see if we can move downwards.
        move_is_valid = True
        for rx in range(0, cur_width):
            for ry in range(0, cur_height):
                if rocks[cur_rock][ry][rx] == 1 and board[cur_bottom_pos+ry-1][cur_left_pos+rx] == 1:
                    move_is_valid = False

        if move_is_valid == True:
            cur_bottom_pos -= 1
        else:
            # Move is blocked, rock comes to rest
            for rx in range(0, cur_width):
                for ry in range(0, cur_height):
                    if rocks[cur_rock][ry][rx] == 1:
                        board[cur_bottom_pos+ry][cur_left_pos+rx] = 1
                        if cur_max_height < cur_bottom_pos+ry:
                            cur_max_height = cur_bottom_pos+ry

            cur_rock = (cur_rock + 1) % len(rocks)
#            print(list(reversed(board)))
            break

print("Total maximum height of tower is", cur_max_height)
