from aocd import submit
from utils import parse_data, group_data_by_separator, group_data_by_size, data_replace, data_to_numpy
from retils import get_between_groups, get_after_group, get_before_group, get_digits
import numpy as np
import copy
import functools

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
RAY_DIRECTIONS = [(1, 0, 0), (-1, 0, 0), (0, 1, 0),
                  (0, -1, 0), (0, 0, 1), (0, 0, -1)]


class Cube():
    def __init__(self):
        self.exposed_sides = {}
        for faceDir in RAY_DIRECTIONS:
            self.exposed_sides[faceDir] = 1

    def ray_hit(self, rayDir):
        self.exposed_sides[(rayDir[0]*-1, rayDir[1]*-1, rayDir[2]*-1)] = 0

    def get_n_exposed_sides(self):
        return sum(self.exposed_sides.values())


def update_range(range, newPos):
    newRange = copy.copy(range)
    if newRange is None:
        newRange = [newPos, newPos]
    if newPos < newRange[0]:
        newRange[0] = newPos
    if newPos > newRange[1]:
        newRange[1] = newPos
    return newRange


cubes = {}
x_range = None
y_range = None
z_range = None
for line in lines:
    digits = get_digits(line, True)
    digits = (int(digits[0]), int(digits[1]), int(digits[2]))
    cubes[digits] = Cube()

    x_range = update_range(x_range, digits[0])
    y_range = update_range(y_range, digits[1])
    z_range = update_range(z_range, digits[2])

ranges = [x_range, y_range, z_range]


def shoot_ray(coords_to_check_for_hit, rayStart, rayDir, maxRayLength):
    global ranges
    rayPos = copy.copy(rayStart)
    if 1 in rayDir:
        coordIndex = rayDir.index(1)
    else:
        coordIndex = rayDir.index(-1)
    range = ranges[coordIndex]
    rayLength = 0
    while True:
        rayPos = (rayPos[0] + rayDir[0],
                  rayPos[1] + rayDir[1],
                  rayPos[2] + rayDir[2])
        if rayPos in coords_to_check_for_hit:
            return rayPos
        if rayPos[coordIndex] < range[0] or rayPos[coordIndex] > range[1]:
            return None
        rayLength += 1
        if maxRayLength is not None and rayLength >= maxRayLength:
            return None


# shoot adjacent cubes only and then sum all faces that didn't get hit
for cubePos in cubes.keys():
    for rayDir in RAY_DIRECTIONS:
        hitCubePos = shoot_ray(cubes.keys(), cubePos, rayDir, 1)
        if hitCubePos is not None:
            cubes[hitCubePos].ray_hit(rayDir)

answer_a = functools.reduce(
    lambda x, y: x + y.get_n_exposed_sides(), cubes.values(), 0)

# find possible air pockets
# possible air pocket = 6 ray hits (one in every direction)
air_pockets = []
for cubePos in cubes.keys():
    for posOffset in RAY_DIRECTIONS:
        n_hits = 0
        maybeAirPocket = (cubePos[0] + posOffset[0],
                          cubePos[1] + posOffset[1],
                          cubePos[2] + posOffset[2])
        if maybeAirPocket in cubes.keys() or maybeAirPocket in air_pockets:
            continue
        for rayDir in RAY_DIRECTIONS:
            if shoot_ray(cubes.keys(), maybeAirPocket, rayDir, None) != None:
                n_hits += 1
        if n_hits == 6:
            air_pockets.append(maybeAirPocket)

# remove any air pocket that in a given direction doesn't
# have a cube directly adjacent and no other air pockets in that direction
prev_n_air_pockets = len(air_pockets)
while True:
    for airPocketPos in air_pockets:
        for rayDir in RAY_DIRECTIONS:
            hitCubePos = shoot_ray(cubes.keys(), airPocketPos, rayDir, 1)
            if hitCubePos is not None:
                continue
            hitAirPos = shoot_ray(air_pockets, airPocketPos, rayDir, None)
            if hitAirPos is None:
                air_pockets.remove(airPocketPos)
                break
        if len(air_pockets) != prev_n_air_pockets:
            break

    if len(air_pockets) == prev_n_air_pockets:
        break
    else:
        prev_n_air_pockets = len(air_pockets)

# shoot all the cubes from the air pockets and then sum all faces that didn't get hit
for airPocketPos in air_pockets:
    for rayDir in RAY_DIRECTIONS:
        hitCubePos = shoot_ray(cubes.keys(), airPocketPos, rayDir, None)
        if hitCubePos is not None:
            cubes[hitCubePos].ray_hit(rayDir)

answer_b = functools.reduce(
    lambda x, y: x + y.get_n_exposed_sides(), cubes.values(), 0)
### --- --- --- ###
submit_a = False
submit_b = False

print("Answer A: {}".format(answer_a))
print("Answer B: {}".format(answer_b))

if submit_a:
    submit(answer_a, part="a", day=day, year=year)
if submit_b:
    submit(answer_b, part="b", day=day, year=year)
