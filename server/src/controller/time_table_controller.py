from view.jwt_decoder import JWTManager, JWTPayload, RequestManager
from model import Local_Database, BaseModel
from model import TimeTableModel


class TImeTableController:
    # league 데이터를 뽑아오는 보편적인 함수
    def get_dashboard_data(self, database:Local_Database, request:RequestManager) -> BaseModel: 
        model = TimeTableModel(database=database)
        
        if request.jwt_payload != "":
            model.set_user_with_email(request=request.jwt_payload)
            # 이건 뭔가 이상한 상황일때 그냥 모델 리턴하는거
            if not model._set_tuser_with_tuid():
                return model
        
        
        
        
        

        return model