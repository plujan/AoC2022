#!/usr/bin/env python3

def check_greater(cur_tot):
    global cur_max
    for i in range(3):
        if cur_tot > cur_max[i]:
            cur_max.insert(i, cur_tot)
            cur_max = cur_max[0:3]
            break

with open("day1.txt") as infile:
    cur_tot = 0
    cur_max = [0, 0, 0]
    for line in infile:
        if len(line.strip()) == 0:
            check_greater(cur_tot)
            cur_tot = 0
        else:
            cur_tot += int(line)

    check_greater(cur_tot)

    print("Sum of three maximum values is",cur_max[0]+cur_max[1]+cur_max[2])
