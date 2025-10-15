#!/usr/bin/env python3

import re

# A first attempt at porting the solution we used for part 1 to part 2. This basically uses the same
# technique but with branches for both our choice and the elephant's choice. Not surprisingly, it's
# way too slow to be able to solve the full problem.

max_time = 26

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

n_useful_valves = 0
for v in valves:
    if valves[v][0] > 0:
        n_useful_valves += 1
        
# Elements in the open set are 8-tuples: your current location, previous location, and time; elephant's
# current location, previous location, and time; current score; and list of opened valves. We keep track of
# the previous location so we can reject paths where we go somewhere and then immediately go back, since those
# are obviously bad. Also, since we've changed the graph around, you may be able to move while the elephant is
# still moving, so we have to track the times separately. This is kind of a pain but I hope it's still better
# than leaving the graph with 4x as many nodes.

open_set = set()
visited_points = set()
open_set.add(('AA', '', 0, 'AA', '', 0, 0, ()))
visited_points.add(('AA', 'AA', 0, 0, 0, ()))
cur_best_score = 0

while True:
    # if we've exhausted all paths, we're done
    if len(open_set) == 0:
        print("Best score is", cur_best_score)
        break

    # Since we don't have a heuristic, we don't really care which element we take
    (you_loc, you_prev, you_t, ele_loc, ele_prev, ele_t, cur_score, cur_list) = open_set.pop()

    if (min(you_t, ele_t) >= max_time - 1) or len(cur_list) == n_useful_valves:
        # Either we're out of time, or we've opened all (useful) valves, so check our score and finish
        if cur_score > cur_best_score:
            cur_best_score = cur_score
        continue
    
    # Now, one of us or the elephant might still be moving, in which case we only need to consider
    # moving the other one. Of course we might need both

    if (you_t < ele_t):
        # Try opening the valve, if it's useful and we haven't already opened it
        if valves[you_loc][0] != 0 and you_loc not in cur_list:
            open_set.add((you_loc, you_loc, you_t+1, ele_loc, ele_prev, ele_t,
                          cur_score+valves[you_loc][0]*(max_time-you_t-1),
                          cur_list + (you_loc,)))

        # Also, try moving to each of the neighbors
        for n in valves[you_loc][1]:
            if n != you_prev and (n, ele_loc, you_t+1, ele_t, cur_score, cur_list) not in visited_points:
                open_set.add((n, you_loc, you_t+valves[you_loc][1][n],
                              ele_loc, ele_prev, ele_t, cur_score, cur_list))
                visited_points.add((n, ele_loc, you_t+valves[you_loc][1][n],
                                    ele_t, cur_score, cur_list))

    elif (ele_t < you_t):
        # Same deal with the elephant
        if valves[ele_loc][0] != 0 and ele_loc not in cur_list:
            open_set.add((you_loc, you_prev, you_t, ele_loc, ele_loc, ele_t+1,
                          cur_score+valves[ele_loc][0]*(max_time-ele_t-1),
                          cur_list+(ele_loc,)))
        for n in valves[ele_loc][1]:
            if n != ele_prev and (you_loc, n, you_t, ele_t+1, cur_score, cur_list) not in visited_points:
                open_set.add((you_loc, you_prev, you_t,
                              n, ele_loc, ele_t+valves[ele_loc][1][n],
                              cur_score, cur_list))
                visited_points.add((you_loc, n, you_t, ele_t+valves[ele_loc][1][n],
                                    cur_score, cur_list))

    elif (you_t == ele_t):
        # ugh
        for ny in [you_loc]+list(valves[you_loc][1]):
            if ny == you_loc:
                if not (valves[you_loc][0] != 0 and you_loc not in cur_list):
                    continue
                new_score = cur_score+valves[you_loc][0]*(max_time-you_t-1)
                new_list = cur_list+(you_loc,)
                new_you_t = you_t+1
                new_you_loc = you_loc
                new_you_prev = you_loc
            else:
                if ny == you_prev:
                    continue
                new_score = cur_score
                new_list = cur_list
                new_you_t = you_t+valves[you_loc][1][ny]
                new_you_loc = ny
                new_you_prev = you_loc
            
            for ne in [ele_loc]+list(valves[ele_loc][1]):
                if ne == ele_loc:
                    if not (valves[ele_loc][0] != 0 and ele_loc not in new_list):
                        continue
                    open_set.add((new_you_loc, new_you_prev, new_you_t,
                                  ele_loc, ele_loc, ele_t+1,
                                  new_score+valves[ele_loc][0]*(max_time-ele_t-1),
                                  new_list+(ele_loc,)))
                elif ne != ele_prev and (new_you_loc, ne, new_you_t, ele_t+valves[ele_loc][1][ne],
                                         new_score, new_list) not in visited_points:
                    open_set.add((new_you_loc, new_you_prev, new_you_t,
                                  ne, ele_loc, ele_t+valves[ele_loc][1][ne],
                                  new_score, new_list))
                    visited_points.add((new_you_loc, ne, new_you_t, ele_t+valves[ele_loc][1][ne],
                                        new_score, new_list))

    
