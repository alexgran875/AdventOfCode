import copy
import math
import numpy as np
from numpy.core.fromnumeric import shape
from numpy.core.numeric import Inf, Infinity

with open('input.txt') as f:
    input = f.readlines()

on_coords = set()
i = 0
i_max = len(input)
for line in input:
    i += 1
    print(f'{i/i_max}')

    x_min = int(line.split("x=")[1].split("..")[0])
    x_max = int(line.split(",y=")[0].split("..")[1])
    y_min = int(line.split(",y=")[1].split("..")[0])
    y_max = int(line.split(",z=")[0].split("..")[-1])
    z_min = int(line.split(",z=")[-1].replace("\n","").split("..")[0])
    z_max = int(line.split(",z=")[-1].replace("\n","").split("..")[-1])
    if line.count("on"):
        on = True
    else:
        on = False

    """
    if x_max < -50 or y_max < -50 or z_max < -50:
        continue
    if x_min > 50 or y_min > 50 or z_min > 50:
        continue
    x_min = max(x_min,-50)
    y_min = max(y_min,-50)
    z_min = max(z_min,-50)
    x_max = min(x_max,50)
    y_max = min(y_max,50)
    z_max = min(z_max,50)
    """
    
    for x in range(x_min,x_max+1):
        for y in range(y_min,y_max+1):
            for z in range(z_min,z_max+1):
                if on:
                    on_coords.add((x,y,z))
                else:
                    if (x,y,z) in on_coords:
                        on_coords.remove((x,y,z))
    

print(len(on_coords))

