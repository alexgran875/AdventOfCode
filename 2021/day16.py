import copy
import math

import numpy as np
from numpy.core.fromnumeric import shape
from numpy.core.numeric import Infinity

with open('input.txt') as f:
    input = f.readlines()

input = input[0].replace("\n","")
input = bin(int(input, 16))[2:].zfill(int(len(input) * np.log2(16)))

class Packet():
    def __init__(self, version, type_id, length_type_id, L_field, sub_packets) -> None:
        self.version = version
        self.type_id = type_id
        self.length_type_id = length_type_id
        self.L_field = L_field
        self.sub_packets = copy.deepcopy(sub_packets)

def parse(input):
    transmission_ended = False
    while not transmission_ended:
        packet_version = ""
        packet_type_id = ""
        packet_length_type_id = ""
        idx_within_packet = 0
        L_field = ""
        for char in input:
            # parsing a packet 
            if 0 <= idx_within_packet <= 2:
                # VVV
                packet_version += char
            elif 3 <= idx_within_packet <= 5:
                # TTT
                packet_type_id += char
            elif 6 <= idx_within_packet and int(packet_type_id,2) == 4:                
                if idx_within_packet == 6:
                    sub_packets = [""]
                packet_idx = int(math.floor((idx_within_packet-6)/5))
                if packet_idx == len(sub_packets):
                    if transmission_ended:
                        n_garbage_bits = 4 - (idx_within_packet % 4)
                        break
                    elif char == "0":
                        transmission_ended = True

                    sub_packets.append("")
                sub_packets[packet_idx] += char
            elif idx_within_packet == 6:
                # I
                packet_length_type_id += char
            elif packet_length_type_id == "1" and 7 <= idx_within_packet <= 17:
                # L*11, number of sub-packets
                L_field += char
            elif packet_length_type_id == "0" and 7 <= idx_within_packet <= 21:
                # L*15, length of sub-packets
                L_field += char
            elif packet_length_type_id == "1" and 18 <= idx_within_packet <= 17+(int(L_field,2)*11):
                # number of sub-packets
                # all of them are 11 bits long enough, so still the same
                if idx_within_packet == 18:
                    sub_packets = [""]*int(L_field,2)
                packet_idx = int(math.floor((idx_within_packet-18)/11))
                sub_packets[packet_idx] += char
            elif packet_length_type_id == "0" and 22 <= idx_within_packet <= 21+int(L_field,2):
                # length of sub-packets 
                if idx_within_packet == 22:
                    num_packets = math.floor(int(L_field,2)/11)
                    sub_packets = [""]*num_packets
                packet_idx = int(math.floor((idx_within_packet-22)/11))
                if packet_idx == len(sub_packets):
                    sub_packets[-1] += char 
                else: 
                    sub_packets[packet_idx] += char
            else:
                transmission_ended = True
                #n_garbage_bits = 56 - idx_within_packet, least likely, data too short
                #n_garbage_bits = 0#, non divisable by 4, also unlikely, L too high
                #n_garbage_bits = 4 - (idx_within_packet % 4), L becomes insanely high
                n_garbage_bits = 8 - (idx_within_packet % 4), nope -> wrong version sum 
                break

            idx_within_packet += 1

    if packet_length_type_id == "":
        rv = [Packet(int(packet_version,2), int(packet_type_id,2), -1, 
    -1, sub_packets), copy.deepcopy(input[idx_within_packet+n_garbage_bits:])]
    else:
        rv = [Packet(int(packet_version,2), int(packet_type_id,2), int(packet_length_type_id,2), 
    int(L_field,2), sub_packets), copy.deepcopy(input[idx_within_packet+n_garbage_bits:])]
    return rv


packets = []
data = copy.deepcopy(input)
version_sum = 0
while len(data) > 0:
    parsed = parse(data)
    packets.append(parsed[0])
    data = parsed[1]
    version_sum += parsed[0].version
    x = 5

x = 5