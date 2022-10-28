import asyncio

async def one(time=0):
    await asyncio.sleep(time)
    print(1)

async def two(time=0):
    await asyncio.sleep(time)
    print(2)

async def main():
    x = asyncio.create_task(one(8))
    y = asyncio.create_task(two(9))

    while not x.done() or not y.done():
        await asyncio.sleep(0)

asyncio.run(main())