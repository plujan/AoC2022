#!/usr/bin/env python3

import re
import math

# This was my first attempt (well, technically third after a couple of things that obviously didn't work).
# First it did a lower-resolution scan by dividing it into 2000x2000 blocks, and eliminating blocks there,
# hopefully leaving few enough possibilities that we can go through them one by one.  This approach almost
# worked, but it was clear that it needed very careful treatment of blocks that were only partially covered,
# which the code below didn't quite do. I think a better approach would be to extend the size by a block or
# two in each direction, just to give a bit of a buffer, and then check for blocks for which the distance to
# all four corners was less than the beacon distance for the sensor. However, I ended up trying something
# entirely different instead.

max_dimension = 4000000
block_size = 2000
n_blocks = max_dimension // block_size

sensors = []
allowed_squares = []
for i in range(0, n_blocks+1):
    allowed_squares.append(set(range(0, n_blocks+1)))

print("Beginning low-resolution scan...")
    
with open("day15.txt") as infile:
    for line in infile:
        result = re.search("Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)", line)
        if result:
            sx = int(result.group(1))
            sy = int(result.group(2))
            bx = int(result.group(3))
            by = int(result.group(4))
            dist_to_beacon = abs(bx-sx) + abs(by-sy)
            sensors.append((sx, sy, dist_to_beacon))
            #print(sx,sy,dist_to_beacon,
            #      max(0, math.ceil((sy-dist_to_beacon)/block_size)),
            #      min(n_blocks, math.floor((sy+dist_to_beacon)/block_size))+1)
                  
            for y in range(max(0, math.ceil((sy-dist_to_beacon)/block_size)),
                           min(n_blocks, math.floor((sy+dist_to_beacon)/block_size))+1):
                y_dist = max((y+1)*block_size-sy, sy-y*block_size)
                #print(sx, sy, y, y_dist)
                for x in range(max(0, math.ceil((sx-(dist_to_beacon-y_dist))/block_size)),
                               min(n_blocks, math.floor((sx+(dist_to_beacon-y_dist))/block_size))+1):
                    allowed_squares[y].discard(x)
        else:
            print("Found malformed line", line)

tot_squares = 0
for i in range(0, n_blocks+1):
    tot_squares += len(allowed_squares[i])
print("Total of", tot_squares, "squares to check at high resolution")
            
# Now go through these squares at higher resolution and check to see if they're compatible with the beacons.
# Basically the same as above but without the reduction applied.

for i in range(0, n_blocks+1):
    for j in allowed_squares[i]:
        print("Now checking",i,j)

        xmin = j*block_size
        xmax = (j+1)*block_size
        ymin = i*block_size
        ymax = (i+1)*block_size
        allowed_squares_fine = {}
        for k in range(ymin, ymax+1):
            allowed_squares_fine[k] = set(range(xmin, xmax+1))
            
        for (sx, sy, dist_to_beacon) in sensors:
            for y in range(max(ymin, sy-dist_to_beacon), min(ymax, sy+dist_to_beacon)+1):
                y_dist = abs(sy-y)
                for x in range(max(xmin, sx-(dist_to_beacon-y_dist)),
                               min(xmax, sx+(dist_to_beacon-y_dist))+1):
                    allowed_squares_fine[y].discard(x)

        for vy in allowed_squares_fine:
            for vx in allowed_squares_fine[vy]:
                print("Possible location at", vx, vy, "frequency=", max_dimension*vx+vy)
