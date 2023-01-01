use std::process::ExitCode;

fn fib(n: u64) -> u64 {
    if n <= 1 {
        return n;
    }
    fib(n - 1) + fib(n - 2)
}

fn main() -> ExitCode {
    //println!("{}", fib(47));
    ExitCode::from((fib(47) != 2971215073) as u8)
}
