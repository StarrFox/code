import trio


async def server(server_stream, client_stream, rx):
    async for server_data in server_stream:
        print(f"s -> c: {server_data.hex(' ').upper()}")
        await client_stream.send_all(server_data)


async def client(client_stream, server_stream, tx):
    async for client_data in client_stream:
        print(f"c -> s: {client_data.hex(' ').upper()}")
        await server_stream.send_all(client_data)


async def proxy(stream):
    queue_send, queue_recieve = trio.open_memory_channel(1)

    ki = await trio.open_tcp_stream("login.us.wizard101.com", 12000)
    async with trio.open_nursery() as nursery:
        nursery.start_soon(client, stream, ki, queue_send)
        nursery.start_soon(server, ki, stream, queue_recieve)


if __name__ == "__main__":
    trio.run(trio.serve_tcp, proxy, 12000)
