import asyncio
import websockets
from websockets.exceptions import ConnectionClosedOK

all_clients = []


async def send_message(message: str):
    disconnected_clients = []
    for client in all_clients:
        try:
            await client.send(message)
        except ConnectionClosedOK:
            disconnected_clients.append(client)
    for client in disconnected_clients:
        all_clients.remove(client)


async def new_client_connected(client_socket: websockets.WebSocketClientProtocol, path: str):
    print('New client connected!')
    all_clients.append(client_socket)
    try:
        while True:
            new_message = await client_socket.recv()
            print('New message from a client: ', new_message)
            await send_message(message=new_message)
    except ConnectionClosedOK:
        print('Client disconnected')
    finally:
        all_clients.remove(client_socket)


async def start_server():
    async with websockets.serve(new_client_connected, "localhost", 12345):
        await asyncio.Future()  # run forever

if __name__ == '__main__':
    asyncio.run(start_server())
