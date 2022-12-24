#!/usr/bin/env python3

# I'm doing this the VERY lazy way, just copy and paste three times, and also assuming that the best path to
# do all three steps is equal to the best path for each subpart, otherwise we're really screwed

# Three-dimensional map: first is time, then coordinates. Also each element of the map is itself a list, to
# account for multiple blizzards being in a single space.
map = [[]]

large_val = 999999999

with open("day24.txt") as infile:
    for line in infile:
        map[0].append([list(x) for x in line.rstrip()])

nrows = len(map[0])
ncols = len(map[0][0])

start_row = 0
start_col = map[0][start_row].index(['.'])
end_row = nrows-1
end_col = map[0][end_row].index(['.'])

# Now change all of the dots to empty arrays, since that's easier to use.
for y in range(nrows):
    for x in range(ncols):
        if map[0][y][x] == ['.']:
            map[0][y][x] = []

def print_map(t):
    for y in range(nrows):
        for x in range(ncols):
            if y == cur_row and x == cur_col:
                print('E', end='')
            elif len(map[t][y][x]) == 0:
                print('.', end='')
            elif len(map[t][y][x]) == 1:
                print(map[t][y][x][0], end='')
            else:
                print(len(map[t][y][x]), end='')
        print()

def simulate_next_time():
    t = len(map)-1
    map.append([[[] for x in range(ncols)] for y in range(nrows)])
    for y in range(nrows):
        for x in range(ncols):
            for b in map[t][y][x]:
                if b == '<':
                    if x == 1:
                        map[t+1][y][ncols-2].append('<')
                    else:
                        map[t+1][y][x-1].append('<')
                elif b == '>':
                    if x == ncols-2:
                        map[t+1][y][1].append('>')
                    else:
                        map[t+1][y][x+1].append('>')
                elif b == '^':
                    if y == 1:
                        map[t+1][nrows-2][x].append('^')
                    else:
                        map[t+1][y-1][x].append('^')
                elif b == 'v':
                    if y == nrows-2:
                        map[t+1][1][x].append('v')
                    else:
                        map[t+1][y+1][x].append('v')
                elif b == '#':
                    map[t+1][y][x].append('#')

# use taxicab metric
def h(row, col):
    return abs(row-end_row) + abs(col-end_col)

def do_astar():
    cur_best_time = large_val
    while True:
        # if we've exhausted all paths, we're done
        if len(open_set) == 0:
            return cur_best_time

        cur_best_fscore = large_val
        for i in open_set:
            if i[3] < cur_best_fscore:
                cur_best_fscore = i[3]
                cur_best_i = i

        (cur_t, cur_row, cur_col, cur_gscore) = cur_best_i
        open_set.remove(cur_best_i)

        if cur_row == end_row and cur_col == end_col:
            # Hooray, we found a solution, we can stop here
            cur_best_time = cur_t
            continue

        # We're already worse than our best, don't explore this path further
        if cur_t >= cur_best_time:
            continue

        # If we don't know what the board will look like in 1 minute, simulate that
        if cur_t == len(map)-1:
            simulate_next_time()

        for x in [(0, 0), (0, 1), (0, -1), (1, 0), (-1, 0)]:
            new_row = cur_row + x[0]
            new_col = cur_col + x[1]
            if (new_row >= 0 and new_row < nrows and len(map[cur_t+1][new_row][new_col]) == 0 and
                (cur_t+1, new_row, new_col) not in explored_points):

                open_set.add((cur_t+1, new_row, new_col, cur_t+1+h(new_row, new_col)))
                explored_points.add((cur_t+1, new_row, new_col))

# First verse
open_set = set()
open_set.add((0, start_row, start_col, h(start_row, start_col)))
explored_points = set()
cur_best_time = do_astar()
                
# Second verse, almost the same as the first
open_set = set()
open_set.add((cur_best_time, end_row, end_col, h(end_row, end_col)))
old_end_row = end_row
old_end_col = end_col
end_row = start_row
end_col = start_col
explored_points = set()
cur_best_time = do_astar()

# Third verse, you know the drill
open_set = set()
open_set.add((cur_best_time, start_row, start_col, h(start_row, start_col)))
end_row = old_end_row
end_col = old_end_col
explored_points = set()
cur_best_time = do_astar()

print("Best time for all the trips is", cur_best_time)
