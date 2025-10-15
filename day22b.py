#!/usr/bin/env python3

# Possibly the trickiest part of this is finding a good way to represent the faces of a cube.
# I finally settled on this method:
# - a 3-tuple with the individual lattice point within the cube
# - a 3-tuple representing the face that we're on, defined as the normal vector pointing outward from that face
# - a 2-tuple with the point on the original plane
# - the contents (empty or wall)

import re
import sys

cube_size = 50
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

# Basic routine for traversing the cube.
# Direction should be one of (+/-1, 0, 0), (0, +/-1, 0), (0, 0, +/-1)
def navigate_cube(pos, face, direction):
    new_pos = list(pos)
    new_face = list(face)
    new_direction = list(direction)
    
    # There are 24 possibilities where we cross an edge (12 edges * 2 directions). With clever math we could
    # probably do this with fewer cases than we have here, but that's ok. Note that when we cross an edge, the
    # position doesn't change, because we're just moving onto a new face of the same 1x1x1 cube. The new direction
    # is always the opposite of the norm vector of the old face we're moving from
    # The six possibilities below are for moving onto the back face, front face, left face, right face, bottom
    # face, and top face, respectively.
    if pos[0] + direction[0] < 0:
        new_face = [-1, 0, 0]
        new_direction = [-x for x in face]
    elif pos[0] + direction[0] >= cube_size:
        new_face = [1, 0, 0]
        new_direction = [-x for x in face]
    elif pos[1] + direction[1] < 0:   
        new_face = [0, -1, 0]
        new_direction = [-x for x in face]
    elif pos[1] + direction[1] >= cube_size:
        new_face = [0, 1, 0]
        new_direction = [-x for x in face]
    elif pos[2] + direction[2] < 0:
        new_face = [0, 0, -1]
        new_direction = [-x for x in face]
    elif pos[2] + direction[2] >= cube_size:
        new_face = [0, 0, 1]
        new_direction = [-x for x in face]
    else:
        # We didn't cross an edge, so just move us along the current edge
        new_pos = [pos[i] + direction[i] for i in range(3)]

    return (new_pos, new_face, new_direction)

# cross product, used for rotating on the cube
def cross_product(a, b):
    # [ i  j  k  ]
    # [ a0 a1 a2 ]
    # [ b0 b1 b2 ]

    return [a[1]*b[2] - a[2]*b[1], a[2]*b[0] - a[0]*b[2], a[0]*b[1] - a[1]*b[0]]

# For making left turns and right turns on the cube, we just need to take the cross product of the current
# direction and the norm vector (since those are both unit vectors)
def rotate_right(direction, face):
    return cross_product(direction, face)

def rotate_left(direction, face):
    return cross_product(face, direction)

# Next, "wrap" the board on the cube. In order to do this, we do a traversal of all of the positions on the
# board, simultaneously tracking our movement across the board and the cube, so that we can map each position
# on the cube to its position on the board. In order to do this traversal, start at the position of the first
# dot, which we'll arbitrarily put at the top-left of the top face (note that this means that +y on the board
# is +x on the cube and vice-versa, probably not the most elegant choice), and then do a flood fill algorithm
# on the board positions.

# status on the board
cur_y = 0
cur_x = board[0].index(".")

visited_board_spaces = set()
board_space_pool = []
cube = {}
# each member of the pool is: board x, y, board facing index, cube x,y,z, cube face vector, cube facing vector
board_space_pool.append([cur_x, cur_y, 0, [0, 0, cube_size-1], [0, 0, 1], [0, 1, 0]])
board_space_pool.append([cur_x, cur_y, 1, [0, 0, cube_size-1], [0, 0, 1], [1, 0, 0]])
visited_board_spaces.add((cur_x, cur_y))
cube[str([0, 0, cube_size-1, 0, 0, 1])] = [cur_x, cur_y, board[cur_y][cur_x]]

