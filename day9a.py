#!/usr/bin/env python3

visited_pos = set()
visited_pos.add("0,0")
head_pos = [0, 0]
tail_pos = [0, 0]

with open("day9.txt") as infile:
    for line in infile:
        fields = line.split(" ")
        for n in range(int(fields[1])):
            if fields[0] == "D":
                head_pos[1] -= 1
            elif fields[0] == "U":
                head_pos[1] += 1
            elif fields[0] == "L":
                head_pos[0] -= 1
            elif fields[0] == "R":
                head_pos[0] += 1

            if abs(head_pos[0] - tail_pos[0]) <= 1 and abs(head_pos[1] - tail_pos[1]) <= 1:
                continue
                
            for k in range(2):
                if head_pos[k] > tail_pos[k]:
                    tail_pos[k] += 1
                elif head_pos[k] < tail_pos[k]:
                    tail_pos[k] -= 1

            visited_pos.add(str(tail_pos[0])+","+str(tail_pos[1]))
            
print("Positions visited", len(visited_pos))
