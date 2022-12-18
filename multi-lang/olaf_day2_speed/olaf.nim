import std/strutils

type
  Move = enum
    Rock
    Paper
    Scissors
    Invalid

  Outcome = enum
    Lose
    Draw
    Win

func toMove(c: char): Move {.inline.} =
  result = case c
  of 'A', 'X':
    Move.Rock
  of 'B', 'Y':
    Move.Paper
  of 'C', 'Z':
    Move.Scissors
  else:
    {.linearScanEnd.}
    Move.Invalid

func getOutcome(me: Move, other: Move): Outcome {.inline.} =
  if me == other:
    return Outcome.Draw
  elif (me == Rock and other == Scissors) or 
    (me == Paper and other == Rock) or
    (me == Scissors and other == Paper):
    return Outcome.Win
  else:
    return Outcome.Lose

func getScore(me: Move, other: Move): int {.inline.} =
  result = int(me) + 1
  result += int(getOutcome(me, other)) * 3

var fullscore = 0
for l in lines("input.txt"):
  let
    #s = l.split()
    #(other, me) = (s[0][0].toMove(), s[1][0].toMove())
    (other, me) = (l[0].toMove(), l[2].toMove())
  fullscore += getScore(me, other)
echo fullscore