while board_space_pool:
    (cur_x, cur_y, cur_facing, cube_pos, cube_face, cube_dir) = board_space_pool.pop()
    # print("at",cur_x,cur_y,"->",facings[cur_facing],"<=>",cube_pos,cube_face,"->",cube_dir)
    
    # can we walk one step in the current direction?
    if (cur_x+facings[cur_facing][0] >= 0 and cur_x+facings[cur_facing][0] < board_width and
        cur_y+facings[cur_facing][1] >= 0 and cur_y+facings[cur_facing][1] < board_height):
        # move step on the board
        cur_x += facings[cur_facing][0]
        cur_y += facings[cur_facing][1]
        # move step on the cube
        (cube_pos, cube_face, cube_dir) = navigate_cube(cube_pos, cube_face, cube_dir)
        
        # if we haven't been here yet and it's not an empty square, process it
        if (cur_x, cur_y) not in visited_board_spaces and board[cur_y][cur_x] != " ":
            visited_board_spaces.add((cur_x, cur_y))
            cube[str(cube_pos+cube_face)] = [cur_x, cur_y, board[cur_y][cur_x]]
            
            # Add three possibilities: continuing in the direction we were, rotating left, or rotating right
            board_space_pool.append([cur_x, cur_y, cur_facing, list(cube_pos), list(cube_face), list(cube_dir)])
            board_space_pool.append([cur_x, cur_y, (cur_facing+1) % len(facings), list(cube_pos), list(cube_face),
                                     rotate_right(cube_dir, cube_face)])
            board_space_pool.append([cur_x, cur_y, (cur_facing-1) % len(facings), list(cube_pos), list(cube_face),
                                     rotate_left(cube_dir, cube_face)])
                                     

# Our mapping is done!
#print(cube)
# for x in range(0, cube_size):
#     for y in range(0, cube_size):
#         v = [x, y, 0, 0, 0, -1]
#         print(v, cube[str(v)])
                                       

# Finally, we are ready to actually execute the instructions. Let's start over.
# Starting board position
cur_y = 0
cur_x = board[0].index(".")
cur_facing = 0

cube_pos = [0, 0, cube_size-1]
cube_face = [0, 0, 1]
cube_direction = [0, 1, 0]

facing_chars = ">v<^"

# Nextly, execute the instructions.
for i in instructions:
    if (i == 'R'):
        cur_facing = (cur_facing + 1) % len(facings)
        cube_direction = rotate_right(cube_direction, cube_face)
        board[cur_y][cur_x] = facing_chars[cur_facing]
    elif (i == 'L'):
        cur_facing = (cur_facing - 1) % len(facings)
        cube_direction = rotate_left(cube_direction, cube_face)
        board[cur_y][cur_x] = facing_chars[cur_facing]
    else:
        for n in range(int(i)):
            # Navigate ON THE CUBE and then translate that back to the board
            (new_pos, new_face, new_direction) = navigate_cube(cube_pos, cube_face, cube_direction)
            new_x = cube[str(new_pos+new_face)][0]
            new_y = cube[str(new_pos+new_face)][1]
            new_contents = cube[str(new_pos+new_face)][2]

            if new_contents == '#':
                # we are blocked, don't move here and stop
                break
            elif new_contents == '.':
                # we are ok, move here
                board[cur_y][cur_x] = facing_chars[cur_facing]
                # First, we have to figure out our new facing on the board. If we didn't change faces on the
                # cube, then the facing on the board didn't change. But if we did, it changed in a way that we
                # can't immediately calculate. Instead, find it out by taking one more step on the cube,
                # seeing where that takes us (which will be guaranteed to be one step on the board), and then
                # using that as our facing.
                if new_face != cube_face:
                    (test_pos, test_face, test_direction) = navigate_cube(new_pos, new_face, new_direction)
                    test_x = cube[str(test_pos+test_face)][0]
                    test_y = cube[str(test_pos+test_face)][1]
                    if test_x == new_x+1 and test_y == new_y:
                        cur_facing = 0
                    elif test_x == new_x and test_y == new_y+1:
                        cur_facing = 1
                    elif test_x == new_x-1 and test_y == new_y:
                        cur_facing = 2
                    elif test_x == new_x and test_y == new_y-1:
                        cur_facing = 3
                    else:
                        print("Test to find new facing failed!!!")
                cur_x = new_x
                cur_y = new_y
                cube_pos = new_pos
                cube_face = new_face
                cube_direction = new_direction
            else:
                print("unexpected board content")

for b in board:
    print("".join(b))
                
print("We are at",cur_x,cur_y,"facing",cur_facing)
print("Final value is",1000*(cur_y+1)+4*(cur_x+1)+cur_facing)
