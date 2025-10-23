from __future__ import annotations

from typing import TypeVar, Protocol, Self

# these are called a constrained typevar
def add[T: (int, str)](a: T, b: T) -> T:
    return a + b

add(1, 1) # good
add("a", "a") # good
add(1, "a") # error (good)
add("a", 1) # error

class Addable(Protocol):
    def __add__[A: Addable](self: A, other: A, /) -> A: ...

#T = TypeVar("T", bound=Addable)

def add2[T: Addable](a: T, b: T) -> T:
    return a + b


add2([], 1)
add2(1, 1)


x = [] + 1

from typing import SupportsAbs
