from typing import Any, Optional
from fastapi import FastAPI, Request
from view.master_view import Master_View, RequestHeader
from view.parsers import Head_Parser
from controller import Funding_Controller
from view.jwt_decoder import RequestManager

class Funding_Service_View(Master_View):
    def __init__(self, app:FastAPI, endpoint:str, database, head_parser:Head_Parser,
                 funding_project_manager) -> None:
        super().__init__(head_parser=head_parser)
        self.__app = app
        self._endpoint = endpoint
        self.__database = database
        self.__funding_project_manager = funding_project_manager
        self.get_route(endpoint)
        self.post_route(endpoint)

    def get_route(self, endpoint:str):
        @self.__app.get(endpoint+'/nova_fund')
        def home():
            return 'Hello, This is Funding system'

        # 홈에서 추천 태그로 프로젝트 받기
        @self.__app.get('/nova_fund_system/sample')
        def test_code():
            funding_controller =Funding_Controller()
            model = funding_controller.try_test_func(
                database=self.__database,
                funding_project_manager=self.__funding_project_manager,
                num_project=3)

            body_data = model.get_response_form_data(self._head_parser)
            return body_data
        
        # 홈에서 프로젝트 배너들 받기
        @self.__app.get('/nova_fund_system/home/banner')
        def get_home_banner(request:Request):
            request_manager = RequestManager()
            data_payload = DummyRequest()

            request_manager.try_view_management(data_payload=data_payload, cookies=request.cookies)
            #if not request_manager.jwt_payload.result:
                #raise request_manager.credentials_exception

            funding_controller =Funding_Controller()
            model = funding_controller.get_home_banner(
                database=self.__database,
                request=request_manager,
                funding_project_manager=self.__funding_project_manager)

            body_data = model.get_response_form_data(self._head_parser)
            response = request_manager.make_json_response(body_data=body_data)
            return response

        # 홈에서 추천 tag 받기
        @self.__app.get('/nova_fund_system/home/get_recommend_tag')
        def get_home_recommend_tag(request:Request):
            request_manager = RequestManager()
            data_payload = ProjectGetRequset()

            request_manager.try_view_management(data_payload=data_payload, cookies=request.cookies)
            #if not request_manager.jwt_payload.result:
                #raise request_manager.credentials_exception

            funding_controller =Funding_Controller()
            model = funding_controller.get_recommend_tag(
                database=self.__database,
                request=request_manager,
                funding_project_manager=self.__funding_project_manager,
                num_project=3)

            body_data = model.get_response_form_data(self._head_parser)
            response = request_manager.make_json_response(body_data=body_data)
            return response

        # 홈에서 추천 태그로 프로젝트 받기
        @self.__app.get('/nova_fund_system/home/get_project_as_tag')
        def get_home_project_as_tag(request:Request, tag:Optional[str]=""):
            request_manager = RequestManager()
            data_payload = ProjectGetRequset()

            request_manager.try_view_management(data_payload=data_payload, cookies=request.cookies)
            #if not request_manager.jwt_payload.result:
                #raise request_manager.credentials_exception

            funding_controller =Funding_Controller()
            model = funding_controller.get_sample_project(
                database=self.__database,
                request=request_manager,
                funding_project_manager=self.__funding_project_manager,
                num_project=3)

            body_data = model.get_response_form_data(self._head_parser)
            response = request_manager.make_json_response(body_data=body_data)
            return response

        # 홈에서 최애 펀딩 프로젝트 받기
        @self.__app.get('/nova_fund_system/home/get_bias_project')
        def get_home_bias_project(request:Request):
            request_manager = RequestManager()
            data_payload = ProjectGetRequset()

            request_manager.try_view_management(data_payload=data_payload, cookies=request.cookies)
            #if not request_manager.jwt_payload.result:
                #raise request_manager.credentials_exception

            funding_controller =Funding_Controller()
            model = funding_controller.get_sample_project(
                database=self.__database,
                request=request_manager,
                funding_project_manager=self.__funding_project_manager,
                num_project=3)

            body_data = model.get_response_form_data(self._head_parser)
            response = request_manager.make_json_response(body_data=body_data)
            return response

        # 홈에서 덕질 펀딩 프로젝트 받기
        @self.__app.get('/nova_fund_system/home/get_fan_funding')
        def get_home_fan_funding(request:Request):
            request_manager = RequestManager()
            data_payload = ProjectGetRequset()

            request_manager.try_view_management(data_payload=data_payload, cookies=request.cookies)
            #if not request_manager.jwt_payload.result:
                #raise request_manager.credentials_exception

            funding_controller =Funding_Controller()
            model = funding_controller.get_sample_project(
                database=self.__database,
                request=request_manager,
                funding_project_manager=self.__funding_project_manager,
                num_project=5)

            body_data = model.get_response_form_data(self._head_parser)
            response = request_manager.make_json_response(body_data=body_data)
            return response

        # 베스트 프로젝트 모두 보기에서 필요한 데이터
        # 다른건 없고 [프로젝트 성공 사례의 횟수] 이걸 주면되는듯
        @self.__app.get('/nova_fund_system/home/best_funding_section')
        def get_home_best_funding_section():
            funding_controller =Funding_Controller()
            model = funding_controller.get_best_funding_section(
                database=self.__database,
                funding_project_manager=self.__funding_project_manager
                )
            body_data = model.get_response_form_data(self._head_parser)
            return body_data

        # 홈화면의 노바 펀딩 알아보기에서 줄것
        # 1. 최애 펀딩 알아보기 조회수
        # 2. 일반 펀딩 알아보기 조회수
        # 3. 성공하는 펀딩 기술 조회수
        @self.__app.get('/nova_fund_system/home/get_nova_funding_info')
        def get_home_nova_funding_info():
            funding_controller =Funding_Controller()
            model = funding_controller.get_nova_funding_info(
                database=self.__database,
                funding_project_manager=self.__funding_project_manager
                )
            body_data = model.get_response_form_data(self._head_parser)
            return body_data

        #------------------------ 프로젝트 덕질 프로젝트 페이지에서 요청 ----------------------------

        # 1. 이미 목표 달성에 성공한 프로젝트
        @self.__app.get('/nova_fund_system/fan_project/achieve_the_goal')
        def get_project_list(request:Request, key:Optional[str]="" ):
            request_manager = RequestManager()
            data_payload = ProjectGetRequset(key=key)

            request_manager.try_view_management(data_payload=data_payload, cookies=request.cookies)
            #if not request_manager.jwt_payload.result:
                #raise request_manager.credentials_exception

            funding_controller =Funding_Controller()
            model = funding_controller.get_sample_project(
                database=self.__database,
                request=request_manager,
                funding_project_manager=self.__funding_project_manager,
                num_project=3)

            body_data = model.get_response_form_data(self._head_parser)
            response = request_manager.make_json_response(body_data=body_data)
            return response
        
        # 2. 마감 임박 프로젝트
        @self.__app.get('/nova_fund_system/fan_project/soon_expire')
        def get_project_list(request:Request):
            request_manager = RequestManager()
            data_payload = ProjectGetRequset()

            request_manager.try_view_management(data_payload=data_payload, cookies=request.cookies)
            #if not request_manager.jwt_payload.result:
                #raise request_manager.credentials_exception

            funding_controller =Funding_Controller()
            model = funding_controller.get_sample_project(
                database=self.__database,
                request=request_manager,
                funding_project_manager=self.__funding_project_manager,
                num_project=3)

            body_data = model.get_response_form_data(self._head_parser)
            response = request_manager.make_json_response(body_data=body_data)
            return response

        # 3. 추천 프로젝트 -> 최신순
        @self.__app.get('/nova_fund_system/fan_project/recommend_project')
        def get_project_list(request:Request):
            request_manager = RequestManager()
            data_payload = ProjectGetRequset()

            request_manager.try_view_management(data_payload=data_payload, cookies=request.cookies)
            #if not request_manager.jwt_payload.result:
                #raise request_manager.credentials_exception

            funding_controller =Funding_Controller()
            model = funding_controller.get_sample_project(
                database=self.__database,
                request=request_manager,
                funding_project_manager=self.__funding_project_manager,
                num_project=6)

            body_data = model.get_response_form_data(self._head_parser)
            response = request_manager.make_json_response(body_data=body_data)
            return response

        # 4. 참여 프로젝트
        @self.__app.get('/nova_fund_system/fan_project/funding_project')
        def get_project_list(request:Request):
            request_manager = RequestManager()
            data_payload = ProjectGetRequset()

            request_manager.try_view_management(data_payload=data_payload, cookies=request.cookies)
            #if not request_manager.jwt_payload.result:
                #raise request_manager.credentials_exception

            funding_controller =Funding_Controller()
            model = funding_controller.get_sample_project(
                database=self.__database,
                request=request_manager,
                funding_project_manager=self.__funding_project_manager,
                num_project=6)

            body_data = model.get_response_form_data(self._head_parser)
            response = request_manager.make_json_response(body_data=body_data)
            return response

        # 5. 모금 프로젝트
        @self.__app.get('/nova_fund_system/fan_project/donation_project')
        def get_project_list(request:Request):
            request_manager = RequestManager()
            data_payload = ProjectGetRequset()

            request_manager.try_view_management(data_payload=data_payload, cookies=request.cookies)
            #if not request_manager.jwt_payload.result:
                #raise request_manager.credentials_exception

            funding_controller =Funding_Controller()
            model = funding_controller.get_sample_project(
                database=self.__database,
                request=request_manager,
                funding_project_manager=self.__funding_project_manager,
                num_project=6)

            body_data = model.get_response_form_data(self._head_parser)
            response = request_manager.make_json_response(body_data=body_data)
            return response

        # ----- 여기는 덕질프로젝트에서 전쳅보기하면 줄 거 -------------

        # 1. 이미 목표 달성에 성공한 프로젝트
        @self.__app.get('/nova_fund_system/fan_project_list/achieve_the_goal')
        def get_project_list(request:Request, key:Optional[str]="" ):
            request_manager = RequestManager()
            data_payload = ProjectGetRequset(key=key)

            request_manager.try_view_management(data_payload=data_payload, cookies=request.cookies)
            #if not request_manager.jwt_payload.result:
                #raise request_manager.credentials_exception

            funding_controller =Funding_Controller()
            model = funding_controller.get_sample_project(
                database=self.__database,
                request=request_manager,
                funding_project_manager=self.__funding_project_manager,
                num_project=10)

            body_data = model.get_response_form_data(self._head_parser)
            response = request_manager.make_json_response(body_data=body_data)
            return response
        
        # 2. 마감 임박 프로젝트
        @self.__app.get('/nova_fund_system/fan_project_list/soon_expire')
        def get_project_list(request:Request, key:Optional[str]="" ):
            request_manager = RequestManager()
            data_payload = ProjectGetRequset(key=key)

            request_manager.try_view_management(data_payload=data_payload, cookies=request.cookies)
            #if not request_manager.jwt_payload.result:
                #raise request_manager.credentials_exception

            funding_controller =Funding_Controller()
            model = funding_controller.get_sample_project(
                database=self.__database,
                request=request_manager,
                funding_project_manager=self.__funding_project_manager,
                num_project=10)

            body_data = model.get_response_form_data(self._head_parser)
            response = request_manager.make_json_response(body_data=body_data)
            return response

        # 3. 추천 프로젝트 -> 최신순
        @self.__app.get('/nova_fund_system/fan_project_list/recommend_project')
        def get_project_list(request:Request, key:Optional[str]="" ):
            request_manager = RequestManager()
            data_payload = ProjectGetRequset(key=key)

            request_manager.try_view_management(data_payload=data_payload, cookies=request.cookies)
            #if not request_manager.jwt_payload.result:
                #raise request_manager.credentials_exception

            funding_controller =Funding_Controller()
            model = funding_controller.get_sample_project(
                database=self.__database,
                request=request_manager,
                funding_project_manager=self.__funding_project_manager,
                num_project=10)

            body_data = model.get_response_form_data(self._head_parser)
            response = request_manager.make_json_response(body_data=body_data)
            return response

        # 4. 참여 프로젝트
        @self.__app.get('/nova_fund_system/fan_project_list/funding_project')
        def get_project_list(request:Request, key:Optional[str]="" ):
            request_manager = RequestManager()
            data_payload = ProjectGetRequset(key=key)

            request_manager.try_view_management(data_payload=data_payload, cookies=request.cookies)
            #if not request_manager.jwt_payload.result:
                #raise request_manager.credentials_exception

            funding_controller =Funding_Controller()
            model = funding_controller.get_sample_project(
                database=self.__database,
                request=request_manager,
                funding_project_manager=self.__funding_project_manager,
                num_project=10)

            body_data = model.get_response_form_data(self._head_parser)
            response = request_manager.make_json_response(body_data=body_data)
            return response

        # 5. 모금 프로젝트
        @self.__app.get('/nova_fund_system/fan_project_list/donation_project')
        def get_project_list(request:Request, key:Optional[str]="" ):
            request_manager = RequestManager()
            data_payload = ProjectGetRequset(key=key)

            request_manager.try_view_management(data_payload=data_payload, cookies=request.cookies)
            #if not request_manager.jwt_payload.result:
                #raise request_manager.credentials_exception

            funding_controller =Funding_Controller()
            model = funding_controller.get_sample_project(
                database=self.__database,
                request=request_manager,
                funding_project_manager=self.__funding_project_manager,
                num_project=10)

            body_data = model.get_response_form_data(self._head_parser)
            response = request_manager.make_json_response(body_data=body_data)
            return response

        
    def post_route(self, endpoint:str):
        # 새로운 프로젝트를 요청할 때 넣는 요청
        # 작성한 글을 받는 부분이 따로 있어야될것같음
        # 아마도 page에 따라서 post가 따로 있을 예정
        @self.__app.post('/nova_fund_system/make_new_project')
        def try_make_new_project(request:Request, raw_request:dict):
            request_manager = RequestManager()
            data_payload = MakeNewProjectRequest(request=raw_request)

            request_manager.try_view_management(data_payload=data_payload, cookies=request.cookies)
            #if not request_manager.jwt_payload.result:
                #raise request_manager.credentials_exception

            feed_controller=()
            model = feed_controller.get_feed_with_recommend(database=self.__database,
                                                        request=request_manager,
                                                        feed_search_engine=self.__feed_search_engine)

            body_data = model.get_response_form_data(self._head_parser)
            response = request_manager.make_json_response(body_data=body_data)
            return response
            

class MakeNewProjectRequest(RequestHeader):
    def __init__(self, request) -> None:
        super().__init__(request)
        body = request['body']
        self.email = body['email']
        self.password= body['password']
        self.verification_code = int(body['verification_code'])
        self.age = body['age']
        self.gender = body['gender']


class MyFeedRequest():
    def __init__(self, fid) -> None:
        self.fid= fid


class DummyRequest():
    def __init__(self) -> None:
        pass

class ProjectGetRequset():
    def __init__(self, key=-1) -> None:
        self.key=key

