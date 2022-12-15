from aocd import submit
from utils import parse_data, group_data_by_separator, group_data_by_size, data_replace, data_to_numpy
from retils import get_between_groups, get_after_group, get_before_group, get_digits
import numpy as np
import copy
import functools
from tqdm import tqdm

day = 15
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


def get_dist(sensor_pos, beacon_pos):
    return abs(sensor_pos[0] - beacon_pos[0]) + abs(sensor_pos[1] - beacon_pos[1])


sensors = []
visibility_radii = []
for line in lines:
    digits = list(map(int, get_digits(line, True)))
    sensor_pos = (digits[0], digits[1])
    beacon_pos = (digits[2], digits[3])
    visibility_radius = get_dist(sensor_pos, beacon_pos)
    sensors.append(sensor_pos)
    visibility_radii.append(visibility_radius)


def get_ranges(y_level, min_pos, max_pos):
    x_ranges = []
    for i in range(len(sensors)):
        sensor_pos = sensors[i]
        visibility_radius = visibility_radii[i]
        dist_to_y_target = get_dist(sensor_pos, (sensor_pos[0], y_level))

        if dist_to_y_target > visibility_radius:
            continue

        n_visible = visibility_radius - dist_to_y_target

        if min_pos != None and max_pos != None:
            x_ranges.append(range(
                max(sensor_pos[0]-n_visible, min_pos),
                min(sensor_pos[0]+n_visible, max_pos)
            ))
        else:
            x_ranges.append(range(
                sensor_pos[0]-n_visible,
                sensor_pos[0]+n_visible
            ))
    return x_ranges


def get_combined_range(ranges):
    ranges = sorted(ranges, key=lambda l: l.start)
    combined_range = ranges[0]
    for i in range(1, len(ranges)):
        curr_range = ranges[i]
        inclusive_range = range(combined_range.start, combined_range.stop+1)
        if not curr_range.start in inclusive_range and not curr_range.stop in inclusive_range:
            return (combined_range, curr_range)
        if curr_range.start < combined_range.start and curr_range.stop <= combined_range.stop:
            combined_range = range(curr_range.start, combined_range.stop)
        if curr_range.start >= combined_range.start and curr_range.stop > combined_range.stop:
            combined_range = range(combined_range.start, curr_range.stop)
        if curr_range.start < combined_range.start and curr_range.stop > combined_range.stop:
            combined_range = range(curr_range.start, curr_range.stop)
    return combined_range


answer_a = len(get_combined_range(get_ranges(2000000, None, None)))
min_pos = 0
max_pos = 4000000
for y in tqdm(range(min_pos, max_pos+1)):
    combined_range = get_combined_range(get_ranges(y, min_pos, max_pos))
    if type(combined_range) == tuple:
        x = combined_range[0].stop + 1
        freq = x * 4000000 + y
        answer_b = freq
        break

### --- --- --- ###
submit_a = False
submit_b = False

print("Answer A: {}".format(answer_a))
print("Answer B: {}".format(answer_b))

if submit_a:
    submit(answer_a, part="a", day=day, year=year)
if submit_b:
    submit(answer_b, part="b", day=day, year=year)
