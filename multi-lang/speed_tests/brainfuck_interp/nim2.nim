import std/tables


type
  InstructionKind = enum
    MoveCell
    ModifyData
    WriteIo
    ReadIo
    LoopStart
    LoopEnd

  Instruction = object
    case kind: InstructionKind
    of MoveCell, ModifyData:
      count: int
    of LoopStart, LoopEnd:
      dest: int
    else:
      discard

proc countCharRun(data: string, to_count: char, start: int): int =
  for c in data[start..^1]:
    if c != to_count:
      break
    inc result


proc toInstructions(prog: string): seq[Instruction] =
  template putSimpleInstr(t: InstructionKind, negate=false) =
    let
      cnt = countCharRun(prog, c, i)
      val = if negate: -cnt else: cnt
    if result.len() > 0 and t == result[^1].kind:
      result[^1].count += val
    else:
      result.add(Instruction(
        kind : t,
        count: val
      ))
      inc ip

    i += cnt

  template advance() =
    inc ip
    inc i

  var
    i = 0
    ip = 0
    loop_stack: seq[int]
  while i < prog.len():
    let c = prog[i]
    case c
    of '>':
      putSimpleInstr(MoveCell)
    of '<':
      putSimpleInstr(MoveCell, true)
    of '+':
      putSimpleInstr(ModifyData)
    of '-':
      putSimpleInstr(ModifyData, true)
    of '.':
      result.add(Instruction(kind : WriteIo))
      advance()
    of ',':
      result.add(Instruction(kind : ReadIo))
      advance()
    of '[':
      result.add(Instruction(kind : LoopStart, dest : -1))
      loop_stack.add(ip)
      advance()
    of ']':
      let dest = loop_stack.pop()
      result.add(Instruction(kind : LoopEnd, dest : dest))
      result[dest].dest = ip
      advance()
    else:
      inc i

proc execute(program: seq[Instruction]) =
  var
    tape = newSeq[byte](30_000)
    data_pointer = 0
    inst_pointer = 0

  while inst_pointer < program.len():
    let instruction = program[inst_pointer]
    case instruction.kind
    of MoveCell:
      data_pointer += instruction.count
    of ModifyData:
      {.linearScanEnd.}
      tape[data_pointer] += cast[byte](instruction.count)
    of WriteIo:
      stdout.write(tape[data_pointer].char) 
    of ReadIo:
      echo "bad"
    of LoopStart:
      if tape[data_pointer] == 0:
        inst_pointer = instruction.dest
    of LoopEnd:
      if tape[data_pointer] != 0:
        inst_pointer = instruction.dest

    inc inst_pointer

proc main() =
  let prog = readFile("program.bf").toInstructions()
  execute(prog)

when isMainModule:
  main()
