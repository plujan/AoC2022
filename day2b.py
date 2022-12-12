#!/usr/bin/env python3

shape_val = {"R": 1, "P": 2, "S": 3}

strategy_matrix = {"A": {"X": "S", "Y": "R", "Z": "P"},
                   "B": {"X": "R", "Y": "P", "Z": "S"},
                   "C": {"X": "P", "Y": "S", "Z": "R"}}

outcome_val = {"X": 0, "Y": 3, "Z": 6}

with open("day2.txt") as infile:
    tot_points = 0
    for line in infile:
        target_outcome = line[2]
        target_strategy = strategy_matrix[line[0]][target_outcome]
        tot_points += shape_val[target_strategy] + outcome_val[target_outcome]

    print("Total points is", tot_points)
