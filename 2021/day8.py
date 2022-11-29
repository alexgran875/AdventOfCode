import numpy as np
from numpy.core.fromnumeric import shape
import copy
from numpy.lib.function_base import append

with open('input.txt') as f:
    input = f.readlines()

output = list(map(lambda line: line.split("|")[1].split(), input))

n_appearances = 0
for line in output:
    for signal in line:
        if len(signal) in [2,4,3,7]:
            n_appearances += 1

print(n_appearances)

def get_signals_of_len(signals,length):
    rv = []
    for signal in signals:
        if len(signal) == length:
            rv.append(''.join(sorted(signal)))
    return rv

def get_diff_between_strings(string1, string2):
    first_set = set(string1)
    second_set = set(string2)
    return list(first_set.symmetric_difference(second_set))[0]

def get_union_between_strings(string1, string2):
    rv = list(set(string1)&set(string2))
    rv.sort()
    return rv

def sort_string(string1):
    sorted_characters = sorted(string1)    
    return "".join(sorted_characters)

def list_to_str(char_list):
    return ''.join(char_list)

answer2 = 0
for line in input:
    all_patterns = line.replace("|","").split()

    one = get_signals_of_len(all_patterns,2)[0]
    four = get_signals_of_len(all_patterns,4)[0]
    seven = get_signals_of_len(all_patterns,3)[0]
    eight = get_signals_of_len(all_patterns,7)[0]
    
    zero_six_nine = get_signals_of_len(all_patterns,6)
    nine = list(map(lambda signal: get_union_between_strings(signal,four),zero_six_nine))
    for i in range(len(nine)):
        if len(nine[i]) == 4:
            nine = list_to_str(zero_six_nine[i])
            break
    
    zero_six = [value for value in zero_six_nine if value != nine]
    union_one = list(map(lambda i: get_union_between_strings(i,one),zero_six))
    for i in range(len(union_one)):
        if len(union_one[i]) == 2:
            zero = zero_six[i]
        elif len(union_one[i]) == 1:
            six = zero_six[i]

    two_three_five = get_signals_of_len(all_patterns,5)
    union_one_2 = list(map(lambda i: get_union_between_strings(i,one),two_three_five))
    for i in range(len(union_one_2)):
        if len(union_one_2[i]) == 2:
            three = two_three_five[i]
            
    two_five = [value for value in two_three_five if value != three]
    union_four = list(map(lambda i: get_union_between_strings(i,four),two_five))
    for i in range(len(union_four)):
        if len(union_four[i]) == 3:
            five = two_five[i]
            
    two = [value for value in two_five if value != five][0]

    decoded = [zero, one, two, three, four, five, six, seven, eight, nine]

    output = line.split("|")[1].split()
    output = list(map(lambda i:sort_string(i),output))

    resulting_number = ""
    for i in range(len(output)):
        resulting_number += str(decoded.index(output[i]))
    answer2 += int(resulting_number)

print(answer2)

