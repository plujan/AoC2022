#!/usr/bin/env python3

with open("day1.txt") as infile:
    cur_tot = 0
    cur_max = 0
    for line in infile:
        if len(line.strip()) == 0:
            if cur_tot > cur_max:
                cur_max = cur_tot
            cur_tot = 0
        else:
            cur_tot += int(line)

    if cur_tot > cur_max:
        cur_max = cur_tot

    print("Maximum value is",cur_max)
