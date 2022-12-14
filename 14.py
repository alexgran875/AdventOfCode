from aocd import submit
from utils import parse_data, group_data_by_separator, group_data_by_size, data_replace, data_to_numpy
from retils import get_between_groups, get_after_group, get_before_group, get_digits
import numpy as np
import copy
import functools

day = 14
year = 2022

read_online = True
if read_online:
    input_lines = parse_data(day, year)
else:
    input_lines = parse_data()
groups = group_data_by_separator(input_lines)

answer_a = None
answer_b = None
### --- --- --- ###

# parsing
lines = []
x_range = None
y_range = None
for i in input_lines:
    line = i.split(" -> ")
    line = list(map(lambda l: l.split(","), line))
    line = list(map(lambda l: list(map(int, l)), line))
    lines.append(line)
    for j in line:
        x = j[0]
        y = j[1]
        if x_range is None:
            x_range = [x, x]
        elif x > x_range[1]:
            x_range[1] = x
        elif x < x_range[0]:
            x_range[0] = x

        if y_range is None:
            y_range = [y, y]
        elif y > y_range[1]:
            y_range[1] = y
        elif y < y_range[0]:
            y_range[0] = y

# draw lines
cavern_a = np.zeros((y_range[1] - y_range[0] + 1, x_range[1] - x_range[0] + 1))
for line in lines:
    for point_idx in range(len(line)-1):
        col_idx_start = line[point_idx][0] - x_range[0]
        row_idx_start = line[point_idx][1] - y_range[0]
        col_idx_end = line[point_idx+1][0] - x_range[0]
        row_idx_end = line[point_idx+1][1] - y_range[0]
        cavern_a[
            min(row_idx_start, row_idx_end):max(row_idx_start, row_idx_end)+1,
            min(col_idx_start, col_idx_end):max(col_idx_start, col_idx_end)+1
        ] = 1

# rows above up to the sand source
cavern_a = np.vstack((np.zeros((y_range[0], cavern_a.shape[1])), cavern_a))
# 2 extra rows below for the floor
cavern_b = np.vstack((cavern_a, np.zeros((2, cavern_a.shape[1]))))
required_n_cols = cavern_b.shape[0] - 1
cavern_b = np.hstack(
    (np.zeros((cavern_b.shape[0], required_n_cols)), cavern_b))
cavern_b = np.hstack(
    (cavern_b, np.zeros((cavern_b.shape[0], required_n_cols))))
cavern_b[-1, :] = 1


def fall_sand(cavern, sand_start, sand_mark):
    n_rows, n_cols = cavern.shape
    current_pos = sand_start
    off_edge = False
    while True:
        moved = False
        for rowOffset, colOffset in [(1, 0), (1, -1), (1, 1)]:
            # row edge
            neighbourRowIndex = current_pos[0] + rowOffset
            if neighbourRowIndex < 0 or neighbourRowIndex >= n_rows:
                off_edge = True
                break

            # col edge
            neighbourColIndex = current_pos[1] + colOffset
            if neighbourColIndex < 0 or neighbourColIndex >= n_cols:
                off_edge = True
                break

            neighbourPos = (neighbourRowIndex, neighbourColIndex)
            neighbourValue = cavern[neighbourPos]
            if neighbourValue == 0:
                current_pos = neighbourPos
                moved = True
                break

        # done falling sand 1 step
        if not moved:
            break

    # sand is at rest or off edge
    cavern[current_pos] = sand_mark
    if current_pos == sand_start:
        return True
    else:
        return off_edge


answer_a = 0
answer_b = 0
sand_start_a = 500-x_range[0]
sand_start_b = sand_start_a + required_n_cols
sand_mark = 2
while not fall_sand(cavern_a, (0, sand_start_a), sand_mark):
    answer_a += 1
while not fall_sand(cavern_b, (0, sand_start_b), sand_mark):
    answer_b += 1
answer_b += 1

### --- --- --- ###
submit_a = False
submit_b = False

print("Answer A: {}".format(answer_a))
print("Answer B: {}".format(answer_b))

if submit_a:
    submit(answer_a, part="a", day=day, year=year)
if submit_b:
    submit(answer_b, part="b", day=day, year=year)
