from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from websockets.exceptions import ConnectionClosedError
import asyncio

# 소켓을 관리하기 위해 소켓 사용자를 하나의 객체로 두고 체크할것

class ConnectionManager:
    def __init__(self):
        self.__active_connection: list[LeagueObserver] = []
        print(f'INFO<-[      NOVA Connection Manager NOW READY.')

    async def connect(self, lname, websocket: WebSocket, league_manager):
        leagueObserver = LeagueObserver(lname=lname)
        await leagueObserver.connect(websocket=websocket)
        leagueObserver.set_send_data(send_data=league_manager.get_ws_league_data(league_name=lname))
        self.__active_connection.append(leagueObserver)
        return leagueObserver

    # 연결 해제
    def disconnect(self, observer):
        self.__active_connection.remove(observer)
        return

    # 목표물에게 전송
    def targeting_broadcast(self, target:str, message:str):
        # 타깃을 정하고 보낼 데이터 세팅해주기
        for single_obaserver in self.__active_connection:
            if single_obaserver.get_lname() == target:
                single_obaserver.set_send_data(send_data=message)
        return

    # 목표물에게 전송
    async def all_broadcast(self, message:str):
        # 타깃에게 전송
        for connection in self.__active_connection:
            await connection.send_data(message)
        return

# 리그 관찰자
class LeagueObserver:
    def __init__(self, lname):
        self.__lname = lname
        self.__websocket = None
        self.__send_flag = False
        self.__send_data = ""
        return

    async def connect(self, websocket: WebSocket):
        self.__websocket = websocket
        await self.__websocket.accept()
        return

    # 데이터 전송하기
    async def send_data(self, data:str):
        await self.__websocket.send_text(data)
        return
    
    # 실은 받을 데이터가 없지만 ack 받아봄
    async def recive_data(self):
        data = None
        data = await self.__websocket.receive_text()
        if data:
            self.__send_data = ""
            self.__send_flag = False
            return True
        else:
            self.__send_flag = False
            return False

    def set_send_data(self, send_data):
        self.__send_data = send_data
        self.__send_flag = True
        return
    
    def get_lname(self):
        return self.__lname

    def get_websocket(self):
        return self.__websocket
    
    async def send_operation(self):
        try:
            while True:
                await asyncio.sleep(0.2)
                if self.__send_flag:
                    await self.send_data("ping")
                    await self.send_data(self.__send_data)
                    # 데이터가 안받아지면 죽이삼 (ack)
                    if not await self.recive_data():
                        break
                #else:
                    #await self.send_data("d")
                #print("??")

        except ConnectionClosedError:
            return False
            
        except WebSocketDisconnect:
            return False

        finally:
            return False