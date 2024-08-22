from model import *
from others import UserNotExist, CustomError
from controller.jwt_decoder import JWTDecoder, JWTPayload

class Core_Controller:
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
        

        
    # 나의 바이어스 정보를 뽑아오는 방법
    def get_my_bias_league(self, database:Local_Database, request): 
        jwt_decoder = JWTDecoder()
        model = LeagueModel(database=database)  # 이건 안쓰지만 데이터 베이서 접속을 위해 사용
        try:
            request_payload = jwt_decoder.decode(token=request.token)  # jwt payload(email 정보 포함됨)

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


#----------check_page ------------------------------------------
    # check page 데이터
    # 여기서 부터는 최애인증을 check라고 정의함
    #1. 사용자인지 확인
    #2. 사용자가 팔로우 중인 bias 가 맞는지 확인
    #3. 이미 인증 했는지 확인  
    def get_check_page(self, database:Local_Database, request) -> BaseModel: 
        jwt_decoder = JWTDecoder()
        model = CheckPageModel(database=database)
        try:
            request_payload = jwt_decoder.decode(token=request.token)  # jwt payload(email 정보 포함됨)

            # 유저가 있는지 확인
            if not model.set_user_with_email(request=request_payload):
                raise UserNotExist("Can not find User with email")

        except UserNotExist as e:
            print("Error Catched : ", e)
            model.set_state_code(e.error_code) # 종합 에러
            return model

        try:

            # 타입에 맞는 bias 세팅
            model.set_bias(request)

            model.set_state_code("260")
            
            # 유저가 실제로 팔로우 하고 있는지 확인
            #if not model.is_validate_user():
                #model.set_state_code("261") # 종합 에러
                #return model

            model.check_page_info()

            # 이미 체크했는지 확인
            if not model.is_already_check():
                model = self._user_already_checked(database=database, model=model)
                model.set_state_code("261") # 종합 에러
                return model
            
        except CustomError as e:
            print("Error Catched : ", e.error_type)
            model.set_state_code(e.error_code) # 종합 에러

        finally:
            return model
        
    def _user_already_checked(self, database:Local_Database, model:CheckPageModel):
        new_model = TryCheckModel(database=database)
        # 일단 초기화 하고
        new_model.init_with_mother_model(model=model)

        self.__check_response_maker(model=new_model)

        return new_model

    def __check_response_maker(self, model:TryCheckModel): 
        # 명함 이미지 url 찍어주고
        model.set_name_card_url()
        # 혹시모르니 명함 이름도 주고
        model.set_name_card_name()
        # 특별시가 언제인지도 보내주고 (리스트로)
        model.get_special_check_time()
        # 공유전용 url 하나 파주고
        model.get_shared_url()
        # 특별시 인증 가능한지도 보고(이미 특별시 찍었는지 확인)
        model.is_special_time_check()

        return model

    def try_daily_check(self, database:Local_Database, request) -> BaseModel: 
        jwt_decoder = JWTDecoder()
        model = TryCheckModel(database=database)
        
        try:
            request_payload = jwt_decoder.decode(token=request.token)  # jwt payload(email 정보 포함됨)
            # 유저가 있는지 확인
            if not model.set_user_with_email(request=request_payload):
                raise UserNotExist("Can not find User with email")
        except UserNotExist as e:
            print("Error Catched : ", e)
            model.set_state_code(e.error_code) # 종합 에러
            return model

        try:
            # 타입에 맞는 bias 세팅
            model.set_bias(request)
            model.set_state_code("260")

            # 유저가 실제로 팔로우 하고 있는지 확인
            if not model.is_validate_user():
                model.set_state_code("261") # 종합 에러
                return model

            # 이미 체크했는지 확인
            if not model.is_already_check():
                model.set_result_invalid()
                model.set_state_code("261") # 종합 에러
                return model

            # 정보 만들기
            model.check_page_info()

            # 최애 인증
            model.try_daily_check()
            # 네임카드 만들고 업로드
            model.make_name_card()

            # 인증이랑 관련된 내용 만들기
            model = self.__check_response_maker(model=model)

        except CustomError as e:
            print("Error Catched : ", e.error_type)
            model.set_state_code(e.error_code) # 종합 에러

        finally:
            return model

    def try_special_check(self, database:Local_Database, request) -> BaseModel: 
        jwt_decoder = JWTDecoder()
        model = TrySpecialCheckModel(database=database)
        
        try:
            request_payload = jwt_decoder.decode(token=request.token)  # jwt payload(email 정보 포함됨)
            # 유저가 있는지 확인
            if not model.set_user_with_email(request=request_payload):
                raise UserNotExist("Can not find User with email")
        except UserNotExist as e:
            print("Error Catched : ", e)
            model.set_state_code(e.error_code) # 종합 에러
            return model

        try:
            # 타입에 맞는 bias 세팅
            model.set_bias(request)
            model.set_state_code("260")

            # 유저가 실제로 팔로우 하고 있는지 확인
            if not model.is_validate_user():
                model.set_state_code("261") # 종합 에러
                return model

            # 이미 체크했는지 확인
            if not model.is_already_check():
                model.set_state_code("264") # 이미 체크했는데 또 시도했네
                return model

            # 스페셜 타임인지 체크
            if not model.check_special_time():
                model.set_state_code("265")
                return model

            model.try_special_check()
            model.set_state_code("267")

        except CustomError as e:
            print("Error Catched : ", e.error_type)
            model.set_state_code(e.error_code) # 종합 에러

        finally:
            return model


#-----------채팅 시스템-----------------------------------------------------------
#--------------------------------------------------------------------------------
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
        
    def chatting(self, database:Local_Database, request):
        model = ChatModel(database=database)
        jwt_decoder = JWTDecoder()

        try:
            model.set_chat_data(request=request)  
            request_payload = jwt_decoder.decode(token=model.get_chat_data().token)  # jwt payload(email 정보 포함됨)

            # 유저가 있는지 확인       
            if not model.set_user_with_email(request=request_payload):
                raise UserNotExist("Can not find User with email")
        except UserNotExist as e:
            print("Error Catched : ", e)
            model.set_state_code(e.error_code) # 종합 에러
            return model

        try:
            model.check_item(request=model._user)
            model.save_chat(request=model._user)

        except CustomError as e:
            print("Error Catched : ", e.error_type)
            model.set_state_code(e.error_code) # 종합 에러

        finally:
            return model
        


class LeagueRequest():
    def __init__(self, league_name = None, league_id = None) -> None:
        self.league_name = league_name
        self.league_id = league_id