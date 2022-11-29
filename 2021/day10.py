import numpy as np
from numpy.core.fromnumeric import shape
import copy

with open('input.txt') as f:
    input = f.readlines()

input = list(map(lambda line:line.replace("\n",""), input))

closing_chars = {'(':')',
                '[':']',
                '{':'}',
                '<':'>'}
mistake_pts = {')':3,
                ']':57,
                '}':1197,
                '>':25137}
closing_pts = {')':1,
                ']':2,
                '}':3,
                '>':4}
openings = ['(', '[', '{', '<']
pts = 0

scores = []
for i,line in enumerate(input):
    legal_closings_chars = []
    line_incomplete = False
    for char in line:

        if char in openings:
            legal_closings_chars.append(closing_chars[char])
        elif char == legal_closings_chars[-1]:
            legal_closings_chars.pop(-1)
        else:
            pts += mistake_pts[char]
            line_incomplete = True
            break

    if line_incomplete:
        continue

    closing_score = 0
    for i in range(len(legal_closings_chars)):
        index = len(legal_closings_chars) - i - 1
        closing_score = (closing_score*5) + closing_pts[legal_closings_chars[index]]
    scores.append(closing_score)

print(str(pts))
scores = np.sort(scores)
answer2 = scores[int(len(scores)/2)]
print(str(answer2))

