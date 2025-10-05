from typing import Optional, Union
from fastapi import FastAPI, Request, File, UploadFile, Form
from view.jwt_decoder import RequestManager
from view.master_view import Master_View, RequestHeader
from view.parsers import Head_Parser
from controller import Sub_Controller
from others import FeedSearchEngine
from pprint import pprint

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
        self.bias_setting_route()
        self.sub_service()

    def notice_route(self):
        @self.__app.get("/nova_notice/notice_detail")
        def get_notice_detail(nid:Optional[str]):
            sub_controller = Sub_Controller()
            request = NoticeDetailRequest(nid=nid)
            model = sub_controller.get_notice_detail(database=self.__database, request=request)
            response = model.get_response_form_data(self._head_parser)
            return response
        
        # 최신에 사용중인 최애 기반 커뮤니티 리스트에 나올 공지
        @self.__app.get('/nova_sub_system/get_notice_list')
        def get_notice_list():
            data_payload = DummyRequest()
            
            sub_controller =Sub_Controller()
            model = sub_controller.try_get_notice_sample(database=self.__database,
                                                        data_payload=data_payload)
            response = model.get_response_form_data(self._head_parser)
            return response
        
        @self.__app.post('/nova_sub_system/try_add_new_bias')
        def try_add_new_bias(request:Request, raw_reqeust:dict):
            request_manager = RequestManager(secret_key=self.__jwt_secret_key)
            data_payload = AddNewBiasRequest(raw_reqeust)

            request_manager.try_view_management_need_authorized(data_payload=data_payload, cookies=request.cookies)

            sub_controller =Sub_Controller()
            model = sub_controller.try_add_new_bias(
                database=self.__database,
                request=request_manager,
                feed_search_engine=self.__feed_search_engine
                )

            body_data = model.get_response_form_data(self._head_parser)
            response = request_manager.make_json_response(body_data=body_data)
            return response
        

    def bias_setting_route(self):
        # 바이어스를 String 으로 검색
        @self.__app.get('/nova_sub_system/try_search_bias')
        def try_search_bias(request:Request, keyword:Optional[str] = "", category:Optional[str]="모두", len_bias:Optional[int]=0):
            request_manager = RequestManager(secret_key=self.__jwt_secret_key)
            
            data_payload = BiasSearchRequest(keyword=keyword, category=category, len_bias=len_bias)
            
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
        @self.__app.get('/nova_sub_system/try_follow_bias')
        def try_follow_bias(request:Request, bid:Optional[str]):
            request_manager = RequestManager(secret_key=self.__jwt_secret_key)
            data_payload = BiasSelectRequest(bid=bid)
            
            request_manager.try_view_management_need_authorized(data_payload=data_payload, cookies=request.cookies)

            sub_controller=Sub_Controller()
            model = sub_controller.try_follow_bias(database=self.__database,
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
        
        # 단일 바이어스 불러오기
        @self.__app.get('/nova_sub_system/get_single_bias')
        def try_search_bias_with_category(request:Request, bid:Optional[str]):
            request_manager = RequestManager(secret_key=self.__jwt_secret_key)

            data_payload = BiasRequest(bid=bid)
            request_manager.try_view_management(data_payload=data_payload, cookies=request.cookies)

            sub_controller=Sub_Controller()
            model = sub_controller.get_single_bias(database=self.__database,
                                                    request=request_manager)
            
            body_data = model.get_response_form_data(self._head_parser)
            response = request_manager.make_json_response(body_data=body_data)
            return response


    def sub_service(self):
        @self.__app.post('/nova_sub_system/image_tag')
        def get_image_tag(raw_request:dict):
            data_payload = ImageTagRequest(request=raw_request)
            sub_controller =Sub_Controller()

            model = sub_controller.try_get_image_tag(database=self.__database,
                                                data_payload=data_payload)
            response = model.get_response_form_data(self._head_parser)
            return response
        
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



class DummyRequest():
    def __init__(self) -> None:
        pass
        
class BiasRequest():
    def __init__(self, bid) -> None:
        self.bid=bid
        
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
        

class BiasSearchRequest():
    def __init__(self, keyword, category, len_bias) -> None:
        self.keyowrd=keyword
        self.category=category
        self.len_bias=len_bias
        
class AddNewBiasRequest(RequestHeader):
    def __init__(self, request) -> None:
        super().__init__(request)
        body:dict = request['body']
        self.name = body.get("name", "NONE")
        self.platform = body.get("platform", "NONE")
        self.info = body.get("info", "")

class ImageTagRequest(RequestHeader):
    def __init__(self, request) -> None:
        super().__init__(request)
        body = request['body']
        self.url = body['url']

class BiasSelectRequest(RequestHeader):
    def __init__(self, bid) -> None:
        self.bid = bid
        
        
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

