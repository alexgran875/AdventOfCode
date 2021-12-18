import numpy
import copy
import math
import numpy as np
from numpy.core.fromnumeric import shape
from numpy.core.numeric import Inf, Infinity
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
                send_explosion_recusrively(recursed_number[i],explosion,dir)
    elif dir=="left":
        for i in list(reversed(list(range(len(recursed_number))))):
            if isinstance(recursed_number[i],int):
                recursed_number[i] += explosion
                return 0
            else:
                send_explosion_recusrively(recursed_number[i],explosion,dir)


def explode(whole_number,recursed_number,depth):
    if depth == 4 and not isinstance(recursed_number,int) and len(recursed_number) == 2:
        return recursed_number
    if not isinstance(recursed_number,int):
        for i in range(len(recursed_number)):
            explosion = explode(whole_number,recursed_number[i],depth+1)
            if explosion is None:
                continue
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

#temp = add_snailfish_numbers(input_listed[0],input_listed[1])
#recursive(input_listed)
explode(input_listed,input_listed,-1)
temp = str(input_listed[0])
print(temp)

x = 5
