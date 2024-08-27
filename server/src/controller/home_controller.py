from model import BannerModel, HomeBiasModel, BiasSearchModel, Local_Database, SelectBiasModel, LeagueMetaModel, TokenModel
from others import UserNotExist, CustomError
from controller.jwt_decoder import JWTManager, JWTPayload

class Home_Controller:
    # banner 데이터 요청
    def get_banner_data(self, database:Local_Database) -> BannerModel: 
        model = BannerModel(database=database)
        try:
            model.set_banner_data()
            model.set_state_code("204")
            return model

        except CustomError as e:
            print("Error Catched : ", e.error_type)
            model.set_state_code(e.error_code) # 종합 에러

        except Exception as e:
            print("Error Catched : ", e.error_type)
            model.set_state_code(e.error_code) # 종합 에러

        finally:
            return model
        
    # 홈 화면에서 토큰 발급  시도하는동작
    def get_token(self, database:Local_Database, token) -> TokenModel: 
        jwt_decoder = JWTManager()
        model = TokenModel(database=database)
        request_payload, new_token = jwt_decoder.home_decode(token=token)  # jwt payload(email 정보 포함됨)
        model.set_token_data(new_token=new_token)
        
        # 정상 토큰으로 로그인
        if request_payload.result:
            # 토큰이 아직 만료되지 않음
            if new_token == "":
                model.set_state_code("499")
                return model
            # 토큰이 만료되어 다시 만들어서 보내드림
            else:
                model.set_state_code("498")
                return model
        else:
            # 로그인 상태 이상(토큰에 장애가 있음)
            if new_token == "":
                model.set_state_code("497") 
                return model
    
    # 홈 화면의 bias 정보 
    def get_my_bias_data(self, database:Local_Database, request) -> HomeBiasModel: 
        jwt_decoder = JWTManager()
        request_payload = jwt_decoder.decode(token=request.token)  # jwt payload(email 정보 포함됨)

        model = HomeBiasModel(database=database)
        try:
            # 유저가 있는지 확인
            if not model.set_user_with_email(request=request_payload):
                raise UserNotExist("Can not find User with uid")
        except UserNotExist as e:
            print("Error Catched : ", e)
            model.set_state_code(e.error_code) # 종합 에러
            return model

        try:
            if not model.set_solo_bias_with_bid():
                model.set_state_code("210")

            if not model.set_group_bias_with_bid():
                model.set_state_code("211")
                return model
        except CustomError as e:
            print("Error Catched : ", e.error_type)
            model.set_state_code(e.error_code) # 종합 에러

        except Exception as e:
            print("Error Catched : ", e.error_type)
            model.set_state_code(e.error_code) # 종합 에러

        finally:
            return model

    def search_bias(self, database:Local_Database, request):
        model = BiasSearchModel(database=database)

        try:
            if not model.try_search_bias(request=request):
                model.set_state_code("210")

        except CustomError as e:
            print("Error Catched : ", e.error_type)
            model.set_state_code(e.error_code) # 종합 에러

        except Exception as e:
            print("Error Catched : ", e.error_type)
            model.set_state_code(e.error_code) # 종합 에러

        finally:
            return model

    def select_bias(self, database:Local_Database, request):
        jwt_decoder = JWTManager()
        request_payload = jwt_decoder.decode(token=request.token)  # jwt payload(email 정보 포함됨)

        model = SelectBiasModel(database=database)
        try:
            # 유저가 있는지 확인
            if not model.set_user_with_email(request=request_payload):
                raise UserNotExist("Can not find User with uid")
        except UserNotExist as e:
            print("Error Catched : ", e)
            model.set_state_code(e.error_code) # 종합 에러
            return model

        try:
            if not model.find_bias(request=request):
                model.set_state_code("209")
            if not model.set_my_bias():
                model.set_state_code("210")

        except CustomError as e:
            print("Error Catched : ", e.error_type)
            model.set_state_code(e.error_code) # 종합 에러

        except Exception as e:
            print("Error Catched : ", e.error_type)
            model.set_state_code(e.error_code) # 종합 에러

        finally:
            return model

    def get_league_meta_data(self, database:Local_Database, request):
        model = LeagueMetaModel(database=database)

        try:
            if not model.set_league(request=request):
                model.set_state_code("265")

        except CustomError as e:
            print("Error Catched : ", e.error_type)
            model.set_state_code(e.error_code) # 종합 에러

        except Exception as e:
            print("Error Catched : ", e.error_type)
            model.set_state_code(e.error_code) # 종합 에러

        finally:
            return model