most of these are from https://github.com/drujensen/fib

I switched them to not print to avoid timing print formatting

the correct answer is 2971215073

current results:
```
  './build/fibc' ran
    1.76 ± 0.02 times faster than './build/fibclang'
    1.82 ± 0.02 times faster than './build/fibrust'
    2.00 ± 0.03 times faster than './build/fibnewzig'
    2.11 ± 0.03 times faster than './build/fibzig'
    2.93 ± 0.03 times faster than './build/fibgo'
```

notes:
  cpp and c produce the exact same binaries: https://godbolt.org/z/6dTo7Ga4n
  
  I'm not sure how to get julia to produce a binary
