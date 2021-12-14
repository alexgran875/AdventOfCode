import numpy as np
from numpy.core.fromnumeric import shape
import copy

with open('input.txt') as f:
    input = f.readlines()

template = input[0].replace("\n","")
match_to_new_patterns = {}
pattern_count = {}
element_count = {}
for i in range(len(template)):
    if i == len(template) - 1:
        break
    key = template[i]+template[i+1]
    if key not in pattern_count:
        pattern_count[key] = 1
    else:
        pattern_count[key] += 1

    if template[i] not in element_count:
        element_count[template[i]] = 1
    else:
        element_count[template[i]] += 1

if template[i] not in element_count:
    element_count[template[i]] = 1
else:
    element_count[template[i]] += 1

for i,line in enumerate(input):
    if i <= 1:
        continue

    pattern1 = line[0] + line[6]
    pattern2 = line[6] + line[1]
    match = line[0] + line[1]
    match_to_new_patterns[match] = [pattern1, pattern2]


new_pattern_count = copy.deepcopy(pattern_count)
for time_step in range(40):
    for match in match_to_new_patterns.keys():
        if match in pattern_count:
            patterns_to_add_to = match_to_new_patterns[match]
            num_matches = pattern_count[match]
            if patterns_to_add_to[0][1] not in element_count:
                element_count[patterns_to_add_to[0][1]] = num_matches
            else:
                element_count[patterns_to_add_to[0][1]] += num_matches
            new_pattern_count[match] -= pattern_count[match]
            if patterns_to_add_to[0] in new_pattern_count:
                new_pattern_count[patterns_to_add_to[0]] += num_matches
            else:
                new_pattern_count[patterns_to_add_to[0]] = num_matches
            
            if patterns_to_add_to[1] in new_pattern_count:
                new_pattern_count[patterns_to_add_to[1]] += num_matches
            else:
                new_pattern_count[patterns_to_add_to[1]] = num_matches


    pattern_count = copy.deepcopy(new_pattern_count)


print(f'{max(element_count.values())-min(element_count.values())}')

