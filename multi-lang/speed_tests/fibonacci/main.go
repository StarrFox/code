package main

import "os"

func fib(n uint64) uint64 {
	if n <= 1 { return n }
	return fib(n - 1) + fib(n - 2)
}

func main() {
	if fib(47) != 2971215073 {
		os.Exit(1)
	}
	os.Exit(0)
}
