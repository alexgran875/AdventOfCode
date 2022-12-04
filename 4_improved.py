from aocd import submit
from utils import parse_data, group_data_by_separator, group_data_by_size, data_replace, data_to_numpy
from retils import get_between_groups, get_after_group, get_before_group, get_digits
import numpy as np

day = 4
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
fully_contained = []
overlap = []
for line in lines:
    digits = get_digits(line, getall = True)
    range1 = set(range(int(digits[0]), int(digits[1]) + 1))
    range2 = set(range(int(digits[2]), int(digits[3]) + 1))

    if range1.issubset(range2) or range2.issubset(range1):
        fully_contained.append(line)

    if range1.intersection(range2) != set():
        overlap.append(line)

answer_a = len(fully_contained)
answer_b = len(overlap)
### --- --- --- ###
submit_a = False
submit_b = False

print("Answer A: {}".format(answer_a))
print("Answer B: {}".format(answer_b))

if submit_a:
    submit(answer_a, part="a", day=day, year=year)
if submit_b:
    submit(answer_b, part="b", day=day, year=year)