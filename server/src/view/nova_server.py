from fastapi import FastAPI
from view.core_system_view import Core_Service_View
from view.parsers import Head_Parser
import uvicorn
from fastapi.middleware.cors import CORSMiddleware


class NOVA_Server:
    def __init__(self, database) -> None:
        self.__app = FastAPI()

        self.__app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],  # 원격 호스트의 웹소켓 연결을 허용할 도메인 설정
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

        head_parser = Head_Parser()
        self.__core_system_view = Core_Service_View(app=self.__app,
                                                   endpoint='/core_system',
                                                   database=database,
                                                   head_parser=head_parser)
        self.__core_system_view()

    def run_server(self, host='127.0.0.1', port=6000):
        uvicorn.run(app=self.__app, host=host, port=port)



