#!/usr/bin/env python3

tree_data = []
with open("day8.txt") as infile:
    for line in infile:
        tree_data.append(line.rstrip())

nrows = len(tree_data)
ncols = len(tree_data[0])

visibility = []
for i in range(nrows):
    visibility.append([False] * ncols)

def find_visibility(start_row, start_col, row_inc, col_inc):
    trees_visible = 0
    my_height = int(tree_data[start_row][start_col])
    cur_row = start_row + row_inc
    cur_col = start_col + col_inc
    while (cur_row >= 0 and cur_row < nrows and cur_col >= 0 and cur_col < ncols):
        trees_visible += 1
        cur_height = int(tree_data[cur_row][cur_col])
        if cur_height >= my_height:
            break
        cur_row += row_inc
        cur_col += col_inc
    return trees_visible

max_scenic_score = 0
for i in range(nrows):
    for j in range(ncols):
        scenic_score = (find_visibility(i, j, 0, 1) * find_visibility(i, j, 0, -1) *
                        find_visibility(i, j, 1, 0) * find_visibility(i, j, -1, 0))
        if scenic_score > max_scenic_score:
            max_scenic_score = scenic_score

print("Maximum scenic score: ", max_scenic_score)
