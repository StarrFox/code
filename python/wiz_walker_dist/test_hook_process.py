import asyncio
import traceback

from wizwalker import WizWalker


async def crasher(walker):
    client = walker.get_new_clients()[0]

    await client.activate_hooks()

    spell_checkboxes = await client.root_window.get_windows_with_type("SpellCheckBox")
    print(f"{len(spell_checkboxes)}")

    for checkbox in spell_checkboxes:
        print(f"{await checkbox.name()}: {await checkbox.flags()}")


async def handle_exceptions():
    walker = WizWalker()
    try:
        await crasher(walker)
    except (Exception, KeyboardInterrupt):
        traceback.print_exc()

    print("closing")
    await walker.close()


asyncio.run(handle_exceptions())
