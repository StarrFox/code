import asyncio

from wizwalker import WizWalker
from wizwalker.combat import CombatHandler


class LostSoulDestroyer(CombatHandler):
    async def handle_round(self):
        cards = await self.get_cards()
        members = await self.get_members()

        print(f"{len(cards)=} {len(members)=}")

        thunder_snake = None
        for card in cards:
            name = await card.name()
            print(f"Card name = {name}")

            if "thunder snake" in name.lower():
                thunder_snake = card
                break

        if thunder_snake is None:
            raise Exception("Didn't have a thunder snake")

        lost_soul = None
        for member in members:
            if await member.is_monster():
                lost_soul = member
                break

        if lost_soul is None:
            raise Exception("Couldn't find lost soul")

        await card.cast(member)


async def destory_lost_soul(client):
    await client.activate_hooks()
    await client.mouse_handler.activate_mouseless()

    handler = LostSoulDestroyer(client)

    print("Hooked and waiting for battle")
    while not await client.in_battle():
        await asyncio.sleep(0.5)

    await handler.handle_combat()


async def main():
    walker = WizWalker()
    client = walker.get_new_clients()[0]
    try:
        await destory_lost_soul(client)
    except:
        import traceback
        traceback.print_exc()

    await client.close()


if __name__ == "__main__":
    asyncio.run(main())
