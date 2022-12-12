#!/usr/bin/env python3

with open("day3.txt") as infile:
    tot_prio = 0
    for line1 in infile:
        line2 = next(infile)
        line3 = next(infile)
        s1 = set(line1.rstrip())
        s2 = set(line2.rstrip())
        s3 = set(line3.rstrip())

        i = set.intersection(s1, s2, s3)
        
        a = ord(list(i)[0])
        if a >= 65 and a <= 90:
            v = a - 64 + 26
        elif a >= 97 and a <= 126:
            v = a - 96
        else:
            print ("Unknown character", c)
        tot_prio += v

    print("Total priority is", tot_prio)
