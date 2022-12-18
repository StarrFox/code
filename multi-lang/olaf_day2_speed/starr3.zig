const std = @import("std");

const input = @embedFile("input.txt");

pub fn main() anyerror!void {
    var lines = std.mem.split(u8, input, "\n");

    var score: u32 = 0;

    while (lines.next()) |line| {
        // newline at end of file
        if (line.len == 0) {
            continue;
        }

        const enemy = (line[0] - 'A' + 1);
        const self = (line[2] - 'X' + 1);

        // won
        if ((enemy == 3 and self == 1) or (enemy < self and !(enemy == 1 and self == 3))) {
            score += 6;
        }
        // tie
        else if (enemy == self) {
            score += 3;
        }
        score += self;
    }

    std.debug.print("score = {d}", .{score});
}
