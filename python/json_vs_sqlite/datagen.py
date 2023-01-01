# gen some random data for testing
import sqlite3
import orjson
import random
import string
import time


DATA_SIZE = 1_000_000

letter_len = len(string.ascii_letters)

def random_string():
    start = random.randint(0, letter_len)
    end = random.randint(start, letter_len)
    return string.ascii_letters[start:end]



"""
test data:
    {
        id(int): {
            name: str
            category: 1|2|3
        },
        ...
    }
"""


test_data = {}

for id in range(DATA_SIZE):
    test_data[str(id)] = {"name": random_string(), "category": random.randint(1,3)}


def get_time(func, *args, **kwargs):
    start = time.perf_counter()
    func(*args, **kwargs)
    end = time.perf_counter()
    print(f"{func.__name__}: {end - start}")

# orjson is really fast
# get_time(str, test_data)
# get_time(orjson.dumps, test_data)

with open("test_data.json", "wb+") as fp:
    fp.write(orjson.dumps(test_data))

connection = sqlite3.connect("test_data.db")
cursor = connection.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS "data" (
    "id" INTEGER UNIQUE,
    "name" TEXT,
    "category" INTEGER,
    PRIMARY KEY("id")
);
""")
for id in test_data:
    name, category = test_data[id].values()
    cursor.execute(
        "INSERT INTO data (id, name, category) VALUES (?, ?, ?);", 
        (id, name, category),
    )

connection.commit()
