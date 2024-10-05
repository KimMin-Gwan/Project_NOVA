from fastapi import FastAPI, WebSocket
import asyncio
import uvicorn 
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.websocket("/")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()  # 클라이언트 연결 수락
    while True:
        await asyncio.sleep(2)  # 2초 대기
        await websocket.send_text("hello")  # 클라이언트에게 "hello" 전송

uvicorn.run(app=app, port=4000)