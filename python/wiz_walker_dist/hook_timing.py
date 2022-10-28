import time
import asyncio
import re

import pymem
import wizwalker
from wizwalker.windows.memory import hooks


global total_scanned
total_scanned = 0

global byte_re
byte_re = re.compile(b"\x8B\x48\x2C\x8B\x50\x30\x8B\x40\x34\xEB\x2A")


# Modified to not handle memory protections
# This licence covers the below function
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

    global byte_re
    match = byte_re.search(page_bytes)

    if match:
        found = address + match.span()[0]

    return next_region, found


pymem.pattern.scan_pattern_page = scan_pattern_page


# This licence covers the below function
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
def pattern_scan_module(handle, module, pattern, mask):
    base_address = module.lpBaseOfDll
    max_address = module.lpBaseOfDll + module.SizeOfImage
    page_address = base_address

    found = None
    while page_address < max_address:
        next_page, found = scan_pattern_page(handle, page_address, pattern, mask)
        if found:
            break
        page_address = next_page
    # xxx raise not found
    return found


pymem.pattern.pattern_scan_module = pattern_scan_module


async def time_callback(callback, *args, **kwargs) -> int:
    is_async = kwargs.pop("is_async", False)
    if not callable(callable):
        raise ValueError("what are you doing")

    start = time.perf_counter_ns()

    if is_async:
        await callback(*args, **kwargs)
    else:
        callback(*args, **kwargs)

    end = time.perf_counter_ns()

    res = end - start

    print(f"{callback.__qualname__} took {res / 1_000_000_000:f} seconds")


async def time_hook():
    ww = wizwalker.WizWalker()
    ww.get_clients()

    try:
        client = ww.clients[0]
    except:
        print("No clients running 5 head")
        return

    memory = client._memory

    player_hook = hooks.PlayerHook(memory)

    await time_callback(player_hook.hook)

    memory.player_struct_addr = player_hook.player_struct
    memory.active_hooks["player_struct"] = True

    await asyncio.sleep(2)
    print(f"{await client.xyz()=}")

    player_hook.unhook()


async def time_search():
    proc = pymem.Pymem("WizardGraphicalClient.exe")

    module = pymem.process.module_from_name(
        proc.process_handle, "WizardGraphicalClient.exe"
    )

    byte_sig = b"\x8B\x48\x2C\x8B\x50\x30\x8B\x40\x34\xEB\x2A"
    mask = "x" * len(byte_sig)

    await time_callback(
        pymem.pattern.pattern_scan_module,
        proc.process_handle,
        module,
        byte_sig,
        mask
        )

    print(f"{total_scanned=}")


async def main():
    await time_hook()


if __name__ == "__main__":
    asyncio.run(main())
