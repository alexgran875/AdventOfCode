from aocd import submit
from utils import parse_data, group_data_by_separator, group_data_by_size, data_replace, data_to_numpy
from retils import get_between_groups, get_after_group, get_before_group, get_digits
import numpy as np
import copy
import functools
import heapq

day = 12
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
n_rows = len(lines)
n_cols = len(lines[0])
elevation_matrix = np.zeros((n_rows, n_cols))
start = (0, 0)
goal = (0, 0)
for row, line in enumerate(lines):
    for col, char in enumerate(line):
        elevation_matrix[row, col] = ord(char) - 97

        if char == "S":
            elevation_matrix[row, col] = ord("a") - 97
            start = (row, col)
        if char == "E":
            elevation_matrix[row, col] = ord("z") - 97
            goal = (row, col)


def find_shortest_path(start, goal):
    journeys_priorityQ = []
    heapq.heappush(journeys_priorityQ, (len(start), [start]))
    explored_pos = set()
    shortest_path = None
    while len(journeys_priorityQ) > 0:
        current_path = heapq.heappop(journeys_priorityQ)[1]
        current_pos = current_path[-1]
        if current_pos in explored_pos:
            continue
        explored_pos.add(current_pos)
        if goal != "a":
            dist_to_goal = abs(current_pos[0] - goal[0]) + \
                abs(current_pos[1] - goal[1])
        else:
            dist_to_goal = None
        print(f"{current_pos} distance to goal: {dist_to_goal}")
        for rowOffset, colOffset in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            # row edge
            neighbourRowIndex = current_pos[0] + rowOffset
            if neighbourRowIndex < 0 or neighbourRowIndex >= n_rows:
                continue

            # col edge
            neighbourColIndex = current_pos[1] + colOffset
            if neighbourColIndex < 0 or neighbourColIndex >= n_cols:
                continue

            # prevent backtracking
            neighbour_pos = (neighbourRowIndex, neighbourColIndex)
            if neighbour_pos in current_path:
                continue

            neighbour_elevation = elevation_matrix[neighbour_pos]
            current_elevation = elevation_matrix[current_pos]
            elevation_diff = neighbour_elevation - current_elevation
            if goal != "a" and elevation_diff > 1:
                continue
            elif goal == "a" and elevation_diff < -1:
                continue

            new_path = current_path + [neighbour_pos]
            heapq.heappush(journeys_priorityQ, (len(new_path), new_path))

            if goal != "a" and neighbour_pos == goal:
                if shortest_path is None or len(new_path) < len(shortest_path):
                    shortest_path = new_path
            elif goal == "a" and neighbour_elevation == 0:
                shortest_path = new_path
                journeys_priorityQ = []

    return len(shortest_path) - 1


answer_a = find_shortest_path(start=start, goal=goal)
answer_b = find_shortest_path(start=goal, goal="a")
### --- --- --- ###
submit_a = False
submit_b = False

print("Answer A: {}".format(answer_a))
print("Answer B: {}".format(answer_b))

if submit_a:
    submit(answer_a, part="a", day=day, year=year)
if submit_b:
    submit(answer_b, part="b", day=day, year=year)
