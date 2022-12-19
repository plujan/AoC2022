#!/usr/bin/env python3

# There's probably a more elegant way to do this than all of these isinstance() invocations,
# but this at least works.

import json

def compare_lists(a, b):
    for i in range(min(len(a), len(b))):
        x = compare_items(a[i], b[i])
        if x != 0:
            return x

    if len(a) < len(b):
        return 1
    if len(a) > len(b):
        return -1
    return 0

def compare_items(a, b):
    if isinstance(a, int) and isinstance(b, int):
        if a < b:
            return 1
        if a > b:
            return -1
        return 0
    if isinstance(a, int) and isinstance(b, list):
        return compare_lists([a], b)
    if isinstance(a, list) and isinstance(b, int):
        return compare_lists(a, [b])
    return compare_lists(a, b)

total_correct = 0

with open("day13.txt") as infile:
    for i, line in enumerate(infile):
        # a little safer than just eval'ing it
        l = json.loads(line)
        line = next(infile)
        r = json.loads(line)
        x = compare_lists(l, r)
        if x == 1:
            total_correct += i+1

        if x == 0:
            print(l, r, i+1, "is identical, not sure what do to about this case")

        # skip blank line
        try:
            line = next(infile)
        except StopIteration:
            break
            
print("Sum of correct indexes is", total_correct)
