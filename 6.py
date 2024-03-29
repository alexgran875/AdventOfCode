from aocd import submit
from utils import parse_data, group_data_by_separator, group_data_by_size, data_replace, data_to_numpy
from retils import get_between_groups, get_after_group, get_before_group, get_digits
import numpy as np
import copy

day = 6
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
last_4 = []
last_14 = []
for i, char in enumerate(lines[0]):
    last_4.append(char)
    last_14.append(char)
    if len(last_4) > 4:
        last_4.pop(0)
    if len(last_14) > 14:
        last_14.pop(0)
    if len(set(last_4)) == 4:
        if (answer_a is None):
            answer_a = i + 1
    if len(set(last_14)) == 14:
        answer_b = i + 1
        break

### --- --- --- ###
submit_a = False
submit_b = False

print("Answer A: {}".format(answer_a))
print("Answer B: {}".format(answer_b))

if submit_a:
    submit(answer_a, part="a", day=day, year=year)
if submit_b:
    submit(answer_b, part="b", day=day, year=year)
