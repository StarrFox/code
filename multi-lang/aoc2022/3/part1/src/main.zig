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

    var priority_sum: u32 = 0;

    while (lines.next()) |line| {
        if (line.len == 0) {
            continue;
        }

        const half_line = line.len / 2;

        const comparment1 = line[0..half_line];
        const comparment2 = line[half_line..line.len];

        var match_type: u8 = undefined;
        for (comparment2) |item| {
            if (u8in(item, comparment1)) {
                match_type = item;
                break;
            }
        }

        if (match_type >= 'a') {
            priority_sum += match_type - 'a' + 1;
        }
        else {
            priority_sum += match_type - 38;
        }
    }

    std.log.info("Priority sum {d}", .{priority_sum});

}
