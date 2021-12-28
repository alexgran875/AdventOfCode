import copy
import numpy as np

with open('input.txt') as f:
    input = f.readlines()

grid = []
for line in input:
    tmp = list(line.replace("\n","").replace(">","1").replace("v","2").replace(".","0"))
    tmp = list(map(int,tmp))
    for i in range(len(tmp)):
        if tmp[i] == 2:
            tmp[i] = -1
    grid.append(tmp)

grid = np.array(grid)
prev_grid = copy.deepcopy(grid)
time_step = 0
while True:
    # east update (1)
    for iRow in range(prev_grid.shape[0]):
        for jCol in range(prev_grid.shape[1]):
            if prev_grid[iRow,jCol] != 1:
                continue
            colIndex = jCol+1
            if colIndex > prev_grid.shape[1]-1:
                colIndex = 0
            if prev_grid[iRow,colIndex] == 0:
                grid[iRow,colIndex] = 1
                grid[iRow,jCol] = 0
    tmp_grid = copy.deepcopy(grid)
    # south update (-1)
    for iRow in range(prev_grid.shape[0]):
        for jCol in range(prev_grid.shape[1]):
            if tmp_grid[iRow,jCol] != -1:
                continue
            rowIndex = iRow+1
            if rowIndex > tmp_grid.shape[0]-1:
                rowIndex = 0
            if tmp_grid[rowIndex,jCol] == 0:
                grid[rowIndex,jCol] = -1
                grid[iRow,jCol] = 0
    time_step += 1
    print(time_step)
    if np.array_equal(prev_grid,grid):
        break
    else:
        prev_grid = copy.deepcopy(grid)

x = 5
