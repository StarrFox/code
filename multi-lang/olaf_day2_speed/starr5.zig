const std = @import("std");

const raw_input align(@alignOf(u32)) = @embedFile("input.txt");

pub fn main() anyerror!void {
    const ints = std.mem.bytesAsSlice(u32, raw_input);

    var result: u32 = @truncate(u32, ints.len);

    for (ints) |int| {
        // what does o stand for
        const o: u32 = (int *% 1887065750) >> 27;
        const number: u32 = 475903013;
        result += @boolToInt(int == 173678658) + (std.math.shr(u32, number, o) & 7);
    }

    std.debug.print("{d}", .{result});
}
