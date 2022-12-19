#!/usr/bin/env python3

cubes = []
with open("day18.txt") as infile:
    for line in infile:
        fields = [int(x) for x in line.split(",")]
        cubes.append((fields[0], fields[1], fields[2]))

# Now we need to find cubes in the interior. There is almost certainly a more elegant way, but here's what I've chosen to do:
# 1) Take the cubic volume surrounding all cubes, plus a margin of 1
# 2) Flood fill to find all of the "external" cubes
# 3) Any cubes left in the volume that aren't either filled with lava or an "external" cube must be internal

xmin = min([c[0] for c in cubes])-1
xmax = max([c[0] for c in cubes])+1
ymin = min([c[1] for c in cubes])-1
ymax = max([c[1] for c in cubes])+1
zmin = min([c[2] for c in cubes])-1
zmax = max([c[2] for c in cubes])+1

external_cubes = set()
external_cubes.add((xmin, ymin, zmin))
cubes_to_process = [(xmin, ymin, zmin)]
internal_cubes = set()

while len(cubes_to_process) > 0:
    c = cubes_to_process.pop(0)
    for d in [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0),
              (0, 0, 1), (0, 0, -1)]:
        n = tuple(map(lambda x, y: x + y, c, d))
        if n[0] < xmin or n[0] > xmax or n[1] < ymin or n[1] > ymax or n[2] < zmin or n[2] > zmax:
            continue
        if n in cubes or n in external_cubes:
            continue
        external_cubes.add(n)
        cubes_to_process.append(n)


for x in range(xmin, xmax+1):
    for y in range(ymin, ymax+1):
        for z in range(zmin, zmax+1):
            if (x, y, z) not in cubes and (x, y, z) not in external_cubes:
                internal_cubes.add((x, y, z))
        
total_surface_area = 0
for c in cubes:
    for d in [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0),
              (0, 0, 1), (0, 0, -1)]:
        n = tuple(map(lambda x, y: x + y, c, d))
        # If the neighboring space is not occupied by another cube,
        # then this is an open face that we should count UNLESS it's an "internal cube"
        if n not in cubes and n not in internal_cubes:
            total_surface_area += 1

print("Total surface area (not counting internal cubes) is", total_surface_area)
