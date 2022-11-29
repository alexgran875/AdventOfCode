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
                duplicates = duplicates[duplicates!=0]
                distance1_idx = np.where(np.in1d(dist_wrt_beacon1, duplicates))[0]
                distance2_idx = np.where(np.in1d(dist_wrt_beacon2, duplicates))[0]

                distances1 = np.argsort(dist_wrt_beacon1[distance1_idx])
                distance1_idx = distance1_idx[distances1]

                distances2 = np.argsort(dist_wrt_beacon2[distance2_idx])
                distance2_idx = distance2_idx[distances2]

                return i,j,distance1_idx,distance2_idx
    return None,None,None,None

def get_transform(origin, other):
    
    origin_mat = copy.deepcopy(origin)
    origin_mat = np.array(origin_mat)
    other_mat = copy.deepcopy(other)
    other_mat = np.array(other)

    combinations = [[0,1,2],[0,2,1],[1,0,2],[2,0,1],[1,2,0],[2,1,0]]

    for iBeacon in range(len(origin)):
        origin_vec = origin_mat[iBeacon,:]
        other_vec = other_mat[iBeacon,:]

        i = 0
        for x in range(-1,2):
            for y in range(-1,2):
                for z in range(-1,2):
                    if (x == 0 or y == 0 or z == 0):
                        continue

                    rotated = other_vec * [x,y,z]
                    for placement in combinations:
                        flipped = np.array([ rotated[placement[0]], rotated[placement[1]], rotated[placement[2]] ])
                        if (flipped == origin_vec).all():

                            all_others_flipped = copy.deepcopy(other_mat)
                            n_matches = 0
                            for i in range(other_mat.shape[0]):
                                all_others_flipped[i,:] = all_others_flipped[i,:] * [x,y,z]
                                replacement = np.array([all_others_flipped[i,placement[0]], all_others_flipped[i,placement[1]], all_others_flipped[i,placement[2]]])
                                all_others_flipped[i,:] = replacement
                                if (all_others_flipped[i,:] == origin_mat[i,:]).all():
                                    n_matches += 1

                            if n_matches == len(origin):
                                return [x,y,z], placement

    raise Exception("No possible transform!")

def apply_transformation(mult, placement, offset, beacons):
    transformed_beacons = copy.deepcopy(beacons)

    for i in range(beacons.shape[0]):
        transformed_beacons[i,:] = beacons[i,:] * mult
        flipped = np.array([ transformed_beacons[i,placement[0]], transformed_beacons[i,placement[1]], transformed_beacons[i,placement[2]] ])
        transformed_beacons[i,:] = flipped
        transformed_beacons[i,:] += offset
    
    return transformed_beacons


scanner_locations = [np.array([0,0,0])]
origo = copy.deepcopy(sensor_readings[0])
sensor_readings.pop(0)
while len(sensor_readings) > 0:
    for sensor in range(len(sensor_readings)):
        origo_distances = get_distances(origo, origo)
        new_sensor_distances = get_distances(sensor_readings[sensor], sensor_readings[sensor])
        matching_beacon_idx1, matching_beacon_idx2, matching_beacon1, matching_beacon2 = find_overlapping_beacons(origo_distances,new_sensor_distances)
        if matching_beacon_idx1 is not None:
            dist_vec_wrt_beacon1 = get_dist_vectors(origo[matching_beacon_idx1], origo)
            dist_vec_wrt_beacon2 = get_dist_vectors(sensor_readings[sensor][matching_beacon_idx2], sensor_readings[sensor])

            mult, placement = get_transform(dist_vec_wrt_beacon1[matching_beacon1], dist_vec_wrt_beacon2[matching_beacon2])
            origin_beacon = origo[matching_beacon_idx1]
            other_beacon = sensor_readings[sensor][matching_beacon_idx2]
            other_beacon *= mult
            other_flipped = np.array([ other_beacon[placement[0]], other_beacon[placement[1]], other_beacon[placement[2]] ])
            offset = origin_beacon - other_flipped

            scanner_locations.append(offset)

            #new_beacons_wrt_origo = apply_transformation(mult, placement, offset, np.array(sensor_readings[sensor])[matching_beacon2])
            new_beacons_wrt_origo = apply_transformation(mult, placement, offset, np.array(sensor_readings[sensor]))
            for i in range(new_beacons_wrt_origo.shape[0]):
                if i in matching_beacon2 or i == matching_beacon_idx2:
                    # TODO: new_beacons_wrt_origo[matching_beacon_idx2] does not equal np.array(origo)[matching_beacon_idx1] for some reason
                    continue
                origo.append(new_beacons_wrt_origo[i,:])
            sensor_readings.pop(sensor)
            print(len(sensor_readings))
            break

print(len(origo)) # num beacons: 457

biggest_m_dist = -Infinity
for iRow in range(len(scanner_locations)):
    manhattan_distance = np.abs(np.array(get_dist_vectors(scanner_locations[iRow], scanner_locations)))
    manhattan_distance = np.max(np.sum(np.abs(manhattan_distance), axis=1))
    if manhattan_distance > biggest_m_dist:
        biggest_m_dist = manhattan_distance

print(biggest_m_dist) # largest manhattan distance between scanners: 13243

