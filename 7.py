# I thought it was going to be easy peasy lemon squeezy,
# but it was difficult diffuclt lemon difficult
from aocd import submit
from utils import parse_data, group_data_by_separator, group_data_by_size, data_replace, data_to_numpy
from retils import get_between_groups, get_after_group, get_before_group, get_digits
import numpy as np
import copy
import functools

day = 7
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


def get_abs_path(curr_dir):
    return functools.reduce(lambda x, y: x + "/" + y, curr_dir)


curr_dir = []
ls_cmd = False
dir_file_sizes = {}
dir_path_depths = {}
for line in lines:
    if line == "$ cd /":
        ls_cmd = False
        curr_dir.append("root")
        dir_file_sizes["root"] = 0
        dir_path_depths["root"] = 1
    elif line.count("$ cd"):
        ls_cmd = False
        # NOTE: don't forget to escape special character $
        # also, only singular cds in the input (i.e. no cd abc/def/hij)
        cd_arg = get_after_group(line, "\$ cd ")
        if cd_arg == "..":
            curr_dir.pop()
        else:
            curr_dir.append(cd_arg)
    elif line.count("$ ls"):
        ls_cmd = True
    elif line.count("dir "):
        tmp_dir = copy.deepcopy(curr_dir)
        tmp_dir.append(get_after_group(line, "dir "))
        abs_path = get_abs_path(tmp_dir)
        if abs_path not in dir_file_sizes.keys():
            dir_file_sizes[abs_path] = 0
            dir_path_depths[abs_path] = len(tmp_dir)
    elif ls_cmd:
        dir_file_sizes[get_abs_path(curr_dir)] += int(get_digits(line))

sorted_dir_path_depths = {k: v for k, v in sorted(
    dir_path_depths.items(), key=lambda item: item[1], reverse=True)}
total_sizes = dict([(key, 0) for key in sorted_dir_path_depths])
for abs_path in sorted_dir_path_depths:
    total_sizes[abs_path] += dir_file_sizes[abs_path]
    if abs_path != "root":
        parent_path = abs_path[:abs_path.rfind("/")]
        total_sizes[parent_path] += total_sizes[abs_path]


descending_sizes = sorted(list(total_sizes.values()), reverse=True)
free_space = 70000000 - descending_sizes[0]
space_to_free = 30000000 - free_space
answer_a = 0
for i, size in enumerate(descending_sizes):
    if size <= 100000:
        answer_a += size
    if size < space_to_free:
        if answer_b is None:
            answer_b = descending_sizes[i-1]

### --- --- --- ###
submit_a = False
submit_b = False

print("Answer A: {}".format(answer_a))
print("Answer B: {}".format(answer_b))

if submit_a:
    submit(answer_a, part="a", day=day, year=year)
if submit_b:
    submit(answer_b, part="b", day=day, year=year)
