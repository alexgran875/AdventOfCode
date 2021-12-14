import numpy as np
from numpy.core.fromnumeric import shape
import copy

with open('input.txt') as f:
    input = f.readlines()

template = input[0].replace("\n","")
pattern_to_idx = {}
idx_to_element = [0]*100
list_unique_elements = []
for i,line in enumerate(input):
    if i <= 1:
        continue
    for element in [line[0],line[1],line[6]]:
        if element not in list_unique_elements:
            list_unique_elements.append(element)
    pattern = line[0]+line[1]
    pattern_to_idx[pattern] = str(len(idx_to_element))
    idx_to_element.append(line[6])

def insert_into_string(string, insertion, idx):
    return string[:idx+1] + str(insertion) + string[idx+1:]

for time_step in range(40):
    idx_inserted = []
    for key in pattern_to_idx.keys():
        while template.count(key) > 0:
            template = insert_into_string(template,pattern_to_idx[key],template.index(key))
            idx_inserted.append(int(pattern_to_idx[key]))
    for i in range(len(idx_inserted)):
        template = template.replace(str(idx_inserted[i]),idx_to_element[idx_inserted[i]])
    print(time_step)

count = []
for element in list_unique_elements:
    count.append(template.count(element)) 
print(f'{max(count)-min(count)}')

x = 5

