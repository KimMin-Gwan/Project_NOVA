from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from websockets.exceptions import ConnectionClosedError
import asyncio
from queue import Queue
from others.data_domain import User
from typing import Callable, List
from datetime import datetime

# 소켓을 관리하기 위해 소켓 사용자를 하나의 객체로 두고 체크할것

# 단톡방 같은 개념임
# 사람이 없으면 사라지게 되어있음
class FeedObserveUnit:
    def __init__(self, fid):
        self.__fid = fid
        self.__observers:List[FeedObserver] = []
        
    def set_fid(self, fid):
        self.__fid = fid
        return
    
    def get_fid(self):
        return self.__fid
    
    def get_observers(self):
        return self.__observers
    
    def add_new_observer(self, user:User):
        for observer in self.__observers:
            if observer.get_observer_uid() == user.uid:
                return None
        
        new_observer = FeedObserver(fid=self.__fid, user=user)
        self.__observers.append(new_observer)
        return new_observer
    
    # 옵져버 지우기
    async def remove_observer(self, observer):
        for observer in self.__observers:
            if observer == observer:
                self.__observers.remove(observer)
                break
        return

    
    # 옵져버들 싱크 맞춰야됨
    async def __sync_observers(self):
        # 그룹에 있는 옵져버 다 대리고와야됨
        target_observsers:List[FeedObserver] = self.__unit.get_observers()
        
        # 만약 그룹에 있는 옵져버 수가 줄었으면 사라진 옵져버를 여기서도 지워줘야됨
        if len(target_observsers) < (self.__observers + 1):
            for observser in self.__observers:
                # 지우기
                if observser not in target_observsers:
                    self.__observers.remove(observser)
                    
        # 만약 그룹에 있는 옵져버 수가 늘었으면 추가된 옵져버를 여기서도 추가해야됨
        elif len(target_observsers) > (self.__observers + 1):
            for observser in target_observsers:
                # 본인은 제외
                if observser.get_observer_uid() == self.__user.uid:
                    continue
                
                # 추가하기
                if observser not in self.__observers:
                    self.__observers.append(observser)
        return
    
    # 메세지 받기 (리시빙~)
    async def recive_data(self):
        data = None
        data = await self.__websocekt.receive_text()
        
        dataform = ChattingDataform(uid=self.__user.uid,
                                    uname=self.__user.uname,
                                    fid=self.__unit.get_fid(),
                                    body=data)
        # data 분석하는 로직이 여기 들어감
        
        for observer in self.__observers:
            await observer.set_send_data(dataform)
        return
        
    def get_websocket(self):
        return self.__websocket

# 단톡에서 채팅을 치는 소켓 입장임
class FeedObserver:
    def __init__(self, user):
        self.__user:User = user
        self.__unit = None
        self.__observers:List[FeedObserver] = []
        self.__websocekt:WebSocket = None
        self.__send_data = Queue()
    
    def get_observer_uid(self):
        return self.__user.uid
    
    def get_unit(self):
        return self.__unit
        
    async def connect(self, websocket:WebSocket, unit:FeedObserveUnit):
        self.__websocket = websocket
        self.__unit = unit
        
        for observer in unit.get_observers():
            if observer.get_observer_uid() == self.__user.uid:
                continue
            else:
                self.__observers.append(observer)
        
        await self.__websocekt.accept()
        return
    
    # 전송할 데이터 que에 넣기
    async def set_send_data(self, send_data):
        self.__send_data.put(send_data)
        return
    
    # 데이터 전송하기
    async def send_data(self, data:str):
        await self.__websocket.send_text(data)
        return
    
    async def observer_operation(self):
        try:
            while True:
                await asyncio.sleep(0.2)  # 일시 정지
                await self.send_data("ping")
                if not self.__send_data.empty():
                    send_data:ChattingDataform = self.__send_data.get()
                    await self.send_data(send_data.get_send_form())
                
                # 데이터가 안받아지면 죽이삼 (ack)
                
                #*********  뭔가 이상하면 이거 들여쓰기 해보라 *********
                
                if not await self.recive_data():
                    break
                
                #****************************************************
                
                # 목표 옵져버들을 다시 체크해야됨(사라진 옵져버를 지우기 위해)
                await self.__sync_observers()

        except ConnectionClosedError:
            return False
            
        except WebSocketDisconnect:
            return False

        finally:
            return False



