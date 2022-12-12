#!/usr/bin/env python3

visited_pos = set()
visited_pos.add("0,0")
nknots = 10

knot_pos = [[0, 0] for x in range(nknots)]

with open("day9.txt") as infile:
    for line in infile:
        fields = line.split(" ")
        for n in range(int(fields[1])):
            if fields[0] == "D":
                knot_pos[0][1] -= 1
            elif fields[0] == "U":
                knot_pos[0][1] += 1
            elif fields[0] == "L":
                knot_pos[0][0] -= 1
            elif fields[0] == "R":
                knot_pos[0][0] += 1

            for i in range(1, nknots):
                if abs(knot_pos[i][0] - knot_pos[i-1][0]) <= 1 and abs(knot_pos[i][1] - knot_pos[i-1][1]) <= 1:
                    continue
                
                for k in range(2):
                    if knot_pos[i-1][k] > knot_pos[i][k]:
                        knot_pos[i][k] += 1
                    elif knot_pos[i-1][k] < knot_pos[i][k]:
                        knot_pos[i][k] -= 1

            visited_pos.add(str(knot_pos[nknots-1][0])+","+str(knot_pos[nknots-1][1]))
        
print("Positions visited", len(visited_pos))
