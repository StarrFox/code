import dis
import builtins

def add(x, y):
    return x + y

a = "\n================"
print("Code_info" + a)
print(dis.code_info(add))
print("Dis" + a)
dis.dis(add)

print("Misc" + a)
print(dir(add.__code__))


