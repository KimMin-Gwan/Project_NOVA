from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from websockets.exceptions import ConnectionClosedError
import asyncio
from queue import Queue
from others.data_domain import User

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
    
    
class FeedObserveUnit:
    def __init__(self, fid):
        self.__fid = fid
        self.__observers = []
        self.__send_data_que = Queue()
        self.__count = 0
        self.__kill_flag = False
        
        
    async def __unit_self_process(self):
        while True:
            if self.__count > 10:
                self.__kill_flag = True
            
            if not self.__send_data_que.empty():
                send_data = self.__send_data_que.get()
                for observer in self.__observers:
                    observer.set_send_data(send_data)
                # 보내고 나면 잠시 대기
                asyncio.sleep(0.5)
            
            if len(self.__observers) == 0:
                self.__count += 1
            else:
                self.__count = 0

    def is_this_feed_killed(self):
        return self.__kill_flag
    
    def add_new_observer(self, user:User):
        if self.__kill_flag:
            return False
        
        for observer in self.__observers:
            if observer.get_observers_uid() == user.uid:
                return False
        
        new_observer = FeedObserver(fid=self.__fid, user=user)
        self.__observers.append(new_observer)
        return True
    
    async def remove_observer(self):
        if self.__kill_flag:
            for observer in self.__observers:
                self.__observers.remove(observer)
        
        for observer in self.__observers:
            if observer.is_observer_disconnected():
                self.__observers.remove(observer)
        return
        
    
    
class FeedObserver:
    def __init__(self, fid, user):
        self.__user = user
        self.__fid = fid
        self.__websocekt:WebSocket = None
        self.__send_flag = False
        self.__send_data = ""
        
    async def connect(self, websocket:WebSocket):
        self.__websocket = websocket
        await self.__websocekt.accept()
        return
    
    async def send_data(self, data:str):
        await self.__websocekt.send_text(data)
        return
    
    async def recive_data(self):
        data = None
        data = await self.__websocekt.receive_text()
        
        # data 분석하는 로직이 여기 들어감
        
        
        
    

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