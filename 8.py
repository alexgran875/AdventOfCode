from aocd import submit
from utils import parse_data, group_data_by_separator, group_data_by_size, data_replace, data_to_numpy
from retils import get_between_groups, get_after_group, get_before_group, get_digits
import numpy as np
import copy
import functools

day = 8
year = 2022

read_online = True
if read_online:
    lines = parse_data(day, year)
else:
    lines = parse_data()
groups = group_data_by_separator(lines)

answer_a = None
answer_b = None
### --- --- --- ###
np_matrix = data_to_numpy(lines)
n_visible_trees = 0
max_scenic_score = 0
for currentRowIndex in range(1, np.shape(np_matrix)[0] - 1):
    for currentColIndex in range(1, np.shape(np_matrix)[1] - 1):
        leftTrees = np_matrix[currentRowIndex, :currentColIndex]
        rightTrees = np_matrix[currentRowIndex, currentColIndex+1:]
        aboveTrees = np_matrix[:currentRowIndex, currentColIndex]
        belowTrees = np_matrix[currentRowIndex+1:, currentColIndex]
        leftMax = np.max(leftTrees)
        rightMax = np.max(rightTrees)
        aboveMax = np.max(aboveTrees)
        belowMax = np.max(belowTrees)

        height = np_matrix[currentRowIndex, currentColIndex]
        if height > leftMax or height > rightMax or height > aboveMax or height > belowMax:
            n_visible_trees += 1

        n_vis_left = 0
        for treeHeight in leftTrees[::-1]:
            n_vis_left += 1
            if treeHeight >= height:
                break

        n_vis_right = 0
        for treeHeight in rightTrees:
            n_vis_right += 1
            if treeHeight >= height:
                break

        n_vis_above = 0
        for treeHeight in aboveTrees[::-1]:
            n_vis_above += 1
            if treeHeight >= height:
                break

        n_vis_below = 0
        for treeHeight in belowTrees:
            n_vis_below += 1
            if treeHeight >= height:
                break

        scenic_score = n_vis_left * n_vis_right * n_vis_above * n_vis_below
        if scenic_score > max_scenic_score:
            max_scenic_score = scenic_score

n_rows = np.shape(np_matrix)[0]
n_cols = np.shape(np_matrix)[1]
n_edge_trees = 2*n_rows + 2*n_cols - 4
answer_a = n_visible_trees + n_edge_trees
answer_b = max_scenic_score

### --- --- --- ###
submit_a = False
submit_b = False

print("Answer A: {}".format(answer_a))
print("Answer B: {}".format(answer_b))

if submit_a:
    submit(answer_a, part="a", day=day, year=year)
if submit_b:
    submit(answer_b, part="b", day=day, year=year)
