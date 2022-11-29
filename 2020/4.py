import utils
import retils
import re
data = utils.parse_data()

n_valid = 0
byr = 0
iyr = 0
eyr = 0
hgt = 0
hcl = 0
ecl = 0
pid = 0
cid = 0
byr_counted = 0
iyr_counted = 0
eyr_counted = 0
hgt_counted = 0
hcl_counted = 0
ecl_counted = 0
pid_counted = 0
cid_counted = 0
for i, line in enumerate(data):

    byr += line.count('byr:')
    assert byr <= 1
    if byr > 0 and byr_counted == 0:
        byr_counted += 1
        val = retils.get_digits(retils.get_after_group(line, 'byr:'))
        if (val.isdigit()) and (int(val) < 1920 or int(val) > 2002):
            byr = 0

    iyr += line.count('iyr:')
    assert iyr <= 1
    if iyr > 0 and iyr_counted == 0:
        iyr_counted += 1
        val = retils.get_digits(retils.get_after_group(line, 'iyr:'))
        if (val.isdigit()) and (int(val) < 2010 or int(val) > 2020):
            iyr = 0

    eyr += line.count('eyr:')
    assert eyr <= 1
    if eyr > 0 and eyr_counted == 0:
        eyr_counted += 1
        val = retils.get_digits(retils.get_after_group(line, 'eyr:'))
        if (val.isdigit()) and (int(val) < 2020 or int(val) > 2030):
            eyr = 0
    
    hgt += line.count('hgt:')
    assert hgt <= 1
    if hgt > 0 and hgt_counted == 0:
        hgt_counted += 1
        val_cm = retils.get_between_groups(line, 'hgt:', 'cm')
        val_in = retils.get_between_groups(line, 'hgt:', 'in')
        if val_cm.isdigit():
            val = int(val_cm)
            if val < 150 or val > 193:
                hgt = 0
        elif val_in.isdigit():
            val = int(val_in)
            if val < 59 or val > 76:
                hgt = 0
        else:
            hgt = 0

    hcl += line.count('hcl:')
    assert hcl <= 1
    if hcl > 0 and hcl_counted == 0:
        hcl_counted += 1
        val = retils.get_after_group(line, 'hcl:#').split(" ")[0]
        if len(val) != 6 or len(re.findall(r'[0-9a-f]{6}', val)) == 0:
            hcl = 0

    ecl += line.count('ecl:')
    assert ecl <= 1
    if ecl > 0 and ecl_counted == 0:
        ecl_counted += 1
        val = retils.get_after_group(line, 'ecl:').split(" ")[0]
        if val not in ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth']:
            ecl = 0

    pid += line.count('pid:')
    assert pid <= 1
    if pid > 0 and pid_counted == 0:
        pid_counted += 1
        val = retils.get_after_group(line, 'pid:').split(" ")[0]
        if len(val) != 9 or not val.isdigit():
            pid = 0
    
    cid += line.count('cid:')
    assert cid <= 1
    if cid > 0 and cid_counted == 0:
        cid_counted += 1
    
    if (line == ""):
        if (byr > 0 and iyr > 0 and eyr > 0 and hgt > 0 and hcl > 0 and ecl > 0 and pid > 0):
            n_valid += 1
        else:
            x = 5
        byr = 0
        iyr = 0
        eyr = 0
        hgt = 0
        hcl = 0
        ecl = 0
        pid = 0
        cid = 0
        byr_counted = 0
        iyr_counted = 0
        eyr_counted = 0
        hgt_counted = 0
        hcl_counted = 0
        ecl_counted = 0
        pid_counted = 0
        cid_counted = 0
print(n_valid)

