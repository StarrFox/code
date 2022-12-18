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

        const enemy = line[0];
        const self = line[2];
        const enemy_converted = (enemy - 'A' + 1);
        const self_converted = (self - 'X' + 1);

        // won
        if ((enemy == 'C' and self == 'X') or (enemy_converted < self_converted and !(enemy == 'A' and self == 'Z'))) {
            score += 6;
        }
        // tie
        else if (enemy_converted == self_converted) {
            score += 3;
        }
        score += self_converted;
    }

    std.debug.print("score = {d}", .{score});
}
