#!/usr/bin/env python3

import re

# An attempt at optimizing our solution for part 2. The idea here is: when we're at a valve and choosing what
# to try next, instead of trying all unopened valves, we go through and reject any valve that is both farther
# away and has a smaller flow rate than another valve in the unopened set. Rather than do this computation
# every time, we calculate a lookup table once (which does require going through all 2^16 combinations of
# unopened valves) at the beginning and then use that.

# The good news is that this reduces the time significantly, to <10 seconds. The bad news is that this
# optimization is too aggressive -- it apparently causes us to miss the best solution. Back to the drawing
# board!

max_time = 26

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
useful_valves = sorted(useful_valves)

# Now, find the shortest path between each pair of valves. We have to do this for all valves, not just
# the useful valves, since we start on a non-useful valve.
valve_distance = {}
for v1 in valves.keys():
    dist = {}
    unvisited = set()
    for v2 in valves.keys():
        dist[v2] = 99999
        unvisited.add(v2)
    # Starting cost of 1 to account for the time of turning the valve so we don't have to add 1 each time
    dist[v1] = 1

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

start_valve = 'AA'

print("Building optimal valve table, one sec...")
optimal_valves = {}
# Now, build a table of optimal connections for each possible set of valves.
for x in range(1, 2**len(useful_valves)):
    # Iterate over all possible combinations of valves remaining. We can skip 0 because there's nothing to do
    # if no valves are left.
    current_valve_set = []
    for i in range(len(useful_valves)):
        if (x >> i) % 2 == 1:
            current_valve_set.append(useful_valves[i])

    # Consider each valve as a possible starting point, unless all valves are closed, in which case we're at
    # the start point
    test_valve_set = list(useful_valves)
    if len(current_valve_set) == len(useful_valves):
        test_valve_set = [start_valve]
    current_valve_key = "".join(current_valve_set)
    
    # Now, iterate over all starting points
    for v1 in test_valve_set:
        if v1 in current_valve_set:
            continue
        # For this starting point and this set of open valves, we want to find valves that are both
        # farther away and have a lower flow rate than another valve in the set, and discard them, in
        # hopes of reducing our possible number of combinations
        result_valves = []
        
        for v2 in current_valve_set:
            save_this_valve = True
            for v3 in current_valve_set:
                if v2 == v3:
                    continue
                if valve_distance[v1][v2] > valve_distance[v1][v3] and valves[v2][0] < valves[v3][0]:
                    save_this_valve = False
                    break
            if save_this_valve:
                result_valves.append(v2)
        # Okay, we're done, save results & move on
        if current_valve_key not in optimal_valves:
            optimal_valves[current_valve_key] = {}
        optimal_valves[current_valve_key][v1] = result_valves
    # print(current_valve_set, optimal_valves[current_valve_key])
    
# Now, let's get to actual solving.
state_pool = []

# Each element of the state pool has the following format:
# - current set of UNOPENED valves
# - time
# - score
# - flow rate
# - next target for us
# - distance to next target for us
# - next target for elephant
# - distance to next target for elephant

# We probably could do something clever to account for the fact that swapping us and the elephant
# results in the same solution, but this seems like a lot of work
for v1 in optimal_valves["".join(useful_valves)][start_valve]:
    for v2 in optimal_valves["".join(useful_valves)][start_valve]:
        if v1 == v2:
            continue
        state_pool.append((set(useful_valves), 0, 0, 0, v1, valve_distance[start_valve][v1],
                           v2, valve_distance[start_valve][v2]))

