from model import *
from others import CustomError
class Administrator_Controller:
    def reset_leagues_point(self, database:Local_Database,requset): 
        model = ResetLeaguesModel(database=database)

        try:
            if not model.check_admin_key(request=requset):
                return model
            
            model.upload_data()

            if not model.set_users():
                return model
            
            if not model.set_biases():
                return model
            
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