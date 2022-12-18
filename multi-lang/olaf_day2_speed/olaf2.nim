import strutils

type
  Move = enum
    Rock = 1
    Paper = 2
    Scissors = 3
    Invalid

  Outcome = enum
    Lose
    Draw
    Win

template toMove(c: char): Move =
  case c
  of 'A', 'X':
    Move.Rock
  of 'B', 'Y':
    Move.Paper
  of 'C', 'Z':
    Move.Scissors
  else:
    Move.Invalid

func getOutcome(me: Move, other: Move): Outcome =
  if me == other:
    return Outcome.Draw
  elif (me == Rock and other == Scissors) or 
    (me == Paper and other == Rock) or
    (me == Scissors and other == Paper):
    return Outcome.Win
  else:
    return Outcome.Lose

template getScore(me: Move, other: Move): int =
  int(me) + int(getOutcome(me, other)) * 3

const file = slurp("input.txt")

var fullscore = 0
for l in file.splitLines():
  let (other, me) = (l[0].toMove(), l[2].toMove())
  fullscore += getScore(me, other)
echo fullscore
