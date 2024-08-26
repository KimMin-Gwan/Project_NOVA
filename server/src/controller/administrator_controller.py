from model import *
from others import CustomError
class Administrator_Controller:
    def reset_leagues_point(self, database:Local_Database,requset): 
        model = ResetLeaguesModel(database=database)

        try:
            #관리자 키 확인
            if not model.check_admin_key(request=requset):
                return model
            #json 업로드
            model.upload_data()
            #유저 불러오기
            if not model.set_users():
                return model
            #bias 불러오기
            if not model.set_biases():
                return model
            #포인트,콤보 초기화
            if not model.reset_point():
                return model
            
        except CustomError as e:
            print("Error Catched : ", e.error_type)
            model.set_state_code(e.error_code) # 종합 에러

        except Exception as e:
            print("Error Catched : ", e.error_type)
            model.set_state_code(e.error_code) # 종합 에러

        finally:
            return model