import numpy as np
import copy 

# data: list of lines
def parse_data():
    with open('input.txt') as f:
        data = f.readlines()
        data = list(map(lambda i:i.replace("\n",""), data))
        return data

def group_data(data, separator = "", include_separator = False):
    groups = []
    tmp = []
    for line in data:
        if line == separator:
            if include_separator:
                tmp.append(line)
            groups.append(tmp)
            tmp = []
        else:
            tmp.append(line)
    if tmp != []:
        groups.append(tmp)
    return groups

def data_replace(data, replacements):
    # replacements: list of string tuples (old, new)
    new_data = copy.deepcopy(data)
    for replacement in replacements:
        for i, line in enumerate(new_data):
            new_data[i] = line.replace(replacement[0], replacement[1])
    return new_data
    
def data_to_numpy(data, dtype = np.int64):
    new_data = copy.deepcopy(data)
    new_data = list(map(list, new_data))
    new_data = np.array(new_data, dtype=dtype)
    return new_data
