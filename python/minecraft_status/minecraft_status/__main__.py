import asyncio


SERVER_URL = ""
SERVER_PORT = 1234

SEGMENT_BITS = 0x7F
CONTINUE_BIT = 0x80


# works well enough
def _decode_varint(data: bytes):
    value = 0
    position = 0
    byte_pos = 0
    while True:
        current = data[byte_pos]
        byte_pos += 1
        value |= (current & SEGMENT_BITS) << position

        if (current & CONTINUE_BIT) == 0:
            break

        position += 7

        if position >= 32:
            raise RuntimeError("VarInt too big")
    
    return value


def _encode_varint(varint: int) -> bytes:
    buffer = bytes()
    while True:
        if (varint & ~SEGMENT_BITS) == 0:
            buffer
            return buffer


class VarInt(int):
    @classmethod
    def from_data(cls, data: bytes):
        pass

    def to_data(self) -> bytes:
        pass


async def main():
    # read, write = await asyncio.open_connection(SERVER_URL, SERVER_PORT)
    test = b"\xff\xff\xff\xff\x07"
    print(_decode_varint(test))


if __name__ == "__main__":
    asyncio.run(main())
