from aocd import submit
from utils import parse_data, group_data_by_separator, group_data_by_size, data_replace, data_to_numpy
from retils import get_between_groups, get_after_group, get_before_group, get_digits
import numpy as np
import copy
import functools
import matplotlib.pyplot as plt
import re

day = 22
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
groups[0] = list(map(lambda x: x.replace(" ", "2"), groups[0]))
groups[0] = data_replace(groups[0], [("#", "1"), (".", "0")])
maxLineLength = len(max(groups[0], key=len))
for i, line in enumerate(groups[0]):
    toAdd = maxLineLength - len(line)
    groups[0][i] = line + ("2"*toAdd)
world = data_to_numpy(groups[0])
instructions = re.findall(r'\d+|R|L', groups[1][0])


def walk_one_step(pos, dir_vector):
    global world
    nextPos = pos + dir_vector
    nextPos[0] = nextPos[0] % np.shape(world)[0]
    nextPos[1] = nextPos[1] % np.shape(world)[1]
    nextVal = world[tuple(nextPos)]
    if nextVal == 0:
        pos = nextPos
    elif nextVal == 1:
        return pos
    elif nextVal == 2:
        lookAhead = nextPos + dir_vector
        lookAhead[0] = lookAhead[0] % np.shape(world)[0]
        lookAhead[1] = lookAhead[1] % np.shape(world)[1]
        nextVal = world[tuple(lookAhead)]
        while nextVal == 2:
            lookAhead += dir_vector
            lookAhead[0] = lookAhead[0] % np.shape(world)[0]
            lookAhead[1] = lookAhead[1] % np.shape(world)[1]
            nextVal = world[tuple(lookAhead)]

        if nextVal == 1:
            return pos
        elif nextVal == 0:
            pos = lookAhead
        else:
            raise Exception('Unhandled!')
    else:
        raise Exception('Unhandled!')

    return pos


DIRS = ("right", "down", "left", "up")
DIR_VECS = (np.array((0, 1)), np.array((1, 0)),
            np.array((0, -1)), np.array((-1, 0)))
DIR_PASSWORD = (0, 1, 2, 3)


def part_a():
    global world
    pos = np.array((0, np.where(world[0, :] == 0)[0][0]))
    facing_idx = 0
    for instruction in instructions:
        if instruction == "R":
            facing_idx = (facing_idx + 1) % len(DIRS)
        elif instruction == "L":
            facing_idx = (facing_idx - 1) % len(DIRS)
        elif instruction.isdigit():
            dir_vector = DIR_VECS[facing_idx]

            lastPos = tuple(pos)
            for _ in range(int(instruction)):
                pos = walk_one_step(pos, dir_vector)
                if tuple(pos) == lastPos:
                    break
                else:
                    lastPos = tuple(pos)

        else:
            raise Exception('Unhandled!')

    return (1000 * (pos[0] + 1)) + \
        (4 * (pos[1] + 1)) + DIR_PASSWORD[facing_idx]


answer_a = part_a()

# TODO: change
"""cube = (
    (0, 0, 1, 0),
    (2, 3, 4, 0),
    (0, 0, 5, 6),
    (0, 0, 0, 0)
)"""
cube = (
    (0, 1, 2),
    (0, 3, 0),
    (4, 5, 0),
    (6, 0, 0)
)
# face_size = 4
face_size = 50   # TODO: change
cube_faces = {}
cube_face_row_col = {}
for iRow, row in enumerate(cube):
    for iCol, val in enumerate(row):
        if val == 0:
            continue
        cube_faces[val] = world[iRow *
                                face_size:(iRow+1)*face_size, iCol*face_size:(iCol+1)*face_size]
        cube_face_row_col[val] = (iRow, iCol)


face_transforms = {}    # TODO: change
"""transforms = [
    # 1
    (
        (6, "left"),
        (4, "down"),
        (3, "down"),
        (2, "down")
    ),

    # 2
    (
        (3, "right"),
        (5, "up"),
        (6, "up"),
        (1, "down")
    ),

    # 3
    (
        (4, "right"),
        (5, "right"),
        (2, "left"),
        (1, "right")
    ),

    # 4
    (
        (6, "down"),
        (5, "down"),
        (3, "left"),
        (1, "up")
    ),

    # 5
    (
        (6, "right"),
        (2, "up"),
        (3, "up"),
        (4, "up")
    ),

    # 6
    (
        (1, "left"),
        (2, "right"),
        (5, "left"),
        (4, "left")
    )
]"""
transforms = [
    # 1
    (
        (2, "right"),
        (3, "down"),
        (4, "right"),
        (6, "right")
    ),

    # 2
    (
        (5, "left"),
        (3, "left"),
        (1, "left"),
        (6, "up")
    ),

    # 3
    (
        (2, "up"),
        (5, "down"),
        (4, "down"),
        (1, "up")
    ),

    # 4
    (
        (5, "right"),
        (6, "down"),
        (1, "right"),
        (3, "right")
    ),

    # 5
    (
        (2, "left"),
        (6, "left"),
        (4, "left"),
        (3, "up")
    ),

    # 6
    (
        (5, "up"),
        (2, "down"),
        (1, "down"),
        (4, "up")
    )
]

