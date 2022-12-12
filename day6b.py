#!/usr/bin/env python3

marker_len = 14

with open("day6.txt") as infile:
    for line in infile:
        cur_buffer = ""
        for i, c in enumerate(line):
            if len(cur_buffer) < marker_len:
                cur_buffer += c
            else:
                cur_buffer = cur_buffer[1:] + c
                if len(set(cur_buffer)) == marker_len:
                    print("Position is",i+1)
                    break
