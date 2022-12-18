const file = block:
  var 
    data = slurp("input.txt")
    i = 0
  while i < data.len():
    data[i] = cast[char](cast[byte](data[i]) - cast[byte]('@'))
    data[i+2] = cast[char](cast[byte](data[i+2]) - cast[byte]('W'))
    i += 4
  data

var score = 0

var i = 0
while i < file.len():
  let
    enemy = file[i]
    me = file[i+2]

  if (enemy == '\x03' and me == '\x01') or (enemy < me and not (enemy == '\x01' and me == '\x03')):
    score += 6
  elif enemy == me:
    score += 3

  score += int(me)
  i += 4

echo score
