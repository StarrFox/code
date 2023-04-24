from pathlib import Path

from lark import Lark, Transformer


ROOT = Path(__file__).parent
GRAMMAR = ROOT / "grammar.lark"

class Parser:
    def __init__(self, grammar_file: str = GRAMMAR):
        with open(grammar_file) as fp:
            grammar = fp.read()

        self.lark = Lark(grammar)

    def parse(self, entry: str, display: bool = False):
        tree = self.lark.parse(entry)
        if display:
            print(tree.pretty())

        transformer = BfTransformer()
        tree = transformer.transform(tree)

        return tree.children


class Instruction:
    def __init__(self, _type: str, arg: int | list["Instruction"] = 0):
        self._type = _type
        self.arg = arg

    def __repr__(self) -> str:
        return f"{self._type}: {self.arg}"


class BfTransformer(Transformer):
    def instruction(self, value):
        return Instruction(value[0].data, len(value[0].children))

    def loop(self, value):
        return Instruction("loop", value)


def parse(program: str) -> list[Instruction]:
    parser = Parser()
    return parser.parse(program)


if __name__ == "__main__":
    parser = Parser()

    test = """++++++++[>++++[>++>+++>+++>+<<<<-]>+>+>->>+[<]<-]>>.>---.+++++++..+++.>>.<-.<.+++.------.--------.>>+.>++."""

    instructions = parser.parse(test, display=False)
    print(instructions)
