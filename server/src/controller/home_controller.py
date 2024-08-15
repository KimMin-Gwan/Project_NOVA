from model import BannerModel, HomeBiasModel, BiasSearchModel, Local_Database, SelectBiasModel, LeagueMetaModel
from others import UserNotExist, CustomError
from controller.jwt_decoder import JWTDecoder, JWTPayload

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
    
    # 홈 화면의 bias 정보 
    def get_my_bias_data(self, database:Local_Database, request) -> HomeBiasModel: 
        jwt_decoder = JWTDecoder()
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
        jwt_decoder = JWTDecoder()
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