for i in range(len(transforms)):
    face_transforms[i+1] = transforms[i]


def rotate(pos, fromDir, toDir):
    global face_size
    transform = (fromDir, toDir)

    # welcome to the jungle :)
    if transform == ("right", "right"):
        pos[1] = 0
    elif transform == ("left", "left"):
        pos[1] = face_size - 1
    elif transform == ("down", "down"):
        pos[0] = 0
    elif transform == ("up", "up"):
        pos[0] = face_size - 1
    elif transform == ("right", "left"):
        pos[0] = face_size - pos[0] - 1
        pos[1] = face_size - 1
    elif transform == ("left", "right"):
        pos[0] = face_size - pos[0] - 1
        pos[1] = 0
    elif transform == ("up", "down"):
        pos[0] = 0
        pos[1] = face_size - pos[1] - 1
    elif transform == ("down", "up"):
        pos[0] = face_size - 1
        pos[1] = face_size - pos[1] - 1
    elif transform == ("right", "down"):
        pos[1] = face_size - pos[0] - 1
        pos[0] = 0
    elif transform == ("right", "up"):
        pos[1] = pos[0]
        pos[0] = face_size - 1
    elif transform == ("left", "down"):
        pos[1] = pos[0]
        pos[0] = 0
    elif transform == ("left", "up"):
        pos[1] = face_size - pos[0] - 1
        pos[0] = face_size - 1
    elif transform == ("down", "right"):
        pos[0] = face_size - pos[1] - 1
        pos[1] = 0
    elif transform == ("down", "left"):
        pos[0] = pos[1]
        pos[1] = face_size - 1
    elif transform == ("up", "right"):
        pos[0] = pos[1]
        pos[1] = 0
    elif transform == ("up", "left"):
        pos[0] = face_size - pos[1] - 1
        pos[1] = face_size - 1
    else:
        raise Exception('Unhandled!')

    return pos


def switch_face(pos):
    global current_cube_face, facing_idx, face_size
    face_dir = DIRS[facing_idx]

    olf_cube_face = current_cube_face
    old_facing_idx = facing_idx
    old_pos = copy.copy(pos)

    transform = face_transforms[current_cube_face][facing_idx]
    current_cube_face = transform[0]
    facing_idx = DIRS.index(transform[1])

    newPos = rotate(pos, face_dir, DIRS[facing_idx])
    if cube_faces[current_cube_face][tuple(newPos)] == 1:
        current_cube_face = olf_cube_face
        facing_idx = old_facing_idx
        return old_pos

    return newPos


def walk_one_step_part_b(pos, dir_vector):
    global cube_faces, face_size
    nextPos = pos + dir_vector
    if max(nextPos) == face_size or min(nextPos) == -1:
        nextPos = switch_face(pos)
    nextVal = cube_faces[current_cube_face][tuple(nextPos)]

    if nextVal == 0:
        pos = nextPos
    elif nextVal == 1:
        return pos
    else:
        raise Exception('Unhandled!')

    return pos


current_cube_face = 1
facing_idx = 0


def part_b():
    global cube_faces, facing_idx, current_cube_face, cube_face_row_col, face_size
    pos = np.array(
        (0, np.where(cube_faces[current_cube_face][0, :] == 0)[0][0]))

    for instruction in instructions:
        if instruction == "R":
            facing_idx = (facing_idx + 1) % len(DIRS)
        elif instruction == "L":
            facing_idx = (facing_idx - 1) % len(DIRS)
        elif instruction.isdigit():

            lastPos = tuple(pos)
            lastCubeFace = copy.copy(current_cube_face)
            for _ in range(int(instruction)):
                dir_vector = DIR_VECS[facing_idx]
                pos = walk_one_step_part_b(pos, dir_vector)
                if tuple(pos) == lastPos and current_cube_face == lastCubeFace:
                    break
                else:
                    lastPos = tuple(pos)
                    lastCubeFace = copy.copy(current_cube_face)

        else:
            raise Exception('Unhandled!')

    abs_row = (cube_face_row_col[current_cube_face]
               [0] * face_size) + pos[0] + 1
    abs_col = (cube_face_row_col[current_cube_face]
               [1] * face_size) + pos[1] + 1
    return (1000*abs_row) + (4*abs_col) + DIR_PASSWORD[facing_idx]


answer_b = part_b()
### --- --- --- ###
submit_a = False
submit_b = False

print("Answer A: {}".format(answer_a))
print("Answer B: {}".format(answer_b))

if submit_a:
    submit(answer_a, part="a", day=day, year=year)
if submit_b:
    submit(answer_b, part="b", day=day, year=year)
