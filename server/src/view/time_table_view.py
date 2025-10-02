from typing import Optional, Union
from fastapi import FastAPI, Request, File, UploadFile, Form
from others import Schedule
from view.master_view import Master_View, RequestHeader
from view.parsers import Head_Parser
from view.jwt_decoder import RequestManager
from controller import TimeTableController
#from websockets.exceptions import ConnectionClosedError
from pprint import pprint
from datetime import datetime
from pydantic import BaseModel, Field
import pytz
import json

from others import ScheduleSearchEngine as SSE


class Time_Table_View(Master_View):
    def __init__(self, app:FastAPI, endpoint:str,
                  database, head_parser:Head_Parser,
                  schedule_search_engine:SSE,
                  jwt_secret_key
                  ) -> None:
        super().__init__(head_parser=head_parser)
        self.__app = app
        self._endpoint = endpoint
        self.__database = database
        self.__jwt_secret_key = jwt_secret_key
        self.__schedule_search_engine = schedule_search_engine
        self.home_route()
        self.schedule_search_route()
        self.my_schedule_route()
        self.make_schedule_route()
        
    def home_route(self):
        # 타임 테이블 페이지의 최 상단 대시보드데이터
        # 파라미터 없음, 비로그인 상태에서는 0으로 리턴함 
        # 업데이트 완료
        @self.__app.get('/time_table_server/try_get_dashboard_data')
        def get_dashboard_data(request:Request, date:Optional[str]=datetime.now().strftime("%Y/%m/%d")):
            request_manager = RequestManager(secret_key=self.__jwt_secret_key)
            data_payload = DateRequest(date=date)
            request_manager.try_view_management(data_payload=data_payload, cookies=request.cookies)

            # if not request_manager.jwt_payload.result:
            #     raise request_manager.credentials_exception
            time_table_controller =TimeTableController()
            model = time_table_controller.get_dashboard_data(database=self.__database,
                                                           request=request_manager,
                                                           schedule_search_engine=self.__schedule_search_engine
                                                           )
            
            body_data = model.get_response_form_data(self._head_parser)
            response = request_manager.make_json_response(body_data=body_data)
            return response
        
        
        # 홈화면의 스케줄 레이어를 바탕으로 검색
        # 업데이트 완료
        @self.__app.get('/time_table_server/get_time_layer_schedule_with_date')
        def get_time_layer_schedule_with_date(request:Request, date:Optional[str]=datetime.now().strftime("%Y/%m/%d")):
            request_manager = RequestManager(secret_key=self.__jwt_secret_key)
            data_payload = DateRequest(date=date)
            
            request_manager.try_view_management(data_payload=data_payload, cookies=request.cookies)

            time_table_controller =TimeTableController()
            model = time_table_controller.get_time_layer_with_date(database=self.__database,
                                                              schedule_search_engine=self.__schedule_search_engine,
                                                              request=request_manager)
            
            body_data = model.get_response_form_data(self._head_parser)
            response = request_manager.make_json_response(body_data=body_data)
            return response       
        
        # bias 페이지에서 요청하는 데이터로 세팅
        # 업데이트 완료
        @self.__app.get('/time_table_server/get_bias_page_schedule')
        def get_bias_page_schedule(request:Request, bid=Optional[str], date:Optional[str]=datetime.now().strftime("%Y/%m/%d")):
            request_manager = RequestManager(secret_key=self.__jwt_secret_key)
            data_payload = BiasDateRequest(bid=bid, date=date)
            
            request_manager.try_view_management(data_payload=data_payload, cookies=request.cookies)

            time_table_controller =TimeTableController()
            model = time_table_controller.get_bias_date_schedule(database=self.__database,
                                                                schedule_search_engine=self.__schedule_search_engine,
                                                                request=request_manager)
            
            body_data = model.get_response_form_data(self._head_parser)
            response = request_manager.make_json_response(body_data=body_data)
            return response       

        
    def schedule_search_route(self):
        # 서치 가능하게 하는 곳
        # keyword : 검색어
        # key : 서치 키값
        # type : schedule, schedule_bundle, event
        # New Model에 대한 테스트 완료

        # 새로운 파라미터를 추가합니다.
        # search_columns : Managed_Table에서 서치할 컬럼을 받아옴
        # Bias 이름에 대한 스케쥴이나 번들을 검색하고 싶을 때, Search_columns = ["bname"]이라고 주면 됩니다.
        # 비어있는 경우에는 Managed_data_domain.py에서 디폴트 컬럼을 결정합니다.
        # 테스트완료
        # 이걸로 바이어스 네임으로 서치 가능


        # filter_option : "not_end", ""
        # 업데이트 완료
        @self.__app.get('/time_table_server/try_search_schedule_with_keyword')
        def try_search_schedule(request:Request, search_columns:Optional[str]="",
                                filter_option:Optional[str]="", keyword:Optional[str]="",
                                key:Optional[int]=-1, type:Optional[str]=""):

            request_manager = RequestManager(secret_key=self.__jwt_secret_key)
            data_payload = SearchRequest(keyword=keyword, search_columns=search_columns, key=key, search_type=type, filter_option=filter_option)
            
            request_manager.try_view_management(data_payload=data_payload, cookies=request.cookies)

            time_table_controller =TimeTableController()
            model = time_table_controller.try_search_schedule_with_keyword(database=self.__database,
                                                            schedule_search_engine=self.__schedule_search_engine,
                                                            request=request_manager)
            
            body_data = model.get_response_form_data(self._head_parser)
            response = request_manager.make_json_response(body_data=body_data)
            return response

        # 스케줄 자세히 보기
        # 업데이트 완료
        @self.__app.post('/time_table_server/get_schedule_with_sids')
        def try_search_bias_with_sid(request:Request, raw_request:dict):
            request_manager = RequestManager(secret_key=self.__jwt_secret_key)
            
            data_payload = GetSchedulesRequest(request=raw_request)
            request_manager.try_view_management(data_payload=data_payload, cookies=request.cookies)

            time_table_controller =TimeTableController()
            model = time_table_controller.get_schedules_with_sids(database=self.__database,
                                                                request=request_manager)

            body_data = model.get_response_form_data(self._head_parser)
            response = request_manager.make_json_response(body_data=body_data)
            return response
        
        # 신기능 (1.2.1)
        # 스케줄 탐색 페이지에서 요청받는 데이터 처리
        # 업데이트 완료
        @self.__app.post('/time_table_server/get_explore_schedules')
        def try_explore_schedule_by_filters(request:Request, raw_request:dict):
            request_manager = RequestManager(secret_key=self.__jwt_secret_key)
            data_payload = ExploreScheduleRequset(request=raw_request)
            
            request_manager.try_view_management(data_payload=data_payload, cookies=request.cookies)

            time_table_controller =TimeTableController()
            model = time_table_controller.try_explore_schedule_with_category(schedule_search_engine=self.__schedule_search_engine,
                                                                             database=self.__database,
                                                                             request=request_manager)

            
            body_data = model.get_response_form_data(self._head_parser)
            response = request_manager.make_json_response(body_data=body_data)
            return response
        
        # 업데이트 완료
        @self.__app.get('/time_table_server/get_monthly_bias_schedule')
        def get_monthly_bias_schedule(request:Request, bid:Optional[str], month:Optional[str], year:Optional[str]):
            request_manager = RequestManager(secret_key=self.__jwt_secret_key)
            data_payload = ScheduleWithBidnDateRequest(bid=bid, year=year, month=month)
            request_manager.try_view_management(data_payload=data_payload, cookies=request.cookies)
            

            time_table_controller =TimeTableController()
            model = time_table_controller.get_monthly_bias_schedule(database=self.__database,
                                                                     schedule_search_engine=self.__schedule_search_engine,
                                                                     request=request_manager)
            
            body_data = model.get_response_form_data(self._head_parser)
            
            response = request_manager.make_json_response(body_data=body_data)
            return response
        


    # 로그인 필수
    def my_schedule_route(self):
        # 내 스케줄에 추가하기
        # sids를 받아서 추가할 것(번들은 쪼개서 sid리스트만 받음, 이벤트는 이곳으로 추가하지 않음)
        # 업데이트 완료
        @self.__app.get('/time_table_server/try_subscribe_schedule')
        def try_subscribe_schedule(request:Request, sid:str):
            request_manager = RequestManager(secret_key=self.__jwt_secret_key)
            data_payload = ScheduleRequest(sid=sid)
            
            request_manager.try_view_management_need_authorized(data_payload=data_payload, cookies=request.cookies)

            time_table_controller =TimeTableController()
            model = time_table_controller.try_add_schedule(database=self.__database,
                                                        request=request_manager)
            
            body_data = model.get_response_form_data(self._head_parser)
            response = request_manager.make_json_response(body_data=body_data)
            return response


    # 스케줄을 만들 때 사용하는 기능.
    def make_schedule_route(self):
        # 단일 일정을 만들기
        # Managed_Table 테스트 완료
        # 업데이트 완료
        @self.__app.post('/time_table_server/try_make_new_schedule')
        def try_make_new_schedule(request: Request, raw_request:dict):
            request_manager = RequestManager(secret_key=self.__jwt_secret_key)
            data_payload = MakeScheduleRequest(request=raw_request)
            
            request_manager.try_view_management_need_authorized(data_payload=data_payload, cookies=request.cookies)
            
            time_table_controller =TimeTableController()
            model = time_table_controller.make_new_single_schedule(schedule_search_engine=self.__schedule_search_engine,
                                                                   database=self.__database,
                                                                   request=request_manager)
            
            body_data = model.get_response_form_data(self._head_parser)
            pprint(body_data)
            response = request_manager.make_json_response(body_data=body_data)
            return response

        # 수정을 위해 작성했던 스케줄을 확인하는 함수
        # 업데이트 완료
        @self.__app.get('/time_table_server/try_get_written_schedule')
        def try_get_written_schedule(request:Request, sid:Optional[str]=""):
            request_manager = RequestManager(secret_key=self.__jwt_secret_key)
            data_payload = ScheduleRequest(sid=sid)
            request_manager.try_view_management(data_payload=data_payload, cookies=request.cookies)
            # request_manager.try_view_management_need_authorized(data_payload=data_payload, cookies=request.cookies)

            time_table_controller =TimeTableController()
            model = time_table_controller.try_get_written_schedule(database=self.__database,
                                                                   request=request_manager)

            body_data = model.get_response_form_data(self._head_parser)
            response = request_manager.make_json_response(body_data=body_data)
            return response
        
        # 스케줄 이미지 업로드 하는 곳
        # 사용되는 타이밍
        # 스케줄이 존재함 -> 이미지 업로드
        # 스케줄을 업로드함 -> 이미지 업로드
        
        # 차후 추가될 내용 -> 이미지 부터 업로드 -> schedule 데이터 생성 (gemini AI 사용)
        @self.__app.post('/time_table_server/try_upload_schedule_image')
        async def try_upload_schedule_image(request:Request, image: Union[UploadFile, None] = File(None),
                                       jsonData: Union[str, None] = Form(None)):
            request_manager = RequestManager(secret_key=self.__jwt_secret_key)
            
            if image:
                image_name = image.filename
                image = await image.read()
            else:
                raise request_manager.system_logic_exception

            if jsonData is None:
                raise request_manager.system_logic_exception
            
            raw_request = json.loads(jsonData)
            data_payload = ScheduleImageRequest(request=raw_request,
                                                image=image,
                                                image_name=image_name)
            
            request_manager.try_view_management_need_authorized(data_payload=data_payload, cookies=request.cookies)

            time_table_controller=TimeTableController()
            model = time_table_controller.try_upload_schedule_image(database=self.__database,
                                                                    schedule_search_engine=self.__schedule_search_engine,
                                                                    request=request_manager)
            body_data = model.get_response_form_data(self._head_parser)
            response = request_manager.make_json_response(body_data=body_data)
            return response


        # 스케줄 데이터 삭제
        # Managed_Table 테스트 완료
        @self.__app.get('/time_table_server/try_delete_schedule')
        def try_delete_schedule(request:Request, sid:Optional[str]=""):
            request_manager = RequestManager(secret_key=self.__jwt_secret_key)
            data_payload = DeleteSingleScheduleRequest(sid=sid)
            request_manager.try_view_management_need_authorized(data_payload=data_payload, cookies=request.cookies)

            time_table_controller = TimeTableController()
            model = time_table_controller.try_delete_schedule(schedule_search_engine=self.__schedule_search_engine,
                                                              database=self.__database,
                                                              request=request_manager)

            body_data = model.get_response_form_data(self._head_parser)
            response = request_manager.make_json_response(body_data=body_data)
            return response



