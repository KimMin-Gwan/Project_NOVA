from model import *
from others import UserNotExist, CustomError
from controller.jwt_decoder import JWTDecoder, JWTPayload

class Sub_Controller:
    def sample_func(self, database:Local_Database, request) -> BaseModel: 
        jwt_decoder = JWTDecoder()
        model = BaseModel(database=database)
        try:

            request_payload = jwt_decoder.decode(token=request.token)  # jwt payload(email 정보 포함됨)

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
        
    # 최애 페이지의 배너 정보
    # 배너가 없으면 뭘 보여줄래?
    def get_bias_banner(self, database:Local_Database, request) -> BaseModel: 
        jwt_decoder = JWTDecoder()
        model = BaseModel(database=database)

        try:
            request_payload = jwt_decoder.decode(token=request.token)  # jwt payload(email 정보 포함됨)

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

    # 최애 페이지의 지지자 기여도 랭크 
    def get_user_contribution(self, database:Local_Database, request) -> UserContributionModel: 
        model = UserContributionModel(database=database)

        try:
            if not model.set_bias_data(request=request):
                model.set_state_code("571") # 실패하면 571
                return model


            # 유저 데이터들 만들기
            if not model.set_user_datas():
                model.set_state_code("572") # 실패하면 572
                return model

            if not model.set_user_alignment():
                model.set_state_code("573") # 실패하면 573
                return model

        except CustomError as e:
            print("Error Catched : ", e.error_type)
            model.set_state_code(e.error_code) # 종합 에러

        except Exception as e:
            print("Error Catched : ", e.error_type)
            model.set_state_code(e.error_code) # 종합 에러

        finally:
            return model

    # 최애 페이지의 지지자 기여도 랭크 
    def get_my_contribution(self, database:Local_Database, request) -> MyContributionModel: 
        jwt_decoder = JWTDecoder()
        model = MyContributionModel(database=database)

        try:
            request_payload = jwt_decoder.decode(token=request.token)  # jwt payload(email 정보 포함됨)
            if not model.set_user_with_email(request=request_payload):
                raise UserNotExist("Can not find User with uid")
        except UserNotExist as e:
            print("Error Catched : ", e)
            model.set_state_code(e.error_code) # 종합 에러
            return model

        try:
            if not model.set_bias_data(request=request):
                model.set_state_code("571") # 실패하면 571
                return model
            
            if not model.is_my_bias():
                model.set_state_code("274") # 실패하면 271
                return model

            # 유저 데이터들 만들기
            if not model.set_user_datas():
                model.set_state_code("572") # 실패하면 572
                return model

            if not model.set_user_alignment():
                model.set_state_code("573") # 실패하면 573
                return model

        except CustomError as e:
            print("Error Catched : ", e.error_type)
            model.set_state_code(e.error_code) # 종합 에러

        except Exception as e:
            print("Error Catched : ", e.error_type)
            model.set_state_code(e.error_code) # 종합 에러

        finally:
            return model


        

        