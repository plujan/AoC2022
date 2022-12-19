#!/usr/bin/env python3

import json
from functools import cmp_to_key

# note: have to reverse 1 and -1 here wrt the first part in order to get
# correct sorting!

def compare_lists(a, b):
    for i in range(min(len(a), len(b))):
        x = compare_items(a[i], b[i])
        if x != 0:
            return x

    if len(a) < len(b):
        return -1
    if len(a) > len(b):
        return 1
    return 0

def compare_items(a, b):
    if isinstance(a, int) and isinstance(b, int):
        if a < b:
            return -1
        if a > b:
            return 1
        return 0
    if isinstance(a, int) and isinstance(b, list):
        return compare_lists([a], b)
    if isinstance(a, list) and isinstance(b, int):
        return compare_lists(a, [b])
    return compare_lists(a, b)

all_packets = []

with open("day13.txt") as infile:
    for line in infile:
        # a little safer than just eval'ing it
        l = json.loads(line)
        line = next(infile)
        r = json.loads(line)

        all_packets.append(l)
        all_packets.append(r)

        # skip blank line
        try:
            line = next(infile)
        except StopIteration:
            break

# add delimiters
all_packets.append([[2]])
all_packets.append([[6]])

sorted_list = sorted(all_packets, key=cmp_to_key(compare_lists))

for i, l in enumerate(sorted_list):
    if l == [[2]]:
        d1 = i+1
    if l == [[6]]:
        print("Decoder key is", d1*(i+1))
        break
