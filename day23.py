import copy
import math

with open('input.txt') as f:
    input = f.readlines()

def exe_ins(input_digs,n_to_inspect):
    variables = {'w':0,'x':0,'y':0,'z':0}
    valid_inputs = []
    inp_id = -1
    for line in input:
        if line.count("inp"):
            if inp_id >= 0:
                if variables['z'] == 0:
                    valid_inputs.append(True)
                else:
                    valid_inputs.append(False)
            inp_id += 1
            if inp_id == n_to_inspect:
                return valid_inputs
            var_arg = line.split()[-1]
            variables[var_arg] = input_digs[inp_id]
            continue

        var_arg = line.split()[1]
        arg2 = line.split()[2]
        if line.count("add"):
            if arg2 in variables:
                variables[var_arg] += variables[arg2]
            else:
                variables[var_arg] += int(arg2)
        if line.count("mul"):
            if arg2 in variables:
                variables[var_arg] *= variables[arg2]
            else:
                variables[var_arg] *= int(arg2)
        if line.count("div"):
            # TODO: not sure about truncuation = round down
            if arg2 in variables:
                assert variables[arg2] != 0
                variables[var_arg] = int(math.floor(variables[var_arg]/variables[arg2]))
            else:
                assert int(arg2) != 0
                variables[var_arg] = int(math.floor(variables[var_arg]/int(arg2)))
        if line.count("mod"):
            assert variables[var_arg] >= 0
            if arg2 in variables:
                assert variables[arg2] > 0
                variables[var_arg] = variables[var_arg] % variables[arg2]
            else:
                assert int(arg2) > 0
                variables[var_arg] = variables[var_arg] % int(arg2)
        if line.count("eql"):
            if arg2 in variables:
                if variables[var_arg] == variables[arg2]:
                    variables[var_arg] = 1
                else:
                    variables[var_arg] = 0
            else:
                if variables[var_arg] == int(arg2):
                    variables[var_arg] = 1
                else:
                    variables[var_arg] = 0
    if variables['z'] == 0:
        valid_inputs.append(True)
    else:
        valid_inputs.append(False)
    return valid_inputs

def find_highest_valid(input_digs_before,input_position):
    current_highest = 0
    in_dig_before = copy.deepcopy(input_digs_before)
    in_dig_before.append(1)
    for i in range(1,10):
        in_dig_before[-1] = i
        rv = exe_ins(in_dig_before,input_position+1)
        last_valid = rv[-1]
        if last_valid and i > current_highest:
            current_highest = i
    in_dig_before[-1] = current_highest
    return in_dig_before
    

model_number = []
for i in range(14):
    model_number = find_highest_valid(model_number,i)

