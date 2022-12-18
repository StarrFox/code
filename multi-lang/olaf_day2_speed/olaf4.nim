const file = slurp("input.txt")

iterator bettersplit(s: string, sep: char): ptr[byte] =
  var last = 0

  while last <= len(s):
    var first = last
    while last < len(s) and not (s[last] == sep):
      inc(last)
    yield cast[ptr[byte]](unsafeAddr s[first])
    inc last

template read(p: pointer, offset: int): byte =
  cast[ptr byte](cast[ByteAddress](p) + offset)[]


var score = 0

for line in bettersplit(file, '\n'):
  if line.read(0) == 0x0A:
    continue

  let
    enemy = line.read(0) - cast[byte]('@')
    me = line.read(2) - cast[byte]('W')
 
  if (enemy == 3 and me == 1) or (enemy < me and not (enemy == 1 and me == 3)):
    score += 6
  elif enemy == me:
    score += 3

  score += int(me)

echo score