#!/usr/bin/env python3

tot_signal_strength = 0
cur_x = 1
cycles_completed = 0

def output_char(i):
    xpos = (i-1) % 40
    if abs(xpos - cur_x) <= 1:
        print("#", end='')
    else:
        print(".", end='')
    if (i % 40) == 0:
        print()
        
with open("day10.txt") as infile:
    for line in infile:
        fields = line.rstrip().split(" ")
        if fields[0] == "noop":
            cycles_completed += 1
            output_char(cycles_completed)
        elif fields[0] == "addx":
            cycles_completed += 1
            output_char(cycles_completed)
            cycles_completed += 1
            output_char(cycles_completed)
            cur_x += int(fields[1])
        else:
            print("Bad input", line)
