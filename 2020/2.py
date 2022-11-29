from utils import parse_data
data = parse_data()

n_valid = 0
for i in data:
    minimal = int(i.split("-")[0])
    maximal = int(i.split("-")[1].split(" ")[0])
    letter = i.split(" ")[1].split(":")[0]
    password = i.split(" ")[2]
    #if minimal <= password.count(letter) <= maximal:
    #    n_valid += 1
    if (password[minimal - 1] == letter) != (password[maximal - 1] == letter):
        n_valid += 1
print(n_valid)


