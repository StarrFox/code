"""
highest damage fire robe:
    function highest
    stat:
        school all (none implied)
        category damage
    item type:
        school fire
        category robe

greater than 10 fire damage with highest ice damage robe:
    function greater than
        args:
            10 fire damage:
                damage > 10 and school == fire
    combinder with (modifys function effects):
        function highest
            args:
                ice damage

    damage > 10 and school == fire with the highest ice damage findable

<function> <school>? <stat category> <school>? <item category>

tests:
    robe|boots|armor|helm:
        lowest fire damage ice boots
        lowest damage boots
        greater than 40 damage with less than boots
        greater than 10 fire damage with highest ice damage robe

    mounts:
        highest speed mount
        lowest speed mount

    jewels:
        highest damage star jewel
"""

from typing import Generator


def b() -> Generator[int, int, None]:
    x = 100
    while True:
        x = (yield x)
        print(x)


def a(x: Generator[int, int, None]):
    while True:
        y = next(x)
        print(f"{y=}")
        x.send(1)

a(b())











