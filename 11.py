from aocd import submit
from utils import parse_data, group_data_by_separator, group_data_by_size, data_replace, data_to_numpy
from retils import get_between_groups, get_after_group, get_before_group, get_digits
import numpy as np
import copy
import functools

day = 11
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


class Monkey():
    def __init__(self, monkey_lines, modulo_arg, divisor):
        test_arg = int(get_digits(monkey_lines[3]))
        test_true = int(get_digits(monkey_lines[4]))
        test_false = int(get_digits(monkey_lines[5]))
        self.test = lambda item: test_true if (
            item % test_arg == 0) else test_false

        operation_line = monkey_lines[2]
        operation_arg = get_digits(operation_line)

        if operation_line.count("*"):
            if operation_arg == "":
                self.operation = lambda item: (
                    (item**2) // divisor) % modulo_arg
            else:
                self.operation = lambda item: (
                    (item*int(operation_arg)) // divisor) % modulo_arg
        elif operation_line.count("+"):
            if operation_arg == "":
                self.operation = lambda item: (
                    (2*item) // divisor) % modulo_arg
            else:
                self.operation = lambda item: (
                    (item+int(operation_arg)) // divisor) % modulo_arg

        self.n_inspections = 0

        self.items = get_digits(monkey_lines[1], True)
        self.items = list(map(int, self.items))

    def turn(self, monkeys_list):
        self.n_inspections += len(self.items)
        self.items = list(map(self.operation, self.items))

        for item in self.items:
            monkeys_list[self.test(item)].items.append(item)

        self.items = []


def simulate(monkey_groups, smallest_common_multiple, divisor, n_rounds):
    monkeys_list = []
    for monkey_lines in monkey_groups:
        monkeys_list.append(
            Monkey(monkey_lines, smallest_common_multiple, divisor))

    for _ in range(n_rounds):
        for monkey in monkeys_list:
            monkey.turn(monkeys_list)

    monkeys_activity = []
    for monkey in monkeys_list:
        monkeys_activity.append(monkey.n_inspections)
    monkeys_activity = sorted(monkeys_activity)

    return monkeys_activity[-1] * monkeys_activity[-2]


smallest_common_multiple = 1
for line in lines:
    if line.count("divisible"):
        smallest_common_multiple *= int(get_digits(line))

answer_a = simulate(groups, smallest_common_multiple, 3, 20)
answer_b = simulate(groups, smallest_common_multiple, 1, 10000)
### --- --- --- ###
submit_a = False
submit_b = False

print("Answer A: {}".format(answer_a))
print("Answer B: {}".format(answer_b))

if submit_a:
    submit(answer_a, part="a", day=day, year=year)
if submit_b:
    submit(answer_b, part="b", day=day, year=year)
