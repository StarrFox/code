# these are called a constrained typevar
def add[T: (int, str)](a: T, b: T) -> T:
    return a + b

add(1, 1) # good
add("a", "a") # good
add(1, "a") # error (good)



