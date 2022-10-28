import os
import ctypes
import struct
import mmap
from pathlib import Path


"""
needed:
    allocate memory in process
    free memory in process
    scan memory in process

done:
    write memory in process
    read memory in process
    get process from id
    get process from name
"""


def get_address_of_ctypes_obj(obj, pointer_format):
    return struct.unpack(pointer_format, bytes(ctypes.pointer(obj)))[0]


def get_pid_from_name(name: str) -> int:
    for thing in Path("/proc").glob("*"):
        # I don't know if there is a better way to do this
        if thing.name.isnumeric():
            cmdline = (thing / "cmdline").read_bytes()
            # remove trailing 0 byte
            cmdline = cmdline.strip(b"\x00").split(b"\x00")
            if cmdline[0].endswith(name.encode()):
                return int(thing.name)


def get_self_pid() -> int:
    return os.getpid()


def read_memory(process_id, address, size):
    with open(f"/proc/{process_id}/mem", "rb") as fp:
        fp.seek(address)
        return fp.read(size)


def write_memory(process_id, address, value):
    with open(f"/proc/{process_id}/mem", "wb") as fp:
        fp.seek(address)
        fp.write(value)

# note: doesn't work
def read_memory_with_mmap(process_id, address, size):
    with open(f"/proc/{process_id}/mem", "rb") as fp:
        with mmap.mmap(fp.fileno(), 0, access=mmap.ACCESS_READ) as memmap:
            return memmap[address:address + size]


def main():
    pid = get_self_pid()

    test_value = ctypes.c_int32(23)
    test_value_address = get_address_of_ctypes_obj(test_value, "<Q")

    assert read_memory(pid, test_value_address, 4) == b"\x17\x00\x00\x00"

    write_memory(pid, test_value_address, b"\x18\x00\x00\x00")
    assert test_value.value == 24


if __name__ == "__main__":
    main()
