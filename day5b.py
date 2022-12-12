#!/usr/bin/env python3

nstacks = 9

with open("day5.txt") as infile:
    read_header = True
    # The 0th element represents the TOP of each stack
    stack_contents = []
    for i in range(nstacks):
        stack_contents.append([])

    for line in infile:
        if read_header:
            if line[1] == '1':
                read_header = False
                line = next(infile) # skip blank line after header
                next
            else:
                for i in range(nstacks):
                    pos = i*4+1
                    if not line[pos] == ' ':
                        stack_contents[i].append(line[pos])
        else:
            # assume all instructions are well-formatted
            fields = line.split(" ")
            qty = int(fields[1])
            src = int(fields[3])-1
            dst = int(fields[5])-1

            # not sure if this condition will happen, but
            # let's protect ourselves
            if len(stack_contents[src]) < qty:
                qty = len(stack_contents[src])

            tr = stack_contents[src][0:qty]
            del stack_contents[src][0:qty]
            stack_contents[dst] = tr + stack_contents[dst]

    outstring = ""
    for i in range(nstacks):
        outstring += stack_contents[i][0]
    print(outstring)
