const std = @import("std");
const input = @embedFile("input");

const CrateStack = struct {
    // how do I make this work with any size array
    stack: [200]u8,

    pub fn init() CrateStack {
        return .{
            .stack = [_]u8{0} ** 200,
        };
    }
};

pub fn main() anyerror!void {
    const stack = CrateStack.init();

    std.log.info("len {d}", .{stack.stack});
}
