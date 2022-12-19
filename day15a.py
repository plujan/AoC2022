#!/usr/bin/env python3

import re

# We just care about the target row, so focus on that
target_row = 2000000
excluded_squares = set()

with open("day15.txt") as infile:
    for line in infile:
        result = re.search("Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)", line)
        if result:
            sx = int(result.group(1))
            sy = int(result.group(2))
            bx = int(result.group(3))
            by = int(result.group(4))
            dist_to_beacon = abs(bx-sx) + abs(by-sy)
            dist_to_target = abs(sy-target_row)
            if dist_to_target <= dist_to_beacon:
                for i in range(sx-(dist_to_beacon-dist_to_target),
                               sx+(dist_to_beacon-dist_to_target)+1):
                    # If the beacon actually IS in the target row,
                    # don't exclude that square!
                    if not (bx == i and by == target_row):
                        excluded_squares.add(i)
        else:
            print("Found malformed line", line)

print("Total number of excluded squares is", len(excluded_squares))