current_best = 0
n_proc = 0
while len(state_pool) > 0:
    n_proc += 1
    if (n_proc % 100000) == 0:
        print("Processed", n_proc, "states; size of state pool is", len(state_pool))
        if n_proc > 10e6:
            sys.exit(1)
        #print(state_pool)
        #sys.exit(1)
    (cur_valves, cur_t, cur_score, cur_flow, next_target_us, target_distance_us,
     next_target_ele, target_distance_ele) = state_pool.pop()
    
    # The code here gets a little clonky because I can't figure out a way to elegantly handle the case where
    # we arrive at our target at the same time as the elephant, only a clonky way

    old_flow = cur_flow
    if target_distance_us < target_distance_ele:
        cur_t += target_distance_us
        cur_valves.remove(next_target_us)
        cur_score += cur_flow*target_distance_us
        cur_flow += valves[next_target_us][0]
    elif target_distance_ele < target_distance_us:
        cur_t += target_distance_ele
        cur_valves.remove(next_target_ele)
        cur_score += cur_flow*target_distance_ele
        cur_flow += valves[next_target_ele][0]
    else:
        cur_t += target_distance_us
        cur_valves.remove(next_target_us)
        cur_valves.remove(next_target_ele)
        cur_score += cur_flow*target_distance_us
        cur_flow += valves[next_target_us][0]
        cur_flow += valves[next_target_ele][0]

    cur_valves_key = "".join(sorted(cur_valves))
        
    if cur_t >= max_time:
        # We're done, correct our score for the stuff we shouldn't have gotten
        cur_score -= old_flow*(cur_t-max_time)
        if cur_score > current_best:
            current_best = cur_score
    else:
        if len(cur_valves) == 0:
            # We've opened all valves; just increase the score as appropriate and finish up.
            cur_score += cur_flow*(max_time-cur_t)
            if cur_score > current_best:
                current_best = cur_score
        else:
            # Consider all possible next targets for either us, the elephant, or both
            if target_distance_us < target_distance_ele:
                # If there's only one valve left, it's already claimed by the elephant, so just send us to nowhere
                if len(cur_valves) == 1:
                    state_pool.append((set(cur_valves), cur_t, cur_score, cur_flow, start_valve, 999999,
                                       next_target_ele, target_distance_ele-target_distance_us))

                for v in optimal_valves[cur_valves_key][next_target_us]:
                    if v == next_target_ele:
                        continue
                    state_pool.append((set(cur_valves), cur_t, cur_score, cur_flow, v, valve_distance[next_target_us][v],
                                       next_target_ele, target_distance_ele-target_distance_us))
            elif target_distance_ele < target_distance_us:
                if len(cur_valves) == 1:
                    state_pool.append((set(cur_valves), cur_t, cur_score, cur_flow, next_target_us,
                                       target_distance_us-target_distance_ele, start_valve, 999999))
                
                for v in optimal_valves[cur_valves_key][next_target_ele]:
                    if v == next_target_us:
                        continue
                    state_pool.append((set(cur_valves), cur_t, cur_score, cur_flow, next_target_us,
                                       target_distance_us-target_distance_ele, v, valve_distance[next_target_ele][v]))
            else:
                # Here, the corner case is even sneakier -- if there's only one valve left, it won't get claimed at all
                # because of the criterion that we send us and the elephant to different places. So send whoever's closest
                # there and the other person nowhere.
                
                for v1 in optimal_valves[cur_valves_key][next_target_us]:
                    if len(cur_valves) == 1:
                        if valve_distance[next_target_us][v1] <= valve_distance[next_target_ele][v1]:
                            state_pool.append((set(cur_valves), cur_t, cur_score, cur_flow, v1,
                                               valve_distance[next_target_us][v1], start_valve, 999999))
                        else:
                            state_pool.append((set(cur_valves), cur_t, cur_score, cur_flow, start_valve, 999999,
                                               v1, valve_distance[next_target_ele][v1]))

                    for v2 in optimal_valves[cur_valves_key][next_target_ele]:
                        if v1 == v2:
                            continue
                        state_pool.append((set(cur_valves), cur_t, cur_score, cur_flow, v1,
                                           valve_distance[next_target_us][v1], v2, valve_distance[next_target_ele][v2]))
            # case where two are equal
        # pick new targets
    # while state pool nonempty

print("Best score is", current_best)
