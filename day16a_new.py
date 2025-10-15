#!/usr/bin/env python3

import re

# This uses a very different approach to my initial attempt at this problem. What we do is:
# 1) Focus only on the valves which actually are useful to open
# 2) Use Dijkstra's algorithm to determine the shortest paths between each pair of valves in this set
# 3) Each time we need to make a decision, add the set of all other valves that we haven't opened yet
#
# This results in a much larger number of choices at each decision point, but many fewer choices
# total, so hopefully it will be a net gain. Let's find out! The goal with this method is to build a
# working solution to part 2, but I want to see if it works on part 1 first.
#
# Result: much faster than the old way!

max_time = 30

valves = {}
useful_valves = []

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
            if valve_rate > 0:
                useful_valves.append(valve_name)
        else:
            print("Found malformed line", line)


# Now, find the shortest path between each pair of valves. We have to do this for all valves, not just
# the useful valves, since we start on a non-useful valve.
valve_distance = {}
for v1 in valves.keys():
    dist = {}
    unvisited = set()
    for v2 in valves.keys():
        dist[v2] = 99999
        unvisited.add(v2)
    dist[v1] = 0

    while len(unvisited) > 0:
        # Find the current member of the unvisited set with the lowest distance.
        cur_min = 999
        cur_node = None
        for v2 in unvisited:
            if dist[v2] < cur_min:
                cur_node = v2
                cur_min = dist[v2]

        # Explore all the connections of this node. If the distance from cur_node + 1 is less than the
        # current best distance to that node, then update the best distance. (+1 because all tunnels in
        # this problem have a value of 1)
        for conn in valves[cur_node][1]:
            new_dist = dist[cur_node] + 1
            if new_dist < dist[conn]:
                dist[conn] = new_dist

        unvisited.remove(cur_node)
    valve_distance[v1] = dist

# print(valve_distance)

# Now, let's get to actual solving.
state_pool = []
start_valve = 'AA'

# Each element of the state pool has the following format:
# - current set of UNOPENED valves
# - time
# - score
# - flow rate
# - next target
# - distance to next target

for v in useful_valves:
    state_pool.append((set(useful_valves), 0, 0, 0, v, valve_distance[start_valve][v]+1))

current_best = 0
while len(state_pool) > 0:
    (cur_valves, cur_t, cur_score, cur_flow, next_target, target_distance) = state_pool.pop()

    cur_t += target_distance
    cur_valves.remove(next_target)
    cur_score += cur_flow*target_distance

    if cur_t >= max_time:
        # We're done, correct our score for the stuff we shouldn't have gotten
        cur_score -= cur_flow*(cur_t-max_time)
        if cur_score > current_best:
            current_best = cur_score
    else:
        cur_flow += valves[next_target][0]
        if len(cur_valves) == 0:
            # We've opened all valves; just increase the score as appropriate and finish up
            cur_score += cur_flow*(max_time-cur_t)
            if cur_score > current_best:
                current_best = cur_score
        else:
            # Consider all possible next targets
            for v in cur_valves:
                # We need the +1 to account for the time to open the valve when we get there
                state_pool.append((set(cur_valves), cur_t, cur_score, cur_flow, v, valve_distance[next_target][v]+1))

print("Best score is", current_best)
