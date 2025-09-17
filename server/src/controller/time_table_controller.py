from view.jwt_decoder import RequestManager
from model import Mongo_Database, BaseModel , ScheduleTimeLayerModel
from model import TimeTableModel
from model import MultiScheduleModel, AddScheduleModel
from others import ScheduleSearchEngine as SSE

from datetime import datetime


class TimeTableController:
    # sid 리스트로 스케줄 데이터 뽑아내기
    def get_schedules_with_sids(self, database:Mongo_Database, request:RequestManager) -> BaseModel: 
        model = MultiScheduleModel(database=database)
        
        if request.jwt_payload!= "":
            model.set_user_with_email(request=request.jwt_payload)
        
        # 주제 수 찍어주면됨
        model.set_schedules_with_sids(data_payload=request.data_payload)
        return model

    # 타임 테이블 페이지의 최 상단 대시보드데이터
    # 파라미터 없음, 비로그인 상태에서는 0으로 리턴함 
    def get_dashboard_data(self, database:Mongo_Database, request:RequestManager, schedule_search_engine:SSE) -> BaseModel: 
        model = TimeTableModel(database=database)
        
        if request.jwt_payload!= "":
            model.set_user_with_email(request=request.jwt_payload)
        
        # 주제 수 찍어주면됨
        #model.set_num_bias()
        model.set_num_schedule(schedule_search_engine=schedule_search_engine)
        
        # 맨 위에 출력되는 문자열 이거임
        model.set_target_date(date= request.data_payload.date)
        
        return model


    # 내 타임 차트 가지고 오기
    def get_time_layer_with_date(self, database:Mongo_Database, schedule_search_engine:SSE, request:RequestManager) -> BaseModel: 
        model = ScheduleTimeLayerModel(database=database)

        if request.jwt_payload!= "":
            model.set_user_with_email(request=request.jwt_payload)

        model.make_my_schedule_data(target_date=request.data_payload.date,
                                 schedule_search_engine=schedule_search_engine)
        model.set_my_schedule_layer()
        
        
        target_date = datetime.strptime(request.data_payload.date, "%Y/%m/%d")
        
        if datetime.today().date() <= target_date.date():
            if model.make_recommand_schedule_data(): # 추천 스케줄 데이터 생성
                model.set_recommand_schedule_layer() # 추천 스케줄 레이어 생성
        
        model.change_layer_form()
            
        return model


    # 스케줄 추가
    def try_add_schedule(self, database:Mongo_Database, request:RequestManager ) -> BaseModel:
        model = AddScheduleModel(database=database)

        if request.jwt_payload!= "":
            model.set_user_with_email(request=request.jwt_payload)
        else:
            return model

        model.add_schedule(sids=request.data_payload.sids)
        return model


    # 내가 가진 스케줄에서 제외
    def try_reject_from_my_schedule(self, database:Mongo_Database, request:RequestManager) -> BaseModel:
        model = AddScheduleModel(database=database)

        if request.jwt_payload!= "":
            model.set_user_with_email(request=request.jwt_payload)

        model.reject_from_my_week_schedule(sid=request.data_payload.sid)
        return model


    # 내가 팔로우하고 있는 셀럽들의 출력용 폼 반환 함수
    def try_get_following_bias_printed_form(self, database:Mongo_Database, request:RequestManager) -> BaseModel:
        model = MultiScheduleModel(database=database)

        if request.jwt_payload!= "":
            model.set_user_with_email(request=request.jwt_payload)
            if not model._set_tuser_with_tuid():
                return model

        model.get_print_forms_my_bias()

        return model


    # 키워드를 통한 검색
    # 테스트 완료 (진짜)
    def try_search_schedule_with_keyword(self, schedule_search_engine:SSE, database:Mongo_Database,
                                         request:RequestManager, num_schedules=8) -> BaseModel:
        model = MultiScheduleModel(database=database)
        
        if request.jwt_payload!= "":
            model.set_user_with_email(request=request.jwt_payload)

        # 키워드를 넘겨 검색 후, 반환받음
        model.search_schedule_with_keyword(schedule_search_engine=schedule_search_engine,
                                            keyword=request.data_payload.keyword,
                                            search_columns=request.data_payload.search_columns,
                                            when=request.data_payload.filter_option,
                                            last_index=request.data_payload.key,
                                            num_schedules=num_schedules)
        return model


    # 스케줄 탐색 페이지에서 요청받는 데이터 처리
    def try_explore_schedule_with_category(self, schedule_search_engine:SSE, database:Mongo_Database,
                                           request:RequestManager, num_schedules:int=6) -> BaseModel:
        model = MultiScheduleModel(database=database)

        if request.jwt_payload!= "":
            model.set_user_with_email(request=request.jwt_payload)

        model.get_explore_schedule_with_category(schedule_search_engine=schedule_search_engine,
                                                 time_section=request.data_payload.time_section,
                                                 style=request.data_payload.style,
                                                 gender=request.data_payload.gender,
                                                 num_schedules=num_schedules,
                                                 last_index=request.data_payload.key,
                                                 category=request.data_payload.category
                                                 )
        return model
    
    # 해당 bias 의 스케줄을 월 단위로 반환
    def get_monthly_bias_schedule(self, schedule_search_engine:SSE, database:Mongo_Database, request:RequestManager) -> BaseModel:
        model = MultiScheduleModel(database=database)
        
        if request.jwt_payload!= "":
            model.set_user_with_email(request=request.jwt_payload)
        else:
            return model
            
        if not model.set_bias_data(bid=request.data_payload.bid):
            return model
        
        model.set_schedule_in_monthly(schedule_search_engine=schedule_search_engine,
                                            date=request.data_payload.date)
        return model


    # 새로운 스케줄 만들기
    def make_new_single_schedule(self, schedule_search_engine:SSE, database:Mongo_Database, request:RequestManager) -> BaseModel:
        model = AddScheduleModel(database=database)
        
        if request.jwt_payload!= "":
            model.set_user_with_email(request=request.jwt_payload)
        
            
            
        schedule = model.make_new_single_schedule(request_schedule=request.data_payload.schedule)

        if schedule is None:
            return model
        
        if request.data_payload.schedule.sid:
            schedule, result = model.verifiy_modifying_schedule(schedule=schedule, sid=request.data_payload.schedule.sid)
            if result:
                model.update_modify_schedule()
        else:
            # 해당 날짜에 이미 다른 스케줄이 있는지 검증
            if model.check_schedule_not_in_time(schedule_search_engine=schedule_search_engine, schedule=schedule):
                model.save_new_schedule(schedule_search_engine=schedule_search_engine, schedule=schedule)
        return model
    

    # 쁘띠 모델 변환기
    def get_schedule_printed_form(self, database:Mongo_Database, request:RequestManager) -> BaseModel:
        model = MultiScheduleModel(database=database)


        if request.jwt_payload!= "":
            model.set_user_with_email(request=request.jwt_payload)

        model.get_print_forms_schedule(schedules = request.data_payload.schedules,
                                        bid=request.data_payload.bid)

        return model

    # 작성한 스케줄 보내기
    # 하나만 가지고 오므로 Search Engine을 쓰지 않음
    def try_get_written_schedule(self, database:Mongo_Database, request:RequestManager):
        model = MultiScheduleModel(database)

        if request.jwt_payload!= "":
            model.set_user_with_email(request=request.jwt_payload)

        model.get_written_schedule(sid=request.data_payload.sid)
        return model


    # 단일 스케줄 편집
    def try_modify_single_schedule(self, schedule_search_engine:SSE, database:Mongo_Database, request:RequestManager):
        model = AddScheduleModel(database)

        if request.jwt_payload!= "":
            model.set_user_with_email(request=request.jwt_payload)

        schedule = model.modify_single_schedule(schedule=request.data_payload.schedule)
        model.save_modified_schedule(schedule_search_engine=schedule_search_engine, schedules=[schedule])

        return model

    # 스케줄 삭제
    def try_delete_schedule(self, schedule_search_engine:SSE, database:Mongo_Database, request:RequestManager):
        model = AddScheduleModel(database)

        if request.jwt_payload!= "":
            model.set_user_with_email(request=request.jwt_payload)

        model.delete_schedule(schedule_search_engine=schedule_search_engine, sid=request.data_payload.sid)

        return model

