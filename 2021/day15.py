import numpy as np
from numpy.core.fromnumeric import shape
import copy
import heapq
from numpy.core.numeric import Infinity

with open('input.txt') as f:
    input = f.readlines()

input = list(map(lambda line: list(line.replace("\n","")),input))
input = list(map(lambda line:list(map(int,line)),input))
input = np.array(input)

map = copy.deepcopy(input)
extension = copy.deepcopy(input)
for col in range(1,5):
    extension = extension+1
    extension[extension > 9] = 1
    map = np.hstack( (map,extension) )

extension = copy.deepcopy(map)
for row in range(1,5):
    extension = extension+1
    extension[extension > 9] = 1
    map = np.vstack( (map,extension) )

shortest_distances = np.zeros(shape=map.shape)+Infinity
goalRow = map.shape[0]-1
goalCol = map.shape[1]-1

class Vertex():
    def __init__(self, destRow, destCol, prevVertex, dist):
        self.destRow = destRow
        self.destCol = destCol
        self.prevVertex = prevVertex
        self.dist = dist

    def __lt__(self, other):
        return -1

h = []
sourceVertex = Vertex(0,0,None,0)
heapq.heappush(h, (0, sourceVertex) )
shortest_distances[0,0] = 0
distance = 0
prev = None
while len(h) > 0:
    u = heapq.heappop(h)[1]
    iRow = u.destRow
    jCol = u.destCol
    for rowOffset in range(-1,2):
            for colOffset in range(-1,2):
                if (rowOffset == colOffset) or (rowOffset == -colOffset):
                    continue
                rowIndex = iRow+rowOffset
                if rowIndex < 0 or rowIndex > np.shape(map)[0]-1:
                    continue
                colIndex = jCol+colOffset
                if colIndex < 0 or colIndex > np.shape(map)[1]-1:
                    continue
                if u.prevVertex is not None and rowIndex == u.prevVertex.destRow and colIndex == u.prevVertex.destCol:
                    continue

                alt = int(u.dist + map[rowIndex,colIndex])
                if alt < shortest_distances[rowIndex,colIndex]:
                    newVertex = Vertex(rowIndex,colIndex,u,alt)
                    heapq.heappush(h, (alt, newVertex) )
                    shortest_distances[rowIndex,colIndex] = alt
    
    if iRow == goalRow and jCol == goalCol:
        distance = u.dist
        prev = u.prevVertex

print(distance)

x = 5

