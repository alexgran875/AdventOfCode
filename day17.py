import pygad
import numpy
import copy
import math
import numpy as np
from numpy.core.fromnumeric import shape
from numpy.core.numeric import Inf, Infinity

with open('input.txt') as f:
    input = f.readlines()

x_min = int(input[0].split("..")[0].split("=")[-1])
x_max = int(input[0].split("..")[1].split(",")[0])
y_min = int(input[0].split("..")[1].split("=")[-1])
y_max = int(input[0].split("..")[-1])

"""
def eval_fitness(x_vel, y_vel):
    x_pos = 0
    y_pos = 0
    y_highest = 0
    while True:
        if x_pos > x_max:
            return -1
        if y_min > y_pos:
            return -1
        if x_min <= x_pos <= x_max and y_min <= y_pos <= y_max:
            return y_highest
        x_pos += x_vel
        y_pos += y_vel
        if y_pos > y_highest:
            y_highest = y_pos
        if x_vel > 0:
            x_vel -= 1
        elif x_vel < 0:
            x_vel += 1
        y_vel -= 1   

print(eval_fitness(6,9))
"""
"""
y_highest = -Infinity
for x_vel in range(1000):
    for y_vel in range(1000):
        x_pos = (x_vel+1)*x_vel/2
        y_pos = (y_vel+1)*y_vel/2
        if x_min <= x_pos <= x_max and y_pos > y_highest:
            y_highest = y_pos
print(y_highest)
"""

"""
y_highest = -Infinity
for y_vel in range(1,1000):
    y_pos = (y_vel+1)*y_vel/2

    coeff = [1,1,-2*(y_pos - y_min)]
    t = np.max(np.roots(coeff))
    if t.is_integer() and y_pos > y_highest:
        y_highest = y_pos
"""
"""
valid_y_pos = list(range(y_min,y_max+1))
valid_trajectories = 0
for x_vel in range(1,35):
    x_pos = (x_vel+1)*x_vel/2
    if x_min <= x_pos <= x_max:
        for y_vel in range(-15,15):
            x_og = x_vel
            y_og = y_vel
            if y_vel > 0:
                y_pos = (y_vel+1)*y_vel/2
                y_vel = 0
            elif y_vel < 0:
                y_pos = 0
            dist_to_cover = y_pos - y_min
            t = round(math.sqrt(dist_to_cover * 2)) + 1
            for i in range(1,t):
                y_pos += y_vel
                y_vel -= 1
                if y_pos in valid_y_pos:
                    print(f'{x_og},{y_og}')
                    valid_trajectories += 1
                    break
"""

valid_y_pos = list(range(y_min,y_max+1))
valid_x_pos = list(range(x_min,x_max+1))
valid_trajectories = 0
iteration = 0
iteration_max = 1000*2000
for x_vel_ranged in range(1,1000):
    for y_vel_ranged in range(-1000,1000):
        x_vel = x_vel_ranged
        y_vel = y_vel_ranged

        x_pos = 0
        y_pos = 0
        while True:
            if x_pos > x_max:
                break
            if y_min > y_pos:
                break
            if x_min <= x_pos <= x_max and y_min <= y_pos <= y_max:
                valid_trajectories += 1
                break

            x_pos += x_vel
            y_pos += y_vel
            if x_vel > 0:
                x_vel -= 1
            elif x_vel < 0:
                x_vel += 1
            y_vel -= 1
        iteration += 1
        print(f'{iteration/iteration_max}')   

print(valid_trajectories)
x = 5
