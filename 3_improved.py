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
def letter_to_prio(letter):
    order_val = ord(letter)
    if letter.lower() == letter:
        priority = order_val - 96
    else:
        priority = order_val - 38
    return priority

for line in data:
    rucksack_size = int(len(line) / 2)
    first = line[:rucksack_size]
    second = line[rucksack_size:]
    shared_letter = set(first).intersection(set(second))
    answer_a += letter_to_prio(list(shared_letter)[0])

for group in groups:
    shared_letter = set(group[0]).intersection(set(group[1]), set(group[2]))
    answer_b += letter_to_prio(list(shared_letter)[0])


### --- --- --- ###
submit_a = False
submit_b = False

print("Answer A: {}".format(answer_a))
print("Answer B: {}".format(answer_b))

if submit_a:
    submit(answer_a, part="a", day=day, year=year)
if submit_b:
    submit(answer_b, part="b", day=day, year=year)