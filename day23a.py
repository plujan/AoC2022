#!/usr/bin/env python3

from collections import defaultdict

# A set of tuples is probably not the world's most efficient data structure for this problem,
# but it's simple and easy to implement, so!
occupied_spaces = set()

with open("day23.txt") as infile:
    for y, line in enumerate(infile):
        for x, c in enumerate(line.rstrip()):
            if c == '#':
                occupied_spaces.add((x, y))

#              N        S       W        E
directions = ((0, -1), (0, 1), (-1, 0), (1, 0))
cur_first_direction = 0

# for debugging
def print_board():
    x_coords = sorted([i[0] for i in occupied_spaces])
    y_coords = sorted([i[1] for i in occupied_spaces])
    for y in range(y_coords[0], y_coords[-1]+1):
        for x in range(x_coords[0], x_coords[-1]+1):
            if (x, y) in occupied_spaces:
                print('#', end='')
            else:
                print('.', end='')
        print()

for i in range(10):
    n_moved_this_round = 0
    proposed_moves = {} # dictionary containing all proposed moves, (start square)->(target square)
    n_proposed = defaultdict(int) # dictionary containing the number of elves proposing to move to a given target square

    for cur_pos in occupied_spaces:
        # First look to see if there are any neighbors.
        n_neighbors = 0
        cur_x = cur_pos[0]
        cur_y = cur_pos[1]
        for ix in (-1, 0, 1):
            for iy in (-1, 0, 1):
                if ix == 0 and iy == 0:
                    continue
                if (cur_x+ix, cur_y+iy) in occupied_spaces:
                    n_neighbors += 1
        if n_neighbors == 0:
            # don't move this one
            continue

        # Now look to see where we move.
        for i_dir in range(4):
            cur_dir = directions[(cur_first_direction+i_dir) % 4]
            try_this_move = False
            if cur_dir[0] == 0:
                if ((cur_x-1, cur_y+cur_dir[1]) not in occupied_spaces and
                    (cur_x, cur_y+cur_dir[1]) not in occupied_spaces and
                    (cur_x+1, cur_y+cur_dir[1]) not in occupied_spaces):
                    try_this_move = True
            elif cur_dir[1] == 0:
                if ((cur_x+cur_dir[0], cur_y-1) not in occupied_spaces and
                    (cur_x+cur_dir[0], cur_y) not in occupied_spaces and
                    (cur_x+cur_dir[0], cur_y+1) not in occupied_spaces):
                    try_this_move = True
            if try_this_move == False:
                # Note: the spec doesn't specify what happens if all four directions are blocked; I'm just
                # gonna assume that no move happens in that case
                continue
            else:
                # Make the proposal for this move
                proposed_moves[cur_pos] = (cur_x+cur_dir[0], cur_y+cur_dir[1])
                n_proposed[(cur_x+cur_dir[0], cur_y+cur_dir[1])] += 1
                break
                
    # OK, we've completed looking at all elves. Now resolve all proposals.
    for (s, e) in proposed_moves.items():
        if n_proposed[e] == 1:
            occupied_spaces.remove(s)
            occupied_spaces.add(e)
            n_moved_this_round += 1

    # If no one moved this round, we're done!
    if n_moved_this_round == 0:
        break
    # Otherwise advance the current starting proposed direction
    cur_first_direction = (cur_first_direction + 1) % 4

# print_board()
# Finally, find the space occupied.
x_coords = sorted([i[0] for i in occupied_spaces])
y_coords = sorted([i[1] for i in occupied_spaces])
total_area = (x_coords[-1]-x_coords[0]+1) * (y_coords[-1]-y_coords[0]+1)
print("Total empty space is", total_area-len(occupied_spaces))
