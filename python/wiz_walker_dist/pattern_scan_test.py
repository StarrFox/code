import asyncio

from pymem import Pymem

import wizwalker
from wizwalker.memory.memory_reader import MemoryReader


target = (
    rb"\xE9"
)


async def main():
    reader = MemoryReader(Pymem("notepad.exe"))

    try:
        old_res = await reader.pattern_scan(target, return_multiple=True, module="notepad.exe")
    except wizwalker.PatternFailed:
        print("Old pattern failed")
    else:
        print(f"{old_res=}")


if __name__ == "__main__":
    asyncio.run(main())
