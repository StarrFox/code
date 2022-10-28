import wizwalker


ww = wizwalker.WizWalker()
ww.get_clients()

client = ww.clients[0]

async def main():
    await client.activate_hooks("player_struct")
    await client.teleport(x=0.0, y=0.0)


import asyncio
asyncio.run(main())
