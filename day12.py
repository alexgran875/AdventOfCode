import numpy as np
from numpy.core.fromnumeric import shape
import copy

with open('input.txt') as f:
    input = f.readlines()

edges = list(map(lambda line:line.replace("\n","").split("-"),input))
visited_twice_paths = []

def get_next_nodes(path_so_far):
    possible_next_nodes = []
    last_node = path_so_far[-1]
    for edge in edges:
        if last_node in edge:
            idx = edge.index(last_node)
            idx = 1 - idx
            next_node = edge[idx]

            if next_node != "start":
                if next_node == "end":
                    possible_next_nodes.append(next_node)
                elif next_node in path_so_far and next_node == next_node.lower():
                    continue
                else:
                    possible_next_nodes.append(next_node)
                    
    return possible_next_nodes

paths = [["start"]]
found_all_paths = False
while not found_all_paths:
    new_paths = []
    n_ends = 0
    for path in paths:
        if path[-1] == "end":
            new_paths.append(copy.deepcopy(path))
            n_ends += 1
            continue
        next_nodes = get_next_nodes(path)
        for next_node in next_nodes:
            new_path = copy.deepcopy(path)
            new_path.append(next_node)
            new_paths.append(new_path)

    if len(new_paths) == n_ends:
        found_all_paths = True
    else:
        paths = copy.deepcopy(new_paths)

ended_paths = list(map(lambda path:path if path[-1] == "end" else None, paths))
ended_paths = [i for i in ended_paths if i]

print(len(ended_paths))

