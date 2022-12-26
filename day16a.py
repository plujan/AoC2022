#!/usr/bin/env python3

import re

# This uses the same A* algorithm we've used for other puzzles, but without a heuristic function or a way
# to keep track of which paths we can exclude (since even if we're at a node we've explored before, it may
# be with a different time, score, set of valves open). So really it's not A* at all but just straight-up
# brute force. Hope it still works in a reasonable amount of time.
#
# Update: nope! it runs ok on the example, but can't make it through the full problem. So we may need
# a better approach.

large_val = 999999999
max_time = 30

valves = {}

with open("day16.txt") as infile:
    for line in infile:
        result = re.search("Valve (..) has flow rate=(\d+); tunnels? leads? to valves? (.*)", line)
        if result:
            valve_name = result.group(1)
            valve_rate = int(result.group(2))
            tunnels = result.group(3).split(", ")
            valves[valve_name] = (valve_rate, tunnels)
        else:
            print("Found malformed line", line)

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
        if (n, cur_t+1, cur_score, cur_list) not in visited_points:
            open_set.add((n, cur_loc, cur_t+1, cur_score, cur_list))
            visited_points.add((n, cur_t+1, cur_score, cur_list))
