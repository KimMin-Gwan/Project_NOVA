from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import uvicorn
import json

class TestServer:
    def __init__(self):
        self.__app = FastAPI()
        self.manager = ConnectionManager()
        self.route()

    def route(self):
        @self.__app.get("/home")
        def home():
            return "hello world"

        @self.__app.websocket('/chatting')
        async def chatting_socket(websocket:WebSocket):
            await self.manager.connect(websocket)
            try:
                while True:
                    data = await websocket.receive_text()
                    converted_data = json.loads(data)
                    print(type(converted_data))
                    await self.manager.broadcast(f"client text :{data}")
                
            except WebSocketDisconnect:
                self.manager.disconnect(websocket)
                await self.manager.broadcast("client disconnected")
    
    def run_server(self):
        uvicorn.run(app=self.__app, host="127.0.0.1", port=5000)

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