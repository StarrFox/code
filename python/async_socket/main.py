# from socket import create_connection

# with create_connection(("patch.us.wizard101.com", 12500)) as socket:
#     socket.send(b"\x0D\xF0\x24\x00\x00\x00\x00\x00\x08\x01\x20" + bytes(29))
#     socket.recv(4096)  # session offer or whatever
#     data = socket.recv(4096)

import asyncio

async def tcp_echo_client():
    reader, writer = await asyncio.open_connection("patch.us.wizard101.com", 12500)

    writer.write(b"\x0D\xF0\x24\x00\x00\x00\x00\x00\x08\x01\x20" + bytes(29))
    await reader.read(4096)

    data = await reader.read(4096)
    print(f'Received: {data}')

    print('Close the connection')
    writer.close()


asyncio.run(tcp_echo_client())



