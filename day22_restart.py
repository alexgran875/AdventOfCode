import copy

with open('input.txt') as f:
    input = f.readlines()

class Floor():
    def __init__(self,minx,maxx,miny,maxy) -> None:
        self.rectangles = [[minx,maxx,miny,maxy]]

    def add_rectangle(self,minx,maxx,miny,maxy):
        new_rectangles = [[minx,maxx,miny,maxy]]
        while len(new_rectangles) > 0:
            has_intersection = False
            new_rect = new_rectangles[0]
            for rect in self.rectangles:
                inter_x_end = min(rect[1], new_rect[1])
                inter_x_start = max(rect[0], new_rect[0])
                if inter_x_end < inter_x_start:
                    continue
                
                inter_y_end = min(rect[3], new_rect[3])
                inter_y_start = max(rect[2], new_rect[2])
                if inter_y_end < inter_y_start:
                    continue
                
                overlapping_rect = [inter_x_start,inter_x_end,inter_y_start,inter_y_end]
                self.rectangles.append(overlapping_rect)

                new_rectangles.remove(new_rect)
                new_rectangles.extend(self.subtract_rect(new_rect,overlapping_rect))

                self.rectangles.remove(rect)
                self.rectangles.extend(self.subtract_rect(rect,overlapping_rect))
                has_intersection = True
                break
            if not has_intersection:
                new_rectangles.remove(new_rect)
                self.rectangles.append(new_rect)

    def remove_rectangle(self,minx,maxx,miny,maxy):
        new_rectangles = [[minx,maxx,miny,maxy]]
        while len(new_rectangles) > 0:
            has_intersection = False
            new_rect = new_rectangles[0]
            for rect in self.rectangles:
                inter_x_end = min(rect[1], new_rect[1])
                inter_x_start = max(rect[0], new_rect[0])
                if inter_x_end < inter_x_start:
                    continue
                
                inter_y_end = min(rect[3], new_rect[3])
                inter_y_start = max(rect[2], new_rect[2])
                if inter_y_end < inter_y_start:
                    continue
                
                overlapping_rect = [inter_x_start,inter_x_end,inter_y_start,inter_y_end]

                new_rectangles.remove(new_rect)
                new_rectangles.extend(self.subtract_rect(new_rect,overlapping_rect))

                self.rectangles.remove(rect)
                self.rectangles.extend(self.subtract_rect(rect,overlapping_rect))
                has_intersection = True
                break
            if not has_intersection:
                new_rectangles.remove(new_rect)

    def subtract_rect(self,og_rect,overlap):
        if tuple(og_rect) == tuple(overlap):
            return []
        new_rectangles = []
        x_pairings = [(og_rect[0],overlap[0]-1),
                (overlap[0],overlap[1]),
                (overlap[1]+1,og_rect[1])]
        y_pairings = [(og_rect[2],overlap[2]-1),
                (overlap[2],overlap[3]),
                (overlap[3]+1,og_rect[3])]

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

        for x_pair in x_pairings:
            for y_pair in y_pairings:
                if x_pair == (overlap[0],overlap[1]) and y_pair == (overlap[2],overlap[3]):
                    continue
                tmp_rct = [x_pair[0],x_pair[1],y_pair[0],y_pair[1]]
                new_rectangles.append(tmp_rct)
                assert self.get_pts_within_rect(tmp_rct) != 0

        total_pts = self.get_pts_within_rect(overlap)
        for rct in new_rectangles:
            total_pts += self.get_pts_within_rect(rct)
        assert total_pts == self.get_pts_within_rect(og_rect)

        return new_rectangles

    def get_pts_within_rect(self,rectangle):
        return (abs(rectangle[1]-rectangle[0])+1)*(abs(rectangle[3]-rectangle[2])+1)

    def get_n_on(self):
        n_sum = 0
        for rectangle in self.rectangles:
            n_sum += self.get_pts_within_rect(rectangle)
        return n_sum


i = 0
i_max = len(input)
floors = {}
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

    if on:
        for z in range(z_min,z_max+1):
            if z not in floors:
                floors[z] = Floor(x_min,x_max,y_min,y_max)
            else:
                floors[z].add_rectangle(x_min,x_max,y_min,y_max)
    else:
        for z in range(z_min,z_max+1):
            if z in floors:
                floors[z].remove_rectangle(x_min,x_max,y_min,y_max)

n_on = 0
for z in floors.keys():
    n_on += floors[z].get_n_on() 

print(f'Current: {n_on}') # 1325473814582641

