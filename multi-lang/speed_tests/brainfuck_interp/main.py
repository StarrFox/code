# stolen from https://github.com/alexprengere/PythonBrainFuck/blob/70af2a2313c029c1eab640e63f485939ac8f1fb6/bf.py#L40-L56
def create_jump_table(chars):
    jump_table = {}
    left_positions = []

    position = 0
    for char in chars:
        if char == '[':
            left_positions.append(position)

        elif char == ']':
            left = left_positions.pop()
            right = position
            jump_table[left] = right
            jump_table[right] = left
        position += 1

    return jump_table


def execute(program: str):
    tape = [0] * 30000

    end = len(program)

    data_pointer = 0
    inst_pointer = 0
    jumps = create_jump_table(program)

    while inst_pointer < end:
        
        instruction = program[inst_pointer]

        match instruction:
            case ">":
                data_pointer += 1
            case "<":
                data_pointer -= 1
            case "+":
                tape[data_pointer] += 1
            case "-":
                tape[data_pointer] -= 1
            case ".":
                print(chr(tape[data_pointer]), end="")
            case ",":
                print("bad")
                # entry = input()

                # if len(entry) == 0:
                #     tape[data_pointer] = 0

                # tape[data_pointer] = ord(entry[0])
            case "[":
                if tape[data_pointer] == 0:
                    # the +1 at the end of while will move it to the next command after the ]
                    inst_pointer = jumps[inst_pointer]
            case "]":
                if tape[data_pointer] != 0:
                    inst_pointer = jumps[inst_pointer]
            case _:
                pass

        inst_pointer += 1



def main():
    #execute("++++++++[>++++[>++>+++>+++>+<<<<-]>+>+>->>+[<]<-]>>.>---.+++++++..+++.>>.<-.<.+++.------.--------.>>+.>++.")
    execute(open("program.bf").read())


if __name__ == "__main__":
    main()
