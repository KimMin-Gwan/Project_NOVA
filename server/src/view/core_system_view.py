from typing import Any, Optional, Union, List
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request, File, UploadFile, Form
from view.master_view import Master_View, RequestHeader
from view.parsers import Head_Parser
from view.jwt_decoder import RequestManager
from controller import Home_Controller, Core_Controller, Feed_Controller
from fastapi.responses import HTMLResponse
from others import ConnectionManager as CM
from others import LeagueManager as LM
from others import FeedManager as FM
from websockets.exceptions import ConnectionClosedError
import json

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
        #self.web_chatting_route(endpoint)
        self.feed_route()

    def home_route(self, endpoint:str):
        @self.__app.get(endpoint+'/home')
        def home():
            return 'Hello, This is Root of Core-System Service'

        # 홈화
        @self.__app.get('/home/is_valid')
        def is_valid_user(request:Request):
            
            #try:
                #client_host = request.client.host
                #print(f"{client_host}  -  GET /home/is_valid 200 OK")
                #client_ip = request.headers['x-real-ip']
                #print(f"{client_ip}  -  GET /home/is_valid 200 OK")
            #except:
                ##print("Anonymous User Try Contact Us")

            request_manager = RequestManager()
            request_manager.try_view_management_need_authorized(cookies=request.cookies)
            #if not request_manager.jwt_payload.result:
                #raise self._credentials_exception

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
        
        # 홈 화면에 최애 정보
        @self.__app.get('/home/my_bias')
        def get_my_bias(request:Request):
            request_manager = RequestManager()
            data_payload = DummyRequest()
            request_manager.try_view_management_need_authorized(data_payload=data_payload, cookies=request.cookies)
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
        def get_feed_data(request:Request, key:Optional[int] = -4):
            request_manager = RequestManager()
            data_payload = HomeFeedRequest(key=key)
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

        @self.__app.get('/home/realtime_hot_feed')
        def get_feed_data(request:Request, key:Optional[int] = -4):
            request_manager = RequestManager()
            data_payload = HomeFeedRequest(key=key)
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

        @self.__app.get('/home/hot_hashtag')
        def get_hot_hashtag(request:Request):
            request_manager = RequestManager()
            data_payload = DummyRequest()
            request_manager.try_view_management(data_payload=data_payload, cookies=request.cookies)
            #if not request_manager.jwt_payload.result:
                #raise request_manager.credentials_exception

            home_controller=Home_Controller()
            model = home_controller.get_hot_hashtag(database=self.__database,
                                                        request=request_manager)
            body_data = model.get_response_form_data(self._head_parser)
            response = request_manager.make_json_response(body_data=body_data)
            return response

        @self.__app.get('/home/hot_hashtag_feed')
        def get_hot_hashtag_feed(request:Request, hashtag:Optional[str]):
            request_manager = RequestManager()
            data_payload = HomeHashtagFeedRequest(hashtag=hashtag)
            request_manager.try_view_management(data_payload=data_payload, cookies=request.cookies)
            #if not request_manager.jwt_payload.result:
                #raise request_manager.credentials_exception

            home_controller=Feed_Controller()
            model = home_controller.get_home_hot_hashtag_feed(database=self.__database,
                                                        request=request_manager,
                                                        feed_manager=self.__feed_manager)

            body_data = model.get_response_form_data(self._head_parser)
            response = request_manager.make_json_response(body_data=body_data)
            return response
        
        @self.__app.get('/home/realtime_best_hashtag')
        def get_realtime_best_hashtag(request:Request):
            request_manager = RequestManager()
            data_payload = DummyRequest()
            request_manager.try_view_management(data_payload=data_payload, cookies=request.cookies)
            #if not request_manager.jwt_payload.result:
                #raise request_manager.credentials_exception

            home_controller=Home_Controller()
            model = home_controller.get_realtime_best_hashtag(database=self.__database,
                                                        request=request_manager)
            body_data = model.get_response_form_data(self._head_parser)
            response = request_manager.make_json_response(body_data=body_data)
            return response


        # 최애를 검색하는 보편적인 함수
        # 목적 : 나의 최애 선택하기, 홈화면의 최애 검색 기능
        #"http://127.0.0.1:6000/home/search_bias?bias_name=김"  # bias 검색
        @self.__app.get('/home/search_bias')
        def try_search_bias(bias_name:Optional[str] = None):
            request = BiasSearchRequest(bias_name=bias_name)
            home_controller=Home_Controller()
            model = home_controller.search_bias(database=self.__database, request=request)
            response = model.get_response_form_data(self._head_parser)
            return response

        # 나의 최애 선택하기 (취소하기는 없음.... 취소하지 마라)
        @self.__app.post('/home/try_select_my_bias')
        def try_select_my_bias(request:Request, raw_request:dict):
            request_manager = RequestManager()

            data_payload = BiasSelectRequest(request=raw_request)
            request_manager.try_view_management(data_payload=data_payload, cookies=request.cookies)
            if not request_manager.jwt_payload.result:
                raise self._credentials_exception

            home_controller=Home_Controller()
            model = home_controller.select_bias(database=self.__database, request=request_manager)
            body_data = model.get_response_form_data(self._head_parser)
            response = request_manager.make_json_response(body_data=body_data)

            return response
        


    def feed_route(self):

        # feed 데이터 받아오기( 위성 탐색 페이지에서 특정 fclass를 대상으로)
        @self.__app.get('/feed_explore/get_feed')
        def get_feed_data(request:Request, fclass:Optional[str] = "", key:Optional[int] = -4 ):
            request_manager = RequestManager()
            if fclass == "":
                raise request_manager.get_bad_request_exception()
            data_payload = GetFeedRequest(fclass=fclass, key=key)
            request_manager.try_view_management(data_payload=data_payload, cookies=request.cookies)
            #if not request_manager.jwt_payload.result:
                #raise request_manager.credentials_exception

            home_controller=Feed_Controller()
            model = home_controller.get_specific_feed_data(database=self.__database,
                                                        request=request_manager,
                                                        feed_manager=self.__feed_manager)

            body_data = model.get_response_form_data(self._head_parser)
            response = request_manager.make_json_response(body_data=body_data)
            return response

        # feed 랑 상호작용 -> 버튼을 눌렀을 때 ( 홈 또는 위성 탐색 페이지에서 사용)
        @self.__app.get('/feed_explore/interaction_feed')
        def try_interaction_feed(request:Request, fid:Optional[str], action:Optional[int]):
            request_manager = RequestManager()

            data_payload = FeedInteractionRequest(fid=fid, action=action)
            request_manager.try_view_management_need_authorized(data_payload=data_payload, cookies=request.cookies)
            if not request_manager.jwt_payload.result:
                raise request_manager.credentials_exception

            home_controller=Feed_Controller()
            model = home_controller.try_interact_feed(database=self.__database,
                                                        request=request_manager,
                                                        feed_manager=self.__feed_manager)

            body_data = model.get_response_form_data(self._head_parser)
            response = request_manager.make_json_response(body_data=body_data)
            return response

        # feed 랑 상호작용 -> 관심별 버튼 
        @self.__app.get('/feed_explore/check_star')
        def try_check_star(request:Request, fid:Optional[str]):
            request_manager = RequestManager()

            data_payload = FeedStaringRequest(fid=fid)
            request_manager.try_view_management_need_authorized(data_payload=data_payload, cookies=request.cookies)
            if not request_manager.jwt_payload.result:
                raise request_manager.credentials_exception

            home_controller=Feed_Controller()
            model = home_controller.try_staring_feed(database=self.__database,
                                                        request=request_manager,
                                                        feed_manager=self.__feed_manager)
            body_data = model.get_response_form_data(self._head_parser)
            response = request_manager.make_json_response(body_data=body_data)
            return response

        # feed 랑 상호작용 -> 댓글 달기
        @self.__app.post('/feed_explore/make_comment')
        def try_make_comment(request:Request, raw_requset:dict):
            request_manager = RequestManager()
            data_payload = MakeFeedCommentRequest(request=raw_requset)

            request_manager.try_view_management_need_authorized(data_payload=data_payload, cookies=request.cookies)
            if not request_manager.jwt_payload.result:
                raise request_manager.credentials_exception

            home_controller=Feed_Controller()
            model = home_controller.try_make_comment(database=self.__database,
                                                        request=request_manager,
                                                        feed_manager=self.__feed_manager)
            body_data = model.get_response_form_data(self._head_parser)
            response = request_manager.make_json_response(body_data=body_data)
            return response

        # feed 랑 상호작용 -> 댓글 지우기
        @self.__app.get('/feed_explore/remove_comment')
        def try_remove_comment(request:Request, fid:Optional[str], cid:Optional[str]):
            request_manager = RequestManager()

            data_payload = RemoveCommentRequest(fid=fid, cid=cid)
            request_manager.try_view_management_need_authorized(data_payload=data_payload, cookies=request.cookies)
            if not request_manager.jwt_payload.result:
                raise request_manager.credentials_exception

            home_controller=Feed_Controller()
            model = home_controller.try_remove_comment(database=self.__database,
                                                        request=request_manager,
                                                        feed_manager=self.__feed_manager)
            body_data = model.get_response_form_data(self._head_parser)
            response = request_manager.make_json_response(body_data=body_data)
            return response

        # feed 랑 상호작용 -> 댓글 모두보기
        @self.__app.get('/feed_explore/view_comment')
        def get_all_comment(request:Request, fid:Optional[str]):
            request_manager = RequestManager()

            data_payload = FeedStaringRequest(fid=fid)
            request_manager.try_view_management(data_payload=data_payload, cookies=request.cookies)
            #if not request_manager.jwt_payload.result:
                #raise request_manager.credentials_exception

            home_controller=Feed_Controller()
            model = home_controller.get_all_comment_on_feed(database=self.__database,
                                                        request=request_manager,
                                                        feed_manager=self.__feed_manager)
            body_data = model.get_response_form_data(self._head_parser)
            response = request_manager.make_json_response(body_data=body_data)
            return response

        # feed 랑 상호작용 -> 댓글 좋아요 하기
        @self.__app.get('/feed_explore/like_comment')
        def try_like_comment(request:Request, fid:Optional[str], cid:Optional[str]):
            request_manager = RequestManager()

            data_payload = RemoveCommentRequest(fid=fid, cid=cid)
            request_manager.try_view_management_need_authorized(data_payload=data_payload, cookies=request.cookies)
            if not request_manager.jwt_payload.result:
                raise request_manager.credentials_exception

            home_controller=Feed_Controller()
            model = home_controller.try_like_comment(database=self.__database,
                                                        request=request_manager,
                                                        feed_manager=self.__feed_manager)
            body_data = model.get_response_form_data(self._head_parser)
            response = request_manager.make_json_response(body_data=body_data)
            return response

        # feed 를 만들거나 수정하기
        @self.__app.post('/feed_explore/try_edit_feed')
        async def try_edit_feed(request: Request, images: Union[List[UploadFile], None] = File(...),
                        jsonData: Union[str, None] = Form(None)):
        #async def try_edit_feed(request:Request, images: UploadFile| None = File(None), 
                                #jsonData:str | None = Form(None)):
            request_manager = RequestManager()

            print(images)

            return "hello"
            if images is None or len(images) == 0:
                image_names = []
                imgs = []
            else:
                image_names = [image.filename for image in images]
                imgs = [await image.read() for image in images]

            print(image_names)

            if jsonData is None:
                raise request_manager.system_logic_exception

            raw_request = json.loads(jsonData)

            data_payload = EditFeedRequest(request=raw_request,
                                            image_names=image_names,
                                            images=imgs)
            request_manager.try_view_management_need_authorized(data_payload=data_payload, cookies=request.cookies)
            if not request_manager.jwt_payload.result:
                raise request_manager.credentials_exception

            home_controller=Feed_Controller()
            model = home_controller.try_edit_feed(database=self.__database,
                                                        request=request_manager,
                                                        feed_manager=self.__feed_manager)
            body_data = model.get_response_form_data(self._head_parser)
            response = request_manager.make_json_response(body_data=body_data)
            return response

    def check_route(self):
        # 최애 인증 페이지
        @self.__app.post('/nova_check/server_info/check_page')
        def get_check_page(request:Request, raw_request:dict):
            request_manager = RequestManager()

            data_payload= CheckRequest(request=raw_request)
            request_manager.try_view_management_need_authorized(data_payload=data_payload, cookies=request.cookies)
            if not request_manager.jwt_payload.result:
                raise request_manager.credentials_exception

            core_controller=Core_Controller()
            model = core_controller.get_check_page(database=self.__database,
                                                             request=request_manager)
            body_data = model.get_response_form_data(self._head_parser)
            response = request_manager.make_json_response(body_data=body_data)
            return response

        # 최애 인증 시도 
        @self.__app.post('/nova_check/server_info/try_daily_check')
        def get_check_page(request:Request, raw_request:dict):
            request_manager = RequestManager()

            data_payload= CheckRequest(request=raw_request)
            request_manager.try_view_management_need_authorized(data_payload=data_payload, cookies=request.cookies)
            if not request_manager.jwt_payload.result:
                raise request_manager.credentials_exception

            core_controller=Core_Controller()
            model = core_controller.try_daily_check(database=self.__database,
                                                             request=request_manager,
                                                             league_manager=self.__league_manager)
            body_data = model.get_response_form_data(self._head_parser)
            response = request_manager.make_json_response(body_data=body_data)
            return response

        # 최애 특별시 인증
        @self.__app.post('/nova_check/server_info/try_special_check')
        def get_check_page(request:Request, raw_request:dict):
            request_manager = RequestManager()

            data_payload= CheckRequest(request=raw_request)
            request_manager.try_view_management_need_authorized(data_payload=data_payload, cookies=request.cookies)
            if not request_manager.jwt_payload.result:
                raise request_manager.credentials_exception

            core_controller=Core_Controller()
            model = core_controller.try_special_check(database=self.__database,
                                                             request=request_manager,
                                                             league_manager=self.__league_manager)
            body_data = model.get_response_form_data(self._head_parser)
            response = request_manager.make_json_response(body_data=body_data)
            return response

        @self.__app.get('/nova_check/shared/{name_card}', response_class=HTMLResponse)
        def sample_get(name_card:str):
            request = name_card 
            core_controller=Core_Controller()
            html = core_controller.get_shared_url(database=self.__database,
                                                             request=request)
            return html
        

    #def web_chatting_route(self, endpoint:str):
        ##채팅서버
        ##@self.__app.get('/chatting_list')
        ##def get_chatting_list():
            ##core_controller=Core_Controller()
            ##model = core_controller.get_chatting_data(database=self.__database,)
            ##response = model.get_response_form_data(self._head_parser)
            ##return response
            
        ##@self.__app.websocket('/chatting')
        ##async def chatting_socket(websocket:WebSocket):
            ##self.manager = ConnectionManager()
            ##core_controller=Core_Controller()
            ##await self.manager.connect(websocket)
            ##try:
                ##while True:
                    ###{"token":"token"."message":"msg"}
                    ##request = await websocket.receive_text()
                    ##model = core_controller.chatting(database=self.__database, request=request)
                    ##if model.get_check() == True:
                        ##await self.manager.broadcast(f"{model._user.uname} :{model.get_chat_data().message}")
                    ##else:
                        ##continue
                
            ##except WebSocketDisconnect:
                ##self.manager.disconnect(websocket)
            ###    await self.manager.broadcast("client disconnected")

        ## 최애를 검색하는 보편적인 함수
        ## 목적 : 나의 최애 선택하기, 홈화면의 최애 검색 기능
        ##"http://127.0.0.1:6000/home/search_bias?bias_name=김"  # bias 검색
        #@self.__app.get('/league_detail/league_meta_data')
        #def get_league_meta_data():
            #home_controller=Home_Controller()
            #model = home_controller.get_league_meta_data(database=self.__database, league_manager=self.__league_manager)
            #response = model.get_response_form_data(self._head_parser)
            #return response

        #@self.__app.websocket('/league_detail/league_data')
        #async def league_socket(websocket:WebSocket, league_name:Optional[str] = ""):
            #try:
                #if league_name == "":
                    #return
                #observer = await self.__connection_manager.connect(lname=league_name,
                                                                     #websocket=websocket,
                                                                     #league_manager=self.__league_manager,
                                                                     #)
                #result = await observer.send_operation()
                #if not result:
                    #self.__connection_manager.disconnect(observer=observer)

            #except ConnectionClosedError:
                #self.__connection_manager.disconnect(observer=observer)
                
            #except WebSocketDisconnect:
                #self.__connection_manager.disconnect(observer=observer)

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

