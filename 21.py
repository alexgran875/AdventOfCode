from aocd import submit
from utils import parse_data, group_data_by_separator, group_data_by_size, data_replace, data_to_numpy
from retils import get_between_groups, get_after_group, get_before_group, get_digits
import numpy as np
import copy
import functools
import sympy

day = 21
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
lines = list(map(lambda line: line.replace(":", "="), lines))
toEval = copy.copy(lines)
while len(toEval) > 0:
    for line in toEval:
        try:
            exec(line)
            toEval.remove(line)
            break
        except NameError:
            continue

answer_a = root

expressionDict = {}
for line in lines:
    if line.count("humn="):
        continue
    if line.count("root="):
        expressions = line.split("= ")[1].split(" + ")
        final_expression = expressions[0] + "-" + expressions[1]
        continue
    key = line.split("= ")[0]
    value = line.split("= ")[1]
    if value.isdigit():
        expressionDict[key] = value
    else:
        expressionDict[key] = '(' + value.replace(" ", "") + ')'

expressionComplete = False
while not expressionComplete:
    expressionComplete = True
    for (key, value) in expressionDict.items():
        if key in final_expression:
            final_expression = final_expression.replace(key, value)
            expressionComplete = False

final_expression = final_expression.replace("humn", "x")
answer_b = sympy.solve(final_expression)[0]
### --- --- --- ###
submit_a = False
submit_b = False

print("Answer A: {}".format(answer_a))
print("Answer B: {}".format(answer_b))

if submit_a:
    submit(answer_a, part="a", day=day, year=year)
if submit_b:
    submit(answer_b, part="b", day=day, year=year)
