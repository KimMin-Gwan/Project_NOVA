from model import BannerModel, HomeBiasModel, BiasSearchModel, Local_Database, SelectBiasModel, LeagueMetaModel, TokenModel
from others import UserNotExist, CustomError
#from server.src.view.jwt_decoder import JWTManager, JWTPayload
#from view import RequestManager

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
    def get_token(self, database:Local_Database) -> TokenModel: 
        model = TokenModel(database=database)
        return model
    
    # 홈 화면의 bias 정보 
    def get_my_bias_data(self, database:Local_Database, request) -> HomeBiasModel: 
        model = HomeBiasModel(database=database)
        try:
            # 유저가 있는지 확인

            if not model.set_user_with_email(request=request.jwt_payload):
                raise UserNotExist("Can not find User with email")
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
        model = SelectBiasModel(database=database)
        try:
            print("0")
            # 유저가 있는지 확인
            model.set_user_with_email(request=request.jwt_payload)
            print("1")
            if not model.find_bias(request=request.data_payload):
                model.set_state_code("209")
            print("2")
            if not model.set_my_bias():
                model.set_state_code("210")
            print("3")

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