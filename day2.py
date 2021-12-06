with open('input2.txt') as f:
    input = f.readlines()


horizontal = 0
aim = 0
depth = 0
for i in range(len(input)):
    current_cmd = input[i].split("\n")[0]

    if "forward" in current_cmd:
        horizontal += int(current_cmd[-1])
        depth += aim*int(current_cmd[-1])
    elif "down" in current_cmd:
        aim += int(current_cmd[-1])
    elif "up" in current_cmd:
        aim -= int(current_cmd[-1])
        

print(str(horizontal*depth))


