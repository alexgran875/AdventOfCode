from aocd import submit
from utils import parse_data, group_data_by_separator, group_data_by_size, data_replace, data_to_numpy
from retils import get_between_groups, get_after_group, get_before_group, get_digits
import numpy as np
import copy
import functools
import networkx as nx
from itertools import combinations

day = 18
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
lava_coords = set()
for line in lines:
    digits = get_digits(line, True)
    lava_coords.add((int(digits[0]), int(digits[1]), int(digits[2])))


def is_adjacent(c1, c2):
    return abs(c1[0] - c2[0]) + abs(c1[1] - c2[1]) + abs(c1[2] - c2[2]) == 1


def find_area(cubes):
    area = 6 * len(cubes)
    for c1, c2 in combinations(cubes, 2):
        if is_adjacent(c1, c2):
            area -= 2
    return area


answer_a = find_area(lava_coords)

maxx = max([x for x, y, z in lava_coords])
maxy = max([y for x, y, z in lava_coords])
maxz = max([z for x, y, z in lava_coords])

definitely_air_pos = (maxx, maxy, maxz + 1)
air_coords = set((definitely_air_pos, ))
air_graph = nx.Graph()
air_graph.add_node(definitely_air_pos)
# OBS: need some extra space outside the bounding box to make sure all the air is connected
for x in range(-1, maxx + 2):
    for y in range(-1, maxy + 2):
        for z in range(-1, maxz + 2):
            pos = (x, y, z)
            if not pos in lava_coords:
                air_graph.add_node(pos)
                air_coords.add(pos)

for c1, c2 in combinations(air_coords, 2):
    if is_adjacent(c1, c2):
        air_graph.add_edge(c1, c2)

subgraphs = list(nx.connected_components(air_graph))
answer_b = answer_a
for subgraph in subgraphs:
    if definitely_air_pos in subgraph:
        continue
    answer_b -= find_area(list(subgraph))


### --- --- --- ###
submit_a = False
submit_b = False

print("Answer A: {}".format(answer_a))
print("Answer B: {}".format(answer_b))

if submit_a:
    submit(answer_a, part="a", day=day, year=year)
if submit_b:
    submit(answer_b, part="b", day=day, year=year)