KST = pytz.timezone("Asia/Seoul")
        
class DummyRequest():
    def __init__(self) -> None:
        self.email:str="alsrhks2508@naver.com"
        pass
    
class RequestSchedule(BaseModel):
    sid: str
    bid: str
    title: str
    tags: list[str] = []
    datetime: datetime
    duration: int
    

class MakeScheduleRequest(RequestHeader):
    def __init__(self, request: dict) -> None:
        super().__init__(request)

        body: dict = request.get("body", {})
        schedule_data:dict = body.get("schedule", {})
        
        # schedule_data의 필드들을 적절한 타입으로 변환
        schedule_data["duration"] = int(schedule_data.get("duration", 0))

        # schedule 전체를 Pydantic으로 검증
        self.schedule = RequestSchedule(**schedule_data)
        
        # ✅ 생성 후 datetime KST 변환
        dt = self.schedule.datetime
        if dt.tzinfo is None:
            # tz 정보 없으면 UTC로 간주
            dt = dt.replace(tzinfo=pytz.UTC)
        self.schedule.datetime = dt.astimezone(KST)
        
    def __call__(self):
        # 호출하면 schedule 객체를 리턴
        return self.schedule

    def __repr__(self):
        return f"MakeScheduleRequest(schedule={self.schedule})"
  
