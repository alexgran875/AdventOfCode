import copy
import math
import numpy as np
from numpy.core.fromnumeric import shape
from numpy.core.numeric import Inf, Infinity

player1_score = 0
player2_score = 0
player1_pos = 6
player2_pos = 7

last_die_num = 0
n_rolls = 0
while True:
    dice_rolls = list(map(lambda a: a % 100, list(range(last_die_num+1,last_die_num+4))))
    dice_sum = sum(dice_rolls)
    if 0 in dice_rolls:
        dice_sum += 100
    player1_pos += dice_sum
    player1_pos = player1_pos % 10
    if player1_pos == 0:
        player1_pos = 10
    player1_score += player1_pos
    n_rolls += 3
    if player1_score >= 1000:
        break

    dice_rolls = list(map(lambda a: a % 100, list(range(last_die_num+4,last_die_num+7))))
    dice_sum = sum(dice_rolls)
    if 0 in dice_rolls:
        dice_sum += 100
    player2_pos += dice_sum
    player2_pos = player2_pos % 10
    if player2_pos == 0:
        player2_pos = 10
    player2_score += player2_pos
    n_rolls += 3
    if player2_score >= 1000:
        break
    last_die_num += 6
    
print(min([player1_score,player2_score])*n_rolls)


