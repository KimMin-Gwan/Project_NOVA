from datetime import datetime
from typing import Any, Optional, Union
from fastapi import FastAPI, Request, File, UploadFile, Form
from view.jwt_decoder import RequestManager
from view.master_view import Master_View, RequestHeader
from view.parsers import Head_Parser
from controller import Sub_Controller
from fastapi.responses import HTMLResponse
from others import FeedSearchEngine
from others.data_domain import Feed, User
from pprint import pprint

import os

import json

class Sub_Service_View(Master_View):
    def __init__(self, app:FastAPI, endpoint:str, database, head_parser:Head_Parser,
                 feed_search_engine:FeedSearchEngine, jwt_secret_key) -> None:
        super().__init__(head_parser=head_parser)
        self.__app = app
        self._endpoint = endpoint
        self.__database = database
        self.__feed_search_engine=feed_search_engine
        self.__jwt_secret_key = jwt_secret_key
        self.notice_route()
        #self.bias_page_route("/bias_info")
        self.test_route()
        self.bias_setting_route()
        self.sub_service()

        # feed algorithm test
        self.user_add_test()
        self.user_remove_test()
        self.feed_add_test()
        self.feed_remove_test()
        self.like_feed_test()
        self.dislike_feed_test()

    def test_route(self):
        @self.__app.get("/testing/try_get_feed")
        def try_get_feed():

            result = "default"
            result_index = "index"

            # 여기다가 조건을 작성

            target_type = "uname"
            target = "버튜버"
            num_feed= 10
            index = 240
            fid = 10

            # 여기서 만든 함수 실행
            #result , result_index = self.__feed_search_engine.try_get_feed_in_recent(target_type=target_type, target = target, num_feed=num_feed, index=index)
            #result , result_index = self.__feed_search_engine.try_get_feed_in_recent(search_type ="today", num_feed= 6, index=-2)
            
            result = self.__feed_search_engine.try_test_graph_recommend_system(
                fid=fid)
               


            feed_data = self.__database.get_datas_with_ids(target_id="fid", ids=result)

            pprint(feed_data)

            return True
        
    def user_add_test(self):
        @self.__app.get("/testing/try_add_user")
        def try_add_user(user_data_url:str):
            with open(user_data_url, 'r', encoding='utf-8') as f:
                user_data = json.load(f)

            user_list = []
            for user in user_data:
                test_user = User()
                test_user.make_with_dict(dict_data=user)
                user_list.append(test_user)

            self.__feed_search_engine.try_graph_call()

            for single_user in user_list:
                result = self.__feed_search_engine.try_add_user(single_user)
                if result:
                    print(f"'{single_user.uid}' successfully added")
                else:
                    print(f"'{single_user.uid}' is already exist")
            self.__feed_search_engine.try_graph_call()
            return True

    def user_remove_test(self):
        @self.__app.get("/testing/try_remove_user")
        def try_remove_user(target_uid:str):
            if self.__feed_search_engine.try_remove_user(target_uid):
                print(f'{target_uid} successfully removed')
            else:
                print(f'{target_uid} is not exist')

            self.__feed_search_engine.try_graph_call()
            return True

    def feed_add_test(self):
        @self.__app.get("/testing/try_add_feed")
        def try_add_feed(feed_data_url:str):
            with open(feed_data_url, 'r', encoding='utf-8') as f:
                feed_data = json.load(f)

            feed_list = []
            for feed in feed_data:
                test_feed = Feed()
                test_feed.make_with_dict(dict_data=feed)
                feed_list.append(test_feed)

            self.__feed_search_engine.try_graph_call()

            for single_feed in feed_list:
                result = self.__feed_search_engine.try_add_feed(single_feed)
                if result == "case success":
                    print(f'{single_feed.fid} successfully added')
                elif result == "case1":
                    print(f'{single_feed.fid} is already exist')
                elif result == "case2":
                    print(f'{single_feed.fid} successfully add, but user does not exist')

            self.__feed_search_engine.try_graph_call()
            return True

    def feed_remove_test(self):
        @self.__app.get("/testing/try_remove_feed")
        def try_remove_feed(target_fid:str):
            if self.__feed_search_engine.try_remove_feed(target_fid):
                print(f'{target_fid} successfully removed')
            else:
                print(f'{target_fid} is not exist')

            self.__feed_search_engine.try_graph_call()
            return True

    def like_feed_test(self):
        @self.__app.get("/testing/try_like_feed")
        def try_like_feed(fid:str, uid:str):
            like_time_str = datetime.now().strftime("%Y/%m/%d-%H:%M:%S")
            like_time = datetime.strptime(like_time_str, '%Y/%m/%d-%H:%M:%S')

            if self.__feed_search_engine.try_like_feed(fid, uid, like_time):
                print(f'{fid} - {uid} like successfully connected')
            else:
                print(f'{fid} - {uid} like not connect')

            return True

    def dislike_feed_test(self):
        @self.__app.get("/testing/try_dislike_feed")
        def try_dislike_feed(fid:str, uid:str):
            if self.__feed_search_engine.try_dislike_feed(fid, uid):
                print(f'{fid} - {uid} like successfully disconnected')
            else:
                print(f'{fid} - {uid} like not connected')

            return True

    def recommend_feed_test(self):
        @self.__app.get("/testing/try_recommend_feed")
        def try_recommend_feed(fid:str, test_user:User, history:list):
            recommended_fid = self.__feed_search_engine.try_recommend_feed(fid, history, test_user)
            if recommended_fid:
                print(f'successfully recommend, fid = {recommended_fid}')
            else:
                print(f"feed doesn't recommend..")

            return True


    def notice_route(self):
        @self.__app.get("/nova_notice/notice_list")
        def get_notice_list():
            sub_controller = Sub_Controller()
            model = sub_controller.get_notice_list(database=self.__database)
            response = model.get_response_form_data(self._head_parser)
            return response

        @self.__app.get("/nova_notice/notice_detail")
        def get_notice_detail(nid:Optional[str]):
            sub_controller = Sub_Controller()
            request = NoticeDetailRequest(nid=nid)
            model = sub_controller.get_notice_detail(database=self.__database, request=request)
            response = model.get_response_form_data(self._head_parser)
            return response

        @self.__app.post('/nova_sub_system/image_tag')
        def get_image_tag(raw_request:dict):
            data_payload = ImageTagRequest(request=raw_request)
            sub_controller =Sub_Controller()

            model = sub_controller.try_get_image_tag(database=self.__database,
                                                data_payload=data_payload)
            response = model.get_response_form_data(self._head_parser)
            return response
        
        # 최신에 사용중인 최애 기반 커뮤니티 리스트에 나올 공지
        @self.__app.get('/nova_sub_system/sample_notice')
        def try_get_sample_notice():
            data_payload = DummyRequest()
            
            sub_controller =Sub_Controller()
            model = sub_controller.try_get_notice_sample(database=self.__database,
                                                        data_payload=data_payload)
            response = model.get_response_form_data(self._head_parser)
            return response
        

    def bias_setting_route(self):
        # 바이어스를 String 으로 검색
        @self.__app.get('/nova_sub_system/try_search_bias')
        def try_search_bias(request:Request, bname:Optional[str] = -1):
            request_manager = RequestManager(secret_key=self.__jwt_secret_key)
            
            data_payload = BiasSearchRequest(bname=bname)
            
            request_manager.try_view_management(data_payload=data_payload, cookies=request.cookies)
            #if not request_manager.jwt_payload.result:
                #raise request_manager.credentials_exception

            sub_controller=Sub_Controller()
            model = sub_controller.try_search_bias(database=self.__database,
                                                request=request_manager,
                                                feed_search_engine=self.__feed_search_engine
                                                )

            body_data = model.get_response_form_data(self._head_parser)
            response = request_manager.make_json_response(body_data=body_data)
            return response        
        
        # 바이어스 선택 또는 취소
        @self.__app.post('/nova_sub_system/try_select_my_bias')
        def try_select_my_bias(request:Request, raw_request:dict):
            request_manager = RequestManager(secret_key=self.__jwt_secret_key)
            data_payload = BiasSelectRequest(request=raw_request)
            
            request_manager.try_view_management_need_authorized(data_payload=data_payload, cookies=request.cookies)

            sub_controller=Sub_Controller()
            model = sub_controller.try_select_bias(database=self.__database,
                                                 request=request_manager,
                                                 feed_search_engine=self.__feed_search_engine)
            body_data = model.get_response_form_data(self._head_parser)
            response = request_manager.make_json_response(body_data=body_data)
            return response

        # Bias Follow 페이지에 노출될 Bias를 분류에 따라 노출
        @self.__app.get('/nova_sub_system/get_bias_follow_page_data')
        def try_get_bias_follow_page_data():
            sub_controller=Sub_Controller()
            model = sub_controller.try_get_bias_follow_page(database=self.__database)
            body_data = model.get_response_form_data(self._head_parser)
            return body_data
        
        # 바이어스를 카테고리로 검색
        @self.__app.get('/nova_sub_system/try_search_bias_with_category')
        def try_search_bias_with_category(request:Request, category:Optional[str]):
            request_manager = RequestManager(secret_key=self.__jwt_secret_key)

            data_payload = BiasWithCategoryRequest(category=category)
            request_manager.try_view_management(data_payload=data_payload, cookies=request.cookies)

            sub_controller=Sub_Controller()
            model = sub_controller.try_search_bias_with_category(database=self.__database,
                                                                request=request_manager)
            
            body_data = model.get_response_form_data(self._head_parser)
            response = request_manager.make_json_response(body_data=body_data)
            return response

        # 임시 URL주소. 바꾸면 됨
        # 사이드박스에서 각 BIAS별 설정된 Board_type(게시판들)과, BIAS의 플랫폼, 인스타 등 주소를 보내야 함.
        # 펀딩부분은 뭐.. 프론트에서 URL로 이어주겠죠?
        @self.__app.get('/nova_sub_system/try_get_community_side_box')
        def try_get_community_side_box(bid:Optional[str] = ""):
            data_payload = CommunitySideBoxRequest(bid=bid)

            sub_controller=Sub_Controller()
            model = sub_controller.try_get_community_side_box(database=self.__database,
                                                              data_payload=data_payload)
            body_data = model.get_response_form_data(self._head_parser)
            return body_data

    def sub_service(self):
        # 신고 기능
        @self.__app.post('/nova_sub_system/try_report')
        def try_report_post_or_comment(request:Request, raw_request:dict):
            request_manager = RequestManager(secret_key=self.__jwt_secret_key)
            
            data_payload = ReportRequest(request=raw_request)
            
            request_manager.try_view_management(data_payload=data_payload, cookies=request.cookies)

            sub_controller=Sub_Controller()
            model = sub_controller.try_report_post_or_comment(database=self.__database,
                                                              request=request_manager)
            body_data = model.get_response_form_data(self._head_parser)
            response = request_manager.make_json_response(body_data=body_data)
            return response
        
        # 신고 기능
        @self.__app.post('/nova_sub_system/try_report_bug')
        async def try_report_bug(request:Request, images: Union[UploadFile, None] = File(None),
                                       jsonData: Union[str, None] = Form(None)):
     
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
        
            request_manager = RequestManager(secret_key=self.__jwt_secret_key)
            
            data_payload = ReportRequest(request=raw_request,
                                         images=imgs,
                                         image_names=image_names)
            
            request_manager.try_view_management(data_payload=data_payload, cookies=request.cookies)

            sub_controller=Sub_Controller()
            model = sub_controller.try_report_bug(database=self.__database,
                                                              request=request_manager)
            
            body_data = model.get_response_form_data(self._head_parser)
            response = request_manager.make_json_response(body_data=body_data)
            return response

        # 나이변경 기능
        @self.__app.post('/nova_sub_system/try_change_users_age')
        def try_change_users_age(request:Request):
            request_manager = RequestManager(secret_key=self.__jwt_secret_key)
            request_manager.try_view_management(cookies=request.cookies)

            sub_controller=Sub_Controller()
            model = sub_controller.try_change_users_age(database=self.__database,
                                                        request=request_manager)
            body_data = model.get_response_form_data(self._head_parser)
            response = request_manager.make_json_response(body_data=body_data)
            return response

    #def bias_page_route(self, endpoint:str):
        #@self.__app.get(endpoint+'/home')
        #def home():
            #return 'Hello, This is Root of Core-System Service'
        
        ## 최애 페이지에 배너 정보
        #@self.__app.get(endpoint + '/banner')
        #def get_bias_banner(bias_id:Optional[str] = "solo"):
            #home_controller=Sub_Controller()
            #model = home_controller.get_bias_banner(database=self.__database,)
            #response = model.get_response_form_data(self._head_parser)
            #return response

        ## 최애 페이지에 지지자 순위 정보
        #@self.__app.get(endpoint + '/bias_n_league')
        #def get_bias_n_legue(bias_id:Optional[str] = ""):
            #request = BiasPageInfoRequest(bid=bias_id)
            #sub_controller =Sub_Controller()
            #model = sub_controller.get_bias_n_league_data(database=self.__database,
                                                          #request=request)
            #response = model.get_response_form_data(self._head_parser)
            #return response
        
        ## 최애 페이지에 지지자 순위 정보
        #@self.__app.get(endpoint + '/user_contribution')
        #def get_user_contribution(bias_id:Optional[str] = ""):
            #request = BiasPageInfoRequest(bid=bias_id)
            #sub_controller =Sub_Controller()
            #model = sub_controller.get_user_contribution(database=self.__database,
                                                          #request=request)
            #response = model.get_response_form_data(self._head_parser)
            #return response

        ## 최애 페이지에 지지자의 본인 기여도 정보
        #@self.__app.post(endpoint + '/my_contribution')
        #def get_my_contribution(raw_request:dict):
            #request = MyContributionRequest(request=raw_request)
            #sub_controller=Sub_Controller()
            #model = sub_controller.get_my_contribution(database=self.__database,
                                                          #request=request)
            #response = model.get_response_form_data(self._head_parser)
            #return response

