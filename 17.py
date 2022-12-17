from aocd import submit
from utils import parse_data, group_data_by_separator, group_data_by_size, data_replace, data_to_numpy
from retils import get_between_groups, get_after_group, get_before_group, get_digits
import numpy as np
import copy
import functools
from enum import Enum
import hashlib

day = 17
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


class Point(Enum):
    EMPTY = 0
    STATIC = 1
    DRAW_ORIGO = 2  # still moving
    MOVING = 3


board = np.zeros((8, 9))
board[:, 0] = Point.STATIC.value
board[:, -1] = Point.STATIC.value
board[-1, :] = Point.STATIC.value


def add_row():
    global board
    newRow = np.zeros((1, board.shape[1]))
    newRow[0, 0] = Point.STATIC.value
    newRow[0, -1] = Point.STATIC.value
    board = np.vstack((newRow, board))


class Rock(Enum):
    HLINE = 0
    PLUS = 1
    L = 2
    VLINE = 3
    BLOCK = 4


def draw_rock(drawOrigoPos, rockType):
    global board
    board[drawOrigoPos] = Point.DRAW_ORIGO.value
    ptType = Point.MOVING.value
    if rockType == Rock.HLINE:
        board[drawOrigoPos[0], drawOrigoPos[1] +
              1:drawOrigoPos[1]+4] = ptType
    elif rockType == Rock.PLUS:
        board[drawOrigoPos[0]-1:drawOrigoPos[0]+2,
              drawOrigoPos[1]+1] = ptType
        board[drawOrigoPos[0], drawOrigoPos[1]+2] = ptType
    elif rockType == Rock.L:
        board[drawOrigoPos[0], drawOrigoPos[1]+1:drawOrigoPos[1]+3] = ptType
        board[drawOrigoPos[0]-2:drawOrigoPos[0], drawOrigoPos[1]+2] = ptType
    elif rockType == Rock.VLINE:
        board[drawOrigoPos[0]-3:drawOrigoPos[0],
              drawOrigoPos[1]] = ptType
    elif rockType == Rock.BLOCK:
        board[drawOrigoPos[0]-1, drawOrigoPos[1]:drawOrigoPos[1]+2] = ptType
        board[drawOrigoPos[0], drawOrigoPos[1]+1] = ptType


class Direction(Enum):
    LEFT = 0
    RIGHT = 1
    DOWN = 2


def jet_to_dir(jet):
    if jet == ">":
        return Direction.RIGHT
    elif jet == "<":
        return Direction.LEFT


def move_rock(drawOrigoPos, direction, rockType):
    global board
    board[board != Point.STATIC.value] = Point.EMPTY.value
    if direction == Direction.LEFT:
        newPos = (drawOrigoPos[0], drawOrigoPos[1]-1)
    elif direction == Direction.RIGHT:
        newPos = (drawOrigoPos[0], drawOrigoPos[1]+1)
    elif direction == Direction.DOWN:
        newPos = (drawOrigoPos[0]+1, drawOrigoPos[1])
    draw_rock(newPos, rockType)
    return newPos


def get_non_static_pts(drawOrigoPos, rockType):
    global board
    points = [drawOrigoPos]
    if rockType == Rock.HLINE:
        for i in range(drawOrigoPos[1] + 1, drawOrigoPos[1]+4):
            points.append((drawOrigoPos[0], i))
    elif rockType == Rock.PLUS:
        for i in range(drawOrigoPos[0]-1, drawOrigoPos[0]+2):
            points.append((i, drawOrigoPos[1]+1))
        points.append((drawOrigoPos[0], drawOrigoPos[1]+2))
    elif rockType == Rock.L:
        for i in range(drawOrigoPos[1]+1, drawOrigoPos[1]+3):
            points.append((drawOrigoPos[0], i))
        for i in range(drawOrigoPos[0]-2, drawOrigoPos[0]):
            points.append((i, drawOrigoPos[1]+2))
    elif rockType == Rock.VLINE:
        for i in range(drawOrigoPos[0]-3, drawOrigoPos[0]):
            points.append((i, drawOrigoPos[1]))
    elif rockType == Rock.BLOCK:
        for i in range(drawOrigoPos[1], drawOrigoPos[1]+2):
            points.append((drawOrigoPos[0]-1, i))
        points.append((drawOrigoPos[0], drawOrigoPos[1]+1))
    return points


def is_movement_possible(direction, drawOrigoPos, rockType):
    global board
    points = get_non_static_pts(drawOrigoPos, rockType)
    lowest_row = points[0][0]
    movement_possible = True
    if direction == Direction.LEFT:
        for pos in points:
            if pos[0] < lowest_row:
                lowest_row = pos[0]
            if board[pos[0], pos[1]-1] == Point.STATIC.value:
                movement_possible = False
    elif direction == Direction.RIGHT:
        for pos in points:
            if pos[0] < lowest_row:
                lowest_row = pos[0]
            if board[pos[0], pos[1]+1] == Point.STATIC.value:
                movement_possible = False
    elif direction == Direction.DOWN:
        for pos in points:
            if pos[0] < lowest_row:
                lowest_row = pos[0]
            if board[pos[0]+1, pos[1]] == Point.STATIC.value:
                movement_possible = False
    return (movement_possible, lowest_row)


