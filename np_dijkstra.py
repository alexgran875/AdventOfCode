from utils import parse_data, data_to_numpy
import heapq
import numpy as np

lines = parse_data() # input data from 2021, day 15 

class Vertex():
    def __init__(self, destination: tuple, prevVertex, distance):
        self.destination = destination
        self.prevVertex = prevVertex
        self.distance = distance

    def __lt__(self, otherVertex):
        # heapq pops the smallest element (smaller = higher priority)
        # we want to explore the shortest distances first
        return self.distance < otherVertex.distance

np_matrix = data_to_numpy(lines)
start = (0, 0)
goal = (np_matrix.shape[0]-1, np_matrix.shape[1]-1)
diagonals_possible = False

shortest_distances = np.zeros(shape=np_matrix.shape)+np.inf
priorityQ = []
heapq.heappush(priorityQ, Vertex(start, None, 0))
while len(priorityQ) > 0:
    currentVertex = heapq.heappop(priorityQ)
    for rowOffset in range(-1, 2):
        for colOffset in range(-1, 2):
            # diagonals
            if rowOffset != 0 and abs(rowOffset) == abs(colOffset):
                if not diagonals_possible:
                    continue

            # self (current cell)
            if rowOffset == 0 and colOffset == 0:
                continue

            # row edge
            neighbourRowIndex = currentVertex.destination[0] + rowOffset
            if neighbourRowIndex < 0 or neighbourRowIndex >= np.shape(np_matrix)[0]:
                continue

            # col edge
            neighbourColIndex = currentVertex.destination[1] + colOffset
            if neighbourColIndex < 0 or neighbourColIndex >= np.shape(np_matrix)[1]:
                continue

            # prevent backtracking
            if currentVertex.prevVertex is not None and (neighbourRowIndex, neighbourColIndex) == currentVertex.prevVertex.destination:
                continue

            # calculate new distance
            # euclidian_distance = np.sqrt((rowOffset)**2 + (colOffset)**2)
            newDistance = currentVertex.distance + \
                np_matrix[neighbourRowIndex, neighbourColIndex]

            # update shortest distance
            if newDistance < shortest_distances[neighbourRowIndex, neighbourColIndex]:
                heapq.heappush(priorityQ, Vertex(
                    (neighbourRowIndex, neighbourColIndex), currentVertex, newDistance))
                shortest_distances[neighbourRowIndex,
                                   neighbourColIndex] = newDistance

                # Dijkstra explores shortest paths first so the first time we see the goal then we have the shortest path
                if (neighbourRowIndex, neighbourColIndex) == goal:
                    print(f"Shortest distance: {newDistance}")
                    priorityQ = []

