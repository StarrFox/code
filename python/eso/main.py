def execute(program: str):
    position = 0
    variables = {}

    while position < len(program):
        instruction = program[position]

        match instruction:
            case "s":
                variable = program[position + 1]
                value = program[position + 2]

                if value.isnumeric():
                    variables[variable] = int(value)
                else:
                    variables[variable] = ord(value)

                position += 3
            case "p":
                variable = program[position + 1]
                value = variables.get(variable, 0)
                print(chr(value), end="")

                position += 2
            case _:
                position += 1


def main():
    execute("""
sxa
px
""")


if __name__ == "__main__":
    main()
