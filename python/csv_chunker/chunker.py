import csv
import numpy

global collems

def read_csv(path: str):
    global collems
    with open(path, newline='') as fp:
        reader = csv.reader(fp)
        data = [row for row in reader]
        collems = data[0]
        return data[1:]

def make_and_save_csv(name: str, data: list):
    with open(name, "w+", newline='') as fp:
        writer = csv.writer(fp)
        for row in data:
            writer.writerow(row)

def chunk_data(data: list):
    global collems
    def construct(rows):
        return [collems, *rows]
    rows = list(numpy.array_split(numpy.array(data),4))
    print(f"Rows = {rows}")
    return [construct(row_set) for row_set in rows]

def save_chunks(data: list):
    for idx, data_set in enumerate(data):
        make_and_save_csv(f"{idx}.csv", data_set)

def run():
    path = input("Path to file? ")
    data = read_csv(path)
    print(data)
    chunked = chunk_data(data)
    print(chunked)
    save_chunks(chunked)

if __name__ == "__main__":
    run()