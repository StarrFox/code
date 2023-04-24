import std/tables
import std/[strformat, strutils]


type
  InstructionKind = enum
    SetZero
    MoveMod
    ModMove
    SearchZero
    OffsetZero

    MoveCell
    ModifyData
    WriteIo
    ReadIo
    LoopStart
    LoopEnd

  Instruction = object
    case kind: InstructionKind
    of MoveMod, ModMove:
      offset: int
      change: int
    of SearchZero:
      step: int
    of OffsetZero:
      at_offset: int

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

proc toIR(prog: seq[Instruction]): seq[string] =
  var indent = 0

  template put(s: string) =
    result.add(" ".repeat(indent) & s)

  for i in prog:
    case i.kind
      of SetZero:
        put "SetZero"
      of MoveMod:
        put fmt"MoveMod({i.offset}, {i.change})"
      of ModMove:
        put fmt"ModMove({i.change}, {i.offset})"
      of SearchZero:
        put fmt"SearchZero({i.step})"
      of OffsetZero:
        put fmt"OffsetZero({i.at_offset})"

      of MoveCell:
        put fmt"Move({i.count})"
      of ModifyData:
        put fmt"Mod({i.count})"
      of WriteIo:
        put "IOWrite"
      of ReadIo:
        put "IORead"
      of LoopStart:
        put "{"
        indent += 2
      of LoopEnd:
        indent -= 2
        put "}"

proc toInstructions(prog: string, optimize=true): seq[Instruction] =
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

    if optimize and result.len() > 2:
      # TODO: Repeat in while loop so it can be reduced further
      block:
        # left to right
        let
          a = result[^3]
          b = result[^2]
          c = result[^1]
        if a.kind == LoopStart and b.kind == ModifyData and b.count == -1 and c.kind == LoopEnd:
          result.setLen(result.len() - 3)
          result.add(Instruction(kind : SetZero))
          ip -= 2
        elif a.kind == LoopStart and b.kind == MoveCell and c.kind == LoopEnd:
          result.setLen(result.len() - 3)
          result.add(Instruction(
            kind : SearchZero,
            step : b.count
          ))
          ip -= 2
      block:
        let
          a = result[^2]
          b = result[^1]
        if a.kind == MoveCell and b.kind == ModifyData:
          result.setLen(result.len() - 2)
          result.add(Instruction(
            kind : MoveMod,
            offset : a.count,
            change : b.count
          ))
          ip -= 1
        elif a.kind == MoveCell and b.kind == SetZero:
          result.setLen(result.len() - 2)
          result.add(Instruction(
            kind : OffsetZero,
            at_offset : a.count
          ))
          ip -= 1
        elif a.kind == ModifyData and b.kind == MoveCell:
          result.setLen(result.len() - 2)
          result.add(Instruction(
            kind : ModMove,
            offset : b.count,
            change : a.count
          ))
          ip -= 1


proc execute(program: seq[Instruction]) =
  var
    tape: array[30_000, byte]
    data_pointer = 0
    inst_pointer = 0

    current_cell: byte = 0

  template moveTape(offset: int) =
    tape[data_pointer] = current_cell
    data_pointer += offset
    current_cell = tape[data_pointer]

  template setTape(value: byte) =
    #tape[data_pointer] = value
    current_cell = value

  template modTape(change: byte) =
    #tape[data_pointer] += change
    current_cell += change

  template readTape(): byte =
    #tape[data_pointer]
    current_cell

  while inst_pointer < program.len():
    let instruction {.cursor.} = program[inst_pointer]
    case instruction.kind
    of SetZero:
      setTape(0)
    of MoveMod:
      moveTape(instruction.offset)
      modTape(cast[byte](instruction.change))
    of ModMove:
      modTape(cast[byte](instruction.change))
      moveTape(instruction.offset)
    of SearchZero:
      while readTape() != 0:
        moveTape(instruction.step)
    of OffsetZero:
      moveTape(instruction.at_offset)
      setTape(0)

    of MoveCell:
      moveTape(instruction.count)
    of ModifyData:
      {.linearScanEnd.}
      modTape(cast[byte](instruction.count))

    of WriteIo:
      stdout.write(readTape().char) 
    of ReadIo:
      echo "bad"
    of LoopStart:
      if readTape() == 0:
        inst_pointer = instruction.dest
    of LoopEnd:
      if readTape() != 0:
        inst_pointer = instruction.dest

    inc inst_pointer

proc main() =
  let prog = readFile("program.bf").toInstructions()
  execute(prog)

when isMainModule:
  main()
