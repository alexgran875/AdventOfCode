from aocd import submit
from utils import parse_data, group_data_by_separator, group_data_by_size, data_replace, data_to_numpy
from retils import get_between_groups, get_after_group, get_before_group, get_digits
import numpy as np
import copy
import functools

day = 23
year = 2022

read_online = False
if read_online:
    lines = parse_data(day, year)
else:
    lines = parse_data()
groups = group_data_by_separator(lines)

answer_a = None
answer_b = None
### --- --- --- ###
lines = data_replace(lines, [("#", "1"), (".", "0")])
world = data_to_numpy(lines)

up = ((-1, 0), (-1, 1), (-1, -1))
down = ((1, 0), (1, 1), (1, -1))
left = ((0, -1), (-1, -1), (1, -1))
right = ((0, 1), (-1, 1), (1, 1))
dir_vectors = {}
dir_vectors[up] = (-1, 0)
dir_vectors[down] = (1, 0)
dir_vectors[left] = (0, -1)
dir_vectors[right] = (0, 1)
dir_queue = [up, down, left, right]

rowPos, colPos = np.nonzero(world)
elves_positions = set(zip(rowPos, colPos))

part_a = False
if part_a:
    n_rounds = 10
else:
    n_rounds = 9999999

for round in range(n_rounds):
    new_elves_positions = []
    noOneMoved = True
    for iElf, oldPos in enumerate(elves_positions):
        newPos = oldPos
        noElfCount = 0
        for dir in dir_queue:
            dirAvail = True
            for (rowOff, colOff) in dir:
                posOff = (oldPos[0] + rowOff, oldPos[1] + colOff)
                if posOff not in elves_positions:
                    noElfCount += 1
                else:
                    dirAvail = False

            if dirAvail and newPos == oldPos:
                dirVec = dir_vectors[dir]
                newPos = (oldPos[0] + dirVec[0], oldPos[1] + dirVec[1])

        if noElfCount == 12:
            newPos = oldPos
        new_elves_positions.append(newPos)

        if newPos != oldPos:
            noOneMoved = False

    if noOneMoved:
        break

    elves_positions = list(elves_positions)
    for iElf, newPos in enumerate(new_elves_positions):
        if new_elves_positions.count(newPos) == 1:
            elves_positions[iElf] = newPos
    elves_positions = set(elves_positions)

    dir_queue.append(dir_queue.pop(0))

if part_a:
    minx = min(x for x, y in elves_positions)
    maxx = max(x for x, y in elves_positions)
    miny = min(y for x, y in elves_positions)
    maxy = max(y for x, y in elves_positions)
    coords = {(x, y) for x in range(minx, maxx+1) for y in range(miny, maxy+1)}
    coords -= set(elves_positions)
    answer_a = len(coords)
else:
    answer_b = round + 1


### --- --- --- ###
submit_a = False
submit_b = False

print("Answer A: {}".format(answer_a))
print("Answer B: {}".format(answer_b))

if submit_a:
    submit(answer_a, part="a", day=day, year=year)
if submit_b:
    submit(answer_b, part="b", day=day, year=year)
