import numpy as np
from numpy.core.fromnumeric import shape

with open('input.txt') as f:
    input = f.readlines()

sum = None
n = 0
numbers_list = []
numbers_matrix = None
for number in input:
    number = number.split("\n")[0]
    number = np.array(list(number),dtype=int)
    numbers_list.append(number.copy())
    if sum is None:
        sum = number
        numbers_matrix = number.copy()
    else:
        sum += number
        numbers_matrix = np.vstack([numbers_matrix, number.copy()])
    n += 1
    

sum = np.true_divide(sum, n)
sum = np.rint(sum)

bin_sum = ""
inverted_bin_sum = ""
for i in sum:
    to_add = str(i).split(".")[0]
    bin_sum += to_add
    if to_add == "0":
        inverted_bin_sum += "1"
    else:
        inverted_bin_sum += "0"

print(int(bin_sum,2)*int(inverted_bin_sum,2))


num_bits = np.shape(numbers_list[0])[0]
def get_numbers(numbers_matrix, bit_position, to_keep):
    # to_keep: "common"/"uncommon"
    # bit_position: starts at zero
    global num_bits
    if np.shape(numbers_matrix)[0] == 1:
        bin_sum = ""
        for i in range(np.shape(numbers_matrix)[1]):
            to_add = str(numbers_matrix[0,i]).split(".")[0]
            bin_sum += to_add
        return int(bin_sum,2)
    elif bit_position == num_bits:
        raise Exception("Something went wrong!")
    
    number_sum = np.sum(numbers_matrix, axis=0)
    number_sum = np.true_divide(number_sum, np.shape(numbers_matrix)[0])
    if number_sum[bit_position] == 0.5:
        number_sum[bit_position] = 1
    
    number_sum = np.rint(number_sum)
    
    if to_keep == "oxygen":
        bit_value = int(number_sum[bit_position])
    elif to_keep == "carbon":
        bit_value = 1 - int(number_sum[bit_position])
    
    new_numbers_matrix = numbers_matrix[numbers_matrix[:,bit_position] == bit_value]
    return get_numbers(new_numbers_matrix.copy(), bit_position+1, to_keep)

    
oxygen = get_numbers(numbers_matrix, 0, "oxygen")
carbon = get_numbers(numbers_matrix, 0, "carbon")
print(str(oxygen*carbon))

