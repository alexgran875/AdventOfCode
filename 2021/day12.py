import numpy as np
from numpy.core.fromnumeric import shape
import copy

with open('input.txt') as f:
    input = f.readlines()

edges = list(map(lambda line:line.replace("\n","").split("-"),input))
def get_next_nodes(path_so_far, visited_twice):
    possible_next_nodes = []
    last_node = path_so_far[-1]
    v = []
    for edge in edges:
        if last_node in edge:
            idx = edge.index(last_node)
            idx = 1 - idx
            next_node = edge[idx]

            if next_node != "start":
                if next_node == "end":
                    possible_next_nodes.append(next_node)
                    v.append(visited_twice)
                elif next_node in path_so_far and next_node == next_node.lower() and visited_twice:
                    continue
                elif next_node in path_so_far and next_node == next_node.lower():
                    possible_next_nodes.append(next_node)
                    v.append(True)
                else:
                    possible_next_nodes.append(next_node)
                    v.append(visited_twice)
                    
    return (possible_next_nodes,v)

paths = [["start"]]
visited_twice = [False]
found_all_paths = False
while not found_all_paths:
    new_paths = []
    new_visited_twice = []
    n_ends = 0
    for i,path in enumerate(paths):
        if path[-1] == "end":
            new_paths.append(copy.deepcopy(path))
            new_visited_twice.append(visited_twice[i])
            n_ends += 1
            continue
        next_nodes,v = get_next_nodes(path,visited_twice[i])
        for j,next_node in enumerate(next_nodes):
            new_path = copy.deepcopy(path)
            new_path.append(next_node)
            new_paths.append(new_path)
            new_visited_twice.append(v[j])

    if len(new_paths) == n_ends:
        found_all_paths = True
    else:
        paths = copy.deepcopy(new_paths)
        visited_twice = copy.deepcopy(new_visited_twice)

ended_paths = list(map(lambda path:path if path[-1] == "end" else None, paths))
ended_paths = [i for i in ended_paths if i]

print(len(ended_paths))

