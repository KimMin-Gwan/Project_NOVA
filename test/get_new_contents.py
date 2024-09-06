from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 원격 호스트의 웹소켓 연결을 허용할 도메인 설정
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/new_contents')
def new_contentes():
    data = ["1", "2", "3", "4"]

    return data

uvicorn.run(app=app, host="127.0.0.1", port=4000)

