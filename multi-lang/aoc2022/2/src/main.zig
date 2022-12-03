const std = @import("std");

const input = @embedFile("input");

pub fn main() anyerror!void {
    var lines = std.mem.split(u8, input, "\n");

    var current: u32 = 0;
    var top_three = [3]u32{0, 0, 0};

    while (lines.next()) |line| {
        if (line.len == 0) {
            // 1st, 2nd, 3rd
            for ([_]u8{ 0, 1, 2 }) |index| {
                // note: this doesn't account for duplicates
                if (top_three[index] < current) {
                    var overdraft = 2 - index;
                    while (overdraft > 0) {
                        top_three[index + 1] = top_three[index];
                        overdraft -= 1;
                    }
                    top_three[index] = current;
                    break;
                }
            }

            current = 0;
            continue;
        }

        var parsed = try std.fmt.parseInt(u32, line, 0);
        current += parsed;
    }

    var top_three_total: u32 = 0;

    for (top_three) |top_three_entry| {
        top_three_total += top_three_entry;
    }

    std.log.info("Top three = {d}, total = {d}", .{top_three, top_three_total});
}
