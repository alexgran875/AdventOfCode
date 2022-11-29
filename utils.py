def parse_data():
    with open('input.txt') as f:
        data = f.readlines()
        data = list(map(lambda i:i.replace("\n",""), data))
        return data