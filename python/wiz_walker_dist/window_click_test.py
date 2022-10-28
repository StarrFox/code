import asyncio
import traceback

from wizwalker import WizWalker


def get_center_point(base, parent_rects):
    print(f"{base=} {parent_rects=}")
    x_sum = base[0]
    y_sum = base[1]

    upscale_x_sum = base[2]
    upscale_y_sum = base[3]

    # upscale_x_sum = 0
    # upscale_y_sum = 0

    for rect in parent_rects:
        x_sum += rect[0]
        y_sum += rect[1]

        upscale_x_sum += rect[2]
        upscale_y_sum += rect[3]

    print(f"{x_sum=} {y_sum=} {upscale_x_sum=} {upscale_y_sum=}")

    # TODO: check if upscale between client and root is always 80%
    upscale_x_factor = ((x_sum + upscale_x_sum) / (len(parent_rects) + 1)) / 800
    upscale_y_factor = ((y_sum + upscale_y_sum) / (len(parent_rects) + 1)) / 600

    print(f"{upscale_x_factor=} {upscale_y_factor=}")

    converted = (
        int(x_sum * upscale_x_factor),
        int(y_sum * upscale_y_factor),
        int(((base[2] - base[0]) * upscale_x_factor) + (x_sum * upscale_x_factor)),
        int(((base[3] - base[1]) * upscale_y_factor) + (y_sum * upscale_y_factor)),
    )

    print(f"{converted=}")

    center_x = ((converted[2] - converted[0]) // 2) + converted[0]
    center_y = ((converted[3] - converted[1]) // 2) + converted[1]

    return center_x, center_y


def get_center_point_2(base, parent_rects):
    print(f"{base=} {parent_rects=}")
    x1_sum = base[0]
    y1_sum = base[1]

    x2_sum = base[2]
    y2_sum = base[3]

    # upscale_x_sum = base[2] - 999
    # upscale_y_sum = base[3] - 749

    upscale_x_sum = 0
    upscale_y_sum = 0

    for rect in parent_rects:
        x1_sum += rect[0]
        y1_sum += rect[1]

        x2_sum += rect[2]
        y2_sum += rect[3]

        upscale_x_sum += rect[2] - 999
        upscale_y_sum += rect[3] - 749

    print(f"{x1_sum=} {y1_sum=} {x2_sum=} {y2_sum=} {upscale_x_sum=} {upscale_y_sum=}")

    # TODO: check if upscale between client and root is always 80%
    upscale_x_factor = 800 / (999 + upscale_x_sum)
    upscale_y_factor = 600 / (749 + upscale_y_sum)

    print(f"{upscale_x_factor=} {upscale_y_factor=}")

    converted = (
        int(x1_sum * upscale_x_factor),
        int(y1_sum * upscale_y_factor),
        int(((base[2] - base[0]) * upscale_x_factor) + (x1_sum * upscale_x_factor)),
        int(((base[3] - base[1]) * upscale_y_factor) + (y1_sum * upscale_y_factor)),
    )

    print(f"{converted=}")

    center_x = ((converted[2] - converted[0]) // 2) + converted[0]
    center_y = ((converted[3] - converted[1]) // 2) + converted[1]

    return center_x, center_y


def scale_by_80(base, parent_rects):
    print(f"{base=} {parent_rects=}")
    x1_sum = base[0]
    y1_sum = base[1]

    for rect in parent_rects:
        x1_sum += rect[0]
        y1_sum += rect[1]

    upscale_x_factor = 0.8
    upscale_y_factor = 0.8

    print(f"{upscale_x_factor=} {upscale_y_factor=}")

    converted = (
        int(x1_sum * 0.8),
        int(y1_sum * 0.8),
        int(((base[2] - base[0]) * upscale_x_factor) + (x1_sum * upscale_x_factor)),
        int(((base[3] - base[1]) * upscale_y_factor) + (y1_sum * upscale_y_factor)),
    )

    print(f"{converted=}")

    center_x = ((converted[2] - converted[0]) // 2) + converted[0]
    center_y = ((converted[3] - converted[1]) // 2) + converted[1]

    return center_x, center_y


async def click_help_chat_button(client):
    #name = "btnHelpChat"
    name = "Card5"
    #name = "btnSpellbook"
    #name = "btnFriends"

    await client.hook_handler.activate_root_window_hook()
    await client.mouse_handler.activate_mouseless()
    window = (await client.root_window.get_windows_with_name(name))[0]

    base_rect = await window.window_rectangle()

    parent_rects = []
    idx = 0
    for parent in await window.get_parents():
        print(await parent.flags())
        parent_rects.append(await parent.window_rectangle())

    center = scale_by_80(base_rect, parent_rects)

    print(f"{center=}")

    await client.mouse_handler.click(*center)


async def main():
    walker = WizWalker()
    client = walker.get_new_clients()[0]
    try:
        await click_help_chat_button(client)
    except Exception:
        traceback.print_exc()
    await client.close()


if __name__ == "__main__":
    asyncio.run(main())
