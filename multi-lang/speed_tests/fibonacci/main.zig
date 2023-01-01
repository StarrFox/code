//const std = @import("std");

fn fib(x: u64) u64 {
    if (x <= 1) return x;
    return fib(x - 1) + fib(x - 2);
}

pub fn main() u8 {
    //const stdout = std.io.getStdOut().writer();
    //try stdout.print("{d}", .{fib(47)});

    // not sure how much time is lost from this bool to int conversion
    // zig doesn't allow you to return `bool` from main
    return @boolToInt(fib(47) != 2971215073);
}
