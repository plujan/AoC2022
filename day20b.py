#!/usr/bin/env python3

# We store each item as a two-element tuple, the first with the actual item and the second with the
# position. This does unfortunately mean we have to look through the whole list each time to find the next
# item, but that hopefully shouldn't be prohibitive.

# Note: this doesn't quite match the example because if it's, say, moving the 2nd element left two, it places
# it at the beginning, while the example puts it at the end, but that's ok since the list is circular anyway.

decryption_key = 811589153
items = []
with open("day20.txt") as infile:
    for i, line in enumerate(infile):
        items.append((int(line)*decryption_key, i))

for x in range(10):
    items_processed = 0
    while items_processed < len(items):
        # Find next item
        for (i, it) in enumerate(items):
            if it[1] == items_processed:
                # Deal with this item
                new_pos = (i+it[0]) % (len(items)-1)
                items.pop(i)
                items.insert(new_pos, it)
                # if equal, nothing to do!
                items_processed += 1
                break

for (i, it) in enumerate(items):
    if it[0] == 0:
        i1 = (i+1000) % len(items)
        i2 = (i+2000) % len(items)
        i3 = (i+3000) % len(items)
        print("Sum of grove coordinates is", items[i1][0]+items[i2][0]+items[i3][0])
        break

