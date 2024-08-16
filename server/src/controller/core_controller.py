from model import *
from others import UserNotExist, CustomError
from controller.jwt_decoder import JWTDecoder, JWTPayload

class Core_Controller:
    def sample_func(self, database:Local_Database, request) -> BaseModel: 
        jwt_decoder = JWTDecoder()
        request_payload = jwt_decoder.decode(token=request.token)  # jwt payload(email 정보 포함됨)

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
        

        
    # 나의 바이어스 정보를 뽑아오는 방법
    def get_my_bias_league(self, database:Local_Database, request): 
        jwt_decoder = JWTDecoder()
        request_payload = jwt_decoder.decode(token=request.token)  # jwt payload(email 정보 포함됨)

        model = LeagueModel(database=database)  # 이건 안쓰지만 데이터 베이서 접속을 위해 사용
        try:
            # 유저가 있는지 확인
            if not model.set_user_with_email(request=request_payload):
                raise UserNotExist("Can not find User with uid")
        except UserNotExist as e:
            print("Error Catched : ", e)
            model.set_state_code(e.error_code) # 종합 에러
            return model

        try:
            # 리그 타입이 솔로인지 그룹인지 확인
            if request.league_type == "solo":
                target_bid = model.get_user().solo_bid
            elif request.league_type == "group":
                target_bid = model.get_user().solo_bid
            else:
                return model # 구분이 안되면 그냥 냅다 반환시켜버려 

            model.set_bias_data(bid=target_bid)  # 목표 리그를 찾아야해서 bias 부터 검색
            new_request = LeagueRequest(league_id=model.get_bias().lid)  # 목표 리그의 lid 가지고옴
            model = self.get_league(database=database, request=new_request)

        except CustomError as e:
            print("Error Catched : ", e.error_type)
            model.set_state_code(e.error_code) # 종합 에러

        except Exception as e:
            print("Error Catched : ", e.error_type)
            model.set_state_code(e.error_code) # 종합 에러

        finally:
            return model

    # league 데이터를 뽑아오는 보편적인 함수
    def get_league(self, database:Local_Database, request) -> BaseModel: 
        model = LeagueModel(database=database)
        try:
            model.set_leagues(request)
            model.set_biases()
            model.set_list_alignment()

        except CustomError as e:
            print("Error Catched : ", e.error_type)
            model.set_state_code(e.error_code) # 종합 에러

        finally:
            return model
        

    # -----------------------------------------------------------------------


    # 최애 인증 요청 용 컨트롤러 함수
    def requese_daily_check(self, database:Local_Database, request) -> BaseModel: 
        model = RequestDailyCheck(database=database)
        
        try:
            # 유저가 있는지 확인
            if not model.set_user_with_email(request=request):
                raise UserNotExist("Can not find User with email")
        except UserNotExist as e:
            print("Error Catched : ", e)
            model.set_state_code(e.error_code) # 종합 에러
            return model

        try:
            model.request_daily(model._user)
            model.add_solo_bias_point(model._user.solo_bid)
            model.add_group_bias_point(model._user.group_bid)

            

        except CustomError as e:
            print("Error Catched : ", e.error_type)
            model.set_state_code(e.error_code) # 종합 에러

        finally:
            return model

    def request_login(self, database:Local_Database, request) -> BaseModel: 
        model = RequestLogin(database=database)

        try:
            # 유저가 있는지 확인
            if not model.set_user_with_email(request=request):
                raise UserNotExist("Can not find User with uid")
        except UserNotExist as e:
            print("Error Catched : ", e)
            model.set_state_code(e.error_code) # 종합 에러
            return model

        try:
            model.request_login(request=request,token=model._user.token)

        except CustomError as e:
            print("Error Catched : ", e.error_type)
            model.set_state_code(e.error_code) # 종합 에러

        finally:
            return model

#------------------------------------------------------------------------------------------
    def get_chatting_data(self, database:Local_Database):
        model = ChatListModel(database=database)
        try:
            model.set_chat_list()
            model.set_state_code("200")
            return model

        except CustomError as e:
            print("Error Catched : ", e.error_type)
            model.set_state_code(e.error_code) # 종합 에러

        except Exception as e:
            print("Error Catched : ", e.error_type)
            model.set_state_code(e.error_code) # 종합 에러

        finally:
            return model
        
    # def chatting(self, database:Local_Database, request): 
    #     jwt_decoder = JWTDecoder()
    #     model = ChatModel(database=database)
    #     data = json.loads(request)

    #     try:
    #         # 유저가 있는지 확인           
    #         request_payload = jwt_decoder.decode(token=data)
    #         if not model.set_user_with_email(request=request_payload):
    #             raise UserNotExist("Can not find User with email")
    #     except UserNotExist as e:
    #         print("Error Catched : ", e)
    #         model.set_state_code(e.error_code) # 종합 에러
    #         return model

    #     try:
    #         model.set_chat_data(request=request_payload)
    #         model.save_chat(request=request_payload)
    #         model.load_chat()

    #     except CustomError as e:
    #         print("Error Catched : ", e.error_type)
    #         model.set_state_code(e.error_code) # 종합 에러

    #     finally:
    #         return model
        


class LeagueRequest():
    def __init__(self, league_name = None, league_id = None) -> None:
        self.league_name = league_name
        self.league_id = league_id