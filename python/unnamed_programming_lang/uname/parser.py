import lark

from pathlib import Path

from lark import Lark
from lark.indenter import Indenter


ROOT = Path(__file__).parent
GRAMMAR = ROOT / "grammar.lark"


class IndentHandler(Indenter):
    NL_type = '_NEWLINE'
    OPEN_PAREN_types = []
    CLOSE_PAREN_types = []
    INDENT_type = '_INDENT'
    DEDENT_type = '_DEDENT'
    tab_len = 8


class Parser:
    def __init__(self, grammar_file: str = GRAMMAR):
        with open(grammar_file) as fp:
            grammar = fp.read()

        self.lark = Lark(grammar, parser="lalr", postlex=IndentHandler())

    def parse(self, entry: str, display: bool = False):
        tree = self.lark.parse(entry)
        if display:
            print(tree.pretty())


if __name__ == "__main__":
    parser = Parser()

    test = """
let x = {
    let mut a = 1
    a + 1
}

// would print 2
echo(x)

fn add_with_1(x: u4, y: u4) u4:
    return {
        let mut z = x + y
        z + 1
    }

fn main() u4:
    let x: u4 = add_with_1(1, 1)
    print(x)

    0
"""

    parser.parse(test, display=True)

