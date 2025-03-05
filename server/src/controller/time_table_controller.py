from view.jwt_decoder import JWTManager, JWTPayload, RequestManager
from model import Local_Database, BaseModel
from model import TimeTableModel, SingleScheduleModel, MultiScheduleModel


class TImeTableController:

# ----------------------------- HOME ROUTE CONTROLLER ----------------------------------------------------
    # TimeTable(일정) 데이터를 뽑아오는 보편적인 함수
    def get_dashboard_data(self, database:Local_Database, request:RequestManager) -> BaseModel: 
        model = TimeTableModel(database=database)
        
        if request.jwt_payload != "":
            model.set_user_with_email(request=request.jwt_payload)
            # 이건 뭔가 이상한 상황일때 그냥 모델 리턴하는거
            if not model._set_tuser_with_tuid():
                return model
        
        return model

    # 이벤트보드 불러오기
    def get_eventboard_data(self, database:Local_Database, request:RequestManager) -> BaseModel:
        model = EventTableModel(database=database)

        if request.jwt_payload != "":
            model.set_user_with_email(request=request.jwt_payload)
            # 이건 뭔가 이상한 상황일때 그냥 모델 리턴하는거
            if not model._set_tuser_with_tuid():
                return model

        return model

    # 오늘의 일정 차트를 불러오기
    def get_today_time_chart(self, database:Local_Database, request:RequestManager) -> BaseModel:
        model = TimeTableModel(database=database)

        if request.jwt_payload != "":
            model.set_user_with_email(request=request.jwt_payload)
            # 이건 뭔가 이상한 상황일때 그냥 모델 리턴하는거
            if not model._set_tuser_with_tuid():
                return model

        return model

    # 오늘의 일정 테이블을 불러옴
    def get_today_time_table(self, database:Local_Database, request:RequestManager) -> BaseModel:
        model = TimeTableModel(database=database)

        if request.jwt_payload != "":
            model.set_user_with_email(request=request.jwt_payload)
            # 이건 뭔가 이상한 상황일때 그냥 모델 리턴하는거
            if not model._set_tuser_with_tuid():
                return model

        return model

    # 바이어스 추천 리스트 ( 추천 주제 리스트 )
    def get_recommended_bias_list(self, database:Local_Database, request:RequestManager) -> BaseModel:
        model = TimeTableModel(database=database)

        if request.jwt_payload != "":
            model.set_user_with_email(request=request.jwt_payload)
            # 이건 뭔가 이상한 상황일때 그냥 모델 리턴하는거
            if not model._set_tuser_with_tuid():
                return model

        return model

# -------------------------------------------------------------------------------------------------------

# ------------------------------ SCHEDULE SEARCH ROUTE CONTROLLER ---------------------------------------
    # 타임 스케쥴 모델 검색하기
    def try_search_schedule(self, database:Local_Database, request:RequestManager) -> BaseModel:
        model = MultiScheduleModel(database=database)

        if request.jwt_payload != "":
            model.set_user_with_email(request=request.jwt_payload)
            # 이건 뭔가 이상한 상황일때 그냥 모델 리턴하는거
            if not model._set_tuser_with_tuid():
                return model

        return model

    # 일정 키워드 추천
    def try_get_recommend_keyword(self, database:Local_Database, request:RequestManager) -> BaseModel:
        model = MultiScheduleModel(database=database)

        if request.jwt_payload != "":
            model.set_user_with_email(request=request.jwt_payload)
            # 이건 뭔가 이상한 상황일때 그냥 모델 리턴하는거
            if not model._set_tuser_with_tuid():
                return model

        return model

# -------------------------------------------------------------------------------------------------------

# ---------------------------------- MY SCHEDULE ROUTE CONTROLLER ---------------------------------------
    # 스케쥴 추가하기
    def try_add_schedule(self, database:Local_Database, request:RequestManager) -> BaseModel:
        model = SingleScheduleModel(database=database)

        if request.jwt_payload != "":
            model.set_user_with_email(request=request.jwt_payload)
            # 이건 뭔가 이상한 상황일때 그냥 모델 리턴하는거
            if not model._set_tuser_with_tuid():
                return model

        return model

    # 이벤트 추가하기
    def try_add_event(self, database:Local_Database, request:RequestManager) -> BaseModel:
        model = SingleScheduleModel(database=database)

        if request.jwt_payload != "":
            model.set_user_with_email(request=request.jwt_payload)
            # 이건 뭔가 이상한 상황일때 그냥 모델 리턴하는거
            if not model._set_tuser_with_tuid():
                return model

        return model

    # 홈 화면에 노출될 스케쥴 띄우기
    def try_select_my_time_table_schedule(self, database:Local_Database, request:RequestManager) -> BaseModel:
        model = MultiScheduleModel(database=database)

        if request.jwt_payload != "":
            model.set_user_with_email(request=request.jwt_payload)
            # 이건 뭔가 이상한 상황일때 그냥 모델 리턴하는거
            if not model._set_tuser_with_tuid():
                return model

        return model

    # 선택한 스케쥴을 확인
    def try_search_my_schedule_with_bid(self, database:Local_Database, request:RequestManager) -> BaseModel:
        model = MultiScheduleModel(database=database)
        if request.jwt_payload != "":
            model.set_user_with_email(request=request.jwt_payload)
            if not model._set_tuser_with_tuid():
                return model
        return model

    # 선택한 스케쥴을 지우는 과정
    def try_reject_from_my_schedule(self, database:Local_Database, request:RequestManager) -> BaseModel:
        model = MultiScheduleModel(database=database)

        if request.jwt_payload != "":
            model.set_user_with_email(request=request.jwt_payload)
            # 이건 뭔가 이상한 상황일때 그냥 모델 리턴하는거
            if not model._set_tuser_with_tuid():
                return model

        return model

# -------------------------------------------------------------------------------------------------------

# ---------------------------------- MAKE SCHEDULE ROUTE CONTROLLER -------------------------------------
    # 단일 일정을 만들기
    def make_new_single_schedule(self, database:Local_Database, request:RequestManager) -> BaseModel:
        model = SingleScheduleModel(database=database)
        if request.jwt_payload != "":
            model.set_user_with_email(request=request.jwt_payload)
            # 이건 뭔가 이상한 상황일때 그냥 모델 리턴하는거
            if not model._set_tuser_with_tuid():
                return model

        return model

    # 복수 일정을 만들기
    def make_new_multi_schedule(self, database:Local_Database, request:RequestManager) -> BaseModel:
        model = MultiScheduleModel(database=database)
        if request.jwt_payload != "":
            model.set_user_with_email(request=request.jwt_payload)
            # 이건 뭔가 이상한 상황일때 그냥 모델 리턴하는거
            if not model._set_tuser_with_tuid():
                return model

        return model

    # 일정 수정하기
    def modify_schedule(self, database:Local_Database, request:RequestManager) -> BaseModel:
        model = SingleScheduleModel(database=database)
        if request.jwt_payload != "":
            model.set_user_with_email(request=request.jwt_payload)
            # 이건 뭔가 이상한 상황일때 그냥 모델 리턴하는거
            if not model._set_tuser_with_tuid():
                return model

        return model

    # 일정 삭제하기
    def delete_schedule(self, database:Local_Database, request:RequestManager) -> BaseModel:
        model = SingleScheduleModel(database=database)
        if request.jwt_payload != "":
            model.set_user_with_email(request=request.jwt_payload)
            # 이건 뭔가 이상한 상황일때 그냥 모델 리턴하는거
            if not model._set_tuser_with_tuid():
                return model

        return model
