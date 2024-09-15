from typing import Any, Optional
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request
from view.master_view import Master_View, RequestHeader
from view.parsers import Head_Parser
from view.jwt_decoder import RequestManager
from controller import Home_Controller, Core_Controller, Feed_Controller
from fastapi.responses import HTMLResponse
from others import ConnectionManager as CM
from others import LeagueManager as LM
from others import FeedManager as FM
from websockets.exceptions import ConnectionClosedError

class Core_Service_View(Master_View):
    def __init__(self, app:FastAPI, endpoint:str,
                  database, head_parser:Head_Parser,
                  connection_manager:CM, league_manager:LM,
                  feed_manager:FM
                  ) -> None:
        super().__init__(head_parser=head_parser)
        self.__app = app
        self._endpoint = endpoint
        self.__database = database
        self.__connection_manager=connection_manager
        self.__league_manager=league_manager
        self.__feed_manager = feed_manager
        self.home_route(endpoint)
        self.check_route()
        self.web_chatting_route(endpoint)

    def home_route(self, endpoint:str):
        @self.__app.get(endpoint+'/home')
        def home():
            return 'Hello, This is Root of Core-System Service'

        # 홈화
        @self.__app.get('/home/is_valid')
        def get_banner(request:Request):
            request_manager = RequestManager()
            request_manager.try_view_management(cookies=request.cookies)
            if not request_manager.jwt_payload.result:
                raise self._credentials_exception

            home_controller=Home_Controller()
            model = home_controller.get_token(database=self.__database)
            body_data = model.get_response_form_data(self._head_parser)
            response = request_manager.make_json_response(body_data=body_data)
            return response
        
        # 홈화면에 배너 정보
        @self.__app.get('/home/banner')
        def get_banner():
            home_controller=Home_Controller()
            model = home_controller.get_banner_data(database=self.__database,)
            response = model.get_response_form_data(self._head_parser)
            return response
        
        @self.__app.get('/home/feed_data')
        def get_feed_data(request:Request, key:Optional[int] = None):
            request_manager = RequestManager()
            data_payload = HomeFeedRequest(request=key)
            request_manager.try_view_management(data_payload=data_payload, cookies=request.cookies)
            #if not request_manager.jwt_payload.result:
                #raise request_manager.credentials_exception

            home_controller=Feed_Controller()
            model = home_controller.get_home_feed_data(database=self.__database,
                                                        request=request_manager,
                                                        feed_manager=self.__feed_manager)

            body_data = model.get_response_form_data(self._head_parser)
            response = request_manager.make_json_response(body_data=body_data)
            return response

        
        # 홈 화면에 최애 정보
        @self.__app.get('/home/my_bias')
        def get_my_bias(request:Request):
            request_manager = RequestManager()
            data_payload = DummyRequest()
            request_manager.try_view_management(data_payload=data_payload, cookies=request.cookies)
            # 검사 결과에 없으면 없다는 결과로 가야됨
            #if not request_manager.jwt_payload.result:
                #raise self._credentials_exception

            home_controller=Home_Controller()
            model = home_controller.get_my_bias_data(database=self.__database,
                                                             request=request_manager)
            body_data = model.get_response_form_data(self._head_parser)
            response = request_manager.make_json_response(body_data=body_data)

            return response
        
        @self.__app.get('/home/home_feed')
        def new_contentes():
            data = ["1", "2", "3", "4"]
            return data

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

    def check_route(self):
        # 최애 인증 페이지
        @self.__app.post('/nova_check/server_info/check_page')
        def get_check_page(raw_request:dict):
            request = CheckRequest(request=raw_request)
            core_controller=Core_Controller()
            model = core_controller.get_check_page(database=self.__database,
                                                             request=request)
            response = model.get_response_form_data(self._head_parser)
            return response

        # 최애 인증 시도 
        @self.__app.post('/nova_check/server_info/try_daily_check')
        def get_check_page(raw_request:dict):
            request = CheckRequest(request=raw_request)
            core_controller=Core_Controller()
            model = core_controller.try_daily_check(database=self.__database,
                                                             request=request,
                                                             league_manager=self.__league_manager)
            response = model.get_response_form_data(self._head_parser)
            return response

        # 최애 특별시 인증
        @self.__app.post('/nova_check/server_info/try_special_check')
        def get_check_page(raw_request:dict):
            request = CheckRequest(request=raw_request)
            core_controller=Core_Controller()
            model = core_controller.try_special_check(database=self.__database,
                                                             request=request,
                                                             league_manager=self.__league_manager)
            response = model.get_response_form_data(self._head_parser)
            return response

        @self.__app.get('/nova_check/shared/{name_card}', response_class=HTMLResponse)
        def sample_get(name_card:str):
            request = name_card 
            core_controller=Core_Controller()
            html = core_controller.get_shared_url(database=self.__database,
                                                             request=request)
            return html

    def web_chatting_route(self, endpoint:str):
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

        @self.__app.websocket('/league_detail/league_data')
        async def league_socket(websocket:WebSocket, league_name:Optional[str] = ""):
            try:
                print("connection")
                print(league_name)
                if league_name == "":
                    return
                observer = await self.__connection_manager.connect(lname=league_name,
                                                                     websocket=websocket,
                                                                     league_manager=self.__league_manager,
                                                                     )
                result = await observer.send_operation()
                if not result:
                    self.__connection_manager.disconnect(observer=observer)

            except ConnectionClosedError:
                self.__connection_manager.disconnect(observer=observer)
                
            except WebSocketDisconnect:
                self.__connection_manager.disconnect(observer=observer)

class DummyRequest():
    def __init__(self) -> None:
        pass

class SampleRequest(RequestHeader):
    def __init__(self, request) -> None:
        super().__init__(request)
        body = request['body']
        self.uid = body['uid']
        self.date = body['date']

class HomeFeedRequest(RequestHeader):
    def __init__(self, key) -> None:
        self.key = key

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

class CheckRequest(RequestHeader):
    def __init__(self, request) -> None:
        super().__init__(request)
        body = request['body']
        self.token = body['token']
        self.type = body['type']

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



