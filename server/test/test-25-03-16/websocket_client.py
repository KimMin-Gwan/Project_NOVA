import asyncio
import websockets
from threading import Thread
import json

async def connect_to_websocket():
    uri = "ws://127.0.0.1:6000/chatting"  # 서버 주소
    async with websockets.connect(uri) as websocket:
        try:
            while True:
                # 서버로 메시지 전송
                message = input("Enter message to send: ")
                token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InRlc3RVc2VyQG5hdmVyLmNvbSIsImlhdCI6MTcyMzg3OTQ5MSwiZXhwIjoxNzIzODgxMjkxfQ.6TfocB9uJxB4JNOghUGbSabNVfR1aUkCABroOOiw1p0"
                content ={
                    'token' : token,
                    'message' : message
                }
                
                await websocket.send(json.dumps(content))

                # 서버로부터 응답 수신
                response = await websocket.recv()
                print(f"Received from server: {response}")

        except websockets.exceptions.ConnectionClosedError:
            print("Connection closed")

if __name__ == "__main__":
    asyncio.run(connect_to_websocket())
