import copy
import math
import numpy as np
from numpy.core.fromnumeric import shape
from numpy.core.numeric import Inf, Infinity

with open('input.txt') as f:
    input = f.readlines()

cubes = []
class Cube():
    def __init__(self, x_min, x_max, y_min, y_max, z_min, z_max, on) -> None:
        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max
        self.z_min = z_min
        self.z_max = z_max
        self.on = on
        self.sub_cubes = []
        self.volume = self.get_volume()

    def add_sub_cube(self, sub_cube):
        """
        for cube in self.sub_cubes:
            rv = cube.get_overlapping_cube(sub_cube)
            if rv is not None:
                cube.add_sub_cube(rv)
                sub_cube.add_sub_cube(rv)
        """
        self.sub_cubes.append(sub_cube)

    def get_volume(self):
        return abs(self.x_max-self.x_min)*abs(self.y_max-self.y_min)*abs(self.z_max-self.z_min)

    def get_overlapping_cube(self, other_cube):
        x_end = min(self.x_max, other_cube.x_max)
        x_beginning = max(self.x_min, other_cube.x_min)
        if x_end < x_beginning:
            return None
        
        y_end = min(self.y_max, other_cube.y_max)
        y_beginning = max(self.y_min, other_cube.y_min)
        if y_end < y_beginning:
            return None
        
        z_end = min(self.z_max, other_cube.z_max)
        z_beginning = max(self.z_min, other_cube.z_min)
        if z_end < z_beginning:
            return None

        return Cube(x_beginning, x_end, y_beginning, y_end, z_beginning, z_end, other_cube.on)
        
    def find_sub_overlaps(self):
        for i in range(len(self.sub_cubes)):
            for j in range(len(self.sub_cubes)):
                if i == j:
                    continue
                sub_overlap = self.sub_cubes[i].get_overlapping_cube(self.sub_cubes[j])
                if sub_overlap is None:
                    continue
                else:
                    self.sub_cubes[i].add_sub_cube(sub_overlap)
                    self.sub_cubes[j].add_sub_cube(sub_overlap)
                    
        


    def get_delta_n_on(self, delta_n_on):
        for i in range(len(self.sub_cubes)):
            for j in range(len(self.sub_cubes)):
                if i == j:
                    continue
                sub_overlap = self.sub_cubes[i].get_overlapping_cube(self.sub_cubes[j])
                if sub_overlap is None:
                    continue
                else:
                    x = 5
            """
            if sub_cube.on:
                delta_n_on[0] -= sub_cube.volume    # sub volume has been counted twice
            else:
                delta_n_on[0] -= 2*sub_cube.volume
            """
        




n_on = 0
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

    new_cube = Cube(x_min, x_max, y_min, y_max, z_min, z_max, on)
    for cube in cubes:
        overlapping_cube = cube.get_overlapping_cube(new_cube)
        if overlapping_cube is not None:
            cube.add_sub_cube(overlapping_cube)
            new_cube.add_sub_cube(overlapping_cube)

    if on:
        cubes.append(new_cube)
        n_on += new_cube.volume


delta_n_on = [0]
for cube in cubes:
    cube.find_sub_overlaps()
    #cube.get_delta_n_on(delta_n_on)

n_on += delta_n_on[0]

x = 5   