class DummyRequest():
    def __init__(self) -> None:
        pass
        
class BiasWithCategoryRequest():
    def __init__(self, category) -> None:
        self.category=category
        
class NoticeDetailRequest():
    def __init__(self, nid = None) -> None:
        self.nid=nid
        
class NoticeSampleRequest():
    def __init__(self, bid="", last_nid="") -> None:
        self.bid=bid
        self.last_nid=last_nid
        
class BiasPageInfoRequest():
    def __init__(self, bid = None) -> None:
        self.bid=bid  

class BiasSearchRequest():
    def __init__(self, bname) -> None:
        self.bname=bname

class MyContributionRequest(RequestHeader):
    def __init__(self, request) -> None:
        super().__init__(request)
        body = request['body']
        self.token = body['token']
        self.bid = body['bid']

class ImageTagRequest(RequestHeader):
    def __init__(self, request) -> None:
        super().__init__(request)
        body = request['body']
        self.url = body['url']

class BiasSelectRequest(RequestHeader):
    def __init__(self, request) -> None:
        super().__init__(request)
        body = request['body']
        self.bid = body['bid']
        
class ReportRequest(RequestHeader):
    def __init__(self, request, image_names=[], images=[]) -> None:
        super().__init__(request)
        body:dict = request['body']
        self.type = body.get("type", "")
        self.detail = body.get("detail", "")
        self.cid = body.get("cid", "")
        self.fid = body.get("fid", "")
        self.image_names = image_names
        self.images = images

class CommunitySideBoxRequest(RequestHeader):
    def __init__(self, bid) -> None:
        self.bid=bid
