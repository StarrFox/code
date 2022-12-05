const std = @import("std");

const input = @embedFile("input");

pub fn main() anyerror!void {
    var lines = std.mem.split(u8, input, "\n");

    var overlapping: u32 = 0;
    while (lines.next()) |line| {
        if (line.len == 0) {
            continue;
        }

        // is there a way to do something like elf1, elf2 = split(...)
        var elfs = std.mem.split(u8, line, ",");

        const elf1 = elfs.next().?;
        const elf2 = elfs.next().?;

        var elf1_range = std.mem.split(u8, elf1, "-");
        var elf2_range = std.mem.split(u8, elf2, "-");

        const elf1_start = try std.fmt.parseInt(u8, elf1_range.next().?, 0);
        const elf1_end = try std.fmt.parseInt(u8, elf1_range.next().?, 0);

        const elf2_start = try std.fmt.parseInt(u8, elf2_range.next().?, 0);
        const elf2_end = try std.fmt.parseInt(u8, elf2_range.next().?, 0);

        if ((elf2_start <= elf1_start and elf1_start <= elf2_end) or (elf1_start <= elf2_end and elf2_end <= elf1_start)) {
            overlapping += 1;
        }
        else if ((elf1_start <= elf2_start and elf2_start <= elf1_end) or (elf2_start <= elf1_end and elf1_end <= elf2_start)) {
            overlapping += 1;
        }

    }

    std.log.info("{d}", .{overlapping});
}
