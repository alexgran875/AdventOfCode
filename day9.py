import numpy as np
from numpy.core.fromnumeric import shape
import copy

with open('input.txt') as f:
    input = f.readlines()

input = list(map(lambda line:line.replace("\n",""),input))
input = list(map(lambda line:list(map(int,line)),input))
input = np.array(input)

risk_levels = np.zeros(shape=np.shape(input))
for iRow in range(np.shape(input)[0]):
    for jCol in range(np.shape(input)[1]):
        higher_or_equal_count = 0

        for rowOffset in range(-1,2):
            for colOffset in range(-1,2):

                if (rowOffset == colOffset) or (rowOffset == -colOffset):
                    continue

                rowIndex = iRow+rowOffset
                if rowIndex < 0 or rowIndex > np.shape(input)[0]-1:
                    continue

                colIndex = jCol+colOffset
                if colIndex < 0 or colIndex > np.shape(input)[1]-1:
                    continue

                if input[iRow,jCol] >= input[rowIndex,colIndex]:
                    higher_or_equal_count += 1

        if higher_or_equal_count == 0:
            risk_levels[iRow,jCol] = input[iRow,jCol] + 1

print(np.sum(risk_levels))

risk_levels[risk_levels != 0] = -1
arrays_equal = False
old_risklevels = copy.deepcopy(risk_levels)
new_risklevels = copy.deepcopy(risk_levels)
while not arrays_equal:
    for iRow in range(np.shape(input)[0]):
        for jCol in range(np.shape(input)[1]):
            for rowOffset in range(-1,2):
                for colOffset in range(-1,2):
                    if old_risklevels[iRow,jCol] != -1:
                        # only check the -1 since they need exploring
                        continue

                    if (rowOffset == colOffset) or (rowOffset == -colOffset):
                        continue

                    rowIndex = iRow+rowOffset
                    if rowIndex < 0 or rowIndex > np.shape(input)[0]-1:
                        continue

                    colIndex = jCol+colOffset
                    if colIndex < 0 or colIndex > np.shape(input)[1]-1:
                        continue

                    if old_risklevels[rowIndex,colIndex] < 0:
                        # don't compare to -1 and -2
                        continue

                    if input[rowIndex,colIndex] != 9 and input[rowIndex,colIndex] > input[iRow,jCol]:
                        new_risklevels[rowIndex,colIndex] = -1

            if old_risklevels[iRow,jCol] == -1:
                new_risklevels[iRow,jCol] = -2

    arrays_equal = np.array_equal(old_risklevels,new_risklevels)
    old_risklevels = new_risklevels

x = 5