class GetSchedulesRequest(RequestHeader):
    def __init__(self, request:dict)-> None:
        body:dict = request['body']
        self.sids=body.get('sids', [])     
      

class MakeMultipleScheduleRequest(RequestHeader):
    def __init__(self, request) -> None:
        super().__init__(request)
        # self.email:str="alsrhks2508@naver.com"
        body:dict = request['body']
        self.title = body['title']
        self.bid = body['bid']
        self.type = body.get("type", "bundle")
        self.schedules = [Schedule().make_with_dict(dict_data=single_schedule_data) for single_schedule_data in body.get("schedules", []) if single_schedule_data != ""]

class ModifySingleScheduleRequest(RequestHeader):
    def __init__(self, request):
        super().__init__(request)
        body:dict = request['body']
        self.sid = body['sid']
        self.title = body['title']
        self.platform = body['platform']
        self.bid = body.get('bid', "")
        self.start_date = body["start_date"]
        self.start_time = body["start_time"]
        self.end_date = body["end_date"]
        self.end_time = body["end_time"]
        self.tags = body.get('tags', [])

# class ModifyMultipleScheduleRequest:
class ModifyMultipleScheduleRequest(RequestHeader):
    def __init__(self, request) -> None:
        super().__init__(request)
        # self.email:str="alsrhks2508@naver.com"
        body:dict = request['body']
        self.sbid = body.get('sbid', "")
        self.title = body.get('title', "")
        self.bid = body['bid']
        self.type = body.get("type", "")
        self.schedules = [Schedule().make_with_dict(dict_data=single_schedule_data) for single_schedule_data in body.get("schedules", []) if single_schedule_data != ""]

