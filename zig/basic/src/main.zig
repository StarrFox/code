const std = @import("std");

const numbers = [_]u8{ 1, 2, 3 };

fn sum_list(comptime list: []const u8) u32 {
    var sum: u32 = 0;

    for (list) |num| {
        sum += num;
    }

    return sum;
}

fn add(a: u32, b: u32) u32 {
    return a + b;
}

pub fn main() anyerror!void {
    var sum: u32 = 0;

    for (numbers) |num| {
        sum += num;
    }

    std.debug.print("summed = {d}\n", .{sum_list(&numbers)});
    std.debug.print("2 + 2 = {d}\n", .{add(2, 2)});
}
