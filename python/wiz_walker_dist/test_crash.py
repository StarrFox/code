import asyncio
import traceback

from wizwalker import WizWalker


async def crasher(walker):
    client = walker.get_new_clients()[0]

    index = 0
    while True:
        print(index)
        index += 1
        await client.hook_handler.activate_player_hook()
        await asyncio.sleep(1)
        await client.close()
        await asyncio.sleep(5)


async def handle_exceptions():
    walker = WizWalker()
    try:
        await crasher(walker)
    except (Exception, KeyboardInterrupt):
        traceback.print_exc()

    print("closing")
    await walker.close()


asyncio.run(handle_exceptions())
