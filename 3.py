from aocd import submit
from utils import parse_data, group_data_by_separator, group_data_by_size, data_replace, data_to_numpy
from retils import get_between_groups, get_after_group, get_before_group, get_digits
import numpy as np

day = 3
year = 2022

read_online = True
if read_online:
    data = parse_data(day, year)
else:
    data = parse_data()
groups = group_data_by_size(data, 3)

answer_a = 0
answer_b = 0
### --- --- --- ###
def shared_to_prio(shared_letters):
    if (len(shared_letters) == 0):
        return 0
    
    most_common = max(set(shared_letters), key=shared_letters.count)
    order_val = ord(most_common)
    if most_common.lower() == most_common:
        priority = order_val - 96
    elif most_common.upper() == most_common:
        priority = order_val - 38
    else:
        raise Exception("Unhandled case")
    return priority

for line in data:
    rucksack_size = int(len(list(line)) / 2)
    first = line[:rucksack_size]
    second = line[rucksack_size:]
    assert len(first) == len(second)
    shared_letters = []
    for letter in line:
        if letter in first and letter in second:
            shared_letters.append(letter)
    
    answer_a += shared_to_prio(shared_letters)

for group in groups:
    shared_letters = []
    for line in group:
        for letter in line:
            if letter in group[0] and letter in group[1] and letter in group[2]:
                shared_letters.append(letter)

    answer_b += shared_to_prio(shared_letters)


### --- --- --- ###
submit_a = False
submit_b = False

print("Answer A: {}".format(answer_a))
print("Answer B: {}".format(answer_b))

if submit_a:
    submit(answer_a, part="a", day=day, year=year)
if submit_b:
    submit(answer_b, part="b", day=day, year=year)