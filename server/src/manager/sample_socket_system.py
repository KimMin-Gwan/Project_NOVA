from fastapi import  WebSocket, WebSocketDisconnect
#from model import CommentModel
from websockets.exceptions import ConnectionClosedError
import asyncio
from queue import Queue
from others.data_domain import User
from typing import List
from datetime import datetime
import random
import string

# 소켓을 관리하기 위해 소켓 사용자를 하나의 객체로 두고 체크할것
YELLOW = "\033[33m"
RESET = "\033[0m"
# 단톡방 같은 개념임
# 사람이 없으면 사라지게 되어있음

# 단톡에서 채팅을 치는 소켓 입장임
class Observer:
    def __init__(self, user:User, active_observer):
        self.__user:User = user
        self.__observers:List[Observer] = []
        self.__websocket:WebSocket = None
        self.__send_data = Queue()
        self.__active_observsers:List[Observer] = active_observer
        
        if self.__user.uid.startswith("t_"):
            self.__is_logged_in = False
        else:
            self.__is_logged_in = True
            
    
    def get_observer_uid(self):
        return self.__user.uid
        
    async def connect(self, websocket:WebSocket, observers):
        self.__websocket = websocket
        
        for observer in observers:
            if observer.get_observer_uid() == self.__user.uid:
                continue
            else:
                self.__observers.append(observer)
        
        await self.__websocket.accept()
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
                await asyncio.sleep(0.2)
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
            #print(f'{YELLOW}INFO{RESET}<-[      NOVA Feed Observer | {self.__user.uid} disconnected')
            return False
        
    # 메세지 받기 (리시빙~)
    async def recive_data(self):
        
        raw_message= None
        raw_message= await self.__websocket.receive_text()
        
        print(raw_message)
        
        print("a")
        # data = body<br>type
        parts = raw_message.split('<br>')
        if len(parts) != 2:
            return True
        
        print("b")
        try:
            dataform = ChattingDataform(uid=self.__user.uid,
                                        uname=self.__user.uname,
                                        body=parts[0],
                                        type=parts[1],
                                        )
        except Exception as e:
            print(e)
            
        
        print("c")
        for observer in self.__observers:
            await observer.set_send_data(dataform)
        
        print("d")
        # 나한테 보내는 데이터는 별도로 구성되게 해야됨
        # 안그러면 is_owner가 동일하게 변경되는 문제가 있음(포인트)
        resend_myself_dataform= ChattingDataform(uid=self.__user.uid,
                                    uname=self.__user.uname,
                                    body=parts[0],
                                    type=parts[1],
                                    cid=dataform.cid
                                    )
        print("e")
        resend_myself_dataform.is_owner = True
        print("f")
        await self.set_send_data(resend_myself_dataform)
        print("g")
        
        return True
        
    def get_websocket(self):
        return self.__websocket

    # 옵져버들 싱크 맞춰야됨
    async def __sync_observers(self):
        # 그룹에 있는 옵져버 다 대리고와야됨
        target_observsers:List[Observer] = self.__active_observsers
        
        # 만약 그룹에 있는 옵져버 수가 줄었으면 사라진 옵져버를 여기서도 지워줘야됨
        if len(target_observsers) < (len(self.__observers) + 1):
            for observser in self.__observers:
                # 지우기
                if observser not in target_observsers:
                    self.__observers.remove(observser)
                    
        # 만약 그룹에 있는 옵져버 수가 늘었으면 추가된 옵져버를 여기서도 추가해야됨
        elif len(target_observsers) > (len(self.__observers) + 1):
            for observser in target_observsers:
                # 본인은 제외
                if observser.get_observer_uid() == self.__user.uid:
                    continue
                
                # 추가하기
                if observser not in self.__observers:
                    self.__observers.append(observser)
        return

class TestConnectionManager:
    def __init__(self):
        #self.__active_connection: list[LeagueObserver] = []
        self.__active_connection: list[Observer] = []
        print(f'{YELLOW}INFO{RESET}<-[      NOVA Connection Manager NOW READY.')
        
    def generate_random_string(self, length=8):
        # string.ascii_lowercase: 모든 소문자 알파벳
        return ''.join(random.choices(string.ascii_lowercase, k=length))
        
    # 커넥션 세팅
    async def connect(self, websocket: WebSocket) -> Observer:
        ## 유저 정보 받아오기
        #user:User = core_controller.get_user_data(database=database,
                                                #request=request.data_payload)
        user=User()
        
        #ㅂ 비회원일때
        if user.uid == "":
            while True:
                flag = True
                
                # 유저 아이디가 없으면 랜덤으로 만들어야
                new_uid = "t_" + self.generate_random_string()
                # 중복체크 
                for connection in self.__active_connection:
                    if connection.get_observer_uid() == new_uid:
                        flag = False
                        break
                
                # 중복이 없으면 break
                if flag:
                    break
            
            user.uid = new_uid

        print("new client! : ", user.uid)
        
        new_observer = self.add_new_observer(user=user)
        
        # 연결 시도!
        await new_observer.connect(websocket=websocket, observers=self.__active_connection)
        
        # 리스트에 넣어서 관리
        self.__active_connection.append(new_observer)
        
        return new_observer

    def add_new_observer(self, user:User):
        for observer in self.__active_connection:
            if observer.get_observer_uid() == user.uid:
                return None
        
        new_observer = Observer(user=user, active_observer=self.__active_connection)
        self.__active_connection.append(new_observer)
        return new_observer
    
    # 연결 해제
    async def disconnect(self, observer:Observer):
        self.__active_connection.remove(observer)
        return


    # 모든 목표물에게 전송
    async def all_broadcast(self, message:str):
        # 타깃에게 전송
        for connection in self.__active_connection:
            await connection.send_data(message)
        return
    
    

        
# 채팅 == 댓글 라서 저장 하거나 전송 가능한 형태로 만들기 위한 세팅!
class ChattingDataform:
    def __init__(self, uid, uname, fid, body, type, cid=""):
        self.uid = uid
        self.uname = uname
        self.fid = fid
        self.body = body
        self.date = datetime.now().strftime("%Y/%m/%d")
        self.type = type
        
        if type == "add":
            if cid == "":
                self.cid = uid+"-"+self.__set_fid_with_datatime()
            else:
                self.cid = cid
        else:
            self.cid=cid
        
        self.is_owner = False
    
    def __set_fid_with_datatime(self):
        now = datetime.now()
        formatted_time = now.strftime("%Y%m%d%H%M%S") + f"{now.microsecond:06d}"
        return formatted_time
    
    
    # type<br>is_owner<br>uid<br>uname<br>cid<br>body<br>date
    # 타입 : add, delete
    def get_send_form(self):
        return f"{self.type}<br>{self.is_owner}<br>{self.uid}<br>{self.uname}<br>{self.cid}<br>{self.body}<br>{self.date}"
        
        