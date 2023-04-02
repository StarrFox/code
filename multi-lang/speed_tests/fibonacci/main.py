def fib(x: int) -> int:
    if x <= 1:
        return x
    
    return fib(x - 1) + fib(x - 2)


def main():
    exit(int(fib(47) != 2971215073))


if __name__ == "__main__":
    main()
