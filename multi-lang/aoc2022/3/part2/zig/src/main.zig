const std = @import("std");

const input = @embedFile("input");

fn u8in(look_for: u8, within: []const u8) bool {
    for (within) |item| {
        if (look_for == item) {
            return true;
        }
    }
    return false;
}

pub fn main() anyerror!void {
    var lines = std.mem.split(u8, input, "\n");

    while (lines.next()) |line| {
        if (line.len == 0) {
            continue;
        }


    }
}
