from typing import Optional
from fastapi import FastAPI, Request
from others import Schedule
from view.master_view import Master_View, RequestHeader
from view.parsers import Head_Parser
from view.jwt_decoder import RequestManager
from controller import TImeTableController
#from websockets.exceptions import ConnectionClosedError
from pprint import pprint
import json
from datetime import datetime


class TimeTableView(Master_View):
    def __init__(self, app:FastAPI, endpoint:str,
                  database, head_parser:Head_Parser,
                  jwt_secret_key
                  ) -> None:
        super().__init__(head_parser=head_parser)
        self.__app = app
        self._endpoint = endpoint
        self.__database = database
        self.__jwt_secret_key = jwt_secret_key
        self.home_route()
        self.schedule_search_route()
        self.my_schedule_route()
        self.make_schedule_route()
        
    def home_route(self):
        # 완료 / 
        # 타임 테이블 페이지의 최 상단 대시보드데이터
        # 파라미터 없음, 비로그인 상태에서는 0으로 리턴함 
        @self.__app.get('/time_table_server/try_get_dashboard_data')
        def get_dashboard_data(request:Request, date:Optional[str]=datetime.now().strftime("%Y-%m-%d")):
            request_manager = RequestManager(secret_key=self.__jwt_secret_key)
            data_payload = DateRequest(date=date)
            request_manager.try_view_management(data_payload=data_payload, cookies=request.cookies)

            # if not request_manager.jwt_payload.result:
            #     raise request_manager.credentials_exception
            time_table_controller =TImeTableController()
            model = time_table_controller.get_dashboard_data(database=self.__database,
                                                           request=request_manager)
            
            body_data = model.get_response_form_data(self._head_parser)
            response = request_manager.make_json_response(body_data=body_data)

            return response
        
        # 이벤트는 보류
        # 타임 테이블 페이지의 최 상단 이벤트 보드 데이터
        # 비로그인 상태에서는 date를 선택하지 않으면 그날 이벤트를 랜덤하게 3개 줄것
        # 로그인 상태에서는 date를 선택하면 그날 이벤트를 모두 줄것
        # date는 안들어오면 오늘 날짜로 자동 선택될 것임
        # date는 "2025/03/05" 형식
        #@self.__app.get('/time_table_server/try_get_eventboard_data')
        #def get_eventboard_data(request:Request, date:Optional[str]=datetime.now().strftime("%Y/%m/%d")):
            #request_manager = RequestManager(secret_key=self.__jwt_secret_key)
            #data_payload = DateRequest(date=date)
            #request_manager.try_view_management(data_payload=data_payload, cookies=request.cookies)

            #time_table_controller =TImeTableController()
            #model = time_table_controller.get_eventboard_data(database=self.__database,
                                                              #request=request_manager)
            #body_data = model.get_response_form_data(self._head_parser)
            #response = request_manager.make_json_response(body_data=body_data)

            #return response

        # 완료
        # 타임 차트에서 데이터 뽑아오기
        # 비로그인 상태에서는 데이터를 반환하지 않아도될듯 -> 아니면 반환할 데이터를 마련해도 될듯
        # 로그인 상태에서는 본인이 추가한 모든 일정(오늘자)이 반환되어야함
        @self.__app.get('/time_table_server/try_get_today_time_chart')
        def try_get_today_time_chart(request:Request, date:Optional[str]=datetime.now().strftime("%Y-%m-%d")):
            request_manager = RequestManager(secret_key=self.__jwt_secret_key)
            data_payload = DateRequest(date=date)
            request_manager.try_view_management(data_payload=data_payload, cookies=request.cookies)

            time_table_controller =TImeTableController()
            model = time_table_controller.get_time_chart(database=self.__database,
                                                              request=request_manager)
            
            body_data = model.get_response_form_data(self._head_parser)
            response = request_manager.make_json_response(body_data=body_data)

            return response
        
        # 타임 차트에 임시 일정들 추가로 넣어주기
        @self.__app.post('/time_table_server/get_time_chart_with_other_schedule')
        def try_get_today_time_chart_with_other_schedule(request:Request, raw_requset:dict):
            request_manager = RequestManager(secret_key=self.__jwt_secret_key)
            data_payload = TimeChartRequest(request=raw_requset)
            
            request_manager.try_view_management(data_payload=data_payload, cookies=request.cookies)

            time_table_controller =TImeTableController()
            model = time_table_controller.get_time_chart_with_sids(database=self.__database,
                                                              request=request_manager)
            
            body_data = model.get_response_form_data(self._head_parser)
            response = request_manager.make_json_response(body_data=body_data)

            return response
        
        # 보류
        # 홈 화면 젤 밑에 나오는 bias 데이터 들인데 이건 여기다가 만들지 말지 고민중임
        @self.__app.get('/time_table_server/try_get_recommended_bias_list')
        def get_recommended_bias_list(request:Request):
            request_manager = RequestManager(secret_key=self.__jwt_secret_key)
            data_payload = DummyRequest()
            request_manager.try_view_management(data_payload=data_payload, cookies=request.cookies)

            time_table_controller =TImeTableController()
            model = time_table_controller.get_recommended_bias_list(database=self.__database,
                                                                    request=request_manager,
                                                                    num_recommend=5)
            
            body_data = model.get_response_form_data(self._head_parser)
            response = request_manager.make_json_response(body_data=body_data)

            return response

        
    def schedule_search_route(self):
        # 서치 가능하게 하는 곳
        # keyword : 검색어
        # key : 서치 키값
        # type : schedule, schedule_bundle, event
        # 완료 (테스트만 필요)
        @self.__app.get('/time_table_server/try_search_schedule_with_keyword')
        def try_search_schedule(request:Request, filter_option:Optional[str]="not_end", keyword:Optional[str] = "", key:Optional[int]=-1, type:Optional[str]=""):
            request_manager = RequestManager(secret_key=self.__jwt_secret_key)
            data_payload = SearchRequest(keyword=keyword, key=key, search_type=type, filter_option=filter_option)
            request_manager.try_view_management(data_payload=data_payload, cookies=request.cookies)

            time_table_controller =TImeTableController()
            model = time_table_controller.try_search_schedule_with_keyword(database=self.__database,
                                                            request=request_manager)
            
            body_data = model.get_response_form_data(self._head_parser)
            response = request_manager.make_json_response(body_data=body_data)
            return response
        
        # keyword 추천
        # 본인이 팔로우한 bias의 카테고리 위주로 제시할 듯
        # 로그인을 안했거나 팔로우한 bias가 없으면 랜덤하게 뿌리면됨
        # 완료 (테스트 완료)
        @self.__app.get('/time_table_server/try_get_recommend_keyword')
        def try_get_recommend_keyword(request:Request):
            request_manager = RequestManager(secret_key=self.__jwt_secret_key)
            data_payload = DummyRequest()
            request_manager.try_view_management(data_payload=data_payload, cookies=request.cookies)

            time_table_controller =TImeTableController()
            model = time_table_controller.try_get_recommend_keyword(database=self.__database,
                                                                    request=request_manager,
                                                                    num_keywords=6)

            # 반환 데이터 : 'recommend_keywords'
            body_data = model.get_response_form_data(self._head_parser)
            response = request_manager.make_json_response(body_data=body_data)
            return response

        # Bias 서치
        # 팔로워 서치부분과는 다르게  둠
        @self.__app.get('/time_table_server/try_search_bias')
        def try_search_bias_with_keyword(request:Request,  keyword:Optional[str]="", key:Optional[int]=-1):
            request_manager = RequestManager(secret_key=self.__jwt_secret_key)
            data_payload = SearchRequest(keyword=keyword, key=key, search_type="bias")
            request_manager.try_view_management(data_payload=data_payload, cookies=request.cookies)

            time_table_controller =TImeTableController()
            model = time_table_controller.try_search_bias_with_keyword(database=self.__database,
                                                                       request=request_manager,
                                                                       num_biases=15)

            body_data = model.get_response_form_data(self._head_parser)
            response = request_manager.make_json_response(body_data=body_data)
            return response
        
        # Bias 서치
        # 팔로워 서치부분과는 다르게  둠
        @self.__app.post('/time_table_server/get_schedule_with_sids')
        def try_search_bias_with_keyword(request:Request, raw_request:dict):
            request_manager = RequestManager(secret_key=self.__jwt_secret_key)
            data_payload = GetSchedulesRequest(request=raw_request)
            request_manager.try_view_management(data_payload=data_payload, cookies=request.cookies)

            time_table_controller =TImeTableController()
            model = time_table_controller.get_schedules_with_sids(database=self.__database,
                                                                request=request_manager)

            body_data = model.get_response_form_data(self._head_parser)
            response = request_manager.make_json_response(body_data=body_data)
            return response

    # 로그인 필수
    def my_schedule_route(self):
        # 완료
        # 내 스케줄에 추가하기
        # sids를 받아서 추가할 것(번들은 쪼개서 sid리스트만 받음, 이벤트는 이곳으로 추가하지 않음)
        @self.__app.post('/time_table_server/try_add_schedule')
        def try_add_schedule(request:Request, raw_request:dict):
            request_manager = RequestManager(secret_key=self.__jwt_secret_key)
            data_payload = GetSchedulesRequest(request=raw_request)
            
            request_manager.try_view_management_need_authorized(data_payload=data_payload, cookies=request.cookies)

            time_table_controller =TImeTableController()
            model = time_table_controller.try_add_schedule(database=self.__database,
                                                        request=request_manager)
            
            body_data = model.get_response_form_data(self._head_parser)
            response = request_manager.make_json_response(body_data=body_data)
            return response

        # 1.5버전까지 반려됨
        # 이벤트는 이곳으로 추가함
        #@self.__app.get('/time_table_server/try_add_event')
        #def try_add_event(request:Request, seid:Optional[str]):
            #request_manager = RequestManager(secret_key=self.__jwt_secret_key)
            #data_payload = AddNewEventRequest(seid=seid)
            #request_manager.try_view_management_need_authorized(data_payload=data_payload, cookies=request.cookies)

            #time_table_controller =TImeTableController()
            #model = time_table_controller.try_add_event(database=self.__database,
                                                        #request=request_manager)
            
            #body_data = model.get_response_form_data(self._head_parser)
            #response = request_manager.make_json_response(body_data=body_data)
            #return response
        
        ## 완료
        ## 홈화면에 노출될 스케줄 정하는건 여기서 함
        #@self.__app.get('/time_table_server/try_select_my_time_table_schedule')
        #def try_select_my_time_table_schedule(request:Request, date:Optional[str],bid:Optional[str]=""):
            #request_manager = RequestManager(secret_key=self.__jwt_secret_key)
            #data_payload = SelectMyTimeTableRequest(date=date, bid=bid)
            #request_manager.try_view_management_need_authorized(data_payload=data_payload, cookies=request.cookies)

            #time_table_controller =TImeTableController()
            #model = time_table_controller.try_select_my_time_table_schedule(database=self.__database,
                                                                            #request=request_manager)
            
            #body_data = model.get_response_form_data(self._head_parser)
            #response = request_manager.make_json_response(body_data=body_data)
            #return response
        
        # 완료
        # bid에서 내가 선택했는 스케줄들 볼때 쓰는 엔드 포인트. 로그인 필수
        # 테스트는 아직 못함
        # @self.__app.get('/time_table_server/try_search_my_schedule_with_bid')
        # def try_search_my_schedule_with_bid(request:Request, bid:Optional[str]="", key:Optional[int]=-1):
        #     request_manager = RequestManager(secret_key=self.__jwt_secret_key)
        #     data_payload = ScheduleWithBidRequest(bid=bid, key=key)
        #     request_manager.try_view_management_need_authorized(data_payload=data_payload, cookies=request.cookies)
        #
        #     time_table_controller =TImeTableController()
        #     model = time_table_controller.try_search_my_schedule_with_bid(database=self.__database,
        #                                                                 request=request_manager)
        #
        #     body_data = model.get_response_form_data(self._head_parser)
        #     response = request_manager.make_json_response(body_data=body_data)
        #     return response

        # 내가 담아놓은 스케줄들을 볼 수 있습니다.
        # 테스트 완료
        @self.__app.get('/time_table_server/try_search_my_schedule_with_bid')
        def try_get_my_selected_schedules(request:Request, bid:Optional[str]="", key:Optional[int]=-1):
            request_manager = RequestManager(secret_key=self.__jwt_secret_key)
            data_payload = ScheduleWithBidRequest(bid=bid, key=key)
            request_manager.try_view_management_need_authorized(data_payload=data_payload, cookies=request.cookies)
            # request_manager.try_view_management(data_payload=data_payload, cookies=request.cookies)

            time_table_controller =TImeTableController()
            model = time_table_controller.try_get_my_selected_schedules(database=self.__database,
                                                                          request=request_manager)

            body_data = model.get_response_form_data(self._head_parser)
            response = request_manager.make_json_response(body_data=body_data)
            return response

        # 완료
        # 선택했던 스케줄을 지우는건 여기서 함
        # 목표 sid를 넘기면 삭제 되게 할 것임. 단 로그인 필수
        @self.__app.get('/time_table_server/try_reject_from_my_schedule')
        def try_reject_from_my_schedule(request:Request, sid:Optional[str]=""):
            request_manager = RequestManager(secret_key=self.__jwt_secret_key)
            data_payload = ScheduleRequest(sid=sid)
            request_manager.try_view_management_need_authorized(data_payload=data_payload, cookies=request.cookies)

            time_table_controller =TImeTableController()
            model = time_table_controller.try_reject_from_my_schedule(database=self.__database,
                                                                        request=request_manager)
            
            body_data = model.get_response_form_data(self._head_parser)
            response = request_manager.make_json_response(body_data=body_data)
            return response

        # 이번 주 일정 불러오기
        @self.__app.get('/time_table_server/try_get_weekday_schedules')
        def try_get_weekday_schedules(request:Request ):
            request_manager = RequestManager(secret_key=self.__jwt_secret_key)
            data_payload = DummyRequest()
            request_manager.try_view_management_need_authorized(data_payload=data_payload, cookies=request.cookies)
            # request_manager.try_view_management(data_payload=data_payload, cookies=request.cookies)

            time_table_controller =TImeTableController()
            model = time_table_controller.try_get_weekday_schedules(database=self.__database,
                                                                      request=request_manager)

            body_data = model.get_response_form_data(self._head_parser)
            response = request_manager.make_json_response(body_data=body_data)
            return response

    def make_schedule_route(self):
        # 단일 일정을 만들기
        @self.__app.post('/time_table_server/try_make_new_single_schedule')
        def try_make_new_single_schedule(request: Request, raw_request:dict):
            request_manager = RequestManager(secret_key=self.__jwt_secret_key)
            data_payload = MakeSingleScheduleRequest(request=raw_request)
            request_manager.try_view_management(data_payload=data_payload, cookies=request.cookies)

            time_table_controller =TImeTableController()
            model = time_table_controller.make_new_single_schedule(database=self.__database,
                                                                    request=request_manager)
            
            body_data = model.get_response_form_data(self._head_parser)
            response = request_manager.make_json_response(body_data=body_data)
            return response

        # 복수 일정을 만들기
        # 테스트 완료 
        @self.__app.post('/time_table_server/try_make_new_multiple_schedule')
        def try_make_new_multiple_schedule(request: Request, raw_request:dict):

            request_manager = RequestManager(secret_key=self.__jwt_secret_key)
            data_payload = MakeMultipleScheduleRequest(request=raw_request)
            request_manager.try_view_management(data_payload=data_payload, cookies=request.cookies)

            time_table_controller =TImeTableController()
            model = time_table_controller.make_new_multiple_schedules(database=self.__database,
                                                                        request=request_manager)
            
            body_data = model.get_response_form_data(self._head_parser)
            response = request_manager.make_json_response(body_data=body_data)
            return response

        # 수정을 위해 작성했던 스케줄을 확인하는 함수
        @self.__app.get('/time_table_server/try_get_written_schedule')
        def try_get_written_schedule(request:Request, sid:Optional[str]=""):
            request_manager = RequestManager(secret_key=self.__jwt_secret_key)
            data_payload = ScheduleRequest(sid=sid)
            request_manager.try_view_management_need_authorized(data_payload=data_payload, cookies=request.cookies)

            time_table_controller =TImeTableController()
            model = time_table_controller.try_get_written_schedule(database=self.__database,
                                                                   request=request_manager)

            body_data = model.get_response_form_data(self._head_parser)
            response = request_manager.make_json_response(body_data=body_data)
            return response

        # 수정할 번들 데이터 불러오기
        @self.__app.get('/time_table_server/try_get_written_bundle')
        def try_get_written_bundle(request:Request, sbid:Optional[str]=""):
            request_manager = RequestManager(secret_key=self.__jwt_secret_key)
            data_payload = ScheduleBundleRequest(sbid=sbid)
            request_manager.try_view_management_need_authorized(data_payload=data_payload, cookies=request.cookies)

            time_table_controller =TImeTableController()
            model = time_table_controller.try_get_written_schedule(database=self.__database,
                                                                   request=request_manager)

            body_data = model.get_response_form_data(self._head_parser)
            response = request_manager.make_json_response(body_data=body_data)
            return response

        # 단일 스케줄 수정
        @self.__app.post('/time_table_server/try_modify_schedule')
        def try_modify_schedule(request:Request, raw_request:dict):
            request_manager = RequestManager(secret_key=self.__jwt_secret_key)
            data_payload = ModifySingleScheduleRequest(request=raw_request)
            request_manager.try_view_management_need_authorized(data_payload=data_payload, cookies=request.cookies)

            time_table_controller =TImeTableController()
            model = time_table_controller.try_modify_single_schedule(database=self.__database,
                                                              request=request_manager)

            body_data = model.get_response_form_data(self._head_parser)
            response = request_manager.make_json_response(body_data=body_data)
            return response

        # 스케줄 번들 수정
        @self.__app.post('/time_table_server/try_modify_schedule_bundle')
        def try_modify_bundle(request:Request, raw_request:dict):
            request_manager = RequestManager(secret_key=self.__jwt_secret_key)
            data_payload = ModifyMultipleScheduleRequest(request=raw_request)
            request_manager.try_view_management_need_authorized(data_payload=data_payload, cookies=request.cookies)

            time_table_controller =TImeTableController()
            model = time_table_controller.try_modify_bundle(database=self.__database,
                                                              request=request_manager)

            body_data = model.get_response_form_data(self._head_parser)
            response = request_manager.make_json_response(body_data=body_data)
            return response

        # 스케줄 데이터 삭제
        @self.__app.get('/time_table_server/try_delete_schedule')
        def try_delete_schedule(request:Request, sid:Optional[str]=""):
            request_manager = RequestManager(secret_key=self.__jwt_secret_key)
            data_payload = DeleteSingleScheduleRequest(sid=sid)
            request_manager.try_view_management_need_authorized(data_payload=data_payload, cookies=request.cookies)

            time_table_controller = TImeTableController()
            model = time_table_controller.try_delete_schedule(database=self.__database,
                                                              request=request_manager)

            body_data = model.get_response_form_data(self._head_parser)
            response = request_manager.make_json_response(body_data=body_data)
            return response

        # 번들 데이터 삭제
        @self.__app.get('/time_table_server/try_delete_bundle')
        def try_delete_bundle(request:Request, sbid:Optional[str]=""):
            request_manager = RequestManager(secret_key=self.__jwt_secret_key)
            data_payload = DeleteScheduleBundleRequest(sbid=sbid)
            request_manager.try_view_management_need_authorized(data_payload=data_payload, cookies=request.cookies)
            # request_manager.try_view_management(data_payload=data_payload, cookies=request.cookies)

            time_table_controller = TImeTableController()
            model = time_table_controller.try_delete_bundle(database=self.__database,
                                                              request=request_manager)

            body_data = model.get_response_form_data(self._head_parser)
            response = request_manager.make_json_response(body_data=body_data)
            return response


        # 여기는 2차 목표임
        ## 일정 수정하기
        #@self.__app.post('/time_table_server/try_modify_schedule')
        #def try_modify_schedule(request: Request, raw_requset:dict):
            #request_manager = RequestManager(secret_key=self.__jwt_secret_key)
            #data_payload = MakeSingleScheduleRequest(request=raw_requset)
            #request_manager.try_view_management(data_payload=data_payload, cookies=request.cookies)

            #time_table_controller =TImeTableController()
            #model = time_table_controller.modify_schedule(database=self.__database,
                                                                        #request=request_manager)
            
            #body_data = model.get_response_form_data(self._head_parser)
            #response = request_manager.make_json_response(body_data=body_data)
            #return response
        
        ## 일정 지우기 
        #@self.__app.post('/time_table_server/try_delete_schedule')
        #def try_delete_schedule(request: Request, raw_requset:dict):
            #request_manager = RequestManager(secret_key=self.__jwt_secret_key)
            #data_payload = MakeSingleScheduleRequest(request=raw_requset)
            #request_manager.try_view_management(data_payload=data_payload, cookies=request.cookies)

            #time_table_controller =TImeTableController()
            #model = time_table_controller.make_new_multiple_schedule(database=self.__database,
                                                                        #request=request_manager)
            
            #body_data = model.get_response_form_data(self._head_parser)
            #response = request_manager.make_json_response(body_data=body_data)
            #return response
        
        