class DeleteSingleScheduleRequest(RequestHeader):
    def __init__(self, sid) -> None:
        self.sid = sid

class DeleteScheduleBundleRequest(RequestHeader):
    def __init__(self, sbid) -> None:
        self.sbid = sbid



class SearchRequest(RequestHeader):
    def __init__(self, keyword="", search_columns="", key=-1, search_type="", filter_option="") -> None:
        self.keyword=keyword
        self.search_columns=search_columns
        self.key=key
        self.type=search_type
        self.filter_option=filter_option
        
    def __call__(self):
        print("keyword:", self.keyword)
        print("search_columns:", self.search_columns)
        print("key:", self.key)
        print("type:", self.type)
        print("filter_option:", self.filter_option)
        return
        

        

class ExploreScheduleRequset(RequestHeader):
    def __init__(self, request:dict)-> None:
        body:dict = request['body']
        self.category:str=body.get("category", "") # category 는 따로 있을듯
        self.key:int=body.get("key", -1)  
        self.time_section:int=body.get("timeSection", 0) # 0 -> 0~6 / 1 -> 6~12 / 2 -> 12~16 / 3 -> 16~24 / -1 -> 0~24(전체)
        self.style:str=body.get("style", "all")  # all, vtuber, cam, nocam -> bias 데이터 (tags)
        self.gender:str=body.get("gender", "all") # male, female, etc -> bias 데이터 (tags)

    def __call__(self):
        print("category:", self.category)
        print("key:", self.key)
        print("time_section:", self.time_section)
        print("style:", self.style)
        return
        

