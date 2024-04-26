from enum import Enum


class FormatType(Enum):
    int = "i"
    uint = "I"


def abc(*types: FormatType): ...






