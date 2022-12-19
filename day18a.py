#!/usr/bin/env python3

cubes = []
with open("day18.txt") as infile:
    for line in infile:
        fields = [int(x) for x in line.split(",")]
        cubes.append((fields[0], fields[1], fields[2]))

total_surface_area = 0
for c in cubes:
    for d in [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0),
              (0, 0, 1), (0, 0, -1)]:
        n = tuple(map(lambda x, y: x + y, c, d))
        # If the neighboring space is not occupied by another cube,
        # then this is an open face that we should count
        if n not in cubes:
            total_surface_area += 1

print("Total surface area is", total_surface_area)
