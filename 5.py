from aocd import submit
from utils import parse_data, group_data_by_separator, group_data_by_size, data_replace, data_to_numpy
from retils import get_between_groups, get_after_group, get_before_group, get_digits
import numpy as np
import copy

day = 5
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
configuration = [[] for _ in range(9)]
groups[0].pop(-1)
for line in list(reversed(groups[0])):
    for i, pos in enumerate(range(1, 34, 4)):
        if line[pos] != ' ':
            configuration[i].append(line[pos])
configuration_2 = copy.deepcopy(configuration)

for line in groups[1]:
    digits = list(map(int, get_digits(line, True)))
    moveFrom = digits[1] - 1
    moveTo = digits[2] - 1
    for nBlocks in range(digits[0]):
        configuration[moveTo].append(configuration[moveFrom].pop())
    nBlocks = digits[0]
    configuration_2[moveTo].extend(configuration_2[moveFrom][-nBlocks:])
    del configuration_2[moveFrom][-nBlocks:]

answer_a = ""
for stack in configuration:
    answer_a += stack[-1]

answer_b = ""
for stack in configuration_2:
    answer_b += stack[-1]

### --- --- --- ###
submit_a = False
submit_b = False

print("Answer A: {}".format(answer_a))
print("Answer B: {}".format(answer_b))

if submit_a:
    submit(answer_a, part="a", day=day, year=year)
if submit_b:
    submit(answer_b, part="b", day=day, year=year)
