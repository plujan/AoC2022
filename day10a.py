#!/usr/bin/env python3

tot_signal_strength = 0
cur_x = 1
cycles_completed = 0

def check_cycle(i):
    global tot_signal_strength
    if (i-20) % 40 == 0:
        tot_signal_strength += i*cur_x
        
with open("day10.txt") as infile:
    for line in infile:
        fields = line.rstrip().split(" ")
        if fields[0] == "noop":
            cycles_completed += 1
            check_cycle(cycles_completed)
        elif fields[0] == "addx":
            cycles_completed += 1
            check_cycle(cycles_completed)
            cycles_completed += 1
            check_cycle(cycles_completed)
            cur_x += int(fields[1])
        else:
            print("Bad input", line)

        if cycles_completed >= 220:
            break

print("Total signal strength", tot_signal_strength)
