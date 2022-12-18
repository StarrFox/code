import strutils

const file = slurp("input.txt")

var score = 0

for line in file.split("\n"):
  if line.len() == 0:
    continue

  let
    enemy = int(line[0]) - int('@')
    me = int(line[2]) - int('W')
  
  if (enemy == 3 and me == 1) or (enemy < me and not (enemy == 1 and me == 3)):
    score += 6
  elif enemy == me:
    score += 3

  score += me

echo score
