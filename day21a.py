#!/usr/bin/env python3

import re
import sys

# For monkeys where we know the value, this just stores the value
known_vals = {}
# For monkeys where we don't yet know the value, this stores the two monkeys
# and the operation, in that order
unknown_vals = {}

with open("day21.txt") as infile:
    for line in infile:
        result = re.search("(....): (\d+)", line)
        if result:
            known_vals[result.group(1)] = int(result.group(2))

        result = re.search("(....): (....) (.) (....)", line)
        if result:
            unknown_vals[result.group(1)] = (result.group(2), result.group(4), result.group(3))

        # Now, go through the unknown (so far) values, and see if we know them. Keep iterating
        # until we haven't found any more.
        make_another_pass = True
        while make_another_pass:
            clear_keys = []
            for (k, v) in unknown_vals.items():
                if v[0] in known_vals and v[1] in known_vals:
                    if v[2] == '+':
                        val = known_vals[v[0]] + known_vals[v[1]]
                    elif v[2] == '-':
                        val = known_vals[v[0]] - known_vals[v[1]]
                    elif v[2] == '*':
                        val = known_vals[v[0]] * known_vals[v[1]]
                    elif v[2] == '/':
                        val = known_vals[v[0]] / known_vals[v[1]]
                    else:
                        print("Bad operator", v[2], "for monkey", k)
                    known_vals[k] = val
                    clear_keys.append(k)
            make_another_pass = False
            if clear_keys:
                make_another_pass = True
            for k in clear_keys:
                del unknown_vals[k]

        if 'root' in known_vals:
            print("Value of root is", known_vals['root'])
            sys.exit(0)
