from utils import parse_data, group_data_by_separator
import numpy as np
data = parse_data()
groups = group_data_by_separator(data)

all_cals = []
for group in groups:
    tmp = 0
    for line in group:
        if line.isdigit():
            tmp += int(line)
    all_cals.append(tmp)

all_cals = np.array(all_cals, dtype=np.int32)
all_cals.sort()
print(all_cals[-1])
print(np.sum(all_cals[-3:]))
