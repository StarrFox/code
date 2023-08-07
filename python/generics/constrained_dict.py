# NOTE: this doesn't work (line 18 isn't seen as invalid)

from typing import TypeVar

T = TypeVar("T")

class ConstrainedDict(dict):
    def __getitem__(self, __key: T) -> T:
        return super().__getitem__(__key)

    def __setitem__(self, __key: T, __value: T):
        return super().__setitem__(__key, __value)

x: ConstrainedDict = ConstrainedDict()

x[1] = 2         # good
x["abc"] = "def" # good
x["test"] = 1    # not good

y = x["test"]
w = x[1]
