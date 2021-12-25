import copy
import math
import numpy as np
from numpy.core.fromnumeric import partition, shape
from numpy.core.numeric import Inf, Infinity

with open('input.txt') as f:
    input = f.readlines()

class Cube():
    def __init__(self, x_min, x_max, y_min, y_max, z_min, z_max, on, addition_order) -> None:
        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max
        self.z_min = z_min
        self.z_max = z_max
        self.on = on
        self.addition_order = addition_order

    def get_volume(self):
        return abs(self.x_max-self.x_min)*abs(self.y_max-self.y_min)*abs(self.z_max-self.z_min)

    def get_overlapping_cube(self, other_cube):
        # TODO: maybe just less than on the comparison?
        x_end = min(self.x_max, other_cube.x_max)
        x_beginning = max(self.x_min, other_cube.x_min)
        if x_end <= x_beginning:
            return None
        
        y_end = min(self.y_max, other_cube.y_max)
        y_beginning = max(self.y_min, other_cube.y_min)
        if y_end <= y_beginning:
            return None
        
        z_end = min(self.z_max, other_cube.z_max)
        z_beginning = max(self.z_min, other_cube.z_min)
        if z_end <= z_beginning:
            return None

        biggest_addition_order = max(self.addition_order,other_cube.addition_order)
        if other_cube.addition_order > self.addition_order:
            state = other_cube.on
        else:
            state = self.on

        return Cube(x_beginning, x_end, y_beginning, y_end, z_beginning, z_end, state, biggest_addition_order)

    def equal_to(self, other_cube):
        if self.x_min != other_cube.x_min or self.x_max != other_cube.x_max:
            return False
            
        if self.y_min != other_cube.y_min or self.y_max != other_cube.y_max:
            return False

        if self.z_min != other_cube.z_min or self.z_max != other_cube.z_max:
            return False

        return True


    def subtract_cube(self, overlapping_cube):
        # TODO: make sure it doesn't double count the sides!!!
        # assert the volume at the end
        # does not return the overlapping cube
        cubes = []
        x_pairings = [(min(self.x_min,overlapping_cube.x_min),overlapping_cube.x_min),
        (min(self.x_max,overlapping_cube.x_max),self.x_max),
        (overlapping_cube.x_min,overlapping_cube.x_max)]

        y_pairings = [(min(self.y_min,overlapping_cube.y_min),overlapping_cube.y_min),
        (min(self.y_max,overlapping_cube.y_max),self.y_max),
        (overlapping_cube.y_min,overlapping_cube.y_max)]

        z_pairings = [(min(self.z_min,overlapping_cube.z_min),overlapping_cube.z_min),
        (min(self.z_max,overlapping_cube.z_max),self.z_max),
        (overlapping_cube.z_min,overlapping_cube.z_max)]

        for x_pair in x_pairings:
            for y_pair in y_pairings:
                for z_pair in z_pairings:
                    if x_pair == (overlapping_cube.x_min, overlapping_cube.x_max) \
                    and y_pair == (overlapping_cube.y_min, overlapping_cube.y_max) \
                    and z_pair == (overlapping_cube.z_min, overlapping_cube.z_max):
                        continue
                        
                    cubes.append(Cube(x_pair[0],x_pair[1],y_pair[0],y_pair[1],z_pair[0],z_pair[1],self.on,self.addition_order))

        total_volume = overlapping_cube.get_volume()
        for cube in cubes:
            total_volume += cube.get_volume()

        assert total_volume == self.get_volume()

        return cubes

# TODO: what happens when the overlap is just a single plane (ie only area and no volume?)

