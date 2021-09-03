import asyncio
import socket
import random


async def handle_client(client):
    loop = asyncio.get_event_loop()
    request = None

    while request != 'quit':
        request = (await loop.sock_recv(client, 255)).decode('utf8').strip()
        response = '0'
        print(request)
        if request == 'DCV?':
            response = f'{random.randint(0, 30)}'
        elif request == 'ACV?':
            response = f'{10000 + random.randint(0, 300)}'
        elif request == 'CF?':
            response = f'1.{random.randint(39, 42)}'
        elif request == 'PKPK?':
            response = f'{random.randint(0, 60)}'
        elif request == 'FREQ?':
            response = '50'

        print(response)
        await loop.sock_sendall(client, response.encode('utf8'))
    client.close()


async def run_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('127.0.0.1', 10733))
    server.listen(8)
    server.setblocking(False)

    loop = asyncio.get_event_loop()

    while True:
        try:
            client, _ = await loop.sock_accept(server)
            loop.create_task(handle_client(client))
        except KeyboardInterrupt:
            client.close()


asyncio.run(run_server())