#!/usr/bin/env python3

with open("day3.txt") as infile:
    tot_prio = 0
    for line in infile:
        line = line.rstrip()
        l = len(line)
        k1 = set(line[0:int(l/2)])
        k2 = set(line[int(l/2):l])
        for c in k1:
            if c in k2:
                # Calculate priority for this
                a = ord(c)
                if a >= 65 and a <= 90:
                    v = a - 64 + 26
                elif a >= 97 and a <= 126:
                    v = a - 96
                else:
                    print ("Unknown character", c)
                tot_prio += v

    print("Total priority is", tot_prio)
