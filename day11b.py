#!/usr/bin/env python3

import re

# Simple brute force will fail horribly, since the numbers just become ridiculously big. Instead, we look at
# the product of all of the divisibility tests and always take the remainder of the value with respect to that
# product, to keep the values reasonble.

monkeys = []
divis_product = 1

# put this in its own function so we can return a closure
def parse_operation(line):
    result = re.search("Operation: new = old (.) (.*)", line)
    if result:
        if result.group(1) == '+':
            if result.group(2) == 'old':
                return lambda x: x+x
            else:
                return lambda x: x+int(result.group(2))
        elif result.group(1) == '*':
            if result.group(2) == 'old':
                return lambda x: x*x
            else:
                return lambda x: x*int(result.group(2))
        else:
            print("Failed to parse operation line", line)
    else:
        print("Expected operation line but got", line)


with open("day11.txt") as infile:
    for line in infile:
        this_monkey = {'items_inspected': 0}
        result = re.search("Monkey (\d+)", line)
        if result:
            if int(result.group(1)) != len(monkeys):
                print("Unexpected monkey number", result.group(1))
        else:
            print("Expected monkey header but got", line)

        line = next(infile)
        result = re.search("Starting items: (.*)", line)
        if result:
            this_monkey['items'] = [int(x) for x in result.group(1).split(", ")]
        else:
            print("Expected list of starting items but got", line)

        line = next(infile)
        this_monkey['function'] = parse_operation(line)

        line = next(infile)
        result = re.search("Test: divisible by (\d+)", line)
        if result:
            this_monkey['test_divis'] = int(result.group(1))
        else:
            print("Expected test line but got", line)
        divis_product *= this_monkey['test_divis']
                    
        line = next(infile)
        result = re.search("If true: throw to monkey (\d+)", line)
        if result:
            this_monkey['true_monkey'] = int(result.group(1))
        else:
            print("Expected if_true line but got", line)

        line = next(infile)
        result = re.search("If false: throw to monkey (\d+)", line)
        if result:
            this_monkey['false_monkey'] = int(result.group(1))
        else:
            print("Expected if_false line but got", line)

        monkeys.append(this_monkey)
            
        # skip blank line
        try:
            line = next(infile)
        except StopIteration:
            break

# Now that we've read in everything, let's actually apply it!
for i in range(10000):
    for m in monkeys:
        for item in m['items']:
            # apply function
            item = m['function'](item)
            # reduce worry
            item = item % divis_product
            # check and throw
            if item % m['test_divis'] == 0:
                monkeys[m['true_monkey']]['items'].append(item)
            else:
                monkeys[m['false_monkey']]['items'].append(item)
        # update total
        m['items_inspected'] += len(m['items'])
        # clear list        
        m['items'] = []
    print("Finished",i,"iterations")
        
total_inspections = sorted([m['items_inspected'] for m in monkeys])
print("Total monkey business is", total_inspections[-1]*total_inspections[-2])
