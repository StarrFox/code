import std/tables


proc createJumpTable(chars: string): Table[int, int] =
  var
    left_positions: seq[int]
    position = 0
  for c in chars:
    if c == '[':
      left_positions.add(position)
    elif c == ']':
      let
        left = left_positions.pop()
        right = position
      result[left] = right
      result[right] = left
    inc position

proc execute(program: string) =
  var
    tape = newSeq[byte](30_000)
    data_pointer = 0
    inst_pointer = 0
  let jumps = createJumpTable(program)

  while inst_pointer < program.len():
    let instruction = program[inst_pointer]
    case instruction
    of '>':
      inc data_pointer
    of '<':
      dec data_pointer
    of '+':
      inc tape[data_pointer]
    of '-':
      #cheating
      #{.linearScanEnd.}
      dec tape[data_pointer]
    of '.':
      stdout.write(tape[data_pointer].char) 
    of ',':
      echo "bad"
    of '[':
      if tape[data_pointer] == 0:
        inst_pointer = jumps[inst_pointer]
    of ']':
      if tape[data_pointer] != 0:
        inst_pointer = jumps[inst_pointer]
    else:
      discard

    inc inst_pointer

proc main() =
  let prog = readFile("program.bf")
  execute(prog)

when isMainModule:
  main()