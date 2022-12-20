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


def traverse(path, arg_time_remaining):
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


def get_max_pressure(start, valid_nodes, time_remaining):
    valid_nodes = tuple(
        filter(lambda l: shortest_paths[start][l[0]] + 1 < time_remaining, valid_nodes))
    if len(valid_nodes) == 0:
        return 0
    optimistic_time_remaining = time_remaining - \
        (min(shortest_paths[start].values()) + 1)
    return (valid_nodes[0][1] * optimistic_time_remaining) + get_max_pressure(valid_nodes[0][0], valid_nodes[1:],
                                                                              optimistic_time_remaining)


max_path_length = ceil(30 / (min(shortest_paths["AA"].values()) + 1)) + 1
for initial_time_remaining in [30, 26]:
    iteration = 0
    best_pressure = 0
    dfs_paths = [(0, ("AA", ))]
    while len(dfs_paths) > 0:
        if iteration % 100000 == 0:
            print(f"[{iteration}] to explore: {len(dfs_paths)}")
        iteration += 1
        current_path = heapq.heappop(dfs_paths)[1]
        pressure, flow_rate, time_remaining = traverse(
            current_path[current_path.index("AA"):], initial_time_remaining)
        if initial_time_remaining == 26:
            pressure_ele, flow_rate_ele, time_remaining_ele = traverse(
                current_path[:current_path.index("AA")+1][::-1], 26)
            pressure += pressure_ele
        if pressure > best_pressure:
            best_pressure = pressure
            if initial_time_remaining == 30:
                answer_a = best_pressure
            else:
                answer_b = best_pressure
            print(f"{best_pressure}: {current_path}")
        current_node = current_path[-1]
        current_ele_node = current_path[0]
        sorted_fr = tuple(filter(lambda x: x[0] not in current_path, sorted(
            non_zero_fr.items(), key=lambda x: x[1], reverse=True)))
        possible_additional_pressure = get_max_pressure(
            current_node, sorted_fr, time_remaining)
        if initial_time_remaining == 26:
            possible_additional_pressure += get_max_pressure(
                current_ele_node, sorted_fr, time_remaining_ele)
        if pressure + possible_additional_pressure < best_pressure:
            continue
        for next_node in shortest_paths[current_node]:
            if next_node in current_path:
                continue
            new_path = current_path
            if shortest_paths[current_node][next_node] + 1 < time_remaining:
                new_path = current_path + (next_node, )
                if initial_time_remaining == 30:
                    heapq.heappush(dfs_paths, (-len(new_path), new_path))

            if initial_time_remaining == 26:
                for ele_node in shortest_paths[current_ele_node]:
                    if ele_node in new_path:
                        continue
                    new_total_path = new_path
                    if shortest_paths[current_ele_node][ele_node] + 1 < time_remaining_ele:
                        new_total_path = (ele_node, ) + new_path
                    if new_total_path != current_path:
                        heapq.heappush(
                            dfs_paths, (-len(new_total_path), new_total_path))
### --- --- --- ###
submit_a = False
submit_b = False

print("Answer A: {}".format(answer_a))
print("Answer B: {}".format(answer_b))

if submit_a:
    submit(answer_a, part="a", day=day, year=year)
if submit_b:
    submit(answer_b, part="b", day=day, year=year)
