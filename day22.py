import copy
import math
import numpy as np
from numpy.core.fromnumeric import partition, shape
from numpy.core.numeric import Inf, Infinity

with open('input.txt') as f:
    input = f.readlines()

def retired_algo(input):
    on_coords = set()
    for line in input:
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
        for x in range(x_min,x_max+1):
            for y in range(y_min,y_max+1):
                for z in range(z_min,z_max+1):
                    if on:
                        on_coords.add((x,y,z))
                    else:
                        if (x,y,z) in on_coords:
                            on_coords.remove((x,y,z))  
    return len(on_coords)

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
        self.volume = None

    def get_volume(self):
        # right now actually counts the number of points within, not just the volume
        if self.volume is not None:
            return self.volume
        self.volume = (abs(self.x_max-self.x_min)+1)*(abs(self.y_max-self.y_min)+1)*(abs(self.z_max-self.z_min)+1)
        return self.volume

    def get_overlapping_cube(self, other_cube):
        # STRICTLY SMALLER THAN! (CHECKED!)
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

        biggest_addition_order = max(self.addition_order,other_cube.addition_order)
        if other_cube.addition_order > self.addition_order:
            state = other_cube.on
        else:
            state = self.on

        return Cube(x_beginning, x_end, y_beginning, y_end, z_beginning, z_end, state, biggest_addition_order)

    def equal_to(self, other_cube):
        if self.get_volume() != other_cube.get_volume():
            return False
        if self.x_min != other_cube.x_min or self.x_max != other_cube.x_max:
            return False
        if self.y_min != other_cube.y_min or self.y_max != other_cube.y_max:
            return False
        if self.z_min != other_cube.z_min or self.z_max != other_cube.z_max:
            return False
        return True

    def subtract_cube(self, overlapping_cube):
        cubes = []
        x_pairings = [(min(self.x_min,overlapping_cube.x_min),overlapping_cube.x_min-1),
        (min(self.x_max,overlapping_cube.x_max)+1,self.x_max),
        (overlapping_cube.x_min,overlapping_cube.x_max)]

        y_pairings = [(min(self.y_min,overlapping_cube.y_min),overlapping_cube.y_min-1),
        (min(self.y_max,overlapping_cube.y_max)+1,self.y_max),
        (overlapping_cube.y_min,overlapping_cube.y_max)]

        z_pairings = [(min(self.z_min,overlapping_cube.z_min),overlapping_cube.z_min-1),
        (min(self.z_max,overlapping_cube.z_max)+1,self.z_max),
        (overlapping_cube.z_min,overlapping_cube.z_max)]

        copied_pairings = copy.deepcopy(x_pairings)
        for x_pair in x_pairings:
            if x_pair[0] > x_pair[1]:
                copied_pairings.remove(x_pair)
        x_pairings = copy.deepcopy(copied_pairings)

        copied_pairings = copy.deepcopy(y_pairings)
        for y_pair in y_pairings:
            if y_pair[0] > y_pair[1]:
                copied_pairings.remove(y_pair)
        y_pairings = copy.deepcopy(copied_pairings)

        copied_pairings = copy.deepcopy(z_pairings)
        for z_pair in z_pairings:
            if z_pair[0] > z_pair[1]:
                copied_pairings.remove(z_pair)
        z_pairings = copy.deepcopy(copied_pairings)
                    
        for x_pair in x_pairings:
            for y_pair in y_pairings:
                for z_pair in z_pairings:
                    if x_pair == (overlapping_cube.x_min, overlapping_cube.x_max) \
                    and y_pair == (overlapping_cube.y_min, overlapping_cube.y_max) \
                    and z_pair == (overlapping_cube.z_min, overlapping_cube.z_max):
                        continue

                    cube = Cube(x_pair[0],x_pair[1],y_pair[0],y_pair[1],z_pair[0],z_pair[1],self.on,self.addition_order)
                    if cube.get_volume() != 0:
                        cubes.append(cube)

        total_volume = overlapping_cube.get_volume()
        for cube in cubes:
            total_volume += cube.get_volume()

        if total_volume != self.get_volume():
            x = 5
            for x_pair in x_pairings:
                for y_pair in y_pairings:
                    for z_pair in z_pairings:
                        if x_pair == (overlapping_cube.x_min, overlapping_cube.x_max) \
                        and y_pair == (overlapping_cube.y_min, overlapping_cube.y_max) \
                        and z_pair == (overlapping_cube.z_min, overlapping_cube.z_max):
                            continue
                            
                        cube = Cube(x_pair[0],x_pair[1],y_pair[0],y_pair[1],z_pair[0],z_pair[1],self.on,self.addition_order)
                        if cube.get_volume() != 0:
                            cubes.append(cube)
        
        assert total_volume == self.get_volume()

        return cubes

    def split_cube_across_borders(self):
        if self.x_min < 0 and self.x_max >= 0:
            return [Cube(self.x_min,-1,self.y_min,self.y_max,self.z_min,self.z_max,self.on,self.addition_order),
            Cube(0,self.x_max,self.y_min,self.y_max,self.z_min,self.z_max,self.on,self.addition_order)]

        if self.y_min < 0 and self.y_max >= 0:
            return [Cube(self.x_min,self.x_max,self.y_min,-1,self.z_min,self.z_max,self.on,self.addition_order),
            Cube(self.x_min,self.x_max,0,self.y_max,self.z_min,self.z_max,self.on,self.addition_order)]

        if self.z_min < 0 and self.z_max >= 0:
            return [Cube(self.x_min,self.x_max,self.y_min,self.y_max,self.z_min,-1,self.on,self.addition_order),
            Cube(self.x_min,self.x_max,self.y_min,self.y_max,0,self.z_max,self.on,self.addition_order)]

        return [self]

