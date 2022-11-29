import re

def handle_return(matches, getall):
    if getall:
        return matches
    else:
        if len(matches) == 0:
            return ''
        else:
            return matches[0]

def get_between_groups(string, first_group, second_group, getall=False):
    matches = re.findall(r'(?<=' + first_group + ')(.*?)(?=' + second_group + ')', string)
    return handle_return(matches, getall)

def get_after_group(string, group, getall=False):
    matches = re.findall(r'(?<=' + group + ')(.*)', string)
    return handle_return(matches, getall)

def get_before_group(string, group, getall=False):
    matches = re.findall(r'(.*)' + group, string)
    return handle_return(matches, getall)

def get_digits(string, getall=False, getall_as_int=True):
    matches = re.findall(r'\d+', string)
    rv = handle_return(matches, getall)
    if getall_as_int:
        if getall:
            rv = [int(x) for x in list(filter(lambda l: l.isdigit(), rv))]
        else:
            if rv.isdigit():
                rv = int(rv)
    return rv

