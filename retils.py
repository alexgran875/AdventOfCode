import re

# getall=False returns a string or ''
# getall=True returns a list of strings or []
# NOTE: IF YOU ARE MATCHING {([\^$|)*+?.} YOU MUST ESCAPE THEM WITH A BACKSLASH
def handle_return(matches, getall):
    if getall:
        return matches
    else:
        if len(matches) == 0:
            return ''
        else:
            return matches[0]

def get_between_groups(string, first_group, second_group, getall=False):
    # NOTE: LAZY - will match as little as possible
    # e.g. if there is a second occurrence of the second group, will only match up to its first occurrence 
    matches = re.findall(r'(?<=' + first_group + r')(.*?)(?=' + second_group + r')', string)
    return handle_return(matches, getall)

def get_after_group(string, group, getall=False):
    # up to a line break
    # NOTE: GREEDY
    matches = re.findall(r'(?<=' + group + r')(.*)', string)
    return handle_return(matches, getall)

def get_before_group(string, group, getall=False):
    # up to a line break
    # NOTE: LAZY
    matches = re.findall(r'(.*?)' + group, string)
    return handle_return(matches, getall)

def get_digits(string, getall=False):
    matches = re.findall(r'\d+', string)
    return handle_return(matches, getall)

