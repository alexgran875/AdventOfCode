from aocd import submit
from utils import parse_data, group_data_by_separator, group_data_by_size, data_replace, data_to_numpy
from retils import get_between_groups, get_after_group, get_before_group, get_digits
import numpy as np
import copy
import functools
import networkx as nx
import heapq
from math import ceil

day = 16
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
non_zero_fr = {}
graph = nx.Graph()
shortest_paths = {}
for line in lines:
    valve_name = get_between_groups(line, "Valve ", " has")
    flow_rate = int(get_digits(get_between_groups(line, "rate=", ";")))
    if flow_rate > 0 or valve_name == "AA":
        non_zero_fr[valve_name] = flow_rate
        shortest_paths[valve_name] = {}

    tunnels_to = get_after_group(line, "valve").replace(
        "s", "").replace(" ", "").split(",")
    for i in tunnels_to:
        graph.add_edge(valve_name, i)

for valve in non_zero_fr.keys():
    for otherValve in non_zero_fr.keys():
        if valve == otherValve:
            continue
        pathLength = len(nx.shortest_path(graph, valve, otherValve)) - 1
        shortest_paths[valve][otherValve] = pathLength


@functools.cache
def traverse(path, arg_time_remaining=30):
    if len(path) > 1:
        travel_open_time = shortest_paths[path[0]][path[1]] + 1
        time_remaining = arg_time_remaining - travel_open_time
        if time_remaining <= 0:
            return (0, 0, 0)
        else:
            flow_rate = non_zero_fr[path[1]]
            pressure_generated = flow_rate * time_remaining
            rv = traverse(path[1:], time_remaining)
            return (pressure_generated + rv[0], flow_rate + rv[1], rv[2])
    else:
        return (0, 0, arg_time_remaining)


if not read_online:
    assert traverse(("AA", "DD", "BB", "JJ", "HH",
                    "EE", "CC")) == (1651, 81, 6)

best_pressure = 0
dfs_paths = [(0, ("AA", ))]

max_path_length = ceil(30 / (min(shortest_paths["AA"].values()) + 1)) + 1
iteration = 0
while len(dfs_paths) > 0:
    if iteration % 100000 == 0:
        print(f"[{iteration}] to explore: {len(dfs_paths)}")
    iteration += 1
    current_path = heapq.heappop(dfs_paths)[1]
    pressure, flow_rate, time_remaining = traverse(current_path)
    if pressure > best_pressure:
        best_pressure = pressure
        print(f"{best_pressure}: {current_path}")
    current_node = current_path[-1]
    for next_node in shortest_paths[current_node]:
        if next_node in current_path:
            continue
        if shortest_paths[current_node][next_node] + 1 >= time_remaining:
            continue
        new_path = current_path + (next_node, )
        if len(new_path) <= max_path_length:
            heapq.heappush(dfs_paths, (-len(new_path), new_path))

answer_a = best_pressure
### --- --- --- ###
submit_a = False
submit_b = False

print("Answer A: {}".format(answer_a))
print("Answer B: {}".format(answer_b))

if submit_a:
    submit(answer_a, part="a", day=day, year=year)
if submit_b:
    submit(answer_b, part="b", day=day, year=year)
