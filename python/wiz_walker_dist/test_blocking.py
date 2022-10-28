import asyncio
import multiprocessing



def block_forever():
    while True:
        print("a")


async def main():
    loop = asyncio.get_event_loop()
    proc = multiprocessing.Process(None, block_forever, daemon=True)
    proc.start()

    import time

    time.sleep(5)

    proc.kill()
    print("after")



asyncio.run(main())