class DummyRequest():
    def __init__(self) -> None:
        pass

class MakeSingleScheduleRequest(RequestHeader):
# class MakeSingleScheduleRequest:
    def __init__(self, request) -> None:
        super().__init__(request)
        # self.email:str="alsrhks2508@naver.com"
        body:dict = request['body']
        self.sname = body['sname']
        self.location = body['location']
        self.bid = body.get("bid", "")
        self.start_date = body['start_date']
        self.start_time = body['start_time']
        self.end_date = body['end_date']
        self.end_time = body['end_time']
        self.state = body.get("status", True)

# class MakeMultipleScheduleRequest:
class MakeMultipleScheduleRequest(RequestHeader):
    def __init__(self, request) -> None:
        super().__init__(request)
        body:dict = request['body']
        self.sname = body['sname']
        self.bid = body['bid']
        self.type = body.get("type", "bundle")
        self.schedules = [Schedule().make_with_dict(dict_data=single_schedule_data) for single_schedule_data in body.get("schedules", []) if single_schedule_data != ""]

class ModifySingleScheduleRequest(RequestHeader):
    def __init__(self, request):
        super().__init__(request)
        body:dict = request['body']
        self.sid = body['sid']
        self.sname = body['sname']
        self.bid = body.get('bid', "")
        self.start_date = body["start_date"]
        self.start_time = body["start_time"]
        self.end_date = body["end_date"]
        self.end_time = body["end_time"]
        self.state = body["state"]

