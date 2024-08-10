from model import *
from others import UserNotExist, CustomError

class Core_Controller:
    def sample_func(self, database:Local_Database, request) -> BaseModel: 
        model = BaseModel(database=database)

        try:
            # 유저가 있는지 확인
            if not model.set_user_with_uid(request=request):
                raise UserNotExist("Can not find User with uid")
        except UserNotExist as e:
            print("Error Catched : ", e)
            model.set_state_code(e.error_code) # 종합 에러
            return model

        try:
            """
            if not model.set_biases_with_bids():
                model.set_state_code("210")
                return model
            """

        except CustomError as e:
            print("Error Catched : ", e.error_type)
            model.set_state_code(e.error_code) # 종합 에러

        except Exception as e:
            print("Error Catched : ", e.error_type)
            model.set_state_code(e.error_code) # 종합 에러

        finally:
            return model