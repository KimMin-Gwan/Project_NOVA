from view.jwt_decoder import JWTManager, JWTPayload, RequestManager
from model import Local_Database, BaseModel 
from model import TimeTableModel, MultiSchduleModel, AddScheduleModel


class TImeTableController:
    
    # 타임 테이블 페이지의 최 상단 대시보드데이터
    # 파라미터 없음, 비로그인 상태에서는 0으로 리턴함 
    def get_dashboard_data(self, database:Local_Database, request:RequestManager) -> BaseModel: 
        model = TimeTableModel(database=database)
        
        if request.jwt_payload != "":
            model.set_user_with_email(request=request.jwt_payload)
            # 이건 뭔가 이상한 상황일때 그냥 모델 리턴하는거
            if not model._set_tuser_with_tuid():
                return model
        
        # 주제 수 찍어주면됨
        model.set_num_bias()
        
        # 맨 위에 출력되는 문자열 이거임
        model.set_target_date()
        
        return model
    
    # 오늘의 이벤트 뽑기
    def get_eventboard_data(self, database:Local_Database, request:RequestManager) -> BaseModel: 
        model = MultiSchduleModel(database=database)
        
        if request.jwt_payload != "":
            model.set_user_with_email(request=request.jwt_payload)
            # 이건 뭔가 이상한 상황일때 그냥 모델 리턴하는거
            if not model._set_tuser_with_tuid():
                return model
            
        
        if model.is_tuser_alive():
            model.set_my_event_in_by_day(date=request.data_payload.date)
        else:
            model.set_event_in_by_day(date=request.data_payload.date)
        
        return model
    
    # 내 타임 차트 가지고 오기
    def get_time_chart(self, database:Local_Database, request:RequestManager) -> BaseModel: 
        model = MultiSchduleModel(database=database)
        
        if request.jwt_payload != "":
            model.set_user_with_email(request=request.jwt_payload)
            # 이건 뭔가 이상한 상황일때 그냥 모델 리턴하는거
            if not model._set_tuser_with_tuid():
                return model

        if model.is_tuser_alive():
            model.set_my_schedule_in_by_day(date=request.data_payload.date)
        else:
            model.set_schedule_in_by_day(date=request.data_payload.date)
        
        return model
    
    # 내 타임테이블 불러오기
    def get_my_time_table(self, database:Local_Database, request:RequestManager) -> BaseModel: 
        model = MultiSchduleModel(database=database)
        
        if request.jwt_payload != "":
            model.set_user_with_email(request=request.jwt_payload)
            # 이건 뭔가 이상한 상황일때 그냥 모델 리턴하는거
            if not model._set_tuser_with_tuid():
                return model
        else:
            return model # 여기 return을 지우면됨       ---

        # 당장에는 로그인 안하면 보내줄 데이터는 없다!
        # 나중에 뭐 추가로 노출 시켜주고 싶으면 위에 return 을 지우고 아래에
        # 비로그인 사용자를 대상으로 하는 로직을 넣어라
        
        # 자동으로 노출 schedule 지우는거 옵션을 나중에 넣어주면 여기 추가하면됨
        model.set_schedule_by_this_week()

        return model

    # 스케줄 추가
    def try_add_schedule(self, database:Local_Database, request:RequestManager) -> BaseModel: 
        model = AddScheduleModel(database=database)
        
        if request.jwt_payload != "":
            model.set_user_with_email(request=request.jwt_payload)
            # 이건 뭔가 이상한 상황일때 그냥 모델 리턴하는거
            if not model._set_tuser_with_tuid():
                return model
        else:
            return model 
        
        model.add_schedule(sids=request.sids)
        return model
    
    # 이벤트 추가
    def try_add_event(self, database:Local_Database, request:RequestManager) -> BaseModel: 
        model = AddScheduleModel(database=database)
        if request.jwt_payload != "":
            model.set_user_with_email(request=request.jwt_payload)
            # 이건 뭔가 이상한 상황일때 그냥 모델 리턴하는거
            if not model._set_tuser_with_tuid():
                return model
        else:
            return model 
        
        model.add_event(seid=request.seid)
        return model
    
    def try_add_event(self, database:Local_Database, request:RequestManager) -> BaseModel: 
        model = AddScheduleModel(database=database)
        if request.jwt_payload != "":
            model.set_user_with_email(request=request.jwt_payload)
            # 이건 뭔가 이상한 상황일때 그냥 모델 리턴하는거
            if not model._set_tuser_with_tuid():
                return model
        else:
            return model 
        
        model.add_event(seid=request.seid)
        return model

    # 키워드를 통한 검색
    def try_search_schedule_with_keyword(self, database:Local_Database, request:RequestManager,
                                         num_schedules=8) -> BaseModel:
        model = MultiSchduleModel(database=database)

        if request.jwt_payload != "":
            model.set_user_with_email(request=request.jwt_payload)
            # 이건 뭔가 이상한 상황일때 그냥 모델 리턴하는거
            if not model._set_tuser_with_tuid():
                return model

        # 키워드를 넘겨 검색 후, 반환받음
        model.try_search_schedule_with_keyword(keyword=request.data_payload.keyword,
                                               type=request.data_payload.type,
                                                last_index=request.data_payload.key,
                                                num_schedules=num_schedules)
        return model

    # 인터페이스만 존재. 검색어 저장 시스템이 있어야 제대로 시스템이 구축 가능할 듯
    def try_get_recommend_keyword(self, database:Local_Database, request:RequestManager, num_keywords=5) -> BaseModel:
        model = MultiSchduleModel(database=database)
        if request.jwt_payload != "":
            model.set_user_with_email(request=request.jwt_payload)
            # 이건 뭔가 이상한 상황일때 그냥 모델 리턴하는거
            if not model._set_tuser_with_tuid():
                return model
        return model