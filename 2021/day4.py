import numpy as np
from numpy.core.fromnumeric import shape

numbers_drawn = "23,30,70,61,79,49,19,37,64,48,72,34,69,53,15,74,89,38,46,36,28,32,45,2,39,58,11,62,97,40,14,87,96,94,91,92,80,99,6,31,57,98,65,10,33,63,42,17,47,66,26,22,73,27,7,0,55,8,56,29,86,25,4,12,51,60,35,50,5,75,95,44,16,93,21,3,24,52,77,76,43,41,9,84,67,71,83,88,59,68,85,82,1,18,13,78,20,90,81,54"
numbers_drawn = numbers_drawn.split(",")
numbers_drawn = list(map(int, numbers_drawn))

with open('input.txt') as f:
    input = f.readlines()
input = input[2:]

boards = np.zeros(shape=(5,5,100))
false_boards = np.array(boards.copy(), dtype=bool)
marked_numbers = None
boards_won = []
i = 0
for line in input:
    board_idx = int(np.floor(i/6))
    line_idx = i % 6
    i += 1
    if line == "\n":
        continue
    board_numbers = line.split("\n")[0].split()
    board_numbers = np.array(list(map(int, board_numbers)), dtype=int)
    boards[line_idx,:,board_idx] = board_numbers.copy()

all_boards_finished = False
for number in numbers_drawn:
    new_marked_numbers = (boards[:,:,:] == number)
    if np.all(marked_numbers) == None:
        marked_numbers = new_marked_numbers
    else:
        marked_numbers = marked_numbers + new_marked_numbers

    boards_to_check = np.array(np.sum(np.sum(new_marked_numbers, 0), 0), dtype=bool)
    boards_to_check = marked_numbers[:,:,boards_to_check]
    row_sums = np.sum(boards_to_check, 0)
    col_sums = np.sum(boards_to_check, 1)
    row_victory = np.sum(row_sums == 5, 0)
    col_victory = np.sum(col_sums == 5, 0)
    victory = np.array(row_victory + col_victory, dtype=bool)

    if np.any(victory):
        for i in range(np.shape(victory)[0]):
            if victory[i] == False:
                continue
            mask = np.reshape(boards_to_check[:,:,i], (5,5,1))
            winning_board_idx = (marked_numbers == mask)
            winning_board_idx = np.sum(np.sum(winning_board_idx, 0), 0) == 25
            winning_board_idx = np.where(winning_board_idx==True)[0]

            idx = winning_board_idx[0]
            
            if (len(boards_won) == 0 or len(boards_won) == 99) and idx not in boards_won:
                winning_board = boards[:,:,idx]
                unmarked_numbers_idx = ~marked_numbers[:,:,idx]
                sum_unmarked_numbers = np.sum(winning_board[unmarked_numbers_idx])
                print(f"Won: {sum_unmarked_numbers*number}")
   
            if idx not in boards_won:
                boards_won.append(idx)
                if len(boards_won) == 100:
                    all_boards_finished = True
                    break

    if all_boards_finished:
        break

    if number == numbers_drawn[-1]:
        idx = boards_won[-1]
        winning_board = boards[:,:,idx]
        unmarked_numbers_idx = ~marked_numbers[:,:,idx]
        sum_unmarked_numbers = np.sum(winning_board[unmarked_numbers_idx])
        print(f"Won: {sum_unmarked_numbers*number}")
    
