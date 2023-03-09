def read_csv(file_path):
    with open(file_path) as fp:
        file_stuff = fp.read().strip("\n")
    
    splited = file_stuff.split("\n")

    collums = splited[0].split(",")
    values = splited[1:]

    csv = {}

    for idx, collum in enumerate(collums):
        collim_values = []

        for value_set in values:
            collim_values += value_set.split(",")[idx]

        csv[collum] = collim_values

    return csv

print(read_csv("my_csv.csv"))
