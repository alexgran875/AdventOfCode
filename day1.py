import numpy as np

with open('input1.txt') as f:
    input = f.readlines()

a = []

prev_reading = ""
larger_meas = 0
for i in range(len(input)):
    current_meas = int(input[i].split("\n")[0])

    if prev_reading == "":
        prev_reading = current_meas
    else:
        if current_meas > prev_reading:
            larger_meas += 1
        prev_reading = current_meas

print(larger_meas)

for i in range(len(input)):
    current_meas = int(input[i].split("\n")[0])
    a.append(current_meas)

def moving_average(a, n=3) :
    ret = np.cumsum(a, dtype=float)
    ret[n:] = ret[n:] - ret[:-n]
    return ret[n - 1:] / n


ma_3 = moving_average(a)
prev_reading = ""
larger_meas = 0
for i in range(len(ma_3)):
    current_meas = ma_3[i]

    if prev_reading == "":
        prev_reading = current_meas
    else:
        if current_meas > prev_reading:
            larger_meas += 1
        prev_reading = current_meas

print(larger_meas)




