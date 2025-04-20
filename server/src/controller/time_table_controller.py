from cryptography.hazmat.primitives.serialization import load_ssh_private_key
from view.jwt_decoder import JWTManager, JWTPayload, RequestManager
from model import Local_Database, BaseModel , ScheduleChartModel
from model import TimeTableModel,  ScheduleRecommendKeywordModel
from model import MultiScheduleModel, AddScheduleModel
from others import ScheduleSearchEngine as SSE



class TImeTableController:
    # sid 리스트로 스케줄 데이터 뽑아내기
    def get_schedules_with_sids(self, database:Local_Database, request:RequestManager) -> BaseModel: 
        model = MultiScheduleModel(database=database)
        
        if request.jwt_payload!= "":
            model.set_user_with_email(request=request.jwt_payload)
            # 이건 뭔가 이상한 상황일때 그냥 모델 리턴하는거
            if not model._set_tuser_with_tuid():
                return model
        
        # 주제 수 찍어주면됨
        model.set_schedules_with_sids(data_payload=request.data_payload)
        return model

    # 타임 테이블 페이지의 최 상단 대시보드데이터
    # 파라미터 없음, 비로그인 상태에서는 0으로 리턴함 
    def get_dashboard_data(self, database:Local_Database, request:RequestManager) -> BaseModel: 
        model = TimeTableModel(database=database)
        
        if request.jwt_payload!= "":
            model.set_user_with_email(request=request.jwt_payload)
            # 이건 뭔가 이상한 상황일때 그냥 모델 리턴하는거
            if not model._set_tuser_with_tuid():
                return model
        
        # 주제 수 찍어주면됨
        model.set_num_bias()
        
        # 맨 위에 출력되는 문자열 이거임
        model.set_target_date(date= request.data_payload.date)
        
        return model


    # 내 타임 차트 가지고 오기
    def get_time_chart(self, database:Local_Database, request:RequestManager) -> BaseModel: 
        model = ScheduleChartModel(database=database)

        if request.jwt_payload!= "":
            model.set_user_with_email(request=request.jwt_payload)
            # 이건 뭔가 이상한 상황일때 그냥 모델 리턴하는거
            if not model._set_tuser_with_tuid():
                return model

        #if model.is_tuser_alive():
        model.set_my_schedule_in_by_day(target_date=request.data_payload.date)
            
        return model
    
    # 내 타임 차트 가지고 오기
    def get_time_chart_with_sids(self, database:Local_Database, request:RequestManager) -> BaseModel: 
        model = ScheduleChartModel(database=database)

        if request.jwt_payload!= "":
            model.set_user_with_email(request=request.jwt_payload)
            # 이건 뭔가 이상한 상황일때 그냥 모델 리턴하는거
            if not model._set_tuser_with_tuid():
                return model

        
        #if model.is_tuser_alive():
        model.set_my_schedule_in_by_day(target_date=request.data_payload.date, sids=request.data_payload.sids)
            
        return model



    # 추천하는 바이어스 불러오기
    def get_recommended_bias_list(self, database:Local_Database, request:RequestManager, num_recommend=5) -> BaseModel:
        model = MultiScheduleModel(database=database)

        if request.jwt_payload!= "":
            model.set_user_with_email(request=request.jwt_payload)
            if not model._set_tuser_with_tuid():
                return model

        model.get_recommend_bias_list(num_biases=num_recommend)

        return model

    # 스케줄 추가
    def try_add_schedule(self, database:Local_Database, request:RequestManager ) -> BaseModel:
        model = AddScheduleModel(database=database)

        if request.jwt_payload!= "":
            model.set_user_with_email(request=request.jwt_payload)
            # 이건 뭔가 이상한 상황일때 그냥 모델 리턴하는거
            if not model._set_tuser_with_tuid():
                return model
        else:
            return model

        model.add_schedule(sids=request.data_payload.sids)
        return model

    # 이벤트 추가하기
    def try_add_event(self, database:Local_Database, request:RequestManager) -> BaseModel:
        model = AddScheduleModel(database=database)
        if request.jwt_payload!= "":
            model.set_user_with_email(request=request.jwt_payload)
            # 이건 뭔가 이상한 상황일때 그냥 모델 리턴하는거
            if not model._set_tuser_with_tuid():
                return model
        else:
            return model

        model.add_event(seid=request.seid)
        return model

    # 내가 가진 스케줄에서 제외
    def try_reject_from_my_schedule(self, database:Local_Database, request:RequestManager) -> BaseModel:
        model = AddScheduleModel(database=database)

        if request.jwt_payload!= "":
            model.set_user_with_email(request=request.jwt_payload)
            # 이건 뭔가 이상한 상황일때 그냥 모델 리턴하는거
            if not model._set_tuser_with_tuid():
                return model

        model.reject_from_my_week_schedule(sid=request.data_payload.sid)
        return model



    # 이번주 타임테이블에 추가하기
    def try_select_my_time_table_schedule(self, schedule_search_engine:SSE, database:Local_Database, request:RequestManager) -> BaseModel:
        model = AddScheduleModel(database=database)
        
        if request.jwt_payload!= "":
            model.set_user_with_email(request=request.jwt_payload)
            # 이건 뭔가 이상한 상황일때 그냥 모델 리턴하는거
            if not model._set_tuser_with_tuid():
                return model
        else:
            return model
        
        model.select_schedule_in_showcase(schedule_search_engine=schedule_search_engine,
                                          date=request.data_payload.date, bid=request.data_payload.bid)
        
        return model

    # 내가 팔로우하고 있는 셀럽들의 출력용 폼 반환 함수
    def try_get_following_bias_printed_form(self, database:Local_Database, request:RequestManager) -> BaseModel:
        model = MultiScheduleModel(database=database)

        if request.jwt_payload!= "":
            model.set_user_with_email(request=request.jwt_payload)
            if not model._set_tuser_with_tuid():
                return model



        model.get_print_forms_bias()

        return model



    # 키워드를 통한 검색
    # 테스트 완료 (진짜)
    def try_search_schedule_with_keyword(self, schedule_search_engine:SSE, database:Local_Database,
                                         request:RequestManager, num_schedules=8) -> BaseModel:
        model = MultiScheduleModel(database=database)
        
        if request.jwt_payload!= "":
            model.set_user_with_email(request=request.jwt_payload)
            # 이건 뭔가 이상한 상황일때 그냥 모델 리턴하는거
            if not model._set_tuser_with_tuid():
                return model

        # 키워드를 넘겨 검색 후, 반환받음
        model.search_schedule_with_keyword(schedule_search_engine=schedule_search_engine,
                                            keyword=request.data_payload.keyword,
                                            search_type=request.data_payload.type,
                                            search_columns=request.data_payload.search_columns,
                                            when=request.data_payload.filter_option,
                                            last_index=request.data_payload.key,
                                            num_schedules=num_schedules)
        return model

    # 키워드를 통해 바이어스를 검색
    # 유이하게 Search Engine을 사용하지 않음
    def try_search_bias_with_keyword(self, database:Local_Database, request:RequestManager, num_biases=10) -> BaseModel:
        # model = TimeTableBiasModel(database=database)
        model = MultiScheduleModel(database=database)

        if request.jwt_payload!= "":
            model.set_user_with_email(request=request.jwt_payload)
            # 이건 뭔가 이상한 상황일때 그냥 모델 리턴하는거
            if not model._set_tuser_with_tuid():
                return model

        model.search_bias_with_keyword(keyword=request.data_payload.keyword,
                                       last_index=request.data_payload.key,
                                       num_biases=num_biases)

        return model



    # 스케줄 탐색 페이지에서 요청받는 데이터 처리
    def try_explore_schedule_with_category(self, schedule_search_engine:SSE, database:Local_Database,
                                           request:RequestManager, num_schedules:int=6) -> BaseModel:
        model = MultiScheduleModel(database=database)

        if request.jwt_payload!= "":
            model.set_user_with_email(request=request.jwt_payload)
            # 이건 뭔가 이상한 상황일때 그냥 모델 리턴하는거
            if not model._set_tuser_with_tuid():
                return model

        model.get_explore_schedule_with_category(schedule_search_engine=schedule_search_engine,
                                                 time_section=request.data_payload.time_section,
                                                 style=request.data_payload.style,
                                                 gender=request.data_payload.gender,
                                                 num_schedules=num_schedules,
                                                 last_index=request.data_payload.key
                                                 )
        # data_payload 참고해서 탐색하는 스케줄 데이터를 보내주면됨
        # 1. 카테고리에 따라 데이터 추출
        # 2. 필터에 따라 데이터 필터링
        # 3. 페이징에 따른 데이터 세팅

        # Data Payload
        # self.category:str=body.get("category", "") # category 는 따로 있을듯
        # self.key:int=body.get("key", -1)
        # self.time_section:int=body.get("timeSection", 0) # 0 -> 0~6 / 1 -> 6~12 / 2 -> 12~16 / 3 -> 16~24 / -1 -> 0~24(전체)
        # self.style:int=body.get("style", "all")  # all, vtuber, cam, nocam -> bias 데이터 (tags)
        # self.gender:int=body.get("gender", "all") # male, female, etc -> bias 데이터 (tags)

        return model

    # 인터페이스만 존재. 검색어 저장 시스템이 있어야 제대로 시스템이 구축 가능할 듯
    # 유이하게 Search Engine을 사용하지 않음
    def try_get_recommend_keyword(self, database:Local_Database, request:RequestManager, num_keywords=6) -> BaseModel:
        model = ScheduleRecommendKeywordModel(database=database)

        if request.jwt_payload!= "":
            model.set_user_with_email(request=request.jwt_payload)

        model.get_category_recommend(num_keywords=num_keywords)

        return model



    # 이번 주 일정을 들고 올 것 (전체에서)
    def try_get_weekday_schedules(self, schedule_search_engine:SSE, database:Local_Database, request:RequestManager) -> BaseModel:
        model = MultiScheduleModel(database=database)

        if request.jwt_payload!= "":
            model.set_user_with_email(request=request.jwt_payload)
            # 이건 뭔가 이상한 상황일때 그냥 모델 리턴하는거
            if not model._set_tuser_with_tuid():
                return model

        model.get_weekday_schedules(schedule_search_engine=schedule_search_engine)

        return model

    # 내가 선택한 일정을 들고 옴
    def try_get_my_selected_schedules(self,schedule_search_engine:SSE, database:Local_Database,
                                      request:RequestManager, num_schedules=6):
        model = MultiScheduleModel(database)

        if request.jwt_payload!= "":
            model.set_user_with_email(request=request.jwt_payload)
            if not model._set_tuser_with_tuid():
                return model

        model.get_my_selected_schedules(schedule_search_engine=schedule_search_engine,
                                        bid=request.data_payload.bid,
                                        last_index=request.data_payload.key,
                                        num_schedules=num_schedules)

        return model






    # 새로운 스케줄 만들기
    def make_new_single_schedule(self, schedule_search_engine:SSE, database:Local_Database, request:RequestManager) -> BaseModel:
        model = AddScheduleModel(database=database)
        
        if request.jwt_payload!= "":
            model.set_user_with_email(request=request.jwt_payload)
            # 이건 뭔가 이상한 상황일때 그냥 모델 리턴하는거
            if not model._set_tuser_with_tuid():
                return model

        schedule = model.make_new_single_schedule(data_payload=request.data_payload, bid=request.data_payload.bid)
        # 리스트로 넣어야됨(파라미터가 list를 받음)
        model.save_new_schedules(schedule_search_engine=schedule_search_engine, schedule=[schedule])
        return model
    
    # 스케줄 여러개 만들기
    def make_new_multiple_schedules(self, schedule_search_engine:SSE, database:Local_Database, request:RequestManager) -> BaseModel:
        model = AddScheduleModel(database=database)

        if request.jwt_payload!= "":
            model.set_user_with_email(request=request.jwt_payload)
            # 이건 뭔가 이상한 상황일때 그냥 모델 리턴하는거
            if not model._set_tuser_with_tuid():
                return model

        # model.set_user_with_email(request=request.data_payload)
        # model._set_tuser_with_tuid()

        schedule_object = model.make_new_multiple_schedule(schedule_search_engine=schedule_search_engine,
                                                           schedules=request.data_payload.schedules,
                                                           sname=request.data_payload.sname,
                                                           bid=request.data_payload.bid,
                                                           data_type=request.data_payload.type)

        model.save_new_multiple_schedule_object_with_type(schedule_search_engine=schedule_search_engine,
                                                          schedule_object=schedule_object,
                                                          data_type=request.data_payload.type)

        return model

    # 쁘띠 모델 변환기
    def get_schedule_printed_form(self, database:Local_Database, request:RequestManager) -> BaseModel:
        model = MultiScheduleModel(database=database)


        if request.jwt_payload!= "":
            model.set_user_with_email(request=request.jwt_payload)
            if not model._set_tuser_with_tuid():
                return model

        model.get_print_forms_schedule(schedules = request.data_payload.schedules,
                                        bid=request.data_payload.bid)

        return model

    # 작성한 스케줄 보내기
    # 하나만 가지고 오므로 Search Engine을 쓰지 않음
    def try_get_written_schedule(self, database:Local_Database, request:RequestManager):
        model = MultiScheduleModel(database)

        if request.jwt_payload!= "":
            model.set_user_with_email(request=request.jwt_payload)
            if not model._set_tuser_with_tuid():
                return model


        model.get_written_schedule(sid=request.data_payload.sid)

        return model

    # 작성한 스케줄 번들을 보내기
    # 하나만 가지고 오므로 Search Engine을 쓰지 않음
    def try_get_written_bundle(self, database:Local_Database, request:RequestManager):
        model = MultiScheduleModel(database)

        if request.jwt_payload!= "":
            model.set_user_with_email(request=request.jwt_payload)
            if not model._set_tuser_with_tuid():
                return model

        model.get_written_bundle(sbid=request.data_payload.sbid)

        return model

    # 단일 스케줄 편집
    def try_modify_single_schedule(self, schedule_search_engine:SSE, database:Local_Database, request:RequestManager):
        model = AddScheduleModel(database)

        if request.jwt_payload!= "":
            model.set_user_with_email(request=request.jwt_payload)
            if not model._set_tuser_with_tuid():
                return model

        schedule = model.modify_single_schedule(data_payload=request.data_payload, sid=request.data_payload.sid)
        model.save_modified_schedule(schedule_search_engine=schedule_search_engine, schedule=[schedule])

        return model

    # 스케줄 번들 편집
    def try_modify_bundle(self, schedule_search_engine:SSE, database:Local_Database, request:RequestManager):
        model = AddScheduleModel(database)

        if request.jwt_payload!= "":
            model.set_user_with_email(request=request.jwt_payload)
            if not model._set_tuser_with_tuid():
                return model

        # model.set_user_with_email(request=request.data_payload)
        # model._set_tuser_with_tuid()

        schedule_object = model.modify_multiple_schedule(schedule_search_engine=schedule_search_engine,
                                                         schedules=request.data_payload.schedules,
                                                         sname=request.data_payload.sname,
                                                         sbid=request.data_payload.sbid,
                                                         bid=request.data_payload.bid,
                                                         data_type=request.data_payload.type)

        model.save_modified_multiple_schedule_object_with_type(schedule_object=schedule_object, data_type=request.data_payload.type)

        return model



    # 스케줄 삭제
    def try_delete_schedule(self, schedule_search_engine:SSE, database:Local_Database, request:RequestManager):
        model = AddScheduleModel(database)

        if request.jwt_payload!= "":
            model.set_user_with_email(request=request.jwt_payload)
            if not model._set_tuser_with_tuid():
                return model

        model.delete_schedule(schedule_search_engine=schedule_search_engine, sid=request.data_payload.sid)

        return model

    # 스케줄 번들 삭제
    def try_delete_bundle(self, schedule_search_engine:SSE, database:Local_Database, request:RequestManager):
        model = AddScheduleModel(database)

        if request.jwt_payload!= "":
            model.set_user_with_email(request=request.jwt_payload)
            if not model._set_tuser_with_tuid():
                return model

        model.delete_bundle(schedule_search_engine=schedule_search_engine, sbid=request.data_payload.sbid)

        return model


    # 오늘의 이벤트 뽑기
    # def get_eventboard_data(self, database:Local_Database, request:RequestManager) -> BaseModel:
    #     model = MultiScheduleModelNew(database=database)
    #
    #     if request.jwt_payload!= "":
    #         model.set_user_with_email(request=request.jwt_payload)
    #         # 이건 뭔가 이상한 상황일때 그냥 모델 리턴하는거
    #         if not model._set_tuser_with_tuid():
    #             return model
    #
    #
    #     if model.is_tuser_alive():
    #         model.set_my_event_in_by_day(date=request.data_payload.date)
    #     else:
    #         model.set_event_in_by_day(date=request.data_payload.date)
    #
    #     return model
