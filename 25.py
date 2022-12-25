from aocd import submit
from utils import parse_data, group_data_by_separator, group_data_by_size, data_replace, data_to_numpy
from retils import get_between_groups, get_after_group, get_before_group, get_digits
import numpy as np
import copy
import functools
import math
import re

day = 25
year = 2022

read_online = False
if read_online:
    lines = parse_data(day, year)
else:
    lines = parse_data()
groups = group_data_by_separator(lines)

answer_a = None
answer_b = None
### --- --- --- ###


def snafu_to_decimal(line):
    decimal = 0
    for i, symbol in enumerate(list(reversed(line))):
        if symbol.isdigit():
            decimal += (5**i)*int(symbol)
        elif symbol == "-":
            decimal += (5**i)*(-1)
        elif symbol == "=":
            decimal += (5**i)*(-2)
        else:
            raise Exception('Unhandled!')
    return decimal


def decimal_to_snafu(decimal):
    snafu = ""
    remainder = decimal
    root = math.ceil(decimal**0.2)
    multipliers = [(2, "2"), (1, "1"), (0, "0"), (-1, "-"), (-2, "=")]
    for i in range(root, -1, -1):
        distances = list(
            map(lambda x: abs(remainder-(x[0]*(5**i))), multipliers))
        multiplier = multipliers[distances.index(min(distances))]
        remainder -= multiplier[0]*(5**i)
        snafu += multiplier[1]
    return re.sub(r'^0*(\d+)', r'\1', snafu)


lines = list(map(snafu_to_decimal, lines))
answer_a = decimal_to_snafu(sum(lines))
### --- --- --- ###
submit_a = False
submit_b = False

print("Answer A: {}".format(answer_a))
print("Answer B: {}".format(answer_b))

if submit_a:
    submit(answer_a, part="a", day=day, year=year)
if submit_b:
    submit(answer_b, part="b", day=day, year=year)
