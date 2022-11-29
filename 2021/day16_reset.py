import copy
import math

import numpy as np
from numpy.core.fromnumeric import shape
from numpy.core.numeric import Inf, Infinity

with open('input.txt') as f:
    input = f.readlines()

input = input[0].replace("\n","")
input = bin(int(input, 16))[2:].zfill(int(len(input) * np.log2(16)))

class Packet():
    def __init__(self, version, type_id, length_type_id=None, L_field=None, sub_packets=None, val=None) -> None:
        self.version = version
        self.type_id = type_id
        if length_type_id is not None:
            self.length_type_id = length_type_id
            self.L_field = L_field
            self.sub_packets = copy.deepcopy(sub_packets)
        elif val is not None:
            self.val = val
        self.v_sum = self.version

    def calc_v_sum(self):
        if self.type_id == 4:
            return self.version
        for sub_packet in self.sub_packets:
            self.v_sum += sub_packet.calc_v_sum()
        return self.v_sum

    def eval_packet(self):
        if self.type_id == 4:
            return self.val
        elif self.type_id == 0:
            eval = 0
            for sub_packet in self.sub_packets:
                eval += sub_packet.eval_packet()
            return eval
        elif self.type_id == 1:
            eval = 1
            for sub_packet in self.sub_packets:
                eval *= sub_packet.eval_packet()
            return eval
        elif self.type_id == 2:
            eval = Infinity
            for sub_packet in self.sub_packets:
                rv = sub_packet.eval_packet()
                if rv < eval:
                    eval = rv
            return eval
        elif self.type_id == 3:
            eval = -Infinity 
            for sub_packet in self.sub_packets:
                rv = sub_packet.eval_packet()
                if rv > eval:
                    eval = rv
            return eval
        elif self.type_id == 5:
            if self.sub_packets[0].eval_packet() > self.sub_packets[1].eval_packet():
                return 1
            else:
                return 0
        elif self.type_id == 6:
            if self.sub_packets[0].eval_packet() < self.sub_packets[1].eval_packet():
                return 1
            else:
                return 0
        elif self.type_id == 7:
            if self.sub_packets[0].eval_packet() == self.sub_packets[1].eval_packet():
                return 1
            else:
                return 0
        

def parse_literal(data):
    val = ""
    idx = 0
    while True:
        if data[idx] == "1":
            val += data[idx+1:idx+5]
            idx += 5
        else:
            val += data[idx+1:idx+5]
            break
    return (int(val,2), idx + 5)

def parse_packet(data):
    v = int(data[:3],2)
    t = int(data[3:6],2)
    if t == 4:
        # literal value
        val, length = parse_literal(data[6:])
        #data = data[6+length:]
        return (Packet(v,t,val=val), length+6)
    else:
        i = int(data[6],2)
        if i == 0:
            # number of bits in sub-packets
            L_field = int(data[7:22],2)
            sub_packets = []
            length_parsed = 0
            while True:
                packet, length = parse_packet(data[22+length_parsed:])
                if isinstance(length, str):
                    length_parsed += len(data[22+length_parsed:]) - len(length)
                else:
                    length_parsed += length
                sub_packets.append(packet)
                if length_parsed == L_field:
                    return (Packet(v,t,i,L_field,sub_packets), data[22+length_parsed:])
        elif i == 1:
            # number of sub-packets
            L_field = int(data[7:18],2)
            sub_packets = []
            length_parsed = 0
            for i in range(L_field):
                packet, length = parse_packet(data[18+length_parsed:])
                if isinstance(length, str):
                    length_parsed += len(data[18+length_parsed:]) - len(length)
                else:
                    length_parsed += length
                sub_packets.append(packet)

            return (Packet(v,t,i,L_field,sub_packets), data[18+length_parsed:])

packets = []
data = copy.deepcopy(input)
version_sum = 0
while True:
    packet, data = parse_packet(data)
    packets.append(packet)
    if len(data) < 29:
        break

for packet in packets:
    version_sum += packet.calc_v_sum()

print(version_sum)
print(packets[0].eval_packet())

