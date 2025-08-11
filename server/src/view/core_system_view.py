from typing import Optional, Union
from fastapi import FastAPI, WebSocket, Request, File, UploadFile, Form, WebSocketDisconnect
from view.master_view import Master_View, RequestHeader
from view.parsers import Head_Parser
from view.jwt_decoder import RequestManager
from controller import Home_Controller, Core_Controller, Feed_Controller
from fastapi.responses import HTMLResponse
from manager import ConnectionManager as CM
from others import FeedManager as FM
from others import FeedSearchEngine as FSE
from websockets.exceptions import ConnectionClosedError
from pprint import pprint
import json
from datetime import datetime

class Core_Service_View(Master_View):
    def __init__(self, app:FastAPI, endpoint:str,
                  database, head_parser:Head_Parser,
                  connection_manager:CM,
                  feed_manager:FM , feed_search_engine:FSE,
                  ai_manager, jwt_secret_key
                  ) -> None:
        super().__init__(head_parser=head_parser)
        self.__app = app
        self._endpoint = endpoint
        self.__database = database
        self.__connection_manager=connection_manager
        self.__feed_manager = feed_manager
        self.__feed_search_engine = feed_search_engine
        self.__ai_manager = ai_manager
        self.__jwt_secret_key = jwt_secret_key
        self.home_route(endpoint)
        #self.check_route()
        self.web_chatting_route(endpoint)
        self.feed_route()

    def home_route(self, endpoint:str):
        @self.__app.get(endpoint+'/home')
        def home():
            return 'Hello, This is Root of Core-System Service'

        # 이 클라이언트는 로그인을 했나요?를 확인하는 곳
        @self.__app.get('/home/is_valid')
        def is_valid_user(request:Request, only_token:Optional[str]="y"):
            request_manager = RequestManager(secret_key=self.__jwt_secret_key)
            request_manager.try_view_management_need_authorized(cookies=request.cookies)

            home_controller=Home_Controller()
            # 토큰 + 유저 UID 필요할때 (게시글 수정에서 본인 확인 등)
            if only_token == "n": 
                model = home_controller.get_token_need_user(request=request_manager,
                                                            database=self.__database)
            else: # 로그인 했는지만 확인할 때
                model = home_controller.get_token(database=self.__database)
            body_data = model.get_response_form_data(self._head_parser)
            response = request_manager.make_json_response(body_data=body_data)
            return response
        
        # 배너 정보
        @self.__app.get('/home/banner')
        def get_banner():
            home_controller=Home_Controller()
            model = home_controller.get_banner_data(database=self.__database,)
            response = model.get_response_form_data(self._head_parser)
            return response
        
        # 내가 팔로우 중인 스트리머 정보 
        @self.__app.get('/home/my_bias')
        def get_my_bias(request:Request):
            request_manager = RequestManager(secret_key=self.__jwt_secret_key)
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


    def feed_route(self):
        # 피드 자세히 보기 (피드 페이지)의 피드 데이터
        @self.__app.get('/feed_explore/feed_detail/feed_data')
        def get_feed_detail(request:Request, fid:Optional[str]):
            request_manager = RequestManager(secret_key=self.__jwt_secret_key)
            data_payload = GetFeedRequest(fid=fid)

            request_manager.try_view_management(data_payload=data_payload, cookies=request.cookies)
            #if not request_manager.jwt_payload.result:
                #raise request_manager.credentials_exception

            feed_controller =Feed_Controller(feed_manager=self.__feed_manager)
            model = feed_controller.get_specific_feed_data(database=self.__database,
                                                        request=request_manager)

            body_data = model.get_response_form_data(self._head_parser)
            # pprint(body_data)
            
            response = request_manager.make_json_response(body_data=body_data)
            return response

        @self.__app.get('/feed_explore/search_feed_with_keyword')
        def search_with_keyword(request:Request, key:Optional[int]=-1, keyword:Optional[str]="", fclass:Optional[str]="",
                                search_columns:Optional[str]=""):
            request_manager = RequestManager(secret_key=self.__jwt_secret_key)
            data_payload = KeywordSearchRequest(key=key, keyword=keyword, fclass=fclass, search_columns=search_columns)
            
            request_manager.try_view_management(data_payload=data_payload, cookies=request.cookies)

            feed_controller =Feed_Controller(feed_manager=self.__feed_manager)
            model = feed_controller.search_feed_with_keyword(database=self.__database,
                                                             request=request_manager,
                                                             feed_search_engine=self.__feed_search_engine,
                                                             num_feed=6)

            body_data = model.get_response_form_data(self._head_parser)
            response = request_manager.make_json_response(body_data=body_data)

            return response

        @self.__app.get('/feed_explore/search_comment_with_keyword')
        def search_with_keyword(request:Request, key:Optional[int]=-1, keyword:Optional[str]=""):
            request_manager = RequestManager(secret_key=self.__jwt_secret_key)
            data_payload = KeywordSearchRequest(key=key, keyword=keyword)
            request_manager.try_view_management(data_payload=data_payload, cookies=request.cookies)

            feed_controller = Feed_Controller(feed_manager=self.__feed_manager)
            model = feed_controller.search_comment_with_keyword(database=self.__database,
                                                                request=request_manager,
                                                                feed_search_engine=self.__feed_search_engine,
                                                                num_comments=6)
            body_data = model.get_response_form_data(self._head_parser)
            response = request_manager.make_json_response(body_data=body_data)

            return response

        # 전체 피드 제공
        @self.__app.post('/feed_explore/all_feed')
        def get_all_feed_filtering(request:Request, raw_request:dict):
            request_manager = RequestManager(secret_key=self.__jwt_secret_key)
            
            data_payload = AllFeedRequest(request=raw_request)
            
            request_manager.try_view_management(data_payload=data_payload, cookies=request.cookies)
            #if not request_manager.jwt_payload.result:
                #raise request_manager.credentials_exception

            feed_controller =Feed_Controller(feed_manager=self.__feed_manager)
            model = feed_controller.get_all_feed_filtered(database=self.__database,
                                                request=request_manager,
                                                feed_search_engine=self.__feed_search_engine,
                                                num_feed= 10)


            body_data = model.get_response_form_data(self._head_parser)
            response = request_manager.make_json_response(body_data=body_data)
            return response

        
        # Bias 기반 커뮤니티 피드
        @self.__app.post('/feed_explore/feed_with_community')
        def get_feed_with_community(request:Request, raw_request:dict):
            request_manager = RequestManager(secret_key=self.__jwt_secret_key)
            # 데이터 페이로드에도 bid 리스트를 넣어야됨
            
            data_payload = CommunityRequest(request=raw_request)
            
            request_manager.try_view_management(data_payload=data_payload, cookies=request.cookies)

            feed_controller =Feed_Controller(feed_manager=self.__feed_manager)
            model = feed_controller.get_feed_in_bias_feed_page(database=self.__database,
                                                    request=request_manager,
                                                    feed_search_engine=self.__feed_search_engine)

            body_data = model.get_response_form_data(self._head_parser)
            response = request_manager.make_json_response(body_data=body_data)
            return response


        ## 게시글 추천하기 기능 -> 갯수만큼 더 받으면됨 (개선이 필요함)
        #@self.__app.post('/feed_explore/get_recommend_feed')
        #def get_recommend_feed(request:Request, raw_request:dict):
            #request_manager = RequestManager(secret_key=self.__jwt_secret_key)
            #data_payload = ShortFeedrecommendRequest(request=raw_request)

            #request_manager.try_view_management(data_payload=data_payload, cookies=request.cookies)
            ##if not request_manager.jwt_payload.result:
                ##raise request_manager.credentials_exception

            #feed_controller =Feed_Controller(feed_manager=self.__feed_manager)
            #model = feed_controller.get_feed_with_recommend(database=self.__database,
                                                        #request=request_manager,
                                                        #feed_search_engine=self.__feed_search_engine)

            #body_data = model.get_response_form_data(self._head_parser)
            #response = request_manager.make_json_response(body_data=body_data)
            #return response

        # 게시글 좋아요 기능
        @self.__app.get('/feed_explore/check_star')
        def try_check_star(request:Request, fid:Optional[str]):
            request_manager = RequestManager(secret_key=self.__jwt_secret_key)

            data_payload = FeedStaringRequest(fid=fid)
            request_manager.try_view_management_need_authorized(data_payload=data_payload, cookies=request.cookies)
            if not request_manager.jwt_payload.result:
                raise request_manager.credentials_exception

            feed_controller =Feed_Controller(feed_manager=self.__feed_manager)
            model = feed_controller.try_staring_feed(database=self.__database,
                                                        request=request_manager,
                                                        feed_manager=self.__feed_manager)
            
            body_data = model.get_response_form_data(self._head_parser)
            response = request_manager.make_json_response(body_data=body_data)
            return response
        

        # feed 를 만들거나 수정하기
        @self.__app.post('/feed_explore/try_edit_feed')
        async def try_edit_feed(request: Request, images: Union[UploadFile, None] = File(None),
                        jsonData: Union[str, None] = Form(None)):
        #async def try_edit_feed(request:Request, images: UploadFile| None = File(None), 
                                #jsonData:str | None = Form(None)):
                               
            request_manager = RequestManager(secret_key=self.__jwt_secret_key)

            form_data = await request.form()
            image_files = form_data.getlist("images")
            
            if images is None or len(image_files) == 0:
                image_names = []
                imgs = []
            else:
                image_names = [image.filename for image in image_files]
                imgs = [await image.read() for image in image_files]

            if jsonData is None:
                raise request_manager.system_logic_exception

            raw_request = json.loads(jsonData)
            
            data_payload = EditFeedRequest(request=raw_request,
                                            image_names=image_names,
                                            images=imgs)
            request_manager.try_view_management_need_authorized(data_payload=data_payload, cookies=request.cookies)
            if not request_manager.jwt_payload.result:
                raise request_manager.credentials_exception

            feed_controller =Feed_Controller(feed_manager=self.__feed_manager)
            model = feed_controller.try_edit_feed(database=self.__database,
                                                        request=request_manager,
                                                        feed_manager=self.__feed_manager,
                                                        ai_manager = self.__ai_manager
                                                        )
            body_data = model.get_response_form_data(self._head_parser)
            response = request_manager.make_json_response(body_data=body_data)
            return response

        @self.__app.get('/feed_explore/try_remove_feed')
        def try_remove_feed(request:Request, fid:Optional[str]):
            request_manager = RequestManager(secret_key=self.__jwt_secret_key)
            data_payload = DeleteFeedRequest(fid=fid)

            # 로그인이 되어있지 않으면, 그 글을 삭제할 수 없음
            request_manager.try_view_management_need_authorized(data_payload=data_payload, cookies=request.cookies)
            if not request_manager.jwt_payload.result:
                raise request_manager.credentials_exception

            feed_controller =Feed_Controller(feed_manager=self.__feed_manager)
            model = feed_controller.try_remove_feed(database=self.__database,
                                                    request=request_manager,
                                                    feed_manager=self.__feed_manager)
            body_data = model.get_response_form_data(self._head_parser)
            response = request_manager.make_json_response(body_data=body_data)
            return response


    def web_chatting_route(self, endpoint:str):
        @self.__app.get('/feed_explore/feed_detail/comment_data')
        def get_comment_data(request:Request, fid:Optional[str], cid:Optional[str]=""):
            request_manager = RequestManager(secret_key=self.__jwt_secret_key)
            data_payload = CommentRequest(fid=fid, cid=cid)
            request_manager.try_view_management(data_payload=data_payload, cookies=request.cookies)

            feed_controller =Feed_Controller(feed_manager=self.__feed_manager)
            model = feed_controller.get_target_comment_on_feed(database=self.__database,
                                                        request=request_manager)
            body_data = model.get_response_form_data(self._head_parser)
            response = request_manager.make_json_response(body_data=body_data)
            return response

        @self.__app.websocket('/feed_detail_realtime/chatting_socket')
        async def try_socket_chatting(websocket:WebSocket, fid:Optional[str] = "", uid:Optional[str] = ""):  
            try:
                if fid == "":
                    return
                
                request_manager = RequestManager(secret_key=self.__jwt_secret_key)
                if uid == "-1":
                    uid = ""
                data_payload= ChattingSocketRequest(uid=uid, fid=fid)
                request_manager.try_view_just_data_payload(data_payload=data_payload)
                
                observer = await self.__connection_manager.connect(
                    request=request_manager,
                    websocket=websocket,
                    database = self.__database,
                    feed_controller=Feed_Controller(feed_manager=self.__feed_manager)
                    )
                
                result = await observer.observer_operation()
                
                if not result:
                    await self.__connection_manager.disconnect(observer=observer)

            except ConnectionClosedError:
                await self.__connection_manager.disconnect(observer=observer)
                
            except WebSocketDisconnect:
                await self.__connection_manager.disconnect(observer=observer)