# TODO: what happens when the overlap is just a single plane (ie only area and no volume?)

def get_octadran_ids(cube):
    ids = []
    if cube.x_min < 0 and cube.y_min < 0 and cube.z_min < 0:
        ids.append(0)
    if cube.x_min < 0 and cube.y_min < 0 and cube.z_min > 0:
        ids.append(1)
    if cube.x_min < 0 and cube.y_min > 0 and cube.z_min < 0:
        ids.append(2)
    if cube.x_min < 0 and cube.y_min < 0 and cube.z_min < 0:
        ids.append(3)
    if cube.x_min < 0 and cube.y_min < 0 and cube.z_min < 0:
        ids.append(4)
    if cube.x_min < 0 and cube.y_min < 0 and cube.z_min < 0:
        ids.append(5)
    if cube.x_min < 0 and cube.y_min < 0 and cube.z_min < 0:
        ids.append(6)
    if cube.x_min > 0 and cube.y_min > 0 and cube.z_min > 0:
        ids.append(7)
    
    return ids
    


i = 0
i_max = len(input)
octadrans = [ [] for _ in range(8) ]
cubes = []
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
    prev_len = len(new_cubes)
    new_len = prev_len
    while True:
        splitup_new_cubes = []
        for c in new_cubes:
            splitup_new_cubes.extend(c.split_cube_across_borders())
        new_cubes = copy.deepcopy(splitup_new_cubes)
        new_len = len(new_cubes)
        if new_len == prev_len:
            break
        else:
            prev_len = new_len 

    # AIM: cubes only contains cubes with no overlap!
    # 0: x <= 0, y <= 0, z <= 0
    # BINARY
    """
    octadran_ids = get_octadran_ids(new_cubes[0])
    cubes = set()
    for id in octadran_ids:
        cubes.update(octadrans[id])
        octadrans[id] = []
    cubes = list(cubes)
    """
    cube_volumes = 0
    for tt in cubes:
        cube_volumes += tt.get_volume()    # 225476 supposed to be after 1.0, 293390 in the end (currently 295214, 1824 too many)
                                    # 67914 unique ons, new cube 71550 area, thus 3636 overlap
    new_cubes_volume = 0
    for tt in new_cubes:
        new_cubes_volume += tt.get_volume() 

    no_additional_checking_needed = []
    while len(new_cubes) > 0:
        new_cube = new_cubes[-1]
        if new_cube.get_volume() == 0:
            new_cubes.remove(new_cube)
            continue
        has_overlaps = False
        same_cube = False
        for cube in cubes:
            if new_cube.equal_to(cube):
                same_cube = True
                break
            overlapping_cube = cube.get_overlapping_cube(new_cube)
            if overlapping_cube is not None:
                has_overlaps = True
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
                no_additional_checking_needed.extend(part_cubes_1)
                if overlapping_cube.on:
                    no_additional_checking_needed.append(overlapping_cube)

                new_cubes.remove(new_cube)
                new_cubes.extend(part_cubes_2)

                confirmed_unoverlapping_volume = 0
                new_cubes_volume2 = 0
                cubes_volume2 = 0
                part_cubes2_volume = 0
                for tt in no_additional_checking_needed:
                    confirmed_unoverlapping_volume += tt.get_volume()
                for tt in new_cubes:
                    new_cubes_volume2 += tt.get_volume()
                for tt in cubes:
                    cubes_volume2 += tt.get_volume()
                for tt in part_cubes_2:
                    part_cubes2_volume += tt.get_volume()
                break
        
        if same_cube:
            # same cube, just update its state
            if new_cube.addition_order > cube.addition_order:
                # TODO: only larger than instead of equal?
                cube.on = new_cube.on
                cube.addition_order = new_cube.addition_order
            new_cubes.remove(new_cube)  
        elif not has_overlaps:
            # new_cube had no overlaps, add it
            new_cubes.remove(new_cube)
            if new_cube.on:
                no_additional_checking_needed.append(new_cube)
            else:
                x = 5


    cubes.extend(no_additional_checking_needed)
    
    """
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
    """

"""
final_cubes = set()
for i in range(len(octadrans)):
    final_cubes.update(octadrans[i])

n_on = 0
for cube in final_cubes:
    assert cube.on
    n_on += cube.get_volume()
"""
n_on = 0
for cube in cubes:
    assert cube.on
    n_on += cube.get_volume()

print(n_on)
print(retired_algo(input))
"""
for i in range(len(cubes)):
    if cubes[i].get_volume() <= 1824:
        print(f'{i}:{cubes[i].get_volume()}')

x = 5
"""