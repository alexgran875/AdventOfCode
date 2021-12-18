import copy
import math
#import numpy as np
#from numpy.core.fromnumeric import shape
#from numpy.core.numeric import Inf, Infinity
import ast

with open('input.txt') as f:
    input = f.readlines()
input = list(map(lambda i: i.replace("\n",""),input))
input_listed = list(map(ast.literal_eval,input))

def add_snailfish_numbers(number1, number2):
    return [number1, number2]

def recursive(number):
    if not isinstance(number,int):
        for i in range(len(number)):
            recursive(number[i])
    else:
        x = 5

def send_explosion_recusrively(recursed_number,explosion,dir):
    if dir=="right":
        for i in range(len(recursed_number)):
            if isinstance(recursed_number[i],int):
                recursed_number[i] += explosion
                return 0
            else:
                if send_explosion_recusrively(recursed_number[i],explosion,dir) == 0:
                    return 0
    elif dir=="left":
        for i in list(reversed(list(range(len(recursed_number))))):
            if isinstance(recursed_number[i],int):
                recursed_number[i] += explosion
                return 0
            else:
                if send_explosion_recusrively(recursed_number[i],explosion,dir) == 0:
                    return 0


def explode(whole_number,recursed_number,depth):
    if depth == 4 and not isinstance(recursed_number,int) and len(recursed_number) == 2:
        return [recursed_number, "fuu"]
    if not isinstance(recursed_number,int):
        for i in range(len(recursed_number)):
            explosion = explode(whole_number,recursed_number[i],depth+1)
            if explosion is None:
                continue
            else:
                if explosion[1] == "fuu":
                    recursed_number[i] = 0
                    explosion = explosion[0]
                else:
                    if explosion[0] and explosion[1]:
                        recursed_number[i] = 0
            if explosion[1] and i+1 < len(recursed_number):
                if isinstance(recursed_number[i+1],int):
                    recursed_number[i+1] += explosion[1]
                    explosion[1] = 0
                else:
                    explosion[1] = send_explosion_recusrively(recursed_number[i+1],explosion[1],"right")
            if explosion[0] and i-1 >= 0:
                if isinstance(recursed_number[i-1],int):    
                    recursed_number[i-1] += explosion[0]
                    explosion[0] = 0
                else:
                    explosion[0] = send_explosion_recusrively(recursed_number[i-1],explosion[0],"left")
            return explosion

def split(whole_number,recursed_number,depth):
    if not isinstance(recursed_number,int):
        for i in range(len(recursed_number)):
            if isinstance(recursed_number[i],int) and recursed_number[i] >= 10:
                recursed_number[i] = [math.floor(recursed_number[i]/2),math.ceil(recursed_number[i]/2)]
                return "done" # only do one split
            else:
                if split(whole_number,recursed_number[i],depth+1) == "done":
                    return "done"


# while exploding until no change
# while splitting until no change


#temp = add_snailfish_numbers(input_listed[0],input_listed[1])
#recursive(input_listed)
#split(input_listed,input_listed,-1)
#explode(input,input_listed,-1)
#temp = str(input_listed[0])
#print(temp)

def explode_all(summarized):
    while True:
        # keep exploding
        pre_explode = copy.deepcopy(summarized)
        explode(input,summarized,0)
        if pre_explode == summarized:
            break
        #print(summarized)

def calc_magnitude(recursed_number):
    for i in range(len(recursed_number)):
        if isinstance(recursed_number[i],int): 
            try:
                return 3*recursed_number[0] + 2*recursed_number[1]
            except TypeError:
                continue
        else:
            rv = calc_magnitude(recursed_number[i])
            if rv is not None:
                recursed_number[i] = rv


def get_magnitude(number1, number2):
    summarized = add_snailfish_numbers(number1,number2)
    #print(summarized)
    while True:
        pre_reduction = copy.deepcopy(summarized)
        explode_all(summarized)
        #print(summarized)
        split(input,summarized,0)
        #print(summarized)
        if pre_reduction == summarized:
            break
    while not isinstance(summarized[0],int):
        calc_magnitude(summarized)
    return summarized[0]*3 + summarized[1]*2

#print(get_magnitude(number1=[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]], number2=[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]))

highest_magnitude = 0
max_it = len(input_listed)**2
total_it = 0
for i in range(len(input_listed)):
    for j in range(len(input_listed)):
        if i == j:
            continue
        rv = get_magnitude(input_listed[i],input_listed[j])
        if rv > highest_magnitude:
            highest_magnitude = rv
        total_it += 1
        print(f'{(total_it)/max_it}')

print(highest_magnitude)
