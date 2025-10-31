#!/usr/bin/env python3

# Since obviously simulating 1 trillion iterations is impractical, we look for a case where:
# 1) the topmost row is filled (so we don't have to worry about blocks falling past it)
# 2) the current rock and jet are the same as a previous case when the topmost row was filled
# Then, we can just do some multiplication and simulate whatever remainder is left over to get to our target.

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

tot_rocks = 1000000000000
cur_rock = 0

with open("day17.txt") as infile:
    jets = list(infile.read().rstrip())

cur_jet = 0

board_width = 7
board = []
board.append([1]*board_width)
cur_max_height = 0

n_placed = 0
n_remaining = -1 # once we're computing the remainder, this is the number of blocks left to place

full_states = []
full_states.append((n_placed, cur_max_height, cur_rock, cur_jet))

while n_remaining != 0:
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

            n_placed += 1
            if n_remaining >= 0:
                n_remaining -= 1
                                
            if board[cur_max_height] == [1, 1, 1, 1, 1, 1, 1]:
                # The top row is full, which means that we're effectively starting from the beginning.
                # See if we've been here before. If so, we're almost done!
                found_match = False
                for x in full_states:
                    if cur_rock == x[2] and cur_jet == x[3]:
                        print("Found state repeat from", x[1], "with", x[0], "rocks to", cur_max_height, "with",
                              n_placed)
                        found_match = True
                        rocks_per_repetition = n_placed-x[0]
                        height_per_repetition = cur_max_height-x[1]
                        n_repetitions = (tot_rocks-n_placed) // rocks_per_repetition
                        n_remaining = tot_rocks-n_placed-rocks_per_repetition*n_repetitions
                        break
                if not found_match:
                    full_states.append((n_placed, cur_max_height, cur_rock, cur_jet))

            # print(list(reversed(board)))
            break
        
print("Total maximum height of tower is", cur_max_height + n_repetitions*height_per_repetition)
