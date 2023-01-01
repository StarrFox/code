import orjson


with open("test_data.json", "rb") as fp:
    file_data = fp.read()
    test_data = orjson.loads(file_data)


count = 0
for entry in test_data.values():
    if entry["category"] == 2:
        count += 1


print(count)
