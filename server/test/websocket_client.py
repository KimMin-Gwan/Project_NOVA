import asyncio
import websockets
from threading import Thread

async def connect_to_websocket():
    uri = "ws://127.0.0.1:5000/chatting"  # 서버 주소
    async with websockets.connect(uri) as websocket:
        try:
            #send_task = asyncio.create_task(send_func(websocket))
            recv_task = asyncio.create_task(recv_func(websocket))

            # 두 태스크를 병렬로 실행
            #await asyncio.gather(send_task, recv_task)
            await asyncio.gather(recv_task)

        except websockets.exceptions.ConnectionClosedError:
            print("Connection closed")

async def send_func(websocket):
    try:
        print("recving")
        while True:
            # 서버로 메시지 전송
            message = input("Enter message to send: ")
            await websocket.send(message)
    except websockets.exceptions.ConnectionClosedError:
        print("Connection closed")

async def recv_func(websocket):
    try:
        while True:
            # 서버로부터 응답 수신
            response = await websocket.recv()
            print(f"Received from server: {response}")
    except websockets.exceptions.ConnectionClosedError:
        print("Connection closed")



if __name__ == "__main__":
    asyncio.run(connect_to_websocket())
