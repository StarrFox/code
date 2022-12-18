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

        const rock_win = 6 + 1;
        const rock_tie = 3 + 1;
        const rock_loss = 1;
        
        const paper_win = 6 + 2;
        const paper_tie = 3 + 2;
        const paper_loss = 2;

        const scissors_win = 6 + 3;
        const scissors_tie = 3 + 3;
        const scissors_loss = 3;

        // A B C | X Y Z
        // rock, paper, scissors
        score += switch (line) {
            "A X" => rock_tie,
            "A Y" => paper_win,
            "A Z" => scissors_loss,

            "B X" => rock_loss,
            "B Y" => paper_tie,
            "B Z" => scissors_win,

            "C X" => rock_win,
            "C Y" => paper_loss,
            "C Z" => 
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
