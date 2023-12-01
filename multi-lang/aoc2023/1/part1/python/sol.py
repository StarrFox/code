import re

x = open("input").read().strip()
print(sum(map(int, (f"{i[0]}{i[-1]}" for i in map(lambda w: re.findall(r"\d", w), x.split("\n"))))))
