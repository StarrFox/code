import asyncio

import pymem.pattern
from wizwalker import WizWalker


# Modified from pymem, I don't have copyright over this
# MIT License
# Copyright (c) 2018 pymem
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
def scan_pattern_page(handle, address, pattern, mask):
    mbi = pymem.memory.virtual_query(handle, address)
    next_region = mbi.BaseAddress + mbi.RegionSize
    page_bytes = pymem.memory.read_bytes(handle, address, mbi.RegionSize)

    found = None
    for offset in range(0, (mbi.RegionSize - len(pattern)), 1):
        partial = page_bytes[offset:offset + len(pattern)]
        for x in range(len(pattern)):
            if mask[x] == '?':
                continue
            if mask[x] == 'x' and not partial[x] == pattern[x]:
                break
        else:
            found = address + offset
            del page_bytes
            return None, found
    return next_region, found


# monkey patch
pymem.pattern.scan_pattern_page = scan_pattern_page


async def main():
    ww = WizWalker()
    ww.get_clients()

    client = ww.clients[0]
    print(f"{client=}")

    await client.activate_hooks("player_struct")
    await asyncio.sleep(2)
    print(f"{await client.xyz()=}")

    await ww.close()


if __name__ == "__main__":
    asyncio.run(main())
