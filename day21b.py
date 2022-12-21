#!/usr/bin/env python3

import re
import sys

# For monkeys where we know the value, this just stores the value
known_vals = {}
# For monkeys where we don't yet know the value, this stores the two monkeys
# and the operation, in that order
unknown_vals = {}

# First we work forwards, like we did the first time, except we discard "humn" since it doesn't
# apply. This means we won't actually know all the values, which is rather the point.

with open("day21.txt") as infile:
    for line in infile:
        result = re.search("(....): (\d+)", line)
        if result and result.group(1) != "humn":
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

# Now we work backwards from "root" to deduce the values of each of the missing words.
r = unknown_vals['root']
if r[0] in known_vals:
    target_val = known_vals[r[0]]
    target_var = r[1]
elif r[1] in known_vals:
    target_val = known_vals[r[1]]
    target_var = r[0]
else:
    print("Error, both", r[0], "and", r[1], "are unknown")
    sys.exit(1)

while target_var != 'humn':
    v = unknown_vals[target_var]
    if v[0] in known_vals:
        known_val = known_vals[v[0]]
        target_var = v[1]
        if v[2] == '+':
            target_val = target_val - known_val
        elif v[2] == '-':
            target_val = known_val - target_val
        elif v[2] == '*':
            target_val = target_val / known_val
        elif v[2] == '/':
            target_val = known_val / target_val
    elif v[1] in known_vals:
        known_val = known_vals[v[1]]
        target_var = v[0]
        if v[2] == '+':
            target_val = target_val - known_val
        elif v[2] == '-':
            target_val = target_val + known_val
        elif v[2] == '*':
            target_val = target_val / known_val
        elif v[2] == '/':
            target_val = target_val * known_val
    else:
        print("Error, both", v[0], "and", v[1], "are unknown")
        sys.exit(1)
        
print("Human value is", target_val)
