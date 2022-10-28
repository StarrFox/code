import re
import ctypes
import time

import pymem
import pymem.pattern
import wizwalker


kernel32 = ctypes.windll.kernel32


class MEMORY_BASIC_INFORMATION(ctypes.Structure):
    _fields_ = [
        ("BaseAddress", ctypes.c_void_p),
        ("AllocationBase", ctypes.c_void_p),
        ("AllocationProtect", ctypes.wintypes.DWORD),
        ("PartitionId", ctypes.wintypes.WORD),
        ("RegionSize", ctypes.c_size_t),
        ("State", ctypes.wintypes.DWORD),
        ("Protect", ctypes.wintypes.DWORD),
        ("Type", ctypes.wintypes.DWORD)
    ]


# Modified to not handle memory protections and use re for matching
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
def scan_pattern_page(handle: int, address: int, pattern: re.Pattern):
    # mbi = pymem.memory.virtual_query(handle, address)
    mbi = MEMORY_BASIC_INFORMATION()

    kernel32.VirtualQueryEx(
        handle,
        address,
        ctypes.byref(mbi),
        ctypes.sizeof(mbi)
    )


    next_region = mbi.BaseAddress + mbi.RegionSize
    page_bytes = pymem.memory.read_bytes(handle, address, mbi.RegionSize)

    #print(f"scan_pattern_page: {address=} {next_region=} {len(page_bytes)=} {mbi.BaseAddress=} {mbi.RegionSize=}")

    found = None

    match = pattern.search(page_bytes)

    if match:
        found = address + match.span()[0]

    return next_region, found


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
def pattern_scan_module(handle: int, module, pattern: re.Pattern):
    base_address = module.lpBaseOfDll
    max_address = module.lpBaseOfDll + module.SizeOfImage
    page_address = base_address

    found = None
    while page_address < max_address:
        next_page, found = scan_pattern_page(handle, page_address, pattern)

        if found:
            break

        page_address = next_page

    return found


TARGET_BYTES = re.compile(b"\x89\x48\x40\x74\x69")


def time_callback(callback, *args, **kwargs) -> int:
    if not callable(callable):
        raise ValueError("what are you doing")

    start = time.perf_counter_ns()

    callback_res = callback(*args, **kwargs)

    end = time.perf_counter_ns()

    res = end - start

    print(f"{callback.__qualname__} took {res / 1_000_000_000:f} seconds")

    return callback_res


def main():
    proc = pymem.Pymem("WizardGraphicalClient.exe")

    print(f"{proc.process_handle=}")

    module = pymem.process.module_from_name(
        proc.process_handle, "WizardGraphicalClient.exe"
    )

    addr = time_callback(
        pattern_scan_module, 
        proc.process_handle,
        module,
        TARGET_BYTES
    )

    print(f"{addr=}")

if __name__ == "__main__":
    main()
