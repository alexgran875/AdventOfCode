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

                    """
                    if old_risklevels[rowIndex,colIndex] < 0:
                        # don't compare to -1 and -2
                        continue
                    """

                    if input[rowIndex,colIndex] > input[iRow,jCol]:
                        if input[rowIndex,colIndex] != 9:
                            new_risklevels[rowIndex,colIndex] = -1

            #if old_risklevels[iRow,jCol] == -1:
            #    new_risklevels[iRow,jCol] = -2

    arrays_equal = np.array_equal(old_risklevels,new_risklevels)
    old_risklevels = copy.deepcopy(new_risklevels)

basin_id = -3
id_risklevels = copy.deepcopy(new_risklevels)
prev_id_risklevels = copy.deepcopy(id_risklevels)
all_idd = False
while not all_idd:
    for iRow in range(np.shape(input)[0]):
        for jCol in range(np.shape(input)[1]):

            if  id_risklevels[iRow,jCol] >= 0:
                # not part of basin
                continue
            
            neighbour_vals = []

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

                    neighbour_vals.append(id_risklevels[rowIndex,colIndex])
            
            min_val = min(neighbour_vals)
            if min_val >= -2:
                # no ID yet assigned to this basin
                id_risklevels[iRow,jCol] = basin_id
                if basin_id == -19:
                    x = 5
                basin_id -= 1
            else:
                id_risklevels[iRow,jCol] = min_val

    all_idd = np.array_equal(prev_id_risklevels,id_risklevels)
    prev_id_risklevels = copy.deepcopy(id_risklevels)

(unique, counts) = np.unique(id_risklevels, return_counts=True)
frequencies = np.asarray((unique, counts)).T

print(np.prod(np.flip(np.sort(counts))[1:4]))
