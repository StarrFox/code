#include <stdint.h>

static uint64_t fib(uint64_t n) {
  if (n <= 1) return n;
  return fib(n - 1) + fib(n - 2);
}

int main(void) {
  return fib(47) != 2971215073;
}