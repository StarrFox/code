from typing import Optional, Union


# python enum's can't hold data
# and codon doesn't support dataclasses
class Instruction:
    # codon issue
    amount: int


class AdvanceCell(Instruction):
    def __init__(self, amount: int = 0):
        self.amount = amount


class DevanceCell(Instruction):
    def __init__(self, amount: int = 0):
        self.amount = amount


class IncrementData(Instruction):
    def __init__(self, amount: int = 0):
        self.amount = amount


class DecrementData(Instruction):
    def __init__(self, amount: int = 0):
        self.amount = amount


class WriteIo(Instruction):
    pass


class ReadIo(Instruction):
    pass


class Loop(Instruction):
    instructions: list[Instruction]

    def __init__(self, instructions: Optional[list[Instruction]] = None):
        if instructions is None:
            instructions = []
        
        self.instructions = instructions


class LoopCollector:
    depth: int
    # codon doesn't allow string type hints
    parent: "LoopCollector"
    loop: Loop

    def __init__(self, parent, depth: int = 0):
        self.depth = depth

        # codon doesn't allow None for this, it's really annoying
        self.parent = parent

        self.loop = Loop(instructions=[])

    def start(self):
        return LoopCollector(parent=self, depth=self.depth + 1)

    def end(self):
        if self.depth != 0:
            self.parent.add(self.loop)

        # codon doesn't like functions that return two types
        # so we have to do the check in execute
        # if self.depth == 0:
        #     return self.loop
        # else:
        #     self.parent.add(self.loop)
        #     return self.parent

    def add(self, instruction: Instruction):
        self.loop.instructions.append(instruction)


def parse(program: str) -> list[Instruction]:
    result: list[Instruction] = []

    last_character = "\x00"
    # codon doesn't want this to be None
    loop_collector = LoopCollector()
    
    looping: bool = True

    for character in program:
        match character:
            case ">" | "<" | "+" | "-":
                if character == last_character:
                    if looping:
                        loop_collector.loop.instructions[-1].amount += 1
                    else:
                        result[-1].amount += 1
                else:
                    match character:
                        case ">":
                            # instruction = AdvanceCell(amount=1)

                            if looping:
                                loop_collector.add(AdvanceCell(amount=1))
                            else:
                                result.append(AdvanceCell(amount=1))
                        case "<":
                            # instruction = DevanceCell(amount=1)

                            if looping:
                                loop_collector.add(DevanceCell(amount=1))
                            else:
                                result.append(DevanceCell(amount=1))
                        case "+":
                            #instruction = IncrementData(amount=1)

                            if looping:
                                loop_collector.add(IncrementData(amount=1))
                            else:
                                result.append(IncrementData(amount=1))
                        case "-":
                            #instruction = DecrementData(amount=1)

                            if looping:
                                loop_collector.add(DecrementData(amount=1))
                            else:
                                result.append(DecrementData(amount=1))

                    # codon didn't like this for some reason
                    # if loop_collector:
                    #     loop_collector.add(instruction)
                    # else:
                    #     result.append(instruction)
            case ".":
                instruction = WriteIo()
                if looping:
                    loop_collector.add(instruction)
                else:
                    result.append(instruction)
            case ",":
                instruction = ReadIo()
                if looping:
                    loop_collector.add(instruction)
                else:
                    result.append(instruction)
            case "[":
                if looping is False:
                    looping = True
                else:
                    loop_collector = loop_collector.start()
            case "]":
                loop_collector.end()

                if loop_collector.depth == 0:
                    result.append(loop_collector.loop)
                    looping = False
                    loop_collector = LoopCollector()

                else:
                    loop_collector = loop_collector.parent

                # end = loop_collector.end()
                # match end:
                #     case LoopCollector():
                #         loop_collector = end
                #     case Loop():
                #         result.append(end)
                #         loop_collector = None

        last_character = character
    
    return result


def execute(instructions: list[Instruction]):
    cells = [0] * 30_000
    position = 0

    def _execute(_instructions):
        nonlocal position

        for instruction in _instructions:
            match instruction:
                case AdvanceCell():
                    position += instruction.amount
                case DevanceCell():
                    position -= instruction.amount
                case IncrementData():
                    cells[position] += instruction.amount
                case DecrementData():
                    cells[position] -= instruction.amount
                case WriteIo():
                    print(chr(cells[position]), end="")
                case ReadIo():
                    print("Readio not supported")
                    exit(-1)
                case Loop():
                    while cells[position] != 0:
                        _execute(instruction.instructions)

    _execute(instructions)


def main():
    instructions = parse(open("program.bf").read())

    #instructions = parse("++++++++[>++++[>++>+++>+++>+<<<<-]>+>+>->>+[<]<-]>>.>---.+++++++..+++.>>.<-.<.+++.------.--------.>>+.>++.")
    execute(instructions)


if __name__ == "__main__":
    main()
