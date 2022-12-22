from aocd import submit
from utils import parse_data, group_data_by_separator, group_data_by_size, data_replace, data_to_numpy
from retils import get_between_groups, get_after_group, get_before_group, get_digits
import numpy as np
import copy
import functools
from enum import Enum
from math import ceil
import heapq

day = 19
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
blueprints = {}
for line in lines:
    digits = list(map(int, get_digits(line, True)))
    blueprints[digits[0]] = (digits[1], digits[2],
                             (digits[3], digits[4]), (digits[5], digits[6]))


class Resource(Enum):
    ORE = 0
    CLAY = 1
    OBSIDIAN = 2
    GEODE = 3


def get_build_time(robotType, resources, resProd, nResReq):
    if (type(nResReq) == int):
        oreReq = nResReq
    else:
        oreReq = nResReq[0]
    timeSkip = ceil((oreReq - resources[0]) / resProd[0])

    if type(nResReq) == tuple:
        if robotType == Resource.OBSIDIAN.value:
            otherResIndex = Resource.CLAY.value
        elif robotType == Resource.GEODE.value:
            otherResIndex = Resource.OBSIDIAN.value
        else:
            raise Exception('Unhandled!')
        if resProd[otherResIndex] == 0:
            return 99
        anotherTimeSkip = ceil(
            (nResReq[1] - resources[otherResIndex]) / resProd[otherResIndex])
        timeSkip = max(timeSkip, anotherTimeSkip)

    timeSkip = max(timeSkip, 0)
    timeSkip += 1   # to build robot
    return timeSkip


def build(buildOrder, resources, resProd, timeLeftArg, blueprint):
    if len(buildOrder) == 0:
        return (resources, resProd, timeLeftArg)
    robotType = buildOrder[0].value
    nResReq = blueprint[robotType]
    newRes = list(resources)
    if type(nResReq) == int:
        newRes[0] -= nResReq
    else:
        newRes[0] -= nResReq[0]
        if robotType == Resource.OBSIDIAN.value:
            otherResIndex = Resource.CLAY.value
        elif robotType == Resource.GEODE.value:
            otherResIndex = Resource.OBSIDIAN.value
        else:
            raise Exception('Unhandled!')
        newRes[otherResIndex] -= nResReq[1]

    timeSkip = get_build_time(robotType, resources,
                              resProd, blueprint[robotType])
    timeLeft = timeLeftArg - timeSkip
    if timeLeft <= 0:
        # last one not built
        unusedRes = list(resources)
        for i in range(len(resources)):
            unusedRes[i] += timeLeftArg * resProd[i]
        return (tuple(unusedRes), resProd, 0)

    for i in range(len(resources)):
        newRes[i] += timeSkip * resProd[i]
    newProd = list(resProd)
    newProd[robotType] += 1
    return build(
        buildOrder[1:],
        tuple(newRes),
        tuple(newProd),
        timeLeftArg - timeSkip,
        blueprint
    )


class BuildOrder():
    def __init__(self, buildOrder) -> None:
        self.buildOrder = buildOrder

    def __lt__(self, other):
        return len(self.buildOrder) > len(other.buildOrder)


total_quality_level = 1
for id in blueprints.keys():
    dfs = [
        BuildOrder((Resource.CLAY, )),
        BuildOrder((Resource.ORE, ))
    ]
    heapq.heapify(dfs)
    highest_n_geodes = 0
    iteration = 0
    blueprint = blueprints[id]
    obsidianOreReq = blueprint[Resource.OBSIDIAN.value][0]
    obsidianClayReq = blueprint[Resource.OBSIDIAN.value][1]
    geodeOreReq = blueprint[Resource.GEODE.value][0]
    maxOreReq = max(obsidianOreReq, geodeOreReq)
    threshold = 1.5
    while len(dfs) > 0:
        if iteration % 10000 == 0:
            print(f"[{id}, {iteration}] to explore: {len(dfs)}")
        iteration += 1
        curr_order = heapq.heappop(dfs).buildOrder
        resources, resProd, timeLeft = build(
            curr_order, (0, 0, 0, 0), (1, 0, 0, 0), 32, blueprint)
        n_geodes = resources[Resource.GEODE.value] + \
            timeLeft * resProd[Resource.GEODE.value]
        if n_geodes > highest_n_geodes:
            highest_n_geodes = n_geodes
            best_bp = blueprint
            print(f"[{n_geodes}, {resources}]: {curr_order}")

        for next_robot in Resource:
            if next_robot == Resource.GEODE and resProd[Resource.OBSIDIAN.value] == 0:
                continue
            if next_robot == Resource.OBSIDIAN and resProd[Resource.CLAY.value] == 0:
                continue
            if resources[Resource.ORE.value] >= maxOreReq and resources[Resource.CLAY.value] >= obsidianClayReq:
                if next_robot == Resource.ORE or next_robot == Resource.CLAY:
                    continue
            if next_robot == Resource.CLAY and resources[Resource.CLAY.value] >= obsidianClayReq * threshold:
                continue
            if next_robot == Resource.ORE and resources[Resource.ORE.value] >= maxOreReq * threshold:
                continue
            buildTime = get_build_time(
                next_robot.value, resources, resProd, blueprint[next_robot.value])
            if buildTime > timeLeft:
                continue
            new_order = curr_order + (next_robot, )
            heapq.heappush(dfs, BuildOrder(new_order))

    total_quality_level *= highest_n_geodes

answer_a = total_quality_level

### --- --- --- ###
submit_a = False
submit_b = False

print("Answer A: {}".format(answer_a))
print("Answer B: {}".format(answer_b))

if submit_a:
    submit(answer_a, part="a", day=day, year=year)
if submit_b:
    submit(answer_b, part="b", day=day, year=year)
