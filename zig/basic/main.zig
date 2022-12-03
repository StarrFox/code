const std = @import("std");
const expect = @import("std").testing.expect;

pub fn main() void {
    // const message = "Hello, World!";
    // std.debug.print("{s}", .{message});
    const array = [_]u8{1, 2, 3};

    std.debug.print("{d} with length {d}\n", .{array, array.len});

    const string = "test";

    for (string) |character, index| {
        std.debug.print("{d}: {c}\n", .{index, character});
    }
}


test "an if statement" {
    var value: i8 = 0;

    if (true) {
        value -= 1;
    }

    try expect(value == -1);
}


test "while statement" {
    var value: u8 = 1;
    while (value < 100) {
        value += value;
    }
    try expect(value == 128);
}


test "for loop" {
    const string = "test";

    for (string) |character, index| {
        std.debug.print("{any}: {any}", .{index, character});
    }
}

