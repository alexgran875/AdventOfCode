from utils import parse_data
data = parse_data()

data = list(map(int, data))

for i in data:
    for j in data:
        for k in data:
            if i + j + k == 2020:
                print(i * j * k)


