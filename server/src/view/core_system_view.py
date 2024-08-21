from typing import Any, Optional
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from view.master_view import Master_View, RequestHeader
from view.parsers import Head_Parser
from controller import Home_Controller, Core_Controller

class Core_Service_View(Master_View):
    def __init__(self, app:FastAPI, endpoint:str, database, head_parser:Head_Parser) -> None:
        super().__init__(head_parser=head_parser)
        self.__app = app
        self._endpoint = endpoint
        self.__database = database
        self.home_route(endpoint)
        self.web_chatting_route(endpoint)

    def home_route(self, endpoint:str):
        @self.__app.get(endpoint+'/home')
        def home():
            return 'Hello, This is Root of Core-System Service'
        
        # 홈화면에 배너 정보
        @self.__app.get('/home/banner')
        def get_banner():
            home_controller=Home_Controller()
            model = home_controller.get_banner_data(database=self.__database,)
            response = model.get_response_form_data(self._head_parser)
            return response
        
        # 홈 화면에 최애 정보
        @self.__app.post('/home/my_bias')
        def get_my_bias(raw_request:dict):
            request = TokenRequest(request=raw_request)
            home_controller=Home_Controller()
            model = home_controller.get_my_bias_data(database=self.__database,
                                                             request=request)
            response = model.get_response_form_data(self._head_parser)
            return response

        # 회원의 bias의 리그를 받아내는 앤드 포인트 (post)
        @self.__app.post('/home/my_bias_league')
        def my_bias_leagues(raw_request:dict):
            request = MyLeagueRequest(request=raw_request)
            core_controller=Core_Controller()
            model = core_controller.get_my_bias_league(database=self.__database, request=request)
            response = model.get_response_form_data(self._head_parser)
            return response
        
        # 메인화면에 전체 리그 보기에서 띄워줄 리그 이름 보내줘야됨
        # http://127.0.0.1:6000/home/league_data?league_type=solo
        @self.__app.get('/home/league_data')
        def show_leagues(league_type:Optional[str] = "solo"):
            request = LeagueTypeRequest(league_type=league_type)
            home_controller=Home_Controller()
            model = home_controller.get_league_meta_data(database=self.__database, request=request)
            response = model.get_response_form_data(self._head_parser)
            return response

        # 리그 정보를 받아내는 기본적인 함수 (get)
        # 리그 정보를 받아내는 방법
        # http://127.0.0.1:6000/home/show_league?league_name=시리우스
        # http://127.0.0.1:6000/home/show_league?league_id=1001
        # http://127.0.0.1:6000/home/show_league?league_name=시리우스&league_id=1001
        @self.__app.get('/home/show_league')
        def show_leagues(league_name:Optional[str] = None, league_id:Optional[str] = None):
            request = LeagueRequest(league_name=league_name, league_id=league_id)
            core_controller=Core_Controller()
            model = core_controller.get_league(database=self.__database, request=request)
            response = model.get_response_form_data(self._head_parser)
            return response

        # 최애를 검색하는 보편적인 함수
        # 목적 : 나의 최애 선택하기, 홈화면의 최애 검색 기능
        #"http://127.0.0.1:6000/home/search_bias?bias_name=김"  # bias 검색
        @self.__app.get('/home/search_bias')
        def show_leagues(bias_name:Optional[str] = None):
            request = BiasSearchRequest(bias_name=bias_name)
            home_controller=Home_Controller()
            model = home_controller.search_bias(database=self.__database, request=request)
            response = model.get_response_form_data(self._head_parser)
            return response

        # 나의 최애 선택하기 (취소하기는 없음.... 취소하지 마라)
        @self.__app.post('/home/try_select_my_bias')
        def try_select_my_bias(raw_request:dict):
            request = BiasSelectRequest(request=raw_request)
            home_controller=Home_Controller()
            model = home_controller.select_bias(database=self.__database, request=request)
            response = model.get_response_form_data(self._head_parser)
            return response
        

        #@self.__app.post(endpoint+'/home/login')
        #def login(raw_request:dict):
            #request = LoginRequest(request=raw_request)
            #core_controller=Core_Controller()
            #model = core_controller.get_my_bias_league(database=self.__database,
                                                             #request=request)
            #response = model.get_response_form_data(self._head_parser)
            #return response
        
        #@self.__app.post(endpoint+'/home/daily')
        #def daily_request(raw_request:dict):
            #request = DailyRequest(request=raw_request)
            #core_controller=Core_Controller()
            #model = core_controller.requese_daily_check(database=self.__database,
                                                             #request=request)
            #response = model.get_response_form_data(self._head_parser)
            #return response


        #@self.__app.get(endpoint+'/{sample}')
        #def sample_get(sample:str):
            #request = sample
            #core_controller=Core_Controller()
            #model = core_controller.sample_func(database=self.__database,
                                                             #request=request)
            #response = model.get_response_form_data(self._head_parser)
            #return response
        
        #@self.__app.post(endpoint+'/post_sample')
        #def sample_post(raw_request:dict):
            #request = SampleRequest(request=raw_request)
            #core_controller=Core_Controller()
            #model = core_controller.sample_func(database=self.__database,
                                                             #request=request)
            #response = model.get_response_form_data(self._head_parser)
            #return response

    def web_chatting_route(self,endpoint:str):
        #채팅서버
        @self.__app.get('/chatting_list')
        def get_chatting_list():
            core_controller=Core_Controller()
            model = core_controller.get_chatting_data(database=self.__database,)
            response = model.get_response_form_data(self._head_parser)
            return response
            
        @self.__app.websocket('/chatting')
        async def chatting_socket(websocket:WebSocket):
            self.manager = ConnectionManager()
            core_controller=Core_Controller()
            await self.manager.connect(websocket)
            try:
                while True:
                    #{"token":"token"."message":"msg"}
                    request = await websocket.receive_text()
                    model = core_controller.chatting(database=self.__database, request=request)
                    if model.get_check() == True:
                        await self.manager.broadcast(f"{model._user.uname} :{model.get_chat_data().message}")
                    else:
                        continue
                
            except WebSocketDisconnect:
                self.manager.disconnect(websocket)
            #    await self.manager.broadcast("client disconnected")

class SampleRequest(RequestHeader):
    def __init__(self, request) -> None:
        super().__init__(request)
        body = request['body']
        self.uid = body['uid']
        self.date = body['date']

class LoginRequest(RequestHeader):
    def __init__(self, request) -> None:
        super().__init__(request)
        body = request['body']
        self.token = body['token']

class TokenRequest(RequestHeader):
    def __init__(self, request) -> None:
        super().__init__(request)
        body = request['body']
        self.token = body['token']

class MyLeagueRequest(RequestHeader):
    def __init__(self, request) -> None:
        super().__init__(request)
        body = request['body']
        self.token = body['token']
        self.league_type = body['type']

class LeagueTypeRequest():
    def __init__(self, league_type= None) -> None:
        self.league_type = league_type

class LeagueRequest():
    def __init__(self, league_name = None, league_id = None) -> None:
        self.league_name = league_name
        self.league_id = league_id

class BiasSearchRequest():
    def __init__(self, bias_name= None) -> None:
        self.bias_name =bias_name 


class BiasSelectRequest(RequestHeader):
    def __init__(self, request) -> None:
        super().__init__(request)
        body = request['body']
        self.token = body['token']
        self.bid = body['bid']

class DailyRequest(RequestHeader):
    def __init__(self, request) -> None:
        super().__init__(request)
        body = request['body']
        self.token = body['token']

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



