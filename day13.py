import numpy as np
from numpy.core.fromnumeric import shape
import copy
import matplotlib.pyplot as plt

with open('input.txt') as f:
    input = f.readlines()

coords = []
adding_folds = False
x_folds = []
y_folds = []
folds = []
for line in input:
    if line == "\n":
        adding_folds = True
        continue

    if not adding_folds:
        coords.append(list(map(int,line.replace("\n","").split(","))))
    else:
        split = line.split("=")
        if split[0][-1] == "x":
            x_folds.append(int(split[1]))
            folds.append("x")
        else:
            y_folds.append(int(split[1]))
            folds.append("y")

coords = np.array(coords)
max_y = np.max(coords[:,0])
max_x = np.max(coords[:,1])

dots = np.zeros((2*y_folds[0]+1,2*x_folds[0]+1))

for iRow in range(coords.shape[0]):
    dots[coords[iRow,1],coords[iRow,0]] = 1


x_idx = 0
y_idx = 0
for fold in folds:
    if fold == "x":
        new_dots = dots[:,:x_folds[x_idx]]
        fold = dots[:,x_folds[x_idx]+1:]
        fold = np.flip(fold, axis=1)
        new_dots[fold == 1] = 1
        x_idx += 1
    else:
        new_dots = dots[:y_folds[y_idx],:]
        fold = dots[y_folds[y_idx]+1:,:]
        fold = np.flip(fold, axis=0)
        new_dots[fold == 1] = 1
        y_idx += 1
    dots = copy.deepcopy(new_dots)


print(np.count_nonzero(new_dots==1))

plt.imshow(new_dots, cmap='binary', interpolation='nearest')
plt.show()

