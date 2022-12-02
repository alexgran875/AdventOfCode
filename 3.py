from aocd import submit
from utils import parse_data, group_data, data_replace, data_to_numpy
from retils import get_between_groups, get_after_group, get_before_group, get_digits
import numpy as np

day = 3
year = 2022

data = parse_data(day, year)
groups = group_data(data)

answer_a = None
answer_b = None
### --- --- --- ###




### --- --- --- ###
submit_a = False
submit_b = False

print("Answer A: {}".format(answer_a))
print("Answer B: {}".format(answer_b))

if submit_a:
    submit(answer_a, part="a", day=day, year=year)
if submit_b:
    submit(answer_b, part="b", day=day, year=year)