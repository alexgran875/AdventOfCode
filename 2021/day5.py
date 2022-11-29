import numpy as np

with open('input.txt') as f:
    input = f.readlines()

input = list(map(lambda line:line.replace("->",",").replace(" ", "").replace("\n","").split(","), input))
input = list(map(lambda line:list(map(lambda element:int(element), line)), input))

n_overlaps = np.zeros((2000,2000))

for line in input:
    x1 = line[0]
    x2 = line[2]
    y1 = line[1]
    y2 = line[3]
    
    if x1==x2:
        # vertical line
        y_vals = list(range(min(y1,y2), max(y1,y2)+1))
        for y in y_vals:
            n_overlaps[y,x1] += 1     
    elif y1==y2:
        # horizontal line
        x_vals = list(range(min(x1,x2), max(x1,x2)+1))
        for x in x_vals:
            n_overlaps[y1,x] += 1     
    else:
        # diagonal line
        x_start = min(x1,x2)
        x_end = max(x1,x2)+1
        x_vals = list(range(x_start, x_end))

        if line.index(x_start) == 0:
            y_start = y1
            y_end = y2
        else:
            y_start = y2
            y_end = y1
        k = np.sign(y_end-y_start)

        for i,x in enumerate(x_vals):
            n_overlaps[y_start+i*k,x] += 1  

print(len(n_overlaps[n_overlaps>=2]))


