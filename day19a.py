#!/usr/bin/python3

# This uses a rather brute-force approach where, each time we build a robot, we consider all possible options
# for what to build next (ore and clay always, obsidian if and only if we have clay, geode if and only if we
# have obsidian). It runs pretty slowly but it does work.

import re

blueprints = []

# Open and read the blueprint file.

with open("day19.txt") as infile:
    for line in infile:
        result = re.search("Blueprint (\d+): Each ore robot costs (\d+) ore. Each clay robot costs (\d+) ore. Each obsidian robot costs (\d+) ore and (\d+) clay. Each geode robot costs (\d+) ore and (\d+) obsidian.", line)
        if result:
            this_blueprint = {"id": int(result.group(1)),
                              "ore": int(result.group(2)),
                              "clay": int(result.group(3)),
                              "obsidian": [int(result.group(4)), int(result.group(5))],
                              "geode": [int(result.group(6)), int(result.group(7))]}
            blueprints.append(this_blueprint)
        else:
            print("Failed to parse blueprint line")

print("Read in", len(blueprints), "blueprints")
quality_number = 0
for b in blueprints:
    # Run the simulation.

    # Number of minutes elapsed, then
    # number of ore/clay/obsidian/geode, then
    # number of ore/clay/obsidian/geode robots
    start_state = [0, 0, 0, 0, 0, 1, 0, 0, 0]

    cur_best_outcome = 0

    state_pool = []
    
    state_pool.append((list(start_state), 0)) # build ore robot first
    state_pool.append((list(start_state), 1)) # build clay robot first
                      
    while state_pool:
        (cur_state, next_target) = state_pool.pop()

        cur_state[0] += 1

        # Check to see if we can produce something.

        build_item = 0
        if next_target == 0 and cur_state[1] >= b["ore"]:
            cur_state[1] -= b["ore"]
            build_item = 5
        elif next_target == 1 and cur_state[1] >= b["clay"]:
            cur_state[1] -= b["clay"]
            build_item = 6
        elif next_target == 2 and cur_state[1] >= b["obsidian"][0] and cur_state[2] >= b["obsidian"][1]:
            cur_state[1] -= b["obsidian"][0]
            cur_state[2] -= b["obsidian"][1]
            build_item = 7
        elif next_target == 3 and cur_state[1] >= b["geode"][0] and cur_state[3] >= b["geode"][1]:
            cur_state[1] -= b["geode"][0]
            cur_state[3] -= b["geode"][1]
            build_item = 8

        # Robots create items; check for done.

        for i in [1, 2, 3, 4]:
            cur_state[i] += cur_state[i+4]
        if cur_state[0] == 24:
            if cur_state[4] > cur_best_outcome:
                print("Best so far for blueprint", b["id"], "is", cur_state[4], "geodes")
                cur_best_outcome = cur_state[4]
        else:
            # Otherwise, build robot if we did, and if so choose a new target
            if build_item > 0:
                cur_state[build_item] += 1
                state_pool.append((list(cur_state), 0))
                state_pool.append((list(cur_state), 1))
                # can only target an obsidian robot if we are making clay
                if cur_state[6] > 0:
                    state_pool.append((list(cur_state), 2))
                # similarly, can only target a geode robot if we are making obsidian
                if cur_state[7] > 0:
                    state_pool.append((list(cur_state), 3))
            # Just continue working on what we were working on
            else:
                state_pool.append((list(cur_state), next_target))

    # Done! Increase the quality number
    print("Finished blueprint", b["id"], "with best of", cur_best_outcome)
    quality_number += b["id"]*cur_best_outcome

print("Overall quality level is", quality_number)
