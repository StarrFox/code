function fib(n)
    if n <= 1
        return n
    end

    return fib(n - 1) + fib(n - 2)
end

function main()
    exit(fib(47) != 2971215073)
end

main()
