import asyncio
from enum import IntFlag

import pymem

from wizwalker.memory import MemoryReader


class WindowStyle(IntFlag):
    has_back = 1
    scale_children = 2
    can_move = 4
    can_scroll = 16
    focus_locked = 64
    can_focus = 128
    can_dock = 32
    do_not_capture_mouse = 256
    is_transparent = 256
    effect_fadeid = 512
    effect_highlight = 1024
    has_no_border = 2048
    ignore_parent_scale = 4096
    use_alpha_bounds = 8192
    auto_grow = 16384
    auto_shrink = 32768
    auto_resize = 49152


class Scanner(MemoryReader):
    pass


async def run():
    pm = pymem.Pymem("WizardGraphicalClient.exe")
    scanner = Scanner(pm)

    pattern = rb"PlanningPhaseWindow"
    results = await scanner.pattern_scan(pattern, module="WizardGraphicalClient.exe", return_multiple=True)
    print(f"{len(results)=}")

    for addr in results:
        base = addr - 80

        rect1 = await scanner.read_typed(base + 0xa0, "int")
        rect2 = await scanner.read_typed(base + 0xa4, "int")
        rect3 = await scanner.read_typed(base + 0xa8, "int")
        rect4 = await scanner.read_typed(base + 0xac, "int")

        style = await scanner.read_typed(base + 0x98, "int")
        # print(f"{hex(base)}")
        # print(WindowStyle(style))

        # print(f"Rect = {(rect1, rect2, rect3, rect4)}")

        if rect1 < 10000 and rect2 < 10000 and rect3 < 10000 and rect4 < 10000:
            print(f"{rect1=} {rect2=} {rect3=} {rect4=} {hex(base)=}")
            print(WindowStyle(style))


if __name__ == "__main__":
    asyncio.run(run())
