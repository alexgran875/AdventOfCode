from aocd import submit
from utils import parse_data, group_data_by_separator, group_data_by_size, data_replace, data_to_numpy
from retils import get_between_groups, get_after_group, get_before_group, get_digits
import numpy as np
import copy
import functools

day = 9
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


def get_dir_vec(step_dir):
    if step_dir == "D":
        return (0, -1)
    elif step_dir == "U":
        return (0, 1)
    elif step_dir == "R":
        return (1, 0)
    elif step_dir == "L":
        return (-1, 0)


def simulate_tail(lines, n_knots):
    knots = [np.array([0, 0]) for _ in range(n_knots)]
    t_visited = set()
    for line in lines:
        h_dir_vec = np.array(get_dir_vec(line[0]))
        n_steps = int(get_digits(line))
        for _ in range(n_steps):
            knots[0] += h_dir_vec
            for i in range(1, len(knots)):
                distance = np.linalg.norm(knots[i-1] - knots[i])
                if distance >= 2.0:
                    knot_dir_vec = knots[i-1] - knots[i]
                    knot_dir_vec[knot_dir_vec > 1] = 1
                    knot_dir_vec[knot_dir_vec < -1] = -1
                    knots[i] += knot_dir_vec
                if i == n_knots - 1:  # tail
                    t_visited.add((knots[i][0], knots[i][1]))
    return t_visited


answer_a = len(simulate_tail(lines, 2))
answer_b = len(simulate_tail(lines, 10))
### --- --- --- ###
submit_a = False
submit_b = False

print("Answer A: {}".format(answer_a))
print("Answer B: {}".format(answer_b))

if submit_a:
    submit(answer_a, part="a", day=day, year=year)
if submit_b:
    submit(answer_b, part="b", day=day, year=year)
