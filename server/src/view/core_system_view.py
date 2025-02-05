from typing import Any, Optional, Union, List
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request, File, UploadFile, Form
from view.master_view import Master_View, RequestHeader
from view.parsers import Head_Parser
from view.jwt_decoder import RequestManager, TempCookieManager
from controller import Home_Controller, Core_Controller, Feed_Controller
from fastapi.responses import HTMLResponse
from others import ConnectionManager as CM
from others import LeagueManager as LM
from others import FeedManager as FM
from others import FeedSearchEngine as FSE
from websockets.exceptions import ConnectionClosedError
from pprint import pprint
import json
import time

import numpy as np

class Core_Service_View(Master_View):
    def __init__(self, app:FastAPI, endpoint:str,
                  database, head_parser:Head_Parser,
                  connection_manager:CM, league_manager:LM,
                  feed_manager:FM , feed_search_engine:FSE) -> None:
        super().__init__(head_parser=head_parser)
        self.__app = app
        self._endpoint = endpoint
        self.__database = database
        self.__connection_manager=connection_manager
        self.__league_manager=league_manager
        self.__feed_manager = feed_manager
        self.__feed_search_engine = feed_search_engine
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

        @self.__app.get('/home/hot_hashtag')
        def get_hot_hashtag(request:Request):
            request_manager = RequestManager()
            data_payload = DummyRequest()
            request_manager.try_view_management(data_payload=data_payload, cookies=request.cookies)
            #if not request_manager.jwt_payload.result:
                #raise request_manager.credentials_exception

            home_controller=Home_Controller(feed_manager=self.__feed_manager)

            # 만약 인기 해시태그의 리스트가 0이면 어떻게 다른걸 해야됨!!

            model = home_controller.get_hot_hashtag(database=self.__database,
                                                        request=request_manager,
                                                        feed_search_engine=self.__feed_search_engine)
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

            home_controller=Home_Controller(feed_manager=self.__feed_manager)
            model = home_controller.get_realtime_best_hashtag(database=self.__database,
                                                        request=request_manager,
                                                        feed_search_engine=self.__feed_search_engine)
            body_data = model.get_response_form_data(self._head_parser)
            response = request_manager.make_json_response(body_data=body_data)
            return response

        @self.__app.get('/home/today_spiked_hot_hashtag')
        def get_today_hot_hashtag(request:Request):
            request_manager = RequestManager()
            data_payload = DummyRequest()
            request_manager.try_view_management(data_payload=data_payload, cookies=request.cookies)

            # if not request_manager.jwt_payload.result:
            #     raise request_manager.credentials_exception
            home_controller=Home_Controller(feed_manager=self.__feed_manager)
            model = home_controller.get_today_best_hashtag(database=self.__database,
                                                           request=request_manager,
                                                           feed_search_engine=self.__feed_search_engine)
            body_data = model.get_response_form_data(self._head_parser)
            response = request_manager.make_json_response(body_data=body_data)

            return response

        # 이거 까지
        @self.__app.get('/home/weekly_spiked_hot_hashtag')
        def get_weekly_hot_hashtag(request:Request):
            request_manager = RequestManager()
            data_payload = DummyRequest()
            request_manager.try_view_management(data_payload=data_payload, cookies=request.cookies)

            # if not request_manager.jwt_payload.result:
            #     raise request_manager.credentials_exception
            home_controller=Home_Controller(feed_manager=self.__feed_manager)
            model = home_controller.get_weekly_best_hashtag(database=self.__database,
                                                            request=request_manager,
                                                            feed_search_engine=self.__feed_search_engine)
            body_data = model.get_response_form_data(self._head_parser)
            response = request_manager.make_json_response(body_data=body_data)

            return response

        # /home/search_feed_with_hashtag?hashtag=뭐
        @self.__app.get('/home/search_feed_with_hashtag')
        def get_hot_hashtag_feed(request:Request, hashtag:Optional[str]):

            request_manager = RequestManager()

            data_payload = HashtagFeedRequest(hashtag=hashtag)

            request_manager.try_view_management(data_payload=data_payload, cookies=request.cookies)
            #if not request_manager.jwt_payload.result:
                #raise request_manager.credentials_exception

            feed_controller=Feed_Controller(feed_manager=self.__feed_manager)
            model = feed_controller.get_feed_with_hashtag(database=self.__database,
                                                        request=request_manager,
                                                        feed_search_engine=self.__feed_search_engine,
                                                        feed_manager=self.__feed_manager,
                                                        num_feed=5)

            body_data = model.get_response_form_data(self._head_parser)
            #pprint(body_data)
            response = request_manager.make_json_response(body_data=body_data)
            return response

        # /home/search_feed_with_bid?bid=뭐
        @self.__app.get('/home/search_feed_with_bid')
        def get_feed_with_bid(request:Request, bid:Optional[str]=""):

            request_manager = RequestManager()

            data_payload = GetFeedBidRequest(bid=bid)

            request_manager.try_view_management(data_payload=data_payload, cookies=request.cookies)
            #if not request_manager.jwt_payload.result:
                #raise request_manager.credentials_exception

            feed_controller=Feed_Controller(feed_manager=self.__feed_manager)
            model = feed_controller.get_feed_with_bid(database=self.__database,
                                                        request=request_manager,
                                                        feed_search_engine=self.__feed_search_engine,
                                                        num_feed=5)

            body_data = model.get_response_form_data(self._head_parser)
            #pprint(body_data)
            response = request_manager.make_json_response(body_data=body_data)
            return response

        # 추천 키워드 시스템.
        # 현재는 일부러 주간 핫태그를 내보내도록 했습니다.
        @self.__app.get('/home_search/get_recommend_keyword')
        def get_recommend_keyword(request:Request):
            request_manager = RequestManager()
            data_payload = DummyRequest()
            request_manager.try_view_management(data_payload=data_payload, cookies=request.cookies)

            home_controller = Home_Controller(feed_manager=self.__feed_manager)
            model = home_controller.get_recommend_keyword(database=self.__database,
                                                          request=request_manager,
                                                          feed_search_engine=self.__feed_search_engine,
                                                          )
            body_data = model.get_response_form_data(self._head_parser)
            response = request_manager.make_json_response(body_data=body_data)
            return response

        @self.__app.get('/home/all_feed')
        def get_feed_data(request:Request, key:Optional[int] = -1):
            request_manager = RequestManager()
            data_payload = HomeFeedRequest(key=key)
            request_manager.try_view_management(data_payload=data_payload, cookies=request.cookies)
            #if not request_manager.jwt_payload.result:
                #raise request_manager.credentials_exception

            feed_controller =Feed_Controller(feed_manager=self.__feed_manager)
            model = feed_controller.get_all_feed(database=self.__database,
                                                request=request_manager,
                                                feed_search_engine=self.__feed_search_engine,
                                                num_feed=6)

            body_data = model.get_response_form_data(self._head_parser)
            response = request_manager.make_json_response(body_data=body_data)
            return response

        # 오늘의 인기 게시글
        @self.__app.get('/home/today_best')
        def get_feed_data(request:Request, key:Optional[int] = -1):
            request_manager = RequestManager()
            data_payload = HomeFeedRequest(key=-1)
            request_manager.try_view_management(data_payload=data_payload, cookies=request.cookies)
            #if not request_manager.jwt_payload.result:
                #raise request_manager.credentials_exception

            feed_controller =Feed_Controller(feed_manager=self.__feed_manager)
            model = feed_controller.get_today_best(database=self.__database,
                                                    request=request_manager,
                                                    feed_search_engine=self.__feed_search_engine,
                                                    num_feed=4)

            body_data = model.get_response_form_data(self._head_parser)
            response = request_manager.make_json_response(body_data=body_data)
            return response

        # 주간 베스트 피드
        @self.__app.get('/home/weekly_best')
        def get_feed_data(request:Request, key:Optional[int] = -1):
            request_manager = RequestManager()
            data_payload = HomeFeedRequest(key=-1)
            request_manager.try_view_management(data_payload=data_payload, cookies=request.cookies)
            #if not request_manager.jwt_payload.result:
                #raise request_manager.credentials_exception

            feed_controller =Feed_Controller(feed_manager=self.__feed_manager)
            model = feed_controller.get_weekly_best(database=self.__database,
                                                    request=request_manager,
                                                    feed_search_engine=self.__feed_search_engine,
                                                    num_feed=4)

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

        # 나의 최애 선택하기 (다시 누르면 취소하기됨0)
        @self.__app.post('/home/try_select_my_bias')
        def try_select_my_bias(request:Request, raw_request:dict):
            request_manager = RequestManager()

            data_payload = BiasSelectRequest(request=raw_request)
            request_manager.try_view_management(data_payload=data_payload, cookies=request.cookies)
            if not request_manager.jwt_payload.result:
                raise self._credentials_exception

            home_controller=Home_Controller()
            model = home_controller.select_bias(database=self.__database,
                                                 request=request_manager,
                                                 feed_search_engine=self.__feed_search_engine)
            body_data = model.get_response_form_data(self._head_parser)
            response = request_manager.make_json_response(body_data=body_data)
            return response

    def feed_route(self):
        # 피드 자세히 보기 (피드 페이지)의 피드 데이터
        @self.__app.get('/feed_explore/feed_detail/feed_data')
        def get_feed_detail(request:Request, fid:Optional[str]):
            request_manager = RequestManager()
            data_payload = GetFeedRequest(fid=fid)

            request_manager.try_view_management(data_payload=data_payload, cookies=request.cookies)
            #if not request_manager.jwt_payload.result:
                #raise request_manager.credentials_exception

            feed_controller =Feed_Controller(feed_manager=self.__feed_manager)
            model = feed_controller.get_specific_feed_data(database=self.__database,
                                                        request=request_manager)

            body_data = model.get_response_form_data(self._head_parser)
            response = request_manager.make_json_response(body_data=body_data)
            return response

        # 피드 자세히 보기의 댓글 데이터
        @self.__app.get('/feed_explore/feed_detail/comment_data')
        def get_feed_detail(request:Request, fid:Optional[str]):
            request_manager = RequestManager()
            data_payload = GetFeedRequest(fid=fid)

            request_manager.try_view_management(data_payload=data_payload, cookies=request.cookies)
            #if not request_manager.jwt_payload.result:
                #raise request_manager.credentials_exception

            feed_controller =Feed_Controller(feed_manager=self.__feed_manager)
            model = feed_controller.get_all_comment_on_feed(database=self.__database,
                                                        request=request_manager)

            body_data = model.get_response_form_data(self._head_parser)

            # pprint("댓글데이터")
            # pprint(body_data)
            response = request_manager.make_json_response(body_data=body_data)
            return response

        # 해시태그로 검색
        @self.__app.get('/feed_explore/search_feed_with_hashtag')
        def search_feed_with_hashtag(request:Request, hashtag:Optional[str], key:Optional[int] = -1):
            request_manager = RequestManager()
            data_payload = HashtagFeedRequest(hashtag=hashtag, key=key)
            request_manager.try_view_management(data_payload=data_payload, cookies=request.cookies)
            #if not request_manager.jwt_payload.result:
                #raise request_manager.credentials_exception

            feed_controller =Feed_Controller(feed_manager=self.__feed_manager)
            model = feed_controller.get_feed_with_hashtag(database=self.__database,
                                                        request=request_manager,
                                                        feed_search_engine=self.__feed_search_engine,
                                                        feed_manager=self.__feed_manager,
                                                        num_feed=5)

            body_data = model.get_response_form_data(self._head_parser)
            response = request_manager.make_json_response(body_data=body_data)
            return response

        # /home/search_feed_with_bid?bid=뭐
        @self.__app.get('/feed_explore/search_feed_with_bid')
        def search_feed_with_bid(request:Request, bid:Optional[str]="", key:Optional[int] = -1):

            request_manager = RequestManager()

            data_payload = GetFeedBidRequest(bid=bid, key=key)

            request_manager.try_view_management(data_payload=data_payload, cookies=request.cookies)
            #if not request_manager.jwt_payload.result:
                #raise request_manager.credentials_exception

            home_controller=Feed_Controller(feed_manager=self.__feed_manager)
            model = home_controller.get_feed_with_bid(database=self.__database,
                                                        request=request_manager,
                                                        feed_search_engine=self.__feed_search_engine,
                                                        num_feed=3)

            body_data = model.get_response_form_data(self._head_parser)
            #pprint(body_data)
            response = request_manager.make_json_response(body_data=body_data)
            return response

        @self.__app.get('/feed_explore/search_feed_with_keyword')
        def search_with_keyword(request:Request, key:Optional[int]=-1, keyword:Optional[str]=""):
            request_manager = RequestManager()

            data_payload = KeywordSearchRequest(key=key, keyword=keyword)
            request_manager.try_view_management(data_payload=data_payload, cookies=request.cookies)

            feed_controller =Feed_Controller(feed_manager=self.__feed_manager)
            model = feed_controller.search_feed_with_keyword(database=self.__database,
                                                             request=request_manager,
                                                             feed_search_engine=self.__feed_search_engine,
                                                             num_feed=6)

            body_data = model.get_response_form_data(self._head_parser)
            response = request_manager.make_json_response(body_data=body_data)

            return response


        # 전체 피드 제공
        @self.__app.post('/feed_explore/all_feed')
        def get_all_feed_filtering(request:Request, raw_request:dict):
            request_manager = RequestManager()
            
            data_payload = AllFeedRequest(request=raw_request)
            request_manager.try_view_management(data_payload=data_payload, cookies=request.cookies)
            #if not request_manager.jwt_payload.result:
                #raise request_manager.credentials_exception

            feed_controller =Feed_Controller(feed_manager=self.__feed_manager)
            model = feed_controller.get_all_feed_filtered(database=self.__database,
                                                request=request_manager,
                                                feed_search_engine=self.__feed_search_engine,
                                                num_feed=3)

            body_data = model.get_response_form_data(self._head_parser)
            response = request_manager.make_json_response(body_data=body_data)
            return response

        # 오늘의 인기 게시글
        @self.__app.get('/feed_explore/today_best')
        def get_today_best_in_search(request:Request, key:Optional[int] = -1):
            request_manager = RequestManager()
            data_payload = HomeFeedRequest(key=key)
            request_manager.try_view_management(data_payload=data_payload, cookies=request.cookies)
            #if not request_manager.jwt_payload.result:
                #raise request_manager.credentials_exception

            feed_controller =Feed_Controller(feed_manager=self.__feed_manager)
            model = feed_controller.get_today_best(database=self.__database,
                                                    request=request_manager,
                                                    feed_search_engine=self.__feed_search_engine,
                                                    num_feed=4)

            body_data = model.get_response_form_data(self._head_parser)
            response = request_manager.make_json_response(body_data=body_data)
            return response

        # 주간 베스트 피드
        @self.__app.get('/feed_explore/weekly_best')
        def get_weekly_best_in_search(request:Request, key:Optional[int] = -1):
            request_manager = RequestManager()
            data_payload = HomeFeedRequest(key=key)
            request_manager.try_view_management(data_payload=data_payload, cookies=request.cookies)
            #if not request_manager.jwt_payload.result:
                #raise request_manager.credentials_exception

            feed_controller =Feed_Controller(feed_manager=self.__feed_manager)
            model = feed_controller.get_weekly_best(database=self.__database,
                                                    request=request_manager,
                                                    feed_search_engine=self.__feed_search_engine,
                                                    num_feed=4)

            body_data = model.get_response_form_data(self._head_parser)
            response = request_manager.make_json_response(body_data=body_data)
            return response
        
        # Bias 기반 커뮤니티 피드
        @self.__app.post('/feed_explore/feed_with_community')
        def get_feed_with_community(request:Request, raw_request:dict):
            request_manager = RequestManager()
            
            # 데이터 페이로드에도 bid 리스트를 넣어야됨
            data_payload = CommunityRequest(request=raw_request)

            data = []
            # pprint(raw_request)
            
            request_manager.try_view_management(data_payload=data_payload, cookies=request.cookies)

            feed_controller =Feed_Controller(feed_manager=self.__feed_manager)
            model = feed_controller.get_feed_in_bias_feed_page(database=self.__database,
                                                    request=request_manager,
                                                    feed_search_engine=self.__feed_search_engine)

            body_data = model.get_response_form_data(self._head_parser)
            response = request_manager.make_json_response(body_data=body_data)
            return response

        # 임시 인터페이스.
        # 필터링 옵션을 통해 글들을 필터링 합니다.
        # 1차 필터링 (위 함수로 동작된 결과)를 끌고오지 않고, 이 함수에서 새롭게 시동합니다.
        # 1차 필터링 (BIAS, 커뮤니티 필터링), 2차 필터링 (옵션 필터링)으로 최종적으로 선별된 Feed를 반환합니다.
        # @self.__app.get('/feed_explore/feed_filtering_with_options')
        # def get_feed_filtering_with_options(request:Request, raw_request:dict):
        #     request_manager = RequestManager()
        #     data_payload = CommunityFilteredRequest(request=raw_request)
        #     request_manager.try_view_management(data_payload=data_payload, cookies=request.cookies)
        #
        #     feed_controller =Feed_Controller(feed_manager=self.__feed_manager)
        #     # get_all_feed와 혼용할 계획
        #     model = feed_controller.get_all_feed(database=self.__database,
        #                                         request=request_manager,
        #                                         feed_search_engine=self.__feed_search_engine)
        #
        #
        #     body_data = model.get_response_form_data(self._head_parser)
        #     response = request_manager.make_json_response(body_data=body_data)
        #     return response

        # 숏피드에서 맨처음에 feed 데이터를 fid로 검색하기
        @self.__app.get('/feed_explore/get_feed')
        def get_feed_data(request:Request, fid:Optional[str]="" ):
            request_manager = RequestManager()
            data_payload = GetFeedRequest(fid=fid)
            request_manager.try_view_management(data_payload=data_payload, cookies=request.cookies)
            #if not request_manager.jwt_payload.result:
                #raise request_manager.credentials_exception

            feed_controller =Feed_Controller(feed_manager=self.__feed_manager)
            model = feed_controller.try_search_in_fid(database=self.__database,
                                                        request=request_manager,
                                                        feed_search_engine=self.__feed_search_engine)

            body_data = model.get_response_form_data(self._head_parser)
            response = request_manager.make_json_response(body_data=body_data)
            return response
        
        # 숏 피드에서 다음 피드를 요청할 때
        @self.__app.post('/feed_explore/get_next_feed')
        def get_next_feed(request:Request, raw_request:dict):
            request_manager = RequestManager()
            data_payload = ShortFeedrecommendRequest(request=raw_request)

            request_manager.try_view_management(data_payload=data_payload, cookies=request.cookies)
            #if not request_manager.jwt_payload.result:
                #raise request_manager.credentials_exception

            feed_controller =Feed_Controller(feed_manager=self.__feed_manager)
            model = feed_controller.get_feed_with_recommend(database=self.__database,
                                                        request=request_manager,
                                                        feed_search_engine=self.__feed_search_engine)

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

            feed_controller =Feed_Controller(feed_manager=self.__feed_manager)
            model = feed_controller.try_interact_feed(database=self.__database,
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

            feed_controller =Feed_Controller(feed_manager=self.__feed_manager)
            model = feed_controller.try_staring_feed(database=self.__database,
                                                        request=request_manager,
                                                        feed_manager=self.__feed_manager)
            
            body_data = model.get_response_form_data(self._head_parser)
            response = request_manager.make_json_response(body_data=body_data)
            return response

        # feed 랑 상호작용 -> 댓글 달기
        @self.__app.post('/feed_explore/make_comment')
        def try_make_comment(request:Request, raw_requset:dict):
            request_manager = RequestManager()
            print(raw_requset)
            data_payload = MakeFeedCommentRequest(request=raw_requset)

            request_manager.try_view_management_need_authorized(data_payload=data_payload, cookies=request.cookies)
            if not request_manager.jwt_payload.result:
                raise request_manager.credentials_exception

            feed_controller =Feed_Controller(feed_manager=self.__feed_manager)
            model = feed_controller.try_make_comment(database=self.__database,
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

            feed_controller =Feed_Controller(feed_manager=self.__feed_manager)
            model = feed_controller.try_remove_comment(database=self.__database,
                                                        request=request_manager,
                                                        feed_manager=self.__feed_manager)
            body_data = model.get_response_form_data(self._head_parser)
            response = request_manager.make_json_response(body_data=body_data)
            return response

        # def try_make_reply_comment(request:Request, raw_requset:dict):
        #     request_manager = RequestManager()
        #     data_payload = MakeFeedCommentRequest(request=raw_requset)
        #
        #     request_manager.try_view_management_need_authorized(data_payload=data_payload, cookies=request.cookies)
        #     if not request_manager.jwt_payload.result:
        #         raise request_manager.credentials_exception
        #
        #     feed_controller =Feed_Controller(feed_manager=self.__feed_manager)
        #     model = feed_controller.try_make_comment(database=self.__database,
        #                                              request=request_manager,
        #                                              feed_manager=self.__feed_manager)
        #     body_data = model.get_response_form_data(self._head_parser)
        #     response = request_manager.make_json_response(body_data=body_data)
        #     return response

        # feed 랑 상호작용 -> 댓글 모두보기
        @self.__app.get('/feed_explore/view_comment')
        def get_all_comment(request:Request, fid:Optional[str]):
            request_manager = RequestManager()

            data_payload = FeedStaringRequest(fid=fid)
            request_manager.try_view_management(data_payload=data_payload, cookies=request.cookies)
            #if not request_manager.jwt_payload.result:
                #raise request_manager.credentials_exception

            feed_controller =Feed_Controller(feed_manager=self.__feed_manager)
            model = feed_controller.get_all_comment_on_feed(database=self.__database,
                                                        request=request_manager)
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

            feed_controller =Feed_Controller(feed_manager=self.__feed_manager)
            model = feed_controller.try_like_comment(database=self.__database,
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
            request_manager = RequestManager()

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
                                                        feed_manager=self.__feed_manager)
            body_data = model.get_response_form_data(self._head_parser)
            response = request_manager.make_json_response(body_data=body_data)
            return response

        @self.__app.get('/feed_explore/try_remove_feed')
        def try_remove_feed(request:Request, fid:Optional[str]):
            request_manager = RequestManager()
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

# Request 아종 같은거라서 이건 재사용 금지
class CommunityRequest(RequestHeader):
    def __init__(self, request) -> None:
        super().__init__(request)
        body = request['body']
        self.bids = np.array(body['bids']).flatten().tolist()
        self.category = body['board']
        self.key:int = body['key']

# class CommunityFilteredRequest(CommunityRequest):
#     def __init__(self, request) -> None:
#         super().__init__(request)
#         body = request['body']
#         self.options = body['options']

class HomeFeedRequest(RequestHeader):
    def __init__(self, key) -> None:
        self.key = key
        
class AllFeedRequest(RequestHeader):
    def __init__(self, request) -> None:
        super().__init__(request)
        body = request['body']
        self.category = body['category']
        self.fclass= body['fclass']
        self.key= body['key']

class KeywordSearchRequest(RequestHeader):
    def __init__(self, key, keyword) -> None:
        self.key = key
        self.keyword = keyword

class HashtagFeedRequest(RequestHeader):
    def __init__(self, hashtag, key=-1) -> None:
        self.hashtag = hashtag 
        self.key = key

class GetFeedBidRequest(RequestHeader):
    def __init__(self, bid, key=-1) -> None:
        self.bid =bid
        self.key=key

class GetFeedRequest(RequestHeader):
    def __init__(self, fid) -> None:
        self.fid= fid

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

class DeleteFeedRequest(RequestHeader):
    def __init__(self,fid) -> None:
        self.fid=fid

class EditFeedRequest(RequestHeader):
    def __init__(self, request, image_names, images) -> None:
        super().__init__(request)
        body = request['body']
        self.fid = body['fid']
        self.body = body['body']
        self.fclass = body['fclass']
        self.choice= body['choice']
        self.hashtag = body['hashtag']
        self.link = body['link']
        self.bid = body['bid']
        self.image_names = image_names
        self.images = images
        
class ShortFeedrecommendRequest(RequestHeader):
    def __init__(self, request) -> None:
        super().__init__(request)
        body = request['body']
        self.fid = body['fid']
        self.history = body['history']

class MakeFeedCommentRequest(RequestHeader):
    def __init__(self, request) -> None:
        super().__init__(request)
        body = request['body']
        self.fid = body['fid']
        self.body = body['body']
        self.target_cid = body['target_cid']

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



