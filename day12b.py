#!/usr/bin/env python3

# part 2 -- guess I should have implemented it as a subroutine after all

map = []
big_val = 999999999

with open("day12.txt") as infile:
    for line in infile:
        map.append(line.rstrip())

nrows = len(map)
ncols = len(map[0])

# fix up the map a bit
for i in range(nrows):
    for j in range(ncols):
        if map[i][j] == 'S':
            map[i] = map[i].replace('S', 'a')
        if map[i][j] == 'E':
            end_row = i
            end_col = j
            map[i] = map[i].replace('E', 'z')

# use taxicab metric
def h(row, col):
    return abs(row-end_row) + abs(col-end_col)

def find_astar_path(start_row, start_col):
    open_set = set()
    open_set.add((start_row, start_col))
    gscore = [[big_val for x in range(ncols)] for y in range(nrows)]
    gscore[start_row][start_col] = 0
    fscore = [[big_val for x in range(ncols)] for y in range(nrows)]
    fscore[start_row][start_col] = h(start_row, start_col)

    while True:
        if len(open_set) == 0:
            return big_val # failure -- no route from start to end

        # obviously a little inefficient to go through the whole set each time, but good enough for our
        # purposes
        cur_best_fscore = big_val
        for i in open_set:
            if fscore[i[0]][i[1]] < cur_best_fscore:
                cur_best_fscore = fscore[i[0]][i[1]]
                cur_best_i = i

        cur_row = cur_best_i[0]
        cur_col = cur_best_i[1]
        if cur_row == end_row and cur_col == end_col:
            return gscore[end_row][end_col]

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

cur_best_path = big_val
for i in range(nrows):
    for j in range(ncols):
        if map[i][j] == 'a':
            cur_dist = find_astar_path(i, j)
            if cur_dist < cur_best_path:
                cur_best_path = cur_dist

print("Overall best path is", cur_best_path)
