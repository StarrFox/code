import asyncio

from wizwalker import Keycode, WizWalker
from wizwalker.combat import CombatHandler


BLADE_NAME = "fireblade"
AOE_NAME = "meteor strike"


class BladeHandler(CombatHandler):
    async def handle_round(self):
        player = await self.get_client_member()
        try:
            blade = await self.get_card_named(BLADE_NAME)
            await blade.cast(player)

        # there wasnt a fireblade
        except ValueError:
            aoe = await self.get_card_named(AOE_NAME)
            await aoe.cast(None)


async def main(walker):
    client = walker.get_new_clients()[0]

    try:
        await client.hook_handler.activate_all_hooks()
        await client.hook_handler.activate_mouseless_cursor_hook()
        print("Ready for battle")

        await BladeHandler(client).wait_for_combat()
    finally:
        await walker.close()


if __name__ == "__main__":
    asyncio.run(main(WizWalker()))
