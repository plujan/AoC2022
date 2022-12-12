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

def scan_line(start_row, start_col, row_inc, col_inc):
    global visibility
    cur_max_height = -1
    cur_row = start_row
    cur_col = start_col
    while (cur_row >= 0 and cur_row < nrows and cur_col >= 0 and cur_col < ncols):
        cur_height = int(tree_data[cur_row][cur_col])
        if cur_height > cur_max_height:
            visibility[cur_row][cur_col] = True
            cur_max_height = cur_height
        cur_row += row_inc
        cur_col += col_inc
    
for i in range(nrows):
    scan_line(i, 0, 0, 1)
    scan_line(i, ncols-1, 0, -1)
for i in range(ncols):
    scan_line(0, i, 1, 0)
    scan_line(nrows-1, i, -1, 0)

tot_vis = 0
for i in range(nrows):
    for j in range(ncols):
        if visibility[i][j]:
            tot_vis += 1

print("Total number of trees visible:", tot_vis)
