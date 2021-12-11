import numpy as np
from numpy.core.fromnumeric import shape
import copy

with open('input.txt') as f:
    input = f.readlines()

input = list(map(lambda i:list(i.replace("\n","")), input))
input = list(map(lambda line:list(map(int,line)),input))
input = np.array(input)

n_flashes = 0
time_step = 0
while True:
    n_nines = 1
    while n_nines > 0:
        for iRow in range(input.shape[0]):
            for jCol in range(input.shape[1]):
                if input[iRow,jCol] < 9:
                    continue
                for rowOffset in range(-1,2):
                    for colOffset in range(-1,2):
                        rowIndex = iRow+rowOffset
                        if rowIndex < 0 or rowIndex > input.shape[0]-1:
                            continue
                        colIndex = jCol+colOffset
                        if colIndex < 0 or colIndex > input.shape[1]-1:
                            continue
                        if input[rowIndex,colIndex] != -1: 
                            input[rowIndex,colIndex] += 1
                input[iRow,jCol] = -1   # -1: already flashed during this time step
                n_flashes += 1
        n_nines = np.count_nonzero(input >= 9)
    input += 1
    time_step += 1
    if int(np.sum(input)) == 0:
        print(f'All flash at: {time_step}')
        break

print(f'Number of  flashes: {n_flashes}')
