// is it faster to shift right or cmp 
#include <stdio.h>

unsigned int is_negative(signed int input) {
    return (unsigned int) input >> (sizeof(signed int) * 8) - 1;
}

int is_negative_compare(signed int input) {
    return input < 0;
}

int main() {
    printf("%d", is_negative(500));

    return 0;
}

