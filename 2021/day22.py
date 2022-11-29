import copy

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
        self.volume = None

    def get_volume(self):
        # actually counts the number of points, so volume + area of faces
        if self.volume is not None:
            return self.volume
        self.volume = (abs(self.x_max-self.x_min)+1)*(abs(self.y_max-self.y_min)+1)*(abs(self.z_max-self.z_min)+1)
        return self.volume

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
        if self.equal_to(overlapping_cube):
            return []
        cubes = []
        x_pairings = [(self.x_min,overlapping_cube.x_min-1),
        (overlapping_cube.x_min,overlapping_cube.x_max),
        (overlapping_cube.x_max+1,self.x_max)]

        y_pairings = [(self.y_min,overlapping_cube.y_min-1),
        (overlapping_cube.y_min,overlapping_cube.y_max),
        (overlapping_cube.y_max+1,self.y_max)]

        z_pairings = [(self.z_min,overlapping_cube.z_min-1),
        (overlapping_cube.z_min,overlapping_cube.z_max),
        (overlapping_cube.z_max+1,self.z_max)]

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
        assert total_volume == self.get_volume()

        return cubes

i = 0
i_max = len(input)
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
    while len(new_cubes) > 0:
        has_overlaps = False
        new_cube = new_cubes[-1]
        for cube in cubes:
            overlapping_cube = cube.get_overlapping_cube(new_cube)
            if overlapping_cube is None:
                continue
            if overlapping_cube.on:
                cubes.append(overlapping_cube)

            new_cubes.remove(new_cube)
            new_cubes.extend(new_cube.subtract_cube(overlapping_cube))

            cubes.remove(cube)
            cubes.extend(cube.subtract_cube(overlapping_cube))
            has_overlaps = True
            break
        if not has_overlaps:
            new_cubes.remove(new_cube)
            if new_cube.on:
                cubes.append(new_cube)
    
n_on = 0
for cube in cubes:
    assert cube.on
    n_on += cube.get_volume()
print(n_on) # 1325473814582641
