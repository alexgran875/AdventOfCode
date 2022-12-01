from aocd import submit
from utils import parse_data, group_data, data_replace, data_to_numpy
from retils import get_between_groups, get_after_group, get_before_group, get_digits
import numpy as np

day = 5
year = 2020

data = parse_data(day, year)
groups = group_data(data)

answer_a = None
answer_b = None
seats = []
### --- --- --- ###
ids = []
for line in data:
    lower_row = 0
    upper_row = 127
    lower_col = 0
    upper_col = 7
    row_diff = upper_row - lower_row
    col_diff = upper_col - lower_col
    for action in line:
        if action == "F":
            row_diff = row_diff // 2
            upper_row = upper_row - row_diff - 1
        elif action == "B":
            row_diff = row_diff // 2
            lower_row = lower_row + row_diff + 1
        elif action == "L":
            col_diff = col_diff // 2
            upper_col = upper_col - col_diff - 1
        elif action == "R":
            col_diff = col_diff // 2
            lower_col = lower_col + col_diff + 1
    assert lower_row == upper_row
    assert lower_col == upper_col
    ID = lower_row * 8 + lower_col
    ids.append(ID)
    seats.append((lower_row, lower_col))
    x = 5

empty_seats = []
for row in range(128):
    for col in range(8):
        if not (row, col) in seats:
            if row != 0 and row != 127:
                empty_seats.append((row, col))

valid_seats = []
for i, seat in enumerate(empty_seats):
    id = seat[0] * 8 + seat[1]
    if (id - 1) in ids and (id + 1) in ids:
        valid_seats.append(seat)

### --- --- --- ###
answer_a = max(ids)
answer_b = valid_seats[0][0] * 8 + valid_seats[0][1]
submit_a = True
submit_b = True

print("Answer A: {}".format(answer_a))
print("Answer B: {}".format(answer_b))

if submit_a:
    submit(answer_a, part="a", day=day, year=year)
if submit_b:
    submit(answer_b, part="b", day=day, year=year)