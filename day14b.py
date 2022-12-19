#!/usr/bin/env python3

import sys

# we'll expand this as necessary
occupied_squares = []

with open("day14.txt") as infile:
    for line in infile:
        points = line.rstrip().split(" -> ")
        for i, p in enumerate(points):
            (x, y) = [int(s) for s in p.split(",")]
            while y > len(occupied_squares)-1:
                occupied_squares.append(set())
            if i == 0:
                x0 = x
                y0 = y
            else:
                if x == x0:
                    for iy in range(min(y, y0), max(y, y0)+1):
                        occupied_squares[iy].add(x)
                else:
                    for ix in range(min(x, x0), max(x, x0)+1):
                        occupied_squares[y].add(ix)
                x0 = x
                y0 = y

# Add two more layers for the empty layer above the floor and the floor itself (which will be handled as a
# special case below).
occupied_squares.append(set())
occupied_squares.append(set())
                
# Now simulate sand.
n_grains = 0
while True:
    x = 500
    y = 0
    while True:
        if y == len(occupied_squares) - 2:
            # We're one above the floor layer, so we're definitely blocked
            pass
        elif x not in occupied_squares[y+1]:
            y += 1
            continue
        elif x-1 not in occupied_squares[y+1]:
            x -= 1
            y += 1
            continue
        elif x+1 not in occupied_squares[y+1]:
            x += 1
            y += 1
            continue

        # Grain has come to rest.
        occupied_squares[y].add(x)
        n_grains += 1

        if (x == 500 and y == 0):
            # We're done!
            print("Total of", n_grains, "grains come to rest")
            sys.exit(0)
        
        break