class DummyRequest():
    def __init__(self) -> None:
        pass

# Request 아종 같은거라서 이건 재사용 금지
class CommunityRequest(RequestHeader):
    def __init__(self, request) -> None:
        super().__init__(request)
        body = request['body']
        self.bid = body['bid']
        self.category = body['board']
        self.key:int = body['key']

class AllFeedRequest(RequestHeader):
    def __init__(self, request) -> None:
        super().__init__(request)
        body = request['body']
        self.category = body['category']
        self.fclass= body['fclass']
        self.key= body['key']
        

class KeywordSearchRequest(RequestHeader):
    def __init__(self, key, keyword, fclass="", search_columns="") -> None:
        self.key = key
        self.keyword = keyword
        self.fclass = fclass
        self.search_columns = search_columns
        # self.email=""
    
    def __call__(self):
        return {
            "key": self.key,
            "keyword": self.keyword,
            "fclass": self.fclass,
            "search_columns": self.search_columns
        }
        

class GetFeedRequest(RequestHeader):
    def __init__(self, fid) -> None:
        self.fid= fid

class FeedStaringRequest(RequestHeader):
    def __init__(self,fid) -> None:
        self.fid=fid 


class DeleteFeedRequest(RequestHeader):
    def __init__(self,fid) -> None:
        self.fid=fid
        

