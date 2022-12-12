#!/usr/bin/env python3

shape_val = {"X": 1, "Y": 2, "Z": 3}

payoff_matrix = {"A": {"X": 3, "Y": 6, "Z": 0},
                 "B": {"X": 0, "Y": 3, "Z": 6},
                 "C": {"X": 6, "Y": 0, "Z": 3}}

with open("day2.txt") as infile:
    tot_points = 0
    for line in infile:
        tot_points += shape_val[line[2]] + payoff_matrix[line[0]][line[2]]

    print("Total points is", tot_points)