def get_octadran_ids(cube):
    ids = []
    if cube.x_min <= 0 and cube.y_min <= 0 and cube.z_min <= 0:
        ids.append(0)
    if cube.x_min <= 0 and cube.y_min <= 0 and cube.z_min > 0:
        ids.append(1)
    if cube.x_min <= 0 and cube.y_min > 0 and cube.z_min <= 0:
        ids.append(2)
    if cube.x_min <= 0 and cube.y_min > 0 and cube.z_min > 0:
        ids.append(3)
    if cube.x_min > 0 and cube.y_min <= 0 and cube.z_min <= 0:
        ids.append(4)
    if cube.x_min > 0 and cube.y_min <= 0 and cube.z_min > 0:
        ids.append(5)
    if cube.x_min > 0 and cube.y_min > 0 and cube.z_min <= 0:
        ids.append(6)
    if cube.x_min > 0 and cube.y_min > 0 and cube.z_min > 0:
        ids.append(7)
    
    return ids
    

i = 0
i_max = len(input)
octadrans = [ [] for _ in range(8) ]
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

    new_cubes = [Cube(x_min, x_max, y_min, y_max, z_min, z_max, on, i)]
    # AIM: cubes only contains cubes with no overlap!
    # 0: x <= 0, y <= 0, z <= 0
    # BINARY
    octadran_ids = get_octadran_ids(new_cubes[0])
    cubes = set()
    for id in octadran_ids:
        cubes.update(octadrans[id])
        octadrans[id] = []

    cubes = list(cubes)
    no_additional_checking_needed = []
    while len(new_cubes) > 0:
        # TODO: no point of a for loop for new cubes since there is an outer while loop,
        # just index new_cubes[0]
        new_cube = new_cubes[-1]
        has_overlaps = False
        for cube in cubes:
            overlapping_cube = cube.get_overlapping_cube(new_cube)
            if overlapping_cube is not None:
                same_cube = new_cube.equal_to(overlapping_cube)
                has_overlaps = True
            if overlapping_cube is not None and not same_cube:
                # break all the cubes into smaller cubes and readd them
                part_cubes_1 = cube.subtract_cube(overlapping_cube)
                part_cubes_2 = new_cube.subtract_cube(overlapping_cube)

                delta_volume = 2*overlapping_cube.get_volume()
                for part_cube_1 in part_cubes_1:
                    delta_volume += part_cube_1.get_volume()
                for part_cube_2 in part_cubes_2:
                    delta_volume += part_cube_2.get_volume()
                delta_volume -= (cube.get_volume() + new_cube.get_volume())
                assert delta_volume == 0

                cubes.remove(cube)
                #cubes.extend(part_cubes_1)
                no_additional_checking_needed.extend(part_cubes_1)
                if overlapping_cube.on:
                    #cubes.append(overlapping_cube)
                    no_additional_checking_needed.append(overlapping_cube)

                new_cubes.remove(new_cube)
                new_cubes.extend(part_cubes_2)
                break
                #new_cubes.extend(part_cubes_1)
                #new_cubes.append(overlapping_cube)
            elif overlapping_cube is not None and same_cube:
                # same cube, just update its state
                if new_cube.addition_order > cube.addition_order:
                    # TODO: only larger than instead of equal?
                    cube.on = new_cube.on
                    cube.addition_order = new_cube.addition_order
                new_cubes.remove(new_cube)
                break
            
        if not has_overlaps:
            # new_cube had no overlaps, add it
            new_cubes.remove(new_cube)
            if new_cube.on:
                # only add if it is on
                #cubes.append(new_cube)
                no_additional_checking_needed.append(new_cube)
            else:
                x = 5
            break

    for cube in cubes:
        cube_ids = get_octadran_ids(cube)
        for id in cube_ids:
            assert cube.on
            octadrans[id].append(cube)

    for cube in no_additional_checking_needed:
        cube_ids = get_octadran_ids(cube)
        for id in cube_ids:
            assert cube.on
            octadrans[id].append(cube)


final_cubes = set()
for i in range(len(octadrans)):
    final_cubes.update(octadrans[i])

n_on = 0
for cube in final_cubes:
    assert cube.on
    n_on += cube.get_volume()

print(n_on)

