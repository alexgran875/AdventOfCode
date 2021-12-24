import copy
import math
import numpy as np
from numpy.core.fromnumeric import shape
from numpy.core.numeric import Inf, Infinity

player1_score = 0
player2_score = 0
player1_pos = 4
player2_pos = 8

def play_game(player1_pos, player1_score, player2_pos, player2_score, player_turn, total_scores, n_universes, prev_rolls, prev_pos):
    dice_rolls = [1,2,3]
    #next_scores = [0,0,0]
    #next_pos = [0,0,0]
    n_universes[0] += 3
    for i,roll in enumerate(dice_rolls):
        if player_turn == 1:
            player1_next_pos = player1_pos + roll
            player1_next_pos = player1_next_pos % 10
            if player1_next_pos == 0:
                player1_next_pos = 10
            player1_score_next = player1_score + player1_next_pos 
            #next_scores[i] = player1_score_next
            #next_pos[i] = player1_next_pos
            if player1_score_next >= 21:
                total_scores[0] += 1 
            else:
                temp = copy.deepcopy(prev_rolls)
                temp.append(roll)
                temp2 = copy.deepcopy(prev_pos)
                temp2.append([player1_next_pos, player2_pos])
                play_game(player1_next_pos, player1_score_next, player2_pos, player2_score, 2, total_scores, n_universes, temp, temp2)
        elif player_turn == 2:
            player2_next_pos = player2_pos + roll
            player2_next_pos = player2_next_pos % 10
            if player2_next_pos == 0:
                player2_next_pos = 10
            player2_score_next = player2_score + player2_next_pos
            #next_scores[i] = player2_score_next
            #next_pos[i] = player2_next_pos
            if player2_score_next >= 21:
                total_scores[1] += 1
            else:
                temp = copy.deepcopy(prev_rolls)
                temp.append(roll)
                temp2 = copy.deepcopy(prev_pos)
                temp2.append([player1_pos, player2_next_pos])
                play_game(player1_pos, player1_score, player2_next_pos, player2_score_next, 1, total_scores, n_universes, temp, temp2)

     x = 5
    """
    for i in range(len(next_scores)):
        if next_scores[i] >= 21:
            continue
        else:
            if player_turn == 1:
                play_game(next_pos[i], next_scores[i], player2_pos, player2_score, 2, total_scores)
            elif player_turn == 2:
                play_game(player1_pos, player1_score, next_pos[i], next_scores[i], 1, total_scores)
    """
n_universes = [0]
total_scores = [0,0]
prev_rolls = []
prev_pos = [[player1_pos, player2_pos]]
play_game(player1_pos, player1_score, player2_pos, player2_score, 1, total_scores, n_universes, prev_rolls, prev_pos)
print(max(total_scores))

