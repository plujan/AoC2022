#!/usr/bin/env python3

with open("day4.txt") as infile:
    tot_pairs = 0
    for line in infile:
        fields = line.split(",")
        range1 = [int(x) for x in fields[0].split("-")]
        range2 = [int(x) for x in fields[1].split("-")]
        if not (range1[1] < range2[0] or range2[1] < range1[0]):
            tot_pairs += 1
            
    print("Total number of overlapping pairs is", tot_pairs)
