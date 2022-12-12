#!/usr/bin/env python3

# This required some reading up on the A* algorithm -- and by reading up I mean implementing the sample
# pseudocode in Wikipedia. Since we only care about the length of the path and not the actual path itself, we
# can skip keeping track of the path, however.

map = []

with open("day12.txt") as infile:
    for line in infile:
        map.append(line.rstrip())

nrows = len(map)
ncols = len(map[0])

# fix up the map a bit
for i in range(nrows):
    for j in range(ncols):
        if map[i][j] == 'S':
            start_row = i
            start_col = j
            map[i] = map[i].replace('S', 'a')
        if map[i][j] == 'E':
            end_row = i
            end_col = j
            map[i] = map[i].replace('E', 'z')

# use taxicab metric
def h(row, col):
    return abs(row-end_row) + abs(col-end_col)
            
open_set = set()
open_set.add((start_row, start_col))
gscore = [[99999999 for x in range(ncols)] for y in range(nrows)]
gscore[start_row][start_col] = 0
fscore = [[99999999 for x in range(ncols)] for y in range(nrows)]
fscore[start_row][start_col] = h(start_row, start_col)

while True:
    cur_best_fscore = 99999999
    for i in open_set:
        if fscore[i[0]][i[1]] < cur_best_fscore:
            cur_best_fscore = fscore[i[0]][i[1]]
            cur_best_i = i

    cur_row = cur_best_i[0]
    cur_col = cur_best_i[1]
    if cur_row == end_row and cur_col == end_col:
        print("Best solution is", gscore[end_row][end_col])
        break

    open_set.remove(cur_best_i)

    for x in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        new_row = cur_row + x[0]
        new_col = cur_col + x[1]
        if (new_row >= 0 and new_row < nrows and new_col >= 0 and new_col < ncols
            and ord(map[cur_row][cur_col]) - ord(map[new_row][new_col]) >= -1):
            new_gscore = gscore[cur_row][cur_col] + 1
            if new_gscore < gscore[new_row][new_col]:
                gscore[new_row][new_col] = new_gscore
                fscore[new_row][new_col] = new_gscore + h(new_row, new_col)
                open_set.add((new_row, new_col))
