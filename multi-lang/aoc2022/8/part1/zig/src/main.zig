const std = @import("std");

const input = @embedFile("input");
const row_length = @truncate(u32, std.mem.indexOfPos(u8, input, 0, "\n").?);
const rows = @truncate(u32, input.len / row_length);

// 30373
// 25512
// 65332
// 33549
// 35390

// vvvvv
// vvv1v
// vv3vv
// v3v4v
// vvvvv

pub fn main() anyerror!void {
    var lines = std.mem.split(u8, input, "\n");
    // first row is skipped
    var row_number: u32 = 1;

    var visable: u32 = 0;

    // top = max; level = min
    var horizontal_top: u8 = 0;
    var horizontal_span: u32 = 0;
    var horizontal_level: u8 = 0;
    var vertical_top = [_]u8{0} ** row_length;
    var vertical_span = [_]u32{0} ** rows;
    var vertical_level = [_]u8{0} ** row_length;

    // [x x x x x]
    //  x x x x x
    //  x hhhhh x
    //  x v x x x
    //  x v x x x
    //  x v x x x
    //  x x x x x
    // [x x x x x]

    const first_row = lines.next().?;
    var first_index: u32 = 0;
    // using a while true might be faster
    for (first_row) |tree| {
        if (first_index == 0) {
            first_index = 1;
            continue;
        }
        else if (first_index == row_length) {
            break;
        }

        vertical_top[first_index] = tree;
        first_index += 1;
    }

    // first row are all visable
    visable += row_length;

    var visable_flag: u1 = 0;

    while (lines.next()) |line| {
        std.log.debug("Row {d}", .{row_number});
        if (line.len == 0) {
            continue;
        }

        visable_flag = 0;
        var tree_index: u32 = 0;

        // last row
        if (row_number == rows - 1) {
            // last row are all visable
            std.log.debug("last row: {d}+{d}", .{visable, row_length});
            visable += row_length;

            for (line) |tree| {
                if (tree_index == 0) {
                    tree_index = 1;
                    continue;
                }

                if (tree < vertical_top[tree_index] or tree < vertical_level[tree_index]) {
                    std.log.debug(
                        "verticle: span passed {c} < {c} visable {d}+{d}",
                        .{tree, vertical_top[tree_index] ,visable, horizontal_span}
                        );
                    visable += vertical_span[tree_index];
                }

                tree_index += 1;
            }

            break;
        }

        horizontal_span = 0;
        for (line) |tree| {
            if (tree_index == 0) {
                horizontal_top = tree;
                tree_index = 1;
                continue;
            }
            // last collum
            else if (tree_index == row_length - 1) {
                if (tree < horizontal_level) {
                    std.log.debug("horizontal: span passed {c} < {c} visable {d}+{d}", .{tree, horizontal_level, visable, horizontal_span});
                    visable += horizontal_span;
                }
                std.log.debug("last collum: visable {d}+1", .{visable});
                visable += 1;
                break;
            }

            std.log.debug("horizontal: compare {c}[{d}] {c}[{d}]", .{tree, tree, horizontal_top, horizontal_top});
            if (tree > horizontal_top) {
                std.log.debug("horizontal: passed visable {d}+1", .{visable});
                visable += 1;
                visable_flag = 1;
                horizontal_top = tree;
                horizontal_span = 0;
                horizontal_level = tree;
            }
            else {
                if (tree <= horizontal_level) {
                    std.log.debug("horizontal: level drop {c} <= {c} span {d}+1", .{tree, horizontal_level, horizontal_span});
                    horizontal_level = tree;
                    horizontal_span += 1;
                }
            }

            std.log.debug("verticle: compare {c}[{d}] {c}[{d}]", .{tree, tree, vertical_top[tree_index], vertical_top[tree_index]});
            if (tree > vertical_top[tree_index]) {
                std.log.debug("verticle: passed", .{});
                if (visable_flag == 0) {
                    std.log.debug("verticle: passed and flag 0ed {d}+1", .{visable});
                    visable += 1;
                }

                vertical_top[tree_index] = tree;
                vertical_span[tree_index] = 0;
                vertical_level[tree_index] = tree;
            }
            else {
                if (tree <= vertical_level[tree_index]) {
                    std.log.debug("verticle: level drop {c} <= {c} span {d}+1", .{tree, vertical_level[tree_index], vertical_span[tree_index]});
                    vertical_level[tree_index] = tree;
                    vertical_span[tree_index] += 1;
                }
            }

            std.log.debug(
                "index {d} tree {c} tops {c} {c} levels {c} {c} spans {d} {d}",
                .{tree_index, tree, horizontal_top, vertical_top, horizontal_level, vertical_level, horizontal_span, vertical_span}
            );

            tree_index += 1;
        }

        row_number += 1;
    }

    // first of each row is visable
    visable += rows;
    std.debug.print("Visable: {d}", .{visable});
}
