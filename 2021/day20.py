# can't believe this worked...
import copy
import math
import numpy as np
from numpy.core.fromnumeric import shape
from numpy.core.numeric import Inf, Infinity

with open('input.txt') as f:
    input = f.readlines()

enhancement_algo = ""

for i,line in enumerate(input):
    if line == "\n":
        temp_image = input[i+1:]
        break
    enhancement_algo += line.replace("\n","").replace("#","1").replace(".","0")

enhancement_algo = list(enhancement_algo)
enhancement_algo = list(map(int,enhancement_algo))

image = np.zeros(shape=(len(temp_image),len(temp_image[0])-1))
for iRow in range(image.shape[0]):
    temp = list(temp_image[iRow].replace("\n","").replace("#","1").replace(".","0"))
    temp = np.array(list(map(int,temp)))
    image[iRow,:] = temp

def apply_enhancement(image):
    new_image = copy.deepcopy(image)
    for iRow in range(image.shape[0]):
        for jCol in range(image.shape[1]):
            enhance_idx = ""
            for rowOffset in range(-1,2):
                for colOffset in range(-1,2):
                    rowIndex = iRow+rowOffset
                    if rowIndex < 0 or rowIndex > image.shape[0]-1:
                        continue
                    colIndex = jCol+colOffset
                    if colIndex < 0 or colIndex > image.shape[1]-1:
                        continue
                    enhance_idx += str(int(image[rowIndex,colIndex]))
            if len(enhance_idx) < 9:
                continue
            new_image[iRow,jCol] = enhancement_algo[int(enhance_idx, 2)]
    return new_image

n_enhancements = 50
image_start = 0
image = np.pad(image, pad_width=100, mode='constant', constant_values=0)
for i in range(n_enhancements):
    image = apply_enhancement(image)
    print(i)

import matplotlib.pyplot as plt
plt.imshow(image, cmap='binary', interpolation='nearest')
plt.show()

#print(np.sum(np.sum(image[50:175,50:175]))) # 5081
print(np.sum(np.sum(image[70:260,40:260]))) # 15088

