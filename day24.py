import copy

with open('input.txt') as f:
    input = f.readlines()

instructions = [[] for _ in range(14)]
inp_id = -1
for line in input:
    if line.count("inp"):
        inp_id += 1
    else:
        instructions[inp_id].append(line.replace("\n",""))

def exe_ins(arg_variables, ins_id):
    # set w in variables directly to the input var (inp w)
    variables = copy.deepcopy(arg_variables)

    if ins_id == 0:
        variables['y'] = variables['w'] + 12
        variables['z'] = variables['y']
        variables['x'] = 1
        return variables
    if ins_id == 1:
        variables['y'] = variables['w'] + 7
        variables['z'] = variables['z']*26 + variables['y']
        variables['x'] = 1
        return variables
    if ins_id == 13:
        variables['y'] = variables['w'] + 13
        variables['x'] = 1
        variables['z'] = int(variables['z']/26)*26 + variables['y']
        return variables
    if ins_id == 12:
        variables['x'] = (variables['z'] % 26) - 4
        if variables['x'] == variables['w']:
            variables['x'] = 1
        else:
            variables['x'] = 0
        variables['x'] = 1 - variables['x']

        variables['y'] = (variables['w'] + 4)*variables['x']
        
        variables['z'] = variables['y'] + int(variables['z']/26)*(25*variables['x'] + 1)
        return variables
    if ins_id == 11:
        add_x = -1
        add_y = 9
        variables['x'] = (variables['z'] % 26) + add_x
        if variables['x'] == variables['w']:
            variables['x'] = 1
        else:
            variables['x'] = 0
        variables['x'] = 1 - variables['x']

        variables['y'] = (variables['w'] + add_y)*variables['x']
        
        variables['z'] = int(variables['z']/26) * (25*variables['x'] + 1) + variables['y']
        return variables
    if ins_id == 10:
        add_x = -8
        add_y = 3
        variables['x'] = (variables['z'] % 26) + add_x
        if variables['x'] == variables['w']:
            variables['x'] = 1
        else:
            variables['x'] = 0
        variables['x'] = 1 - variables['x']

        variables['y'] = (variables['w'] + add_y)*variables['x']
        
        variables['z'] = int(variables['z']/26) * (25*variables['x'] + 1) + variables['y']
        return variables
    if ins_id == 9:
        add_x = 13
        add_y = 13
        div_z = 1
        variables['x'] = (variables['z'] % 26) + add_x
        if variables['x'] == variables['w']:
            variables['x'] = 1
        else:
            variables['x'] = 0
        variables['x'] = 1 - variables['x']

        variables['y'] = (variables['w'] + add_y)*variables['x']
        
        variables['z'] = int(variables['z']/div_z) * (25*variables['x'] + 1) + variables['y']
        return variables
    if ins_id == 8:
        div_z = 26
        add_x = -13
        add_y = 3
        variables['x'] = (variables['z'] % 26) + add_x
        if variables['x'] == variables['w']:
            variables['x'] = 1
        else:
            variables['x'] = 0
        variables['x'] = 1 - variables['x']

        variables['y'] = (variables['w'] + add_y)*variables['x']
        
        variables['z'] = int(variables['z']/div_z) * (25*variables['x'] + 1) + variables['y']
        return variables
    if ins_id == 7:
        div_z = 26
        add_x = -11
        add_y = 13
        variables['x'] = (variables['z'] % 26) + add_x
        if variables['x'] == variables['w']:
            variables['x'] = 1
        else:
            variables['x'] = 0
        variables['x'] = 1 - variables['x']

        variables['y'] = (variables['w'] + add_y)*variables['x']
        
        variables['z'] = int(variables['z']/div_z) * (25*variables['x'] + 1) + variables['y']
        return variables
    if ins_id == 6:
        div_z = 1
        add_x = 10
        add_y = 8
        variables['x'] = (variables['z'] % 26) + add_x
        if variables['x'] == variables['w']:
            variables['x'] = 1
        else:
            variables['x'] = 0
        variables['x'] = 1 - variables['x']

        variables['y'] = (variables['w'] + add_y)*variables['x']
        
        variables['z'] = int(variables['z']/div_z) * (25*variables['x'] + 1) + variables['y']
        return variables 
    if ins_id == 5:
        div_z = 26
        add_x = -16
        add_y = 12
        variables['x'] = (variables['z'] % 26) + add_x
        if variables['x'] == variables['w']:
            variables['x'] = 1
        else:
            variables['x'] = 0
        variables['x'] = 1 - variables['x']

        variables['y'] = (variables['w'] + add_y)*variables['x']
        
        variables['z'] = int(variables['z']/div_z) * (25*variables['x'] + 1) + variables['y']
        return variables 
    if ins_id == 4:
        div_z = 1
        add_x = 11
        add_y = 15
        variables['x'] = (variables['z'] % 26) + add_x
        if variables['x'] == variables['w']:
            variables['x'] = 1
        else:
            variables['x'] = 0
        variables['x'] = 1 - variables['x']

        variables['y'] = (variables['w'] + add_y)*variables['x']
        
        variables['z'] = int(variables['z']/div_z) * (25*variables['x'] + 1) + variables['y']
        return variables 
    if ins_id == 3:
        div_z = 1
        add_x = 12
        add_y = 8
        variables['x'] = (variables['z'] % 26) + add_x
        if variables['x'] == variables['w']:
            variables['x'] = 1
        else:
            variables['x'] = 0
        variables['x'] = 1 - variables['x']

        variables['y'] = (variables['w'] + add_y)*variables['x']
        
        variables['z'] = int(variables['z']/div_z) * (25*variables['x'] + 1) + variables['y']
        return variables 
    if ins_id == 2:
        div_z = 1
        add_x = 10
        add_y = 8
        variables['x'] = (variables['z'] % 26) + add_x
        if variables['x'] == variables['w']:
            variables['x'] = 1
        else:
            variables['x'] = 0
        variables['x'] = 1 - variables['x']

        variables['y'] = (variables['w'] + add_y)*variables['x']
        
        variables['z'] = int(variables['z']/div_z) * (25*variables['x'] + 1) + variables['y']
        return variables 

    for line in instructions[ins_id]:
        var_arg = line.split()[1]
        arg2 = line.split()[2]
        if line.count("add"):
            if arg2 in variables:
                variables[var_arg] += variables[arg2]
            else:
                variables[var_arg] += int(arg2)
            continue
        if line.count("mul"):
            if arg2 in variables:
                variables[var_arg] *= variables[arg2]
            else:
                variables[var_arg] *= int(arg2)
            continue
        if line.count("div"):
            if arg2 in variables:
                assert variables[arg2] != 0
                variables[var_arg] = int(variables[var_arg]/variables[arg2])
            else:
                assert int(arg2) != 0
                variables[var_arg] = int(variables[var_arg]/int(arg2))
            continue
        if line.count("mod"):
            assert variables[var_arg] >= 0
            if arg2 in variables:
                assert variables[arg2] > 0
                variables[var_arg] = variables[var_arg] % variables[arg2]
            else:
                assert int(arg2) > 0
                variables[var_arg] = variables[var_arg] % int(arg2)
            continue
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
            continue
    return variables

