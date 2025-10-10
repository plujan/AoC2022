#!/usr/bin/python3

# This uses the same approach as part 1, since we can finish in a reasonable time even when going up to 32
# minutes. This just changes the number of blueprints read and the formula for calculating the result.

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
        # Consider only the first three blueprints.
        if len(blueprints) == 3:
            break

print("Read in", len(blueprints), "blueprints")
best_product = 1
max_time = 32
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

    # There's no point in building more ore robots than the maximum ore cost of any individual robot, since we can only ever
    # build one robot per turn.
    max_ore = max(b["ore"], b["clay"], b["obsidian"][0], b["geode"][0])
    # Similarly no point in building more clay robots than the clay cost of an obsidian robot.
    max_clay = b["obsidian"][1]
    # Could do the same for the obsidian robots but I doubt we'll ever get there anyway.
    
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
        if cur_state[0] == max_time:
            if cur_state[4] > cur_best_outcome:
                print("Best so far for blueprint", b["id"], "is", cur_state[4], "geode"+("" if cur_state[4]==1 else "s"))
                cur_best_outcome = cur_state[4]
        else:
            # Otherwise, build robot if we did, and if so choose a new target
            if build_item > 0:
                cur_state[build_item] += 1

                # don't build an ore if we already have the maximum number of ore robots we could ever need
                if cur_state[5] < max_ore:
                    state_pool.append((list(cur_state), 0))

                # similarly, don't build a clay if we already have the maximum number of clay robots we could ever need
                if cur_state[6] < max_clay:
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
    best_product *= cur_best_outcome

print("Overall product is", best_product)
