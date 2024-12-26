from typing import Any, Optional
from fastapi import FastAPI, Request
from view.master_view import Master_View, RequestHeader
from view.parsers import Head_Parser
from controller import Funding_Controller
from view.jwt_decoder import RequestManager
from typing import Any, Optional, Union, List
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request, File, UploadFile, Form
import json

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

        # Already Finished
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
            data_payload = ProjectGetRequest()

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

        # 홈에서 추천 태그로 프로젝트 받기, sample, 완성해야함
        @self.__app.get('/nova_fund_system/home/get_project_as_tag')
        def get_home_project_as_tag(request:Request, tag:Optional[str]=""):
            request_manager = RequestManager()
            data_payload = ProjectWithTagRequest(tag=tag)       # 데이터를 받아온 리퀘스트 데이터

            # 쿠키를 통해 데이터를 뜯는 과정
            request_manager.try_view_management(data_payload=data_payload, cookies=request.cookies)
            #if not request_manager.jwt_payload.result:
                #raise request_manager.credentials_exception


            funding_controller =Funding_Controller()
            # 태그를 통해 프로젝트를 찾으러 감.
            # 이 부분은 아직 안 됨. 나중에 다시 들어온다.
            model = funding_controller.get_project_with_tag(
                database=self.__database,
                request=request_manager,
                funding_project_manager=self.__funding_project_manager,
                num_project=3)

            body_data = model.get_response_form_data(self._head_parser)
            response = request_manager.make_json_response(body_data=body_data)
            return response

        # 12월 23일 작업
        # 홈에서 최애 펀딩 프로젝트 받기, FIN
        @self.__app.get('/nova_fund_system/home/get_bias_project')
        def get_home_bias_project(request:Request):
            # 홈에서 최애의 펀딩 프로젝트를 얻어내야한다.
            # 단순히 모든 최애들 프로젝트 중 가장 최신의 것만 얻으면 된다.
            # 그러면, INPUT = X, OUTPUT : 입력받은 최애의 프로젝트 데이터

            request_manager = RequestManager()
            data_payload = ProjectGetRequest()

            # 단순히 최애들의 프로젝트를 띄우고 싶음. 따라서, 로그인 정보는 불필요함
            request_manager.try_view_management(data_payload=data_payload, cookies=request.cookies)
            # if not request_manager.jwt_payload.result:
            #     raise request_manager.credentials_exception

            funding_controller =Funding_Controller()
            # 컨트롤러에 요청하여 받아온다
            model = funding_controller.get_home_bias_project(
                database=self.__database,
                request=request_manager,
                funding_project_manager=self.__funding_project_manager,
                num_project=3)

            # 리스폰스 데이터를 제작한다
            body_data = model.get_response_form_data(self._head_parser)
            # 리퀘스트에 대응하는 리스폰스 제작
            response = request_manager.make_json_response(body_data=body_data)
            return response

        # 12월 23일 작업
        # 홈에서 덕질 펀딩 프로젝트 받기, FIN
        @self.__app.get('/nova_fund_system/home/get_fan_funding')
        def get_home_fan_project(request:Request):
            # 최애의 펀딩시스템과 일맥상통 한다.
            # 그러면 똑같은 방법으로 시동한다.
            request_manager = RequestManager()
            data_payload = ProjectGetRequest()

            request_manager.try_view_management(data_payload=data_payload, cookies=request.cookies)
            #if not request_manager.jwt_payload.result:
                #raise request_manager.credentials_exception

            funding_controller =Funding_Controller()
            model = funding_controller.get_home_fan_project(
                database=self.__database,
                request=request_manager,
                funding_project_manager=self.__funding_project_manager,
                num_project=5)

            body_data = model.get_response_form_data(self._head_parser)
            response = request_manager.make_json_response(body_data=body_data)
            return response

        # 12월 23일 작업
        # FIN
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

        # 이부분은 다른 페이지가 필요하니까 아직
        # 홈화면의 노바 펀딩 알아보기에서 줄것은
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

        # 12월 24일 작업
        # FIN
        # 1. 이미 목표 달성에 성공한 프로젝트
        # 이는 미리보기 형태로, 보여줄 개수가 정해져있다.
        @self.__app.get('/nova_fund_system/fan_project/achieve_the_goal')
        def get_done_project_list(request:Request, key:Optional[str]="" ):
            request_manager = RequestManager()
            data_payload = ProjectGetRequest(key=key)

            request_manager.try_view_management(data_payload=data_payload, cookies=request.cookies)
            #if not request_manager.jwt_payload.result:
                #raise request_manager.credentials_exception

            funding_controller = Funding_Controller()
            model = funding_controller.get_done_project(
                database=self.__database,
                request=request_manager,
                funding_project_manager=self.__funding_project_manager,
                num_project=2,
                ptype="fan"
            )

            body_data = model.get_response_form_data(self._head_parser)
            response = request_manager.make_json_response(body_data=body_data)
            return response

        # 12월 24일 작업
        # FIN
        # 2. 마감 임박 프로젝트
        @self.__app.get('/nova_fund_system/fan_project/soon_expire')
        def get_near_deadline_project_list(request:Request):
            request_manager = RequestManager()
            data_payload = ProjectGetRequest()

            request_manager.try_view_management(data_payload=data_payload, cookies=request.cookies)
            #if not request_manager.jwt_payload.result:
                #raise request_manager.credentials_exception

            funding_controller =Funding_Controller()
            model = funding_controller.get_near_deadline_project(
                database=self.__database,
                request=request_manager,
                funding_project_manager=self.__funding_project_manager,
                num_project=3,
                ptype="fan"
            )

            body_data = model.get_response_form_data(self._head_parser)
            response = request_manager.make_json_response(body_data=body_data)
            return response

        # 3. 추천 프로젝트 -> 최신순
        @self.__app.get('/nova_fund_system/fan_project/recommend_project')
        def get_project_list(request:Request):
            request_manager = RequestManager()
            data_payload = ProjectGetRequest()

            request_manager.try_view_management(data_payload=data_payload, cookies=request.cookies)
            #if not request_manager.jwt_payload.result:
                #raise request_manager.credentials_exception

            funding_controller =Funding_Controller()
            model = funding_controller.get_deadline_sample_project(
                database=self.__database,
                request=request_manager,
                funding_project_manager=self.__funding_project_manager,
                num_project=6)

            body_data = model.get_response_form_data(self._head_parser)
            response = request_manager.make_json_response(body_data=body_data)
            return response

        # 12월 26일 작업
        # FIN, ERROR 있는데 여기와는 무관함. 같은 컨트롤러 함수를 쓰는데 전체보기에서는 문제가 없음
        # 4. 참여 프로젝트
        @self.__app.get('/nova_fund_system/fan_project/funding_project')
        def get_attend_project_list(request:Request):
            request_manager = RequestManager()
            data_payload = ProjectGetRequest()

            request_manager.try_view_management(data_payload=data_payload, cookies=request.cookies)
            #if not request_manager.jwt_payload.result:
                #raise request_manager.credentials_exception

            funding_controller =Funding_Controller()
            model = funding_controller.get_attend_funding_project(
                database=self.__database,
                request=request_manager,
                funding_project_manager=self.__funding_project_manager,
                num_project=6,
                ptype="fan"
            )

            body_data = model.get_response_form_data(self._head_parser)
            response = request_manager.make_json_response(body_data=body_data)
            return response

        # 12월 26일 작업
        # FIN,  ERROR 있는데 여기와는 무관함. 같은 컨트롤러 함수를 쓰는데 전체보기에서는 문제가 없음
        # 5. 모금 프로젝트
        @self.__app.get('/nova_fund_system/fan_project/donation_project')
        def get_donate_project_list(request:Request):
            request_manager = RequestManager()
            data_payload = ProjectGetRequest()

            request_manager.try_view_management(data_payload=data_payload, cookies=request.cookies)
            #if not request_manager.jwt_payload.result:
                #raise request_manager.credentials_exception

            funding_controller =Funding_Controller()
            model = funding_controller.get_donate_funding_project(
                database=self.__database,
                request=request_manager,
                funding_project_manager=self.__funding_project_manager,
                num_project=6,
                ptype="fan"
            )

            body_data = model.get_response_form_data(self._head_parser)
            response = request_manager.make_json_response(body_data=body_data)
            return response

        # ----- 여기는 덕질프로젝트에서 전체보기하면 줄 거 -------------

        # 12월 24일 작업
        # FIN
        # 1. 이미 목표 달성에 성공한 프로젝트
        @self.__app.get('/nova_fund_system/fan_project_list/achieve_the_goal')
        def get_done_project_list_all(request:Request, key:Optional[str]="" ):
            request_manager = RequestManager()
            data_payload = ProjectGetRequest(key=key)

            request_manager.try_view_management(data_payload=data_payload, cookies=request.cookies)
            #if not request_manager.jwt_payload.result:
                #raise request_manager.credentials_exception

            funding_controller =Funding_Controller()
            model = funding_controller.get_done_project(
                database=self.__database,
                request=request_manager,
                funding_project_manager=self.__funding_project_manager,
                num_project=-1,
                ptype="fan"
            )

            body_data = model.get_response_form_data(self._head_parser)
            response = request_manager.make_json_response(body_data=body_data)
            return response

        # 12월 24일 작업
        # FIN
        # 2. 마감 임박 프로젝트
        @self.__app.get('/nova_fund_system/fan_project_list/soon_expire')
        def get_near_deadline_project_list_all(request:Request, key:Optional[str]="" ):
            request_manager = RequestManager()
            data_payload = ProjectGetRequest(key=key)

            request_manager.try_view_management(data_payload=data_payload, cookies=request.cookies)
            #if not request_manager.jwt_payload.result:
                #raise request_manager.credentials_exception

            funding_controller =Funding_Controller()
            model = funding_controller.get_near_deadline_project(
                database=self.__database,
                request=request_manager,
                funding_project_manager=self.__funding_project_manager,
                num_project=-1,
                ptype="fan"
            )


            body_data = model.get_response_form_data(self._head_parser)
            response = request_manager.make_json_response(body_data=body_data)
            return response

        # 3. 추천 프로젝트 -> 최신순
        @self.__app.get('/nova_fund_system/fan_project_list/recommend_project')
        def get_project_list(request:Request, key:Optional[str]="" ):
            request_manager = RequestManager()
            data_payload = ProjectGetRequest(key=key)

            request_manager.try_view_management(data_payload=data_payload, cookies=request.cookies)
            #if not request_manager.jwt_payload.result:
                #raise request_manager.credentials_exception

            funding_controller =Funding_Controller()
            model = funding_controller.get_deadline_sample_project(
                database=self.__database,
                request=request_manager,
                funding_project_manager=self.__funding_project_manager,
                num_project=-1)

            body_data = model.get_response_form_data(self._head_parser)
            response = request_manager.make_json_response(body_data=body_data)
            return response

        # 12월 26일 작업
        # FIN
        # 4. 참여 프로젝트
        @self.__app.get('/nova_fund_system/fan_project_list/funding_project')
        def get_attend_project_list_all(request:Request, key:Optional[str]="" ):
            request_manager = RequestManager()
            data_payload = ProjectGetRequest(key=key)

            request_manager.try_view_management(data_payload=data_payload, cookies=request.cookies)
            #if not request_manager.jwt_payload.result:
                #raise request_manager.credentials_exception

            funding_controller =Funding_Controller()
            model = funding_controller.get_attend_funding_project(
                database=self.__database,
                request=request_manager,
                funding_project_manager=self.__funding_project_manager,
                num_project=-1,
                ptype="fan"
            )

            body_data = model.get_response_form_data(self._head_parser)
            response = request_manager.make_json_response(body_data=body_data)
            return response

        # 12월 26일 작업
        # FIN
        # 5. 모금 프로젝트
        @self.__app.get('/nova_fund_system/fan_project_list/donation_project')
        def get_donate_project_list_all(request:Request, key:Optional[str]="" ):
            request_manager = RequestManager()
            data_payload = ProjectGetRequest(key=key)

            request_manager.try_view_management(data_payload=data_payload, cookies=request.cookies)
            #if not request_manager.jwt_payload.result:
                #raise request_manager.credentials_exception

            funding_controller =Funding_Controller()
            model = funding_controller.get_donate_funding_project(
                database=self.__database,
                request=request_manager,
                funding_project_manager=self.__funding_project_manager,
                num_project=-1,
                ptype="fan"
            )

            body_data = model.get_response_form_data(self._head_parser)
            response = request_manager.make_json_response(body_data=body_data)
            return response

        # Already Finished
        # 프로젝트 디테일 요청,
        @self.__app.get('/nova_fund_system/project_detail')
        def get_project_detail_body(request:Request, pid:Optional[str]="" ):
            request_manager = RequestManager()
            data_payload = ProjectDetailRequest(pid=pid)

            request_manager.try_view_management(data_payload=data_payload, cookies=request.cookies)
            #if not request_manager.jwt_payload.result:
                #raise request_manager.credentials_exception

            funding_controller =Funding_Controller()
            model = funding_controller.get_project_detail(
                database=self.__database,
                request=request_manager,
                funding_project_manager=self.__funding_project_manager)

            body_data = model.get_response_form_data(self._head_parser)
            response = request_manager.make_json_response(body_data=body_data)
            return response

        # 12/26 추가
        # 최애 펀딩 페이지 최상단 - 신규 최애 펀딩
        @self.__app.get('/nova_fund_system/bias_project/new_bias_project')
        def new_bias_project(request:Request, key:Optional[str]="" ):
            request_manager = RequestManager()
            data_payload = DummyRequest()

            request_manager.try_view_management(data_payload=data_payload, cookies=request.cookies)
            #if not request_manager.jwt_payload.result:
                #raise request_manager.credentials_exception

            funding_controller = Funding_Controller()
            model = funding_controller.get_new_bias_project(
                database=self.__database,
                request=request_manager,
                funding_project_manager=self.__funding_project_manager,
                num_project=6)

            body_data = model.get_response_form_data(self._head_parser)
            response = request_manager.make_json_response(body_data=body_data)
            return response

        # 최애 페이지 중단 - 추천하는 프로젝트 (3개)
        # if ftype == "donate" : 달성률 100%이하 and 100%에 근접
        # elif ftype == "attend" : 달성률 100% 초과
        @self.__app.get('/nova_fund_system/bias_project/recommend_project')
        def home_recommend_project(request:Request):
            request_manager = RequestManager()
            data_payload = DummyRequest()

            request_manager.try_view_management(data_payload=data_payload, cookies=request.cookies)
            #if not request_manager.jwt_payload.result:
                #raise request_manager.credentials_exception

            funding_controller = Funding_Controller()
            model = funding_controller.get_recommend_bias_project(
                database=self.__database,
                request=request_manager,
                funding_project_manager=self.__funding_project_manager,
                num_project=3)

            body_data = model.get_response_form_data(self._head_parser)
            response = request_manager.make_json_response(body_data=body_data)
            return response

        # 최애 페이지 하단 - 진행중인 프로젝트(3개)
        # 마감일 순으로, 가장 마감에 임박한 프로젝트 부터 노출
        @self.__app.get('/nova_fund_system/bias_project/all_project')
        def home_all_project(request:Request):
            request_manager = RequestManager()
            data_payload = DummyRequest()

            request_manager.try_view_management(data_payload=data_payload, cookies=request.cookies)
            #if not request_manager.jwt_payload.result:
                #raise request_manager.credentials_exception

            funding_controller = Funding_Controller()
            model = funding_controller.get_all_bias_project(
                database=self.__database,
                request=request_manager,
                funding_project_manager=self.__funding_project_manager,
                num_project=3)

            body_data = model.get_response_form_data(self._head_parser)
            response = request_manager.make_json_response(body_data=body_data)
            return response

        # 최애 프로젝트 리스트 페이지- 추천하는 프로젝트( 요청당 6개)
        # if ftype == "donate" : 달성률 100%이하 and 100%에 근접
        # elif ftype == "attend" : 달성률 100% 초과
        @self.__app.get('/nova_fund_system/bias_project_list/recommend_project')
        def recommend_project_list(request:Request, key:Optional[str]=""):
            request_manager = RequestManager()
            data_payload = ProjectGetRequest(key=key)

            request_manager.try_view_management(data_payload=data_payload, cookies=request.cookies)
            #if not request_manager.jwt_payload.result:
                #raise request_manager.credentials_exception

            funding_controller = Funding_Controller()
            model = funding_controller.get_recommend_bias_project(
                database=self.__database,
                request=request_manager,
                funding_project_manager=self.__funding_project_manager,
                num_project=6)

            body_data = model.get_response_form_data(self._head_parser)
            response = request_manager.make_json_response(body_data=body_data)
            return response

        # 최애 프로젝트 리스트 페이지- 진행중인 프로젝트( 요청당 6개)
        # 마감일 순으로, 가장 마감에 임박한 프로젝트 부터 노출
        @self.__app.get('/nova_fund_system/bias_project_list/all_project')
        def all_project_list(request:Request, key:Optional[str]=""):
            request_manager = RequestManager()
            data_payload = ProjectGetRequest(key=key)

            request_manager.try_view_management(data_payload=data_payload, cookies=request.cookies)
            #if not request_manager.jwt_payload.result:
                #raise request_manager.credentials_exception

            funding_controller = Funding_Controller()
            model = funding_controller.get_all_bias_project(
                database=self.__database,
                request=request_manager,
                funding_project_manager=self.__funding_project_manager,
                num_project=6)

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
            data_payload = DummyRequest(request=raw_request)

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
            
        
        # 새로운 프로젝트 만들기
        @self.__app.post('/nova_fund_system/try_make_new_project')
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

            data_payload = ProjectEditRequest(request=raw_request,
                                            image_names=image_names,
                                            images=imgs)

            request_manager.try_view_management_need_authorized(data_payload=data_payload, cookies=request.cookies)
            if not request_manager.jwt_payload.result:
                raise request_manager.credentials_exception

            funding_controller = Funding_Controller()
            model = funding_controller.try_make_new_project(
                database=self.__database,
                request=request_manager,
                funding_project_manager=self.__funding_project_manager)

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

class ProjectEditRequest():
    def __init__(self, request, image_names, images):
        super().__init__(request)
        body = request['body']
        self.email = body['email']
        self.password= body['password']
        self.age = body['age']
        self.gender = body['gender']
        self.images =images
        self.image_names = image_names

class ProjectGetRequest():
    def __init__(self, key=-1) -> None:
        self.key=key

class ProjectDetailRequest():
    def __init__(self, pid) -> None:
        self.pid=pid

class ProjectWithTagRequest():
    def __init__(self, tag="") -> None:
        self.tag=tag

class ProjectWithBiasRequest():
    def __init__(self, bias="") -> None:
        self.bias=bias