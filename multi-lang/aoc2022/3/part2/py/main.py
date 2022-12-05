import string
import pprint


def chunked(thing, n):
    start = 0
    for iteration in range(len(thing) // n):
        yield thing[n * iteration:n * (iteration + 1)]


def get_priority(item):
    numeric = ord(item)
    if numeric >= ord("a"):
        return numeric - ord("a") + 1
    
    return numeric - 38


with open("input") as input_:
    lines = input_.read().splitlines()


priority_sum = 0


for chunk in chunked(lines, 3):
    lookup = {}

    # you can't subscript sets
    chunk0 = set(chunk[0])
    chunk1 = set(chunk[1])
    chunk2 = set(chunk[2])

    for letter in string.ascii_letters:
        lookup[letter] = 0

    for letter in chunk0:
        if letter in chunk1:
            lookup[letter] += 1
        else:
            lookup[letter] -= 1
    
    for letter in chunk1:
        if letter in chunk2:
            lookup[letter] += 1
    
    for letter in chunk2:
        if letter in chunk0:
            lookup[letter] += 1

    for key, value in lookup.items():
        if value == 3:
            priority = get_priority(key)
            priority_sum += priority
            break


print(priority_sum)
