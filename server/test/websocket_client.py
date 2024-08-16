import asyncio
import websockets
from threading import Thread

async def connect_to_websocket():
    uri = "ws://127.0.0.1:5000/chatting"  # 서버 주소
    async with websockets.connect(uri) as websocket:
        try:
            while True:
                # 서버로 메시지 전송
                message = input("Enter message to send: ")
                await websocket.send(message)

                # 서버로부터 응답 수신
                response = await websocket.recv()
                print(f"Received from server: {response}")

        except websockets.exceptions.ConnectionClosedError:
            print("Connection closed")

if __name__ == "__main__":
    asyncio.run(connect_to_websocket())
