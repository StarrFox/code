const std = @import("std");

const input = @embedFile("input");

pub fn main() anyerror!void {
    var lines = std.mem.split(u8, input, "\n");

    var highest: u32 = 0;
    var current: u32 = 0;

    while (lines.next()) |line| {
        if (line.len == 0) {
            if (current >= highest) {
                    highest = current;
                }

            current = 0;
            continue;
        }

        var parsed = try std.fmt.parseInt(u32, line, 0);
        current += parsed;
    }

    std.log.info("Highest = {d}", .{highest});
}
