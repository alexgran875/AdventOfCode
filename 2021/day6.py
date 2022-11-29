import numpy as np
from collections import deque

with open('input.txt') as f:
    input = f.readlines()

input[0] = input[0].replace("\n","").replace(" ", "").replace("\'","")
input = input[0].split(",")
input = list(map(int, input))
lanternfish = np.array(input)

for day in range(80):
    lanternfish -= 1
    new_lanternfish = len(lanternfish[lanternfish == -1])*[8]
    lanternfish = np.hstack((lanternfish,new_lanternfish))
    lanternfish[lanternfish == -1] = 6 

print(len(lanternfish))
    
num_lanternfish = {}
for i in range(-1,9):
    num_lanternfish[i] = 0

for fish in input:
    num_lanternfish[fish] += 1

def rotate_values(my_dict):
    # no need to cast the keys to list
    values_deque = deque(my_dict.values())
    values_deque.rotate(-1)
    return dict(zip(my_dict.keys(), values_deque))

for day in range(256):
    num_lanternfish = rotate_values(num_lanternfish)
    num_lanternfish[8] += num_lanternfish[-1]
    num_lanternfish[6] += num_lanternfish[-1]
    num_lanternfish[-1] = 0
    #print(f'{day/256}')

total_num_lanternfish = 0
for key in num_lanternfish:
    total_num_lanternfish += num_lanternfish[key]
print(total_num_lanternfish)

