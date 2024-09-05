from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from websockets.exceptions import ConnectionClosedError
from typing import Any, Optional
import uvicorn
import json
import jwt
import time

class TestServer:
    def __init__(self):
        self.__app = FastAPI()
        self.manager = ConnectionManager()
        self.route()

    def route(self):
        @self.__app.get("/get-test")
        def get_test():
            return "hello world"

        @self.__app.post("/post-test")
        def post_test(data:dict):
            return data

        @self.__app.websocket('/chatting')
        async def chatting_socket(websocket:WebSocket, bias_name:Optional[str] = ""):
            await self.manager.connect(websocket)
            print(bias_name)
            secret_key = "your_secret_key"
            try:
                while True:
                    data = await websocket.receive_text()
                    print(data)
                    ##converted_data = json.loads(data)
                    ##decoded_payload = jwt.decode(converted_data['token'], secret_key, algorithms=["HS256"]) 
                    ##await self.manager.broadcast(f"client text :{data['message']}")
                    time.sleep(3)
                    await self.manager.broadcast(f"Hello World")

            except ConnectionClosedError:
                self.manager.disconnect(websocket)
                await self.manager.broadcast("client disconnected")
                
            except WebSocketDisconnect:
                self.manager.disconnect(websocket)
                await self.manager.broadcast("client disconnected")
    
    def run_server(self):
        uvicorn.run(app=self.__app, host="127.0.0.1", port=4000)

class ConnectionManager:
    def __init__(self):
        self.active_connection: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connection.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connection.remove(websocket)

    async def broadcast(self, message:str):
        for connection in self.active_connection:
            await connection.send_text(message)

if __name__ == "__main__":
    server = TestServer()
    server.run_server()