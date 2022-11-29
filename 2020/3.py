from utils import parse_data
import numpy as np

data = parse_data()
data = list(map(lambda i: i.replace("#", "1"), data))
data = list(map(lambda i: i.replace(".", "0"), data))
data = list(map(lambda i: list(map(int, list(i))), data))
data = np.array(data)

rows = data.shape[0]
cols = data.shape[1]

def get_trees(delta_rows, delta_cols):
    pos = (0, 0)
    n_trees = 0
    while (pos[0] < rows - 1):
        pos = (pos[0] + delta_rows, (pos[1] + delta_cols) % cols)
        n_trees += data[pos]
    return n_trees

res = np.array([1], dtype=np.int64)
res[0] *= get_trees(1, 1)
res[0] *= get_trees(1, 3)
res[0] *= get_trees(1, 5)
res[0] *= get_trees(1, 7)
res[0] *= get_trees(2, 1)
print(res)