class ScheduleRequest(RequestHeader):
    def __init__(self, sid)-> None:
        self.sid:str=sid

class DateRequest(RequestHeader):
    def __init__(self, date)-> None:
        self.date:str = date

class BiasDateRequest(RequestHeader):
    def __init__(self, bid, date)-> None:
        print(date)
        self.bid:str = bid
        self.date:str = datetime.strptime(date, "%Y-%m-%d")
        
class TimeChartRequest(RequestHeader):
    def __init__(self, request):
        body:dict = request['body']
        self.date:str=body.get('date',datetime.now().strftime("%Y/%m/%d"))
        self.sids = body.get("sids", [])
        
class ScheduleWithBidnDateRequest(RequestHeader):
    def __init__(self, bid, year:str, month:str) -> None:
        self.bid:str=bid
        self.date = datetime(int(year), int(month), 1)
        
# 이미지 스케줄용 Pydantic 모델
class RequestScheduleImage(BaseModel):
    bid: str
    sid: str
    datetime: datetime
    image_name: str | None = None
    image: bytes | None = None  # 파일 자체를 bytes로 받거나, 필요에 따라 UploadFile로 변경

class ScheduleImageRequest(RequestHeader):
    def __init__(self, request: dict, image_name=None, image=None) -> None:
        super().__init__(request)

        body: dict = request.get("body", {})
        schedule_data: dict = {
            "sid" : body.get("sid", ""),
            "bid": body.get("bid", ""),
            "datetime": body.get("datetime", ""),
            "image_name": image_name,
            "image": image
        }

        # Pydantic 검증
        self.request = RequestScheduleImage(**schedule_data)

        # ✅ datetime KST 변환
        dt = self.request.datetime
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=pytz.UTC)
        self.request.datetime = dt.astimezone(KST)

    def __call__(self):
        return self.request

    def __repr__(self):
        return f"ScheduleImageRequest(schedule={self.request})"