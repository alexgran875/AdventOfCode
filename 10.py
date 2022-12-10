from aocd import submit
from utils import parse_data, group_data_by_separator, group_data_by_size, data_replace, data_to_numpy
from retils import get_between_groups, get_after_group, get_before_group, get_digits
import numpy as np
import copy
import functools

day = 10
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
x = 1
n_cycle = 1
observe_cycles = [i for i in range(20, 221, 40)]
sig_str_sum = 0
drawing_board = ""
for line in lines:
    op_cycle_length = 0
    op_delta_x = 0
    if line.count("noop"):
        op_cycle_length = 1
    if line.count("addx"):
        op_cycle_length = 2
        op_delta_x = int(get_digits(line))
        if line.count("-"):
            op_delta_x *= -1
    
    for _ in range(op_cycle_length):
        index = (n_cycle - 1) % 40  # index = position
        if abs(index - x) <= 1:
            drawing_board += "@"
        else:
            drawing_board += " "

        if len(drawing_board.replace("\n", "") ) % 40 == 0:
            drawing_board += "\n" 
        
        if n_cycle in observe_cycles:
            sig_str = n_cycle * x
            sig_str_sum += sig_str

        n_cycle += 1

    x += op_delta_x

answer_a = sig_str_sum
print(drawing_board)
answer_b = "ZGCJZJFL"

### --- --- --- ###
submit_a = False
submit_b = False

print("Answer A: {}".format(answer_a))
print("Answer B: {}".format(answer_b))

if submit_a:
    submit(answer_a, part="a", day=day, year=year)
if submit_b:
    submit(answer_b, part="b", day=day, year=year)