class ModifyMultipleScheduleRequest(RequestHeader):
    def __init__(self, request) -> None:
        super().__init__(request)
        body:dict = request['body']
        self.sbid = body['sbid']
        self.sname = body['body']
        self.bid = body['bid']
        self.type = body.get("type", "bundle")
        self.schedules = [Schedule().make_with_dict(dict_data=single_schedule_data) for single_schedule_data in body.get("schedules", []) if single_schedule_data != ""]

class DeleteSingleScheduleRequest(RequestHeader):
    def __init__(self, sid) -> None:
        self.sid = sid

class DeleteScheduleBundleRequest(RequestHeader):
    def __init__(self, sbid) -> None:
        # self.email:str="alsrhks2508@naver.com"
        self.sbid = sbid



class SearchRequest(RequestHeader):
    def __init__(self, keyword, key=-1, search_type="", filter_option="") -> None:
        self.keyword=keyword
        self.key=key
        self.type=search_type
        self.filter_option=filter_option

class GetSchedulesRequest(RequestHeader):
    def __init__(self, request:dict)-> None:
        body:dict = request['body']
        self.sids=body.get('sids', [])
        
class AddNewScheduleRequest(RequestHeader):
    def __init__(self, sids=[])-> None:
        self.sids=sids

class AddNewEventRequest(RequestHeader):
    def __init__(self, seid) -> None:
        self.seid:str=seid
        
class SelectMyTimeTableRequest(RequestHeader):
    def __init__(self, date, bid)-> None:
        self.date=date
        self.bid=bid

class ScheduleRequest(RequestHeader):
    def __init__(self, sid)-> None:
        self.sid:str=sid

class ScheduleBundleRequest(RequestHeader):
    def __init__(self, sbid) -> None:
        self.sbid:str = sbid
    
class ScheduleWithBidRequest(RequestHeader):
    def __init__(self, bid, key)-> None:
        # self.email:str="alsrhks2508@naver.com"
        self.bid:str=bid
        self.key:int=key

class DateRequest(RequestHeader):
    def __init__(self, date)-> None:
        self.date:str = date
        
class TimeChartRequest(RequestHeader):
    def __init__(self, request):
        body:dict = request['body']
        self.date:str=body.get('date',datetime.now().strftime("%Y-%m-%d"))
        self.sids = body.get("sids", [])