def find_highest_valid():
    init_variables = {'w':0,'x':0,'y':0,'z':0}
    for a in range(9,0,-1):
        init_variables['w'] = a
        a_variables = exe_ins(init_variables,0)
        for b in range(9,0,-1):
            a_variables['w'] = b
            b_variables = exe_ins(a_variables,1)
            for c in range(9,0,-1):
                b_variables['w'] = c
                c_variables = exe_ins(b_variables,2)
                for d in range(9,0,-1):
                    c_variables['w'] = d
                    d_variables = exe_ins(c_variables,3)
                    for e in range(9,0,-1):
                        d_variables['w'] = e
                        e_variables = exe_ins(d_variables,4)
                        for f in range(9,0,-1):
                            e_variables['w'] = f
                            f_variables = exe_ins(e_variables,5)
                            for g in range(9,0,-1):
                                f_variables['w'] = g
                                g_variables = exe_ins(f_variables,6)
                                for h in range(9,0,-1):
                                    print([a,b,c,d,e,f,g,h,-1,-1,-1,-1,-1,-1])
                                    g_variables['w'] = h
                                    h_variables = exe_ins(g_variables,7)
                                    for i in range(9,0,-1):
                                        h_variables['w'] = i
                                        i_variables = exe_ins(h_variables,8)
                                        for j in range(9,0,-1):
                                            i_variables['w'] = j
                                            j_variables = exe_ins(i_variables,9)
                                            for k in range(9,0,-1):
                                                j_variables['w'] = k
                                                k_variables = exe_ins(j_variables,10)
                                                for l in range(9,0,-1):
                                                    k_variables['w'] = l
                                                    l_variables = exe_ins(k_variables,11)
                                                    for m in range(9,0,-1):
                                                        l_variables['w'] = m
                                                        m_variables = exe_ins(l_variables,12)
                                                        for n in range(9,0,-1):
                                                            m_variables['w'] = n
                                                            n_variables = exe_ins(m_variables,13)
                                                            if n_variables['z'] == 0:
                                                                return [a,b,c,d,e,f,g,h,i,j,k,l,m,n]

print(find_highest_valid())

