from aocd import submit
from utils import parse_data, group_data_by_separator, group_data_by_size, data_replace, data_to_numpy
from retils import get_between_groups, get_after_group, get_before_group, get_digits
import numpy as np
import copy
import functools

day = 20
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
part_a = True
if part_a:
    n_mixes = 1
    multiplier = 1
else:
    n_mixes = 10
    multiplier = 811589153

lines = list(map(lambda l: int(l)*multiplier, lines))
rearranged = [(i, val) for i, val in enumerate(lines)]
n_elements = len(lines)

for _ in range(n_mixes):
    for originalPos in range(n_elements):
        for currentPos, (pos, value) in enumerate(rearranged):
            if pos == originalPos:
                break

        if value == 0:
            continue

        rearranged.pop(currentPos)
        newPos = (currentPos + value) % len(rearranged)
        rearranged.insert(newPos, (pos, value))

for i, (originalPos, value) in enumerate(rearranged):
    if value == 0:
        pos1 = (i + 1000) % len(rearranged)
        pos2 = (i + 2000) % len(rearranged)
        pos3 = (i + 3000) % len(rearranged)
        answer_a = (rearranged[pos1][1] +
                    rearranged[pos2][1] + rearranged[pos3][1])
### --- --- --- ###
submit_a = False
submit_b = False

print("Answer A: {}".format(answer_a))
print("Answer B: {}".format(answer_b))

if submit_a:
    submit(answer_a, part="a", day=day, year=year)
if submit_b:
    submit(answer_b, part="b", day=day, year=year)
