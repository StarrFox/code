from collections import namedtuple
from enum import Enum
from typing import Self


class _Parse_rule_type(Enum):
    arg = 1
    token = 2


Argument = namedtuple("Argument", "name value")
Token = namedtuple("Token", "value")


class _Parse_rule:
    def __init__(self, rule_type: _Parse_rule_type, arg):
        self.rule_type = rule_type
        self.arg = arg

    def parse(self, entry: str) -> Argument | Token:
        match self.rule_type:
            case _Parse_rule_type.arg:
                return Argument(self.arg, entry)
            case _Parse_rule_type.token:
                if self.arg == entry:
                    return Token(value=entry)
            case _:
                raise NotImplemented()


class _Command:
    def __init__(self, name: str):
        self.name = name

        self.parse_rules = []

    def parse(self, entry: str) -> list[Token | Argument]:
        parts = entry.split(" ")

        parsed: list[Token | Argument] = []

        if len(parts) - 1 != len(self.parse_rules):
            raise ValueError("Not enough stuff passed")

        for part, parse_rule in zip(parts[1:], self.parse_rules):
            parsed.append(parse_rule.parse(part))

        return parsed

    def arg(self, name: str) -> Self:
        self.parse_rules.append(_Parse_rule(_Parse_rule_type.arg, name))
        return self

    def token(self, value: str) -> Self:
        self.parse_rules.append(_Parse_rule(_Parse_rule_type.token, value))
        return self


_commands = {
    # select id,name from users
    "select": _Command("select").arg("collum").token("from").arg("table"),
    # post id,name to users 1,jim
    "post": _Command("post").arg("collums").token("to").arg("table").arg("value"),
    "update": _Command("update").arg("")
}


class Query:
    def __init__(self):
        pass

    @classmethod
    def from_string(cls, string: str) -> Self:
        pass


if __name__ == "__main__":
    select = _Command("select").arg("collums").token("from").arg("table")
    parsed = select.parse("select name from users")

    print(parsed)

