from aocd import submit
from utils import parse_data, group_data_by_separator, data_replace, data_to_numpy
from retils import get_between_groups, get_after_group, get_before_group, get_digits
import numpy as np

day = 2
year = 2022

data = parse_data(day, year)
groups = group_data_by_separator(data)

answer_a = None
answer_b = None
### --- --- --- ###
answer_a = 0
answer_b = 0
score_rock = 1
score_paper = 2
score_scissors = 3
loss_score = 0
win_score = 6
draw_score = 3
for line in data:

    if line.count("A"): # rock
        if line.count("Y"): # paper, need to draw
            answer_a += win_score + score_paper
            answer_b += draw_score + score_rock
        elif line.count("Z"):   # scissors, need to win 
            answer_a += loss_score + score_scissors
            answer_b += win_score + score_paper
        elif line.count("X"):   # rock, need to lose
            answer_a += draw_score + score_rock
            answer_b += loss_score + score_scissors

    elif line.count("B"):    # paper
        if line.count("Y"):
            answer_a += draw_score + score_paper
            answer_b += draw_score + score_paper
        elif line.count("Z"):
            answer_a += win_score + score_scissors
            answer_b += win_score + score_scissors
        elif line.count("X"):
            answer_a += loss_score + score_rock
            answer_b += loss_score + score_rock
        
    elif line.count("C"):   # scissors
        if line.count("Y"):
            answer_a += loss_score + score_paper
            answer_b += draw_score + score_scissors
        elif line.count("Z"):
            answer_a += draw_score + score_scissors
            answer_b += win_score + score_rock
        elif line.count("X"):
            answer_a += win_score + score_rock
            answer_b += loss_score + score_paper




### --- --- --- ###
submit_a = False
submit_b = False

print("Answer A: {}".format(answer_a))
print("Answer B: {}".format(answer_b))

if submit_a:
    submit(answer_a, part="a", day=day, year=year)
if submit_b:
    submit(answer_b, part="b", day=day, year=year)