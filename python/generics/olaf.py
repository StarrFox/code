def foo(x: int) -> int | float | str:
    if x == 0:
        return 1
    elif x == 1:
        return 1.0
    return "a"

f = foo(2)
match f:
    case int():
        print("int")
    case float():
        print("float")
    case str():
        pass
