import re


SCHOOLS = [
    "fire",
    "ice",
    "storm",
    "myth",
    "life",
    "death",
    "balance",
    "star",
    "sun",
    "moon",
    "gardening",
    "shadow",
    "fishing",
    "cantrips",
    "castlemagic",
    "whirlyburly",
]

# TODO: add missing
ITEM_CATEGORIES = [
    "helmet",
    "robe",
    "boots",
    "wand",
    "mount",
    "deck",
    "athame",
    "amulet",
]

STAT_CATEGORIES = [
    "damage",
    "critical",
]

tests = [
    "damage robe",
    "fire damage robe",
    "shadow damage robe",
    "ice damage robe",
    "death damage boots",
    "damage mount",
]

schools_combined = "|".join(map(lambda s: "(" + s + ")", SCHOOLS))
stats_combined = "|".join(map(lambda s: "(" + s + ")", STAT_CATEGORIES))
item_type_combined = "|".join(map(lambda s: "(" + s + ")", ITEM_CATEGORIES))

any_school = f"(({schools_combined}) )?"

item_regex = re.compile(rf"{any_school}{stats_combined} {item_type_combined}")

print(rf"{any_school}{stats_combined} {item_type_combined}")

for test in tests:
    assert item_regex.match(test) is not None, f"failed: {test=}"