rock_order = [Rock.HLINE, Rock.PLUS, Rock.L, Rock.VLINE, Rock.BLOCK]


def get_next_rock(currentRockType):
    global rock_order
    index = rock_order.index(currentRockType)
    return rock_order[(index+1) % len(rock_order)]


movement_dirs = list(map(jet_to_dir, lines[0]))


def get_next_dir_index(movement_index):
    global movement_dirs
    return (movement_index+1) % len(movement_dirs)


def add_rows(lowestRow):
    need_space_above = 7    # 3 + 4
    diff = need_space_above - lowestRow
    allTimeLowestRow = lowestRow
    for _ in range(max(diff, 0)):
        allTimeLowestRow += 1
        add_row()
    return allTimeLowestRow


class State():
    def __init__(self, board, drawOrigoPos, rockType, movement_index, n_rocks_stopped, n_removed_rows):
        self.board = copy.copy(board)
        self.drawOrigoPos = drawOrigoPos
        self.rockType = rockType
        self.movement_index = movement_index
        self.n_rocks_stopped = n_rocks_stopped
        self.n_removed_rows = n_removed_rows

    def __hash__(self):
        h = hashlib.sha256()
        h.update(self.board.tobytes())
        h.update(str(self.drawOrigoPos).encode())
        h.update(str(self.rockType).encode())
        h.update(str(self.movement_index).encode())
        return int(h.hexdigest(), 16)

    def __eq__(self, other):
        return (self.board == other.board).all() and self.drawOrigoPos == other.drawOrigoPos and self.rockType == other.rockType and self.movement_index == other.movement_index


past_states = set()
drawOrigoPos = (board.shape[0]-5, 3)
allTimeLowestRow = board.shape[0]-1
rockType = rock_order[0]
movement_index = 0
direction = movement_dirs[movement_index]
n_rocks_stopped = 0
n_rocks_to_simulate = 1000000000000
max_board_height = 50
n_removed_rows = 0
initial_delay = 3000    # n rocks to wait before start saving states
found_period = False
while n_rocks_stopped < n_rocks_to_simulate:
    draw_rock(drawOrigoPos, rockType)
    if n_rocks_stopped > initial_delay and not found_period:
        newState = State(board, drawOrigoPos, rockType,
                         movement_index, n_rocks_stopped, n_removed_rows)
        if newState in past_states:
            past_states_list = list(past_states)
            pastState = past_states_list[past_states_list.index(newState)]
            n_rocks_per_period = newState.n_rocks_stopped - pastState.n_rocks_stopped
            n_periods = (n_rocks_to_simulate -
                         n_rocks_stopped) // n_rocks_per_period
            n_rocks_stopped += n_periods * n_rocks_per_period
            n_rows_removed_per_period = newState.n_removed_rows - pastState.n_removed_rows
            n_removed_rows += n_periods * n_rows_removed_per_period
            found_period = True
            continue
        else:
            past_states.add(newState)
    movementPossible, _ = is_movement_possible(
        direction, drawOrigoPos, rockType)
    if movementPossible:
        drawOrigoPos = move_rock(drawOrigoPos, direction, rockType)
    movement_index = get_next_dir_index(movement_index)
    direction = movement_dirs[movement_index]
    movementPossible, lowestRow = is_movement_possible(
        Direction.DOWN, drawOrigoPos, rockType)
    if not movementPossible:
        n_rocks_stopped += 1
        if n_rocks_stopped == 2022:
            answer_a = (board.shape[0] - 1) - allTimeLowestRow + n_removed_rows
        if lowestRow < allTimeLowestRow:
            allTimeLowestRow = lowestRow
        board[drawOrigoPos] = Point.STATIC.value
        board[board == Point.MOVING.value] = Point.STATIC.value
        rockType = get_next_rock(rockType)
        allTimeLowestRow = add_rows(allTimeLowestRow)
        drawOrigoPos = (allTimeLowestRow - 4, 3)
        if rockType == Rock.PLUS:
            drawOrigoPos = (drawOrigoPos[0]-1, drawOrigoPos[1])
        if board.shape[0] > max_board_height:
            n_delete = board.shape[0] - max_board_height
            board = np.delete(board, slice(
                board.shape[0]-n_delete, board.shape[0]+1), 0)
            n_removed_rows += n_delete
            assert board.shape[0] == max_board_height
        continue
    drawOrigoPos = move_rock(drawOrigoPos, Direction.DOWN, rockType)

answer_b = (board.shape[0] - 1) - allTimeLowestRow + n_removed_rows

### --- --- --- ###
submit_a = False
submit_b = False

print("Answer A: {}".format(answer_a))
print("Answer B: {}".format(answer_b))

if submit_a:
    submit(answer_a, part="a", day=day, year=year)
if submit_b:
    submit(answer_b, part="b", day=day, year=year)
