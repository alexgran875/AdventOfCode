from aocd import get_data
import numpy as np
import copy 

# data: list of lines
def parse_data(day = None, year = None):
    if day is None or year is None:
        with open('input.txt') as f:
            data = f.readlines()
            data = list(map(lambda i:i.replace("\n",""), data))
    else:
        data = get_data(day=day, year=year)
        data = data.split("\n")
    return data

def group_data_by_separator(data, separator = "", include_separator = False):
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

def group_data_by_size(data, size):
    assert len(data) % size == 0
    groups = []
    for i in range(int(len(data)/size)):
        groups.append(data[i*size:(i+1)*size])
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

def neighbour_matrix_looping(data_matrix = np.random.randint(0, 1, size=(10, 10))):
    # copy paste if you need to loop over a matrix while also checking the neighbours
    n_neighbours = 1
    ignore_diagonals = False
    ignore_self = True  # current cell
    wrap_around_rows = True # True: will wrap around, otherwise edge cells will have less neighbours
    wrap_around_cols = True 

    for currentRowIndex in range(np.shape(data_matrix)[0]):
        for currentColIndex in range(np.shape(data_matrix)[1]):
            # start loop over neighbours
            for rowOffset in range(-n_neighbours,1+n_neighbours):
                for colOffset in range(-n_neighbours,1+n_neighbours):

                    # diagonals
                    if rowOffset != 0 and abs(rowOffset) == abs(colOffset):    
                        if ignore_diagonals:
                            continue

                    # self (current sell)
                    if rowOffset == 0 and colOffset == 0:
                        if ignore_self:
                            continue

                    # wrap around rows
                    if wrap_around_rows:
                        neighbourRowIndex = (currentRowIndex + rowOffset) % np.shape(data_matrix)[0]
                    else:
                        neighbourRowIndex = currentRowIndex + rowOffset
                        if neighbourRowIndex < 0 or neighbourRowIndex >= np.shape(data_matrix)[0]:
                            continue

                    # wrap around cols
                    if wrap_around_cols:
                        neighbourColIndex = (currentColIndex + colOffset) % np.shape(data_matrix)[1]
                    else:
                        neighbourColIndex = currentColIndex + colOffset
                        if neighbourColIndex < 0 or neighbourColIndex >= np.shape(data_matrix)[1]:
                            continue

                    # compare current cell with neighbour
                    neighbourValue = data_matrix[neighbourRowIndex, neighbourColIndex]
                    currentValue = data_matrix[currentRowIndex, currentColIndex]
                    bp_place = 5
            # end loop over neighbours
            bp_place = 5
