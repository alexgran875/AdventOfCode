from aocd import submit
from utils import parse_data, group_data_by_separator, group_data_by_size, data_replace, data_to_numpy
from retils import get_between_groups, get_after_group, get_before_group, get_digits
import numpy as np
import copy
import functools
import heapq
import hashlib

day = 24
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
dir_vec_mapping = {">": np.array([0, 1]), "v": np.array(
    [1, 0]), "<": np.array([0, -1]), "^": np.array([-1, 0])}
dir_val_mapping = {">": "3", "v": "4", "<": "5", "^": "6"}
world = data_replace(
    lines, [("#", "1"), (".", "0")] + list(zip(dir_val_mapping.keys(), dir_val_mapping.values())))
world = data_to_numpy(world, np.float64)

only_walls_world = copy.copy(world)
only_walls_world[
    np.logical_not(np.logical_or(only_walls_world == 1, only_walls_world == 0))
] = 0
wind_worlds = {}
for direction, value in dir_val_mapping.items():
    wind_worlds[direction] = np.zeros(world.shape)
    wind_worlds[direction] -= world == int(value)


def construct_world():
    global only_walls_world, wind_worlds
    world = copy.copy(only_walls_world)
    for wind_world in wind_worlds.values():
        world += wind_world
    return world


world_history = [construct_world()]
while True:
    for key in dir_vec_mapping.keys():
        oldPos = np.array(np.where(wind_worlds[key] != 0))
        newPos = oldPos + np.array(dir_vec_mapping[key]).reshape(2, 1)

        newPos[0][newPos[0] == world.shape[0] - 1] = 1
        newPos[1][newPos[1] == world.shape[1] - 1] = 1

        newPos[0][newPos[0] == 0] = world.shape[0] - 2
        newPos[1][newPos[1] == 0] = world.shape[1] - 2

        wind_worlds[key] = np.zeros(wind_worlds[key].shape)
        wind_worlds[key][tuple(newPos)] = -1

    world = construct_world()
    if (world == world_history[0]).all():
        break
    world_history.append(world)

start = (0, np.where(world[0, :] == 0)[0][0])
goal = (world.shape[0]-1, np.where(world[-1, :] == 0)[0][0])


def get_dist(p1, p2):
    # manhattan
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


world_history_len = len(world_history)


class Path():
    def __init__(self, path, time_passed):
        self.path = path
        self.time_passed = time_passed

    def __hash__(self):
        h = hashlib.sha256()
        h.update(str(self.time_passed % world_history_len).encode())
        h.update(str(self.path[-1]).encode())
        return int(h.hexdigest(), 16)

    def __eq__(self, other):
        return ((self.time_passed % world_history_len) == (other.time_passed %
                world_history_len)) and self.path[-1] == other.path[-1]

    def __lt__(self, other):
        goal_dist1 = get_dist(self.path[-1], goal)
        goal_dist2 = get_dist(other.path[-1], goal)
        return (self.time_passed + goal_dist1) < (other.time_passed + goal_dist2)


def get_possible_next_pos(pos, time_passed):
    # includes current position if waiting is possible
    future_world = world_history[(time_passed+1) % world_history_len]
    possible = []
    for offset in dir_vec_mapping.values():
        nextPos = tuple(pos + offset)
        if nextPos[0] == future_world.shape[0]:
            continue
        if future_world[nextPos] == 0:
            possible.append(nextPos)
    if future_world[pos] == 0:
        possible.append(pos)

    return possible


def search(start, goal, start_time):
    bfs = [Path([start], start_time)]
    iteration = 0
    explored_states = set()
    while len(bfs) > 0:
        if iteration % 10000 == 0:
            print(f"[{iteration}] to explore: {len(bfs)}")
        iteration += 1

        pathClass = heapq.heappop(bfs)
        if pathClass in explored_states:
            continue
        explored_states.add(pathClass)
        path = pathClass.path
        time_passed = pathClass.time_passed
        possible_next = get_possible_next_pos(path[-1], time_passed)

        for nextPos in possible_next:
            if path.count(nextPos) >= 10:
                continue
            if nextPos == goal:
                return time_passed + 1

            newPath = Path(path+[nextPos], time_passed+1)
            if newPath in explored_states:
                continue
            heapq.heappush(bfs, newPath)

    raise Exception("No path found!")


answer_a = search(start=start, goal=goal, start_time=0)
answer_b = search(start=goal, goal=start, start_time=answer_a)
answer_b = search(start=start, goal=goal, start_time=answer_b)
### --- --- --- ###
submit_a = False
submit_b = False

print("Answer A: {}".format(answer_a))
print("Answer B: {}".format(answer_b))

if submit_a:
    submit(answer_a, part="a", day=day, year=year)
if submit_b:
    submit(answer_b, part="b", day=day, year=year)
