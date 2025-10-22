#!/usr/bin/env python3

import re

# This is a port of the "new" solution for part 1 to part 2. It uses basically the same method,
# but with moving both you and the elephant.
#
# I tried optimizing it, but it didn't work out, so I did some math and realized that with the small
# optimization of not duplicating solutions that are the same except for swapping us and the elephant, we can
# actually run in about 1.5hr, which is not great, but feasible. And fortunately we did get the right answer
# the first time!

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

# Now, let's get to actual solving.
state_pool = []
start_valve = 'AA'

# Each element of the state pool has the following format:
# - current set of UNOPENED valves
# - time
# - score
# - flow rate
# - next target for us
# - distance to next target for us
# - next target for elephant
# - distance to next target for elephant

# Since swapping us ant the elephant results in the same solution, we can divide the number of start states in
# half
for i1 in range(len(useful_valves)):
    for i2 in range(i1+1, len(useful_valves)):
        state_pool.append((set(useful_valves), 0, 0, 0, useful_valves[i1], valve_distance[start_valve][useful_valves[i1]],
                           useful_valves[i2], valve_distance[start_valve][useful_valves[i2]]))

current_best = 0
n_proc = 0
while len(state_pool) > 0:
    n_proc += 1
    if (n_proc % 1e6) == 0:
        print("Processed %0e states; size of state pool is %d" % (n_proc, len(state_pool)))

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
        
    if cur_t >= max_time:
        # We're done, correct our score for the stuff we shouldn't have gotten
        cur_score -= old_flow*(cur_t-max_time)
        if cur_score > current_best:
            current_best = cur_score
    else:
        if len(cur_valves) == 0:
            # We've opened all valves; just increase the score as appropriate and finish up. This is a little
            # more complicated because if we've finished for one mover but not the other, we need to account
            # for their last move too.
            cur_score += cur_flow*(max_time-cur_t)
            if target_distance_us < target_distance_ele:
                extra_t = cur_t + (target_distance_ele-target_distance_us)
                if extra_t < max_time:
                    cur_score += valves[next_target_ele][0]*(max_time-extra_t)
            elif target_distance_ele < target_distance_us:
                extra_t = cur_t + (target_distance_us-target_distance_ele)
                if extra_t < max_time:
                    cur_score += valves[next_target_us][0]*(max_time-extra_t)
            # Fortunately we don't have to deal with the case where they both finish at the same time, since
            # in that case everyone is accounted for.
            
            if cur_score > current_best:
                current_best = cur_score
        else:
            # Consider all possible next targets for either us, the elephant, or both
            if target_distance_us < target_distance_ele:
                # If there's only one valve left, it's already claimed by the elephant, so just send us to nowhere
                if len(cur_valves) == 1:
                    state_pool.append((set(cur_valves), cur_t, cur_score, cur_flow, start_valve, 999999,
                                       next_target_ele, target_distance_ele-target_distance_us))
                
                for v in cur_valves:
                    if v == next_target_ele:
                        continue
                    state_pool.append((set(cur_valves), cur_t, cur_score, cur_flow, v, valve_distance[next_target_us][v],
                                       next_target_ele, target_distance_ele-target_distance_us))
            elif target_distance_ele < target_distance_us:
                if len(cur_valves) == 1:
                    state_pool.append((set(cur_valves), cur_t, cur_score, cur_flow, next_target_us,
                                       target_distance_us-target_distance_ele, start_valve, 999999))
                
                for v in cur_valves:
                    if v == next_target_us:
                        continue
                    state_pool.append((set(cur_valves), cur_t, cur_score, cur_flow, next_target_us,
                                       target_distance_us-target_distance_ele, v, valve_distance[next_target_ele][v]))
            else:
                # Here, the corner case is even sneakier -- if there's only one valve left, it won't get claimed at all
                # because of the criterion that we send us and the elephant to different places. So send whoever's closest
                # there and the other person nowhere.
                
                for v1 in cur_valves:
                    if len(cur_valves) == 1:
                        if valve_distance[next_target_us][v1] <= valve_distance[next_target_ele][v1]:
                            state_pool.append((set(cur_valves), cur_t, cur_score, cur_flow, v1,
                                               valve_distance[next_target_us][v1], start_valve, 999999))
                        else:
                            state_pool.append((set(cur_valves), cur_t, cur_score, cur_flow, start_valve, 999999,
                                               v1, valve_distance[next_target_ele][v1]))

                    for v2 in cur_valves:
                        if v1 == v2:
                            continue
                        state_pool.append((set(cur_valves), cur_t, cur_score, cur_flow, v1,
                                           valve_distance[next_target_us][v1], v2, valve_distance[next_target_ele][v2]))
            # case where two are equal
        # pick new targets
    # while state pool nonempty

print("Best score is", current_best)