class EditFeedRequest(RequestHeader):
    def __init__(self, request, image_names, images) -> None:
        super().__init__(request)
        body:dict = request['body']
        self.fid = body['fid']
        self.body = body['body']
        self.fclass = body.get("fclass", "short")
        self.board_type = body.get("category", "자유게시판")  # 자유게시판 디폴트
        self.choice= body['choice']
        self.hashtag = body['hashtag']
        self.link:list = body['link']
        self.bid = body.get("bid", "")
        self.date = body.get("date", "")
        self.image_names = image_names
        self.images = images
        
#class ShortFeedrecommendRequest(RequestHeader):
    #def __init__(self, request) -> None:
        #super().__init__(request)
        #body = request['body']
        #self.fid = body['fid']
        #self.history = body['history']

class BiasSearchRequest():
    def __init__(self, bias_name= None) -> None:
        self.bias_name =bias_name

class BiasSelectRequest(RequestHeader):
    def __init__(self, request) -> None:
        super().__init__(request)
        body = request['body']
        self.bid = body['bid']

class ChattingSocketRequest(RequestHeader):
    def __init__(self, uid="",fid="", date=datetime.today()) -> None:
        self.uid=uid
        self.fid= fid
        self.date = date
        
class CommentRequest(RequestHeader):
    def __init__(self, fid="", cid="", date=datetime.today()) -> None:
        self.fid= fid
        self.cid = cid
        self.date = date
        
