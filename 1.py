from utils import parse_data
import numpy as np
data = parse_data()

all_cals = []
tmp = 0
for line in data:
    if line.isdigit():
        tmp += int(line)
    if line == "":
        all_cals.append(tmp)
        tmp = 0

all_cals = np.array(all_cals, dtype=np.int32)
all_cals.sort()
print(all_cals[-1])
print(np.sum(all_cals[-3:]))
