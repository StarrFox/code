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
            'A' => 1,
            'B' => 2,
            'C' => 3,
            else => unreachable,
        };

        var solution = line[2];

        // solution points
        if (solution == 'Z') {
            score += 6;
        }
        else if (solution == 'Y') {
            score += 3;
        }

        // move points
        if (solution == 'Z') {
            if (enemy == 3) {
                score += 1;
            }
            else {
                score += enemy + 1;
            }
        }
        else if (solution == 'Y') {
            score += enemy;
        }
        else if (solution == 'X') {
            if (enemy == 1) {
                score += 3;
            }
            else {
                score += enemy - 1;
            }
        }
    }

    std.log.info("score = {d}", .{score});
}

// a: rock
// b: paper
// c: scissors
//
// x: lose
// y: draw
// z: win
//
// rock draw -> rock 1 + 3 4
// paper lose -> rock 1 + 0 1
// scissors win -> rock 1 + 6 8
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

// 3 beats 2
// 2 beats 1
// 1 beats 3
