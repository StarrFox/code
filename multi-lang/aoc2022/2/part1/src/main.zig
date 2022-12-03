const std = @import("std");

const input = @embedFile("input");

pub fn main() anyerror!void {
    var lines = std.mem.split(u8, input, "\n");

    var score: u32 = 0;

    while (lines.next()) |line| {
        // newline at end of file
        if (line.len == 0) {
            continue;
        }

        var enemy: u8 = switch (line[0]) {
            // I couldn't figure out how to make it accept "A" => 1
            65 => 1,
            66 => 2,
            67 => 3,
            else => unreachable,
        };

        var self: u8 = switch (line[2]) {
            88 => 1,
            89 => 2,
            90 => 3,
            else => unreachable,
        };

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

    std.log.info("score = {d}", .{score});
}

// a: rock
// b: paper
// c: scissors
//
// x: rock
// y: paper
// z: scissors
//
// rock paper -> win 6
// paper rock -> loss 0
// scissors scissors -> draw 3
//
// 1 2 
// 2 1
// 3 3
//
// enemy self
// self > enemy -> win
// self < enemy -> loss
// self == enemy -> tie
//
// special 3 1 
// 1 3 -> loss
// 3 1 -> win
