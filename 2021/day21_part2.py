from functools import lru_cache

player1_score = 0
player2_score = 0
player1_pos = 6
player2_pos = 7

@lru_cache(maxsize=None)
def play_game(player1_pos, player1_score, player2_pos, player2_score, player_turn):
    dice_rolls = [1,2,3]
    rv = [0,0]
    for roll1 in dice_rolls:
        for roll2 in dice_rolls:
            for roll3 in dice_rolls:
                if player_turn == 1:
                    player1_next_pos = player1_pos + roll1 + roll2 + roll3
                    player1_next_pos = player1_next_pos % 10
                    if player1_next_pos == 0:
                        player1_next_pos = 10
                    player1_score_next = player1_score + player1_next_pos
                    if player1_score_next >= 21:
                        rv[0] += 1
                    else:
                        scores = play_game(player1_next_pos, player1_score_next, player2_pos, player2_score, 2)
                        rv[0] += scores[0]
                        rv[1] += scores[1]
                elif player_turn == 2:
                    player2_next_pos = player2_pos + roll1 + roll2 + roll3
                    player2_next_pos = player2_next_pos % 10
                    if player2_next_pos == 0:
                        player2_next_pos = 10
                    player2_score_next = player2_score + player2_next_pos
                    if player2_score_next >= 21:
                        rv[1] += 1
                    else:
                        scores = play_game(player1_pos, player1_score, player2_next_pos, player2_score_next, 1)
                        rv[0] += scores[0]
                        rv[1] += scores[1]
    return rv

victories = play_game(player1_pos, player1_score, player2_pos, player2_score, 1)
print(victories)

