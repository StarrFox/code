import asyncio
import traceback

from wizwalker import WizWalker
from wizwalker.memory.enums import WindowFlags


def lift_rect(rect, f, t):
    (x1, y1, x2, y2) = rect
    (fx1, fy1, fx2, fy2) = f
    (tx1, ty1, tx2, ty2) = t

    fw = fx2 - fx1
    fh = fy2 - fy1

    tw = tx2 - tx1
    th = ty2 - ty1

    return (
        (x1 / fw) * tw,
        (y1 / fh) * th,
        (x2 / fw) * tw,
        (y2 / fh) * th,
    )


async def window_to_screen_rect(window) -> tuple:
    pass


async def print_parents_rects(window):
    parent = await window.parent()
    while parent is not None:
        print(f"{await parent.name()}: {await parent.window_rectangle()} {repr(await parent.style())} {repr(await parent.flags())}")
        parent = await parent.parent()


async def main(walker):
    client = walker.get_new_clients()[0]
    await client.hook_handler.activate_root_window_hook()
    await asyncio.sleep(5)
    spells = await client.root_window.get_windows_with_type("SpellCheckBox")

    print(f"base: {await spells[0].window_rectangle()} {repr(await spells[0].style())} {repr(await spells[0].flags())}")
    await print_parents_rects(spells[0])

    await client.close()

async def handle_exceptions():
    walker = WizWalker()
    try:
        await main(walker)
    except (Exception, KeyboardInterrupt):
        traceback.print_exc()

    print("closing")
    await walker.close()


asyncio.run(handle_exceptions())