class ConnectionManager:
    def __init__(self):
        #self.__active_connection: list[LeagueObserver] = []
        self.__active_connection: list[FeedObserver] = []
        self.__active_observe_unit : list[FeedObserveUnit] = []
        print(f'INFO<-[      NOVA Connection Manager NOW READY.')
        
    # 커넥션 세팅
    async def connect(self, fid, request, websocket: WebSocket, database, core_controller) -> FeedObserver:
        target_unit = FeedObserveUnit(fid="")
        
        
        
        # 여기 컨트롤러 만들면 끝남
        
        
        
        
        # 유저 정보 받아오기
        user:User = core_controller.get_user_data(database=database,
                                                request=request.data_payload)
        
        for unit in self.__active_observe_unit:
            if unit.get_fid() == fid:
                target_unit = unit
                break
            
        # 못찾았으면 만들어야됨
        if target_unit.get_fid() == "":
            target_unit.set_fid(fid=fid)
            new_observer = target_unit.add_new_observer(user=user)
            # 만들고나면 리스트에 넣어서 관리
            self.__active_observe_unit.append(target_unit)
                
        # 찾았으면 거기다가 넣어야됨
        else:
            new_observer = target_unit.add_new_observer(user=user)
        
        # 연결 시도!
        await new_observer.connect(websocket=websocket, unit=target_unit)
        
        # 리스트에 넣어서 관리
        self.__active_connection.append(new_observer)
        
        # 초기 채팅 데이터 가지고 와야됨
        init_chattings = core_controller.get_init_comment_data(fid=fid)
        
        # 초기 데이터가 있으면 보내야되고
        if init_chattings:
            for chatting in init_chattings:
                new_observer.set_send_data(ChattingDataform(uid=chatting.uid, uname=chatting.uname, fid=fid, body=chatting.body))
        # 없으면 조용하다고 보내삼
        else:
            new_observer.set_send_data(ChattingDataform(uid="-1", uname="채팅봇", fid=fid, body="어라... 조용하네요..."))
        return new_observer

    # 연결 해제
    def disconnect(self, observer):
        observer:FeedObserver = observer
        observe_unit:FeedObserveUnit = observer.get_unit()
        
        for unit in self.__active_observe_unit:
            if unit == observe_unit:
                observe_unit.remove_observer(observer)
        
        self.__active_connection.remove(observer)
        return

    ## 목표물에게 전송
    #def targeting_broadcast(self, target:str, message:str):
        ## 타깃을 정하고 보낼 데이터 세팅해주기
        #for single_obaserver in self.__active_connection:
            #if single_obaserver.get_lname() == target:
                #single_obaserver.set_send_data(send_data=message)
        #return

    # 모든 목표물에게 전송
    async def all_broadcast(self, message:str):
        # 타깃에게 전송
        for connection in self.__active_connection:
            await connection.send_data(message)
        return
    

        
# 채팅 == 댓글 라서 저장 하거나 전송 가능한 형태로 만들기 위한 세팅!
class ChattingDataform:
    def __init__(self, uid, uname, fid, body):
        self.uid = uid
        self.uname = uname
        self.fid = fid
        self.body = body
        self.date = "datetimesample"
    
    # 유아이디<br>유저이름<br>피드번호<br>본문<br>날짜
    def get_send_form(self):
        return f"{self.uid}<br>{self.uname}<br>{self.fid}<br>{self.body}<br>{self.date}"
        
        

## 리그 관찰자
#class LeagueObserver:
    #def __init__(self, lname):
        #self.__lname = lname
        #self.__websocket = None
        #self.__send_flag = False
        #self.__send_data = ""
        #return

    #async def connect(self, websocket: WebSocket):
        #self.__websocket = websocket
        #await self.__websocket.accept()
        #return

    ## 데이터 전송하기
    #async def send_data(self, data:str):
        #await self.__websocket.send_text(data)
        #return
    
    ## 실은 받을 데이터가 없지만 ack 받아봄
    #async def recive_data(self):
        #data = None
        #data = await self.__websocket.receive_text()
        #if data:
            #self.__send_data = ""
            #self.__send_flag = False
            #return True
        #else:
            #self.__send_flag = False
            #return False

    #def set_send_data(self, send_data):
        #self.__send_data = send_data
        #self.__send_flag = True
        #return
    
    #def get_lname(self):
        #return self.__lname
    
    #async def send_operation(self):
        #try:
            #while True:
                #await asyncio.sleep(0.2)
                #if self.__send_flag:
                    #await self.send_data("ping")
                    #await self.send_data(self.__send_data)
                    ## 데이터가 안받아지면 죽이삼 (ack)
                    #if not await self.recive_data():
                        #break
                ##else:
                    ##await self.send_data("d")
                ##print("??")

        #except ConnectionClosedError:
            #return False
            
        #except WebSocketDisconnect:
            #return False

        #finally:
            #return False