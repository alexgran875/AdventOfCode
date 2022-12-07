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


class Directory():
    def __init__(self):
        self.contents = []

    def get_size(self):
        total_size = 0
        for content in self.contents:
            if type(content) == Directory:
                total_size += content.get_size()
            else:
                total_size += content
        return total_size

    def add_content(self, content):
        self.contents.append(content)


def get_abs_path(curr_dir):
    return functools.reduce(lambda x, y: x + "/" + y, curr_dir)


curr_dir = []
dirs_dict = {}
for line in lines:
    if line == "$ cd /":
        curr_dir.append("root")
        dirs_dict["root"] = Directory()
    elif line.count("$ cd"):
        # NOTE: don't forget to escape special character $
        # also, only singular cds in the input (i.e. no cd abc/def/hij)
        cd_arg = get_after_group(line, "\$ cd ")
        if cd_arg == "..":
            curr_dir.pop()
        else:
            curr_dir.append(cd_arg)
    elif line.count("dir "):
        abs_path = get_abs_path(curr_dir) + "/" + get_after_group(line, "dir ")
        if abs_path not in dirs_dict.keys():
            new_dir = Directory()
            parent_path = abs_path[:abs_path.rfind("/")]
            dirs_dict[parent_path].add_content(new_dir)
            dirs_dict[abs_path] = new_dir
    elif line.count("$ ls") == 0:
        size = int(line.split(" ")[0])
        dirs_dict[get_abs_path(curr_dir)].add_content(size)

sizes = [directory.get_size() for directory in dirs_dict.values()]
sizes = sorted(sizes, reverse=True)
answer_a = sum(filter(lambda x: x <= 100000, sizes))

free_space = 70000000 - dirs_dict["root"].get_size()
space_to_free = 30000000 - free_space
for i, size in enumerate(sizes):
    if size < space_to_free:
        answer_b = sizes[i-1]
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
