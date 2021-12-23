import copy
import math
import numpy as np
from numpy.core.fromnumeric import shape
from numpy.core.numeric import Inf, Infinity

with open('input.txt') as f:
    input = f.readlines()

sensor_readings = []
scanner_id = -1
for line in input:
    if line == "\n":
        continue

    if line.count("---"):
        sensor_readings.append([])
        scanner_id += 1
        continue

    to_add = line.replace("\n","")
    to_add = to_add.split(",")
    to_add = list(map(int,to_add))

    sensor_readings[scanner_id].append(np.array(to_add))

def get_distances(beginning, end):
    dist_wrt_beginning = np.zeros(shape=(len(beginning),len(end)))
    for iReading in range(len(beginning)):
        dist_vectors = end - np.tile(beginning[iReading],(len(end),1))
        dist_wrt_beginning[iReading,:] = np.linalg.norm(dist_vectors, axis=1)
    return dist_wrt_beginning

def get_dist_vectors(beginning, end):
    dist_vectors = end - np.tile(beginning,(len(end),1))
    return dist_vectors

def find_overlapping_beacons(dist1, dist2):
    for i in range(len(dist1)):
        dist_wrt_beacon1 = dist1[i]
        for j in range(len(dist2)):
            dist_wrt_beacon2 = dist2[j]
            duplicates = np.intersect1d(dist_wrt_beacon1,dist_wrt_beacon2)
            if len(duplicates) >= 12:
                # will always at least match the zero distance to itself, hence 13 instead of 12
                return i,j
    return None,None

def get_transform(origin, distance_to):

    n_matches = len(np.intersect1d(origin[:,0],distance_to[:,0]))
    n_matches += len(np.intersect1d(origin[:,1],distance_to[:,1]))
    n_matches += len(np.intersect1d(origin[:,2],distance_to[:,2]))
    n_matches /= 3
    if n_matches == 12:
        return

    x = 5

origo = copy.deepcopy(sensor_readings[0])
origo_distances = get_distances(origo, origo)
for sensor in range(1, len(sensor_readings)):
    new_sensor_distances = get_distances(sensor_readings[sensor], sensor_readings[sensor])
    beacon_idx_1, beacon_idx_2 = find_overlapping_beacons(origo_distances,new_sensor_distances)
    if beacon_idx_1 is not None:
        dist_vec_wrt_beacon1 = get_dist_vectors(origo[beacon_idx_1], origo)
        dist_vec_wrt_beacon2 = get_dist_vectors(sensor_readings[sensor][beacon_idx_2], sensor_readings[sensor])
        get_transform(dist_vec_wrt_beacon1,dist_vec_wrt_beacon2)

    x = 5

x = 5


