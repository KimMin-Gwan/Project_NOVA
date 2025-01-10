from model import *
from others import UserNotExist, CustomError
from view.jwt_decoder import JWTManager, JWTPayload
from others import CheckManager


class Core_Controller:
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
        

#----------check_page ------------------------------------------
    # check page 데이터
    # 여기서 부터는 최애인증을 check라고 정의함
    #1. 사용자인지 확인
    #2. 사용자가 팔로우 중인 bias 가 맞는지 확인
    #3. 이미 인증 했는지 확인  
    def get_check_page(self, database:Local_Database, request) -> BaseModel: 
        model = CheckPageModel(database=database)
        try:
            model.set_user_with_email(request=request.jwt_payload)
            # 타입에 맞는 bias 세팅
            model.set_bias(request.data_payload)

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
            else:
                model.set_result_valid()
            
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

        # 특별시 인증 했는지 확인
        model.is_already_special_check()

        return model

    def try_daily_check(self, database:Local_Database, request, league_manager) -> BaseModel: 
        model = TryCheckModel(database=database)
        try:
            model.set_user_with_email(request=request.jwt_payload)
            # 타입에 맞는 bias 세팅
            model.set_bias(request.data_payload)
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


            # 최애 인증
            model.try_daily_check(league_manager=league_manager)

            # 정보 만들기
            model.check_page_info()

            # 네임카드 만들고 업로드
            model.make_name_card()

            # 특별시 인증 했는지 확인

            # 인증이랑 관련된 내용 만들기
            model = self.__check_response_maker(model=model)


        except CustomError as e:
            print("Error Catched : ", e.error_type)
            model.set_state_code(e.error_code) # 종합 에러

        finally:
            return model

    def try_special_check(self, database:Local_Database, request, league_manager) -> BaseModel: 
        model = TrySpecialCheckModel(database=database)
        
        try:
            # 타입에 맞는 bias 세팅
            model.set_user_with_email(request=request.jwt_payload)
            model.set_bias(request.data_payload)
            model.set_state_code("260")

            # 유저가 실제로 팔로우 하고 있는지 확인
            if not model.is_validate_user():
                model.set_state_code("261") # 종합 에러
                return model

            # 이미 체크했는지 확인
            if not model.is_already_special_check():
                model.set_state_code("264") # 이미 체크했는데 또 시도했네
                return model

            # 스페셜 타임인지 체크
            if not model.check_special_time():
                model.set_state_code("265")
                return model

            model.try_special_check(league_manager=league_manager)
            model.set_state_code("267")

            # 인증이랑 관련된 내용 만들기
            model = self.__check_response_maker(model=model)

        except CustomError as e:
            print("Error Catched : ", e.error_type)
            model.set_state_code(e.error_code) # 종합 에러

        finally:
            return model
        
    def get_shared_url(self, database, request):
        # URL을 동적으로 생성
        url = f"https://kr.object.ncloudstorage.com/nova-name-card/{request}.png"
        
        # HTML 템플릿에서 URL을 반영
        html = f"""
        <!DOCTYPE html>
        <html lang="ko">

        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>최애 인증하기</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    margin: 0;
                    padding: 0;
                    text-align: center;
                    width: 500px;
                    margin: 0 auto;
                }}

                h1 {{
                    font-size: 18px;
                    margin-bottom: 20px;
                    font-weight: normal;
                }}

                .card {{
                    background-color: #e0e0e0;
                    padding: 20px;
                    border-radius: 10px;
                    position: relative;
                }}

                .card h2 {{
                    margin: 0;
                    font-size: 20px;
                    margin-bottom: 10px;
                }}

                .card a {{
                    display: block;
                    width: 100%;
                    height: 200px;
                    background-color: #d0d0d0;
                    border-radius: 10px;
                    text-align: center;
                    overflow: hidden;
                }}

                .card img {{
                    width: 100%;
                    height: 100%;
                    object-fit: cover;
                    border-radius: 10px;
                }}

                .card span {{
                    display: block;
                    margin-top: 10px;
                    color: #999;
                }}

                .Header {{
                    height: 70px;
                    width: 100%;
                    border-bottom: 1px solid #000000;
                    text-align: center;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                }}

                .ad-placeholder {{
                    background-color: #d0d0d0;
                    padding: 20px;
                    margin-top: 20px;
                    font-size: 16px;
                    color: #666;
                }}
            </style>
        </head>

        <body>
            <div class="container">
                <div class="Header">
                    <div class="Top">
                        <h1>최애 인증하기</h1>
                    </div>
                </div>
                <div class="card">
                    <h2>NOVA</h2>
                    <a href="{url}">
                        <img src="{url}" alt="명함 PNG">
                    </a>
                </div>
                <div class="ad-placeholder">
                    광고 들어갈 예정
                </div>
            </div>
        </body>
        </html>
        """
        return html


class LeagueRequest():
    def __init__(self, league_name = None, league_id = None) -> None:
        self.league_name = league_name
        self.league_id = league_id