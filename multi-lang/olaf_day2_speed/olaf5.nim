const file = slurp("input.txt")

var score = 0

var i = 0
while i < file.len():
  let
    enemy = int(file[i]) - int('@')
    me = int(file[i+2]) - int('W')

  if (enemy == 3 and me == 1) or (enemy < me and not (enemy == 1 and me == 3)):
    score += 6
  elif enemy == me:
    score += 3

  score += int(me)

  inc(i, 4)

echo score