class HomeHashtagFeedRequest(RequestHeader):
    def __init__(self, hashtag) -> None:
        self.hashtag = hashtag 

class GetFeedRequest(RequestHeader):
    def __init__(self,fclass, key) -> None:
        self.fclass = fclass
        self.key = key

class RemoveCommentRequest(RequestHeader):
    def __init__(self,fid,cid) -> None:
        self.fid=fid 
        self.cid=cid

class FeedStaringRequest(RequestHeader):
    def __init__(self,fid) -> None:
        self.fid=fid 

class FeedInteractionRequest(RequestHeader):
    def __init__(self,fid, action) -> None:
        self.fid=fid 
        self.action = action

class EditFeedRequest(RequestHeader):
    def __init__(self, request, image_names, images) -> None:
        super().__init__(request)
        body = request['body']
        self.fid = body['fid']
        self.body = body['body']
        self.fclass = body ['fclass']
        self.choice= body['choice']
        self.hashtag = body['hashtag']
        self.image_names = image_names
        self.images = images

class MakeFeedCommentRequest(RequestHeader):
    def __init__(self, request) -> None:
        super().__init__(request)
        body = request['body']
        self.fid = body['fid']
        self.body = body['body']

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
        self.bid = body['bid']

class CheckRequest(RequestHeader):
    def __init__(self, request) -> None:
        super().__init__(request)
        body = request['body']
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



