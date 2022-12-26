#!/usr/bin/env python3

import re

# This uses the same A* algorithm we've used for other puzzles, but without a heuristic function or a way
# to keep track of which paths we can exclude (since even if we're at a node we've explored before, it may
# be with a different time, score, set of valves open). So really it's not A* at all but just straight-up
# brute force. Hope it still works in a reasonable amount of time.
#
# Update: by adding the valve pruning step below, we can finish the full problem on the scale of a few
# minutes, which isn't great but at least works.

max_time = 30

valves = {}

with open("day16.txt") as infile:
    for line in infile:
        result = re.search("Valve (..) has flow rate=(\d+); tunnels? leads? to valves? (.*)", line)
        if result:
            valve_name = result.group(1)
            valve_rate = int(result.group(2))
            tunnels = result.group(3).split(", ")
            valves[valve_name] = (valve_rate, {})
            for t in tunnels:
                valves[valve_name][1][t] = 1
        else:
            print("Found malformed line", line)

# Next, clean up the valve graph. A *lot* of the valves (especially in the full problem) have flow rate 0
# and only two tunnels, so we can remove them from the graph entirely and just increase the cost of moving
# between the two nodes that actually matter.
valve_set = list(valves.keys())
for v in valve_set:
    # since we might have already deleted this one
    if v not in valves:
        continue
    if valves[v][0] == 0 and len(valves[v][1]) == 2:
        valves_to_delete = [v]
        endpoints = []
        total_cost = 2
        for v2 in valves[v][1]:
            while True:
                if not (valves[v2][0] == 0 and len(valves[v2][1]) == 2):
                    endpoints.append(v2)
                    break
                valves_to_delete.append(v2)
                if list(valves[v2][1].keys())[0] in valves_to_delete:
                    v2 = list(valves[v2][1].keys())[1]
                    total_cost += 1
                else:
                    v2 = list(valves[v2][1].keys())[0]
                    total_cost += 1
        for i in range(0, 2):
            v2 = endpoints[i]
            for v3 in list(valves[v2][1].keys()):
                if v3 in valves_to_delete:
                    del valves[v2][1][v3]
            valves[v2][1][endpoints[1-i]] = total_cost
                
        for v2 in valves_to_delete:
            del valves[v2]

        # print("Established new path from", endpoints[0], "to", endpoints[1], "at cost",
        #       total_cost, "removing valves", valves_to_delete)
            
# Elements in the open set are 5-tuples: current location, previous location, current time, current score,
# list of opened valves. We keep track of the previous location so we can reject paths where we go somewhere
# and then immediately go back, since those are obviously bad
open_set = set()
visited_points = set()
open_set.add(('AA', '', 0, 0, ()))
visited_points.add(('AA', 0, 0, ()))
cur_best_score = 0

while True:
    # if we've exhausted all paths, we're done
    if len(open_set) == 0:
        print("Best score is", cur_best_score)
        break

    # Since we don't have a heuristic, we don't really care which element we take
    (cur_loc, prev_loc, cur_t, cur_score, cur_list) = open_set.pop()

    if (cur_t >= max_time - 1):
        # No time left to do anything else, check our score and finish up
        if cur_score > cur_best_score:
            cur_best_score = cur_score
        continue

    # Try opening the valve, if it's useful and we haven't already opened it
    if valves[cur_loc][0] != 0 and cur_loc not in cur_list:
        if cur_score < -1:
            print("Opening valve",cur_loc,"at time",cur_t+1,"For score",valves[cur_loc][0]*(max_time-cur_t-1),
                  "adding to current score",cur_score)
        open_set.add((cur_loc, cur_loc, cur_t+1, cur_score+valves[cur_loc][0]*(max_time-cur_t-1),
                         cur_list + (cur_loc,)))

    # Also, try moving to each of the neighbors
    for n in valves[cur_loc][1]:
        if n != prev_loc and (n, cur_t+1, cur_score, cur_list) not in visited_points:
            open_set.add((n, cur_loc, cur_t+valves[cur_loc][1][n], cur_score, cur_list))
            visited_points.add((n, cur_t+valves[cur_loc][1][n], cur_score, cur_list))
