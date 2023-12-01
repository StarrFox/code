import re

numbers = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
number_groups = "|".join(map(lambda s: f"({s})", numbers))
number_regex = re.compile(rf"(?={number_groups}|(\d))")

x = open("input").read().strip()

def to_int(matches: list[tuple[str]]) -> int:
    def x(b: tuple[str]):
        content = list(filter(lambda w: len(w) > 0, b))[0]
        try:
            return int(content)
        except ValueError:
            return numbers.index(content) + 1

    as_int = list(map(x, matches))
    return int(f"{as_int[0]}{as_int[-1]}")

print(sum(map(to_int, map(lambda w: re.findall(number_regex, w), x.split("\n")))))
