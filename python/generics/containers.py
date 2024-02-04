from typing import reveal_type

class Obj: ...
class Property: ...

class Pointer[T: Obj | Property](Property):
    def __init__(self, pointed_type: type[T] | T):
        self.pointed_type = pointed_type

    def get(self) -> T:
        if isinstance(self.pointed_type, type):
            return self.pointed_type()
        return self.pointed_type

class A(Obj):
    def __init__(self) -> None:
        self.data = 100

class B: ...

ptr = Pointer(A) # good
ptr_1 = Pointer(B) # error here is expected
ptr_2 = Pointer(Pointer(A)) # good

reveal_type(ptr)
reveal_type(ptr.get())

assert ptr.get().data == 100 # good
