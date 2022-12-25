#!/usr/bin/env python3

# I tried a bunch of solutions to this problem, but this one is the first one that worked. The trick is that
# obviously a point-by-point solution like we used for part 1 won't work, but since the excluded regions are
# always ranges of contiguous numbers, we can just store the excluded ranges. The code for merging ranges when
# we insert a new one is surprisingly tricky (as you can see below), but once that's all sorted, the code
# works in a reasonable amount of time.

import re

area_size = 4000000
excluded_squares = [[] for y in range(area_size+1)]

def insert_range(a, xmin, xmax):
    if a == []:
        a.append([xmin, xmax])
        return
    elif xmin < a[0][0]:
        a.insert(0, [xmin, xmax])
        i = 0
    elif xmin >= a[-1][0]:
        # skip if this is a subset of the last item
        if xmax <= a[-1][1]:
            return
        a.append([xmin, xmax])
        i = len(a)-1
    else:
        for i in range(len(a)-1):
            # This range is a subset of a range that already exists, don't bother
            if xmin >= a[i][0] and xmax <= a[i][1]:
                return
            if (xmin > a[i][0] and xmin <= a[i+1][0]) or (xmin == a[i][0] and xmax > a[i][1]):
                a.insert(i+1, [xmin, xmax])
                i += 1
                break

    # Now check to see if we need to merge with the neighbors.
    # First see if we need to merge right.
    if i+1 < len(a) and xmax >= a[i+1][0]-1:
        j = i+1
        while j+1 < len(a) and xmax >= a[j+1][0]-1:
            j = j+1
        if xmax < a[j][1]:
            a[i][1] = a[j][1]
        del a[i+1:j+1]
    # Now see if we need to merge left.
    if i > 0 and a[i-1][1] >= xmin - 1:
        a[i-1][1] = a[i][1]
        del a[i]

with open("day15.txt") as infile:
    for line in infile:
        result = re.search("Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)", line)
        if result:
            sx = int(result.group(1))
            sy = int(result.group(2))
            bx = int(result.group(3))
            by = int(result.group(4))
            dist_to_beacon = abs(bx-sx) + abs(by-sy)

            for y in range(max(0, sy-dist_to_beacon), min(area_size, sy+dist_to_beacon)+1):
                y_dist = abs(sy-y)
                insert_range(excluded_squares[y],
                             max(0, sx-(dist_to_beacon-y_dist)),
                             min(area_size, sx+(dist_to_beacon-y_dist)))
                # if y == 7:
                #     print(y, sx, dist_to_beacon-y_dist, max(0, sx-(dist_to_beacon-y_dist)),
                #           min(area_size, sx+(dist_to_beacon-y_dist)), excluded_squares[y])


for y in range(area_size+1):
    if excluded_squares[y] != [[0, area_size]]:
        # Assume it's just a discontinuity of 1, otherwise not quite sure how to deal with this
        if len(excluded_squares[y]) == 2 and excluded_squares[y][0][1]+2 == excluded_squares[y][1][0]:
            x = excluded_squares[y][0][1]+1
            print("Found possible location at", x, y, "frequency=",area_size*x+y)
        else:
            print("Row", y, "=", excluded_squares[y])
