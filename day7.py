import numpy as np
import copy

with open('input.txt') as f:
    input = f.readlines()

input = input[0].replace(" ", "").replace("\n", "").split(",")
input = list(map(int,input))

min_pos = min(input)
max_pos = max(input)
positions = list(range(min_pos,max_pos+1))
distances = np.zeros((len(input),len(positions)))
positions = np.array(positions)

for iCrab in range(len(input)):
    distances[iCrab,:] = np.abs(positions - input[iCrab])

fuel_cost = np.sum(distances, axis=0)
print(np.min(fuel_cost))

new_distances = copy.deepcopy(distances)
for iCrab in range(len(input)):
    crab_pos = input[iCrab]
    left_side = np.flip(np.cumsum(np.flip(distances[iCrab,:crab_pos])))
    right_side = np.cumsum(distances[iCrab,crab_pos:])
    new_distances[iCrab,:] = np.hstack((left_side, right_side))

new_fuel_cost = np.sum(new_distances, axis=0)
print(np.min(new_fuel_cost))


