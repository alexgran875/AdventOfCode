import copy
import math

with open('input.txt') as f:
    input = f.readlines()

def is_valid(input_digs):
    variables = {'w':0,'x':0,'y':0,'z':0}
    inp_id = -1
    for line in input:
        if line.count("inp"):
            inp_id += 1
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
                variables[var_arg] = int(variables[var_arg]/variables[arg2])
            else:
                assert int(arg2) != 0
                variables[var_arg] = int(variables[var_arg]/int(arg2))
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
        return True
    else:
        return False

def find_highest_valid():
    input_digs = []
    for a in range(9,0,-1):
        for b in range(9,0,-1):
            for c in range(9,0,-1):
                print(input_digs)
                for d in range(9,0,-1):
                    for e in range(9,0,-1):
                        for f in range(9,0,-1):
                            for g in range(9,0,-1):
                                for h in range(9,0,-1):
                                    for i in range(9,0,-1):
                                        for j in range(9,0,-1):
                                            for k in range(9,0,-1):
                                                for l in range(9,0,-1):
                                                    for m in range(9,0,-1):
                                                        for n in range(9,0,-1):
                                                            input_digs = [a,b,c,d,e,f,g,h,i,j,k,l,m,n]
                                                            valid = is_valid(input_digs)
                                                            if valid:
                                                                return input_digs

model_number = find_highest_valid()
print(model_number)

