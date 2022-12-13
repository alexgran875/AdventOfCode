from aocd import submit
from utils import parse_data, group_data_by_separator, group_data_by_size, data_replace, data_to_numpy
from retils import get_between_groups, get_after_group, get_before_group, get_digits
import numpy as np
import copy
import functools

day = 13
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


def is_correct_order(left, right):
    if type(left) == int and type(right) == int:
        if left < right:
            return True
        elif left > right:
            return False
        else:
            return None
    elif type(left) == list and type(right) == list:
        for i in range(max(len(left), len(right))):
            if i == len(right):
                return False
            elif i == len(left):
                return True
            order_correct = is_correct_order(left[i], right[i])
            if order_correct != None:
                return order_correct
    elif type(left) == int and type(right) == list:
        return is_correct_order([left], right)
    elif type(left) == list and type(right) == int:
        return is_correct_order(left, [right])
    return None


correct_pairs = []
for i, pair in enumerate(groups):
    order_correct = is_correct_order(eval(pair[0]), eval(pair[1]))
    if order_correct == True:
        correct_pairs.append(i + 1)
answer_a = sum(correct_pairs)

ordered_packets = []
remaining_packets = list(filter(lambda line: line != "", lines))
divider_1 = "[[2]]"
divider_2 = "[[6]]"
divider_2_ordered = False
remaining_packets.extend([divider_1, divider_2])
while not divider_2_ordered:
    print(f"Packets to order: {len(remaining_packets)}")
    for left_line in remaining_packets:
        left_is_smallest = True
        for right_line in remaining_packets:
            if left_line == right_line:
                continue

            order_correct = is_correct_order(eval(left_line), eval(right_line))
            if order_correct == False:
                left_is_smallest = False
                break

        if left_is_smallest:
            ordered_packets.append(left_line)
            del remaining_packets[remaining_packets.index(left_line)]
            if left_line == divider_2:
                divider_2_ordered = True
            break

answer_b = (ordered_packets.index(divider_1) + 1) * \
    (ordered_packets.index(divider_2) + 1)
### --- --- --- ###
submit_a = False
submit_b = False

print("Answer A: {}".format(answer_a))
print("Answer B: {}".format(answer_b))

if submit_a:
    submit(answer_a, part="a", day=day, year=year)
if submit_b:
    submit(answer_b, part="b", day=day, year=year)
