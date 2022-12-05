const std = @import("std");

fn atest() u8 {
    return 1;
}

pub fn main() anyerror!void {
    var value = atest();
    std.log.info("value {d}", .{value});
}

test "basic test" {
    try std.testing.expectEqual(10, 3 + 7);
}

test "overflow" {
    const value: u2 = 3;
    try std.testing.expectEqual(0, value +% 1);
}

test "u3" {
    const value: u3 = 7;
    try std.testing.expectEqual(0, value +% 1);
}
