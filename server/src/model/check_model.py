from model.base_model import BaseModel
from model import Local_Database
from others.data_domain import User, Bias
from others import CoreControllerLogicError

class CheckPageModel(BaseModel):
    def __init__(self, database:Local_Database) -> None:
        super().__init__(database)
        self._bias = Bias()
        self.__combo = 0
        self.__point = 0
        self.__contribution = 0.0
        self.__result = "default"

    def set_bias(self, bid):
        try:
            bias_data = self._database.get_data_with_id(target="bid", id=bid)
            self._bias.make_with_dict(bias_data)
            return

        except Exception as e:
            raise CoreControllerLogicError(error_type="set_bias | " + str(e))
    
    # 유저가 실제로 팔로우 하고 있는지 확인
    def is_validate_user(self) -> bool:
        try:
            if self._user.solo_bid == self._bias.bid or self._user.group_bid == self._bias.bid:
                return True
            else:
                # 팔로우 안하고 있으면 invalid 반환
                self.__result = "invalid"
                return False
        except Exception as e:
            raise CoreControllerLogicError(error_type="is_validate_user | " + str(e))

    # 이미 체크 했는지 확인해야됨
    def is_already_check(self) -> bool:
        try:
            if self._bias.type == "solo":
                if self._user.solo_daily:
                    self.__result = "done"
                    return False
            elif self._bias.type == "group":
                if self._user.group_daily:
                    self.__result = "done"
                    return False
            else: 
                self.__result = "error"
                return False
            
            self.__result = "valid"
            return True

        except Exception as e:
            raise CoreControllerLogicError(error_type="is_validate_user | " + str(e))

    # 인증 시도 페이지에 나올 내용 -> 전체 포인트중 현재까지 기여도 퍼센트(소숫점 2자리)
    def check_page_info(self) -> bool:
        total = 1680

        # 누구 대상인지 확인
        if self._bias.type == "solo":
            self.__point = self._user.solo_point
            self.__combo = self._user.solo_combo
        elif self._bias.type == "group":
            self.__point = self._user.group_point
            self.__combo = self._user.group_combo
        else:
            self.__result = "error"
            raise CoreControllerLogicError(error_type="is_check_page_info | bias_type error")
        
        percentage = (self.__point / total) * 100 # 퍼센트 계산
        self.__contribution = round(percentage, 2) # 소숫점 2자리
        return True

    # 바이어스 호출
    def get_bias(self):
        return  self.__bias

    def get_response_form_data(self, head_parser):
        try:
            body = {
                'bias' : self._bias.get_dict_form_data(),
                'point' : self.__point,
                'combo' : self.__combo,
                'contribution' : self.__contribution,
                'result' : self.__result
            }

            response = self._get_response_data(head_parser=head_parser, body=body)
            return response

        except Exception as e:
            raise CoreControllerLogicError("response making error | " + e)


class TryCheckModel(CheckPageModel):
    def __init__(self, database:Local_Database) -> None:
        super().__init__(database)
        self.__result = "default"
        self.__name_card_url = ""
        self.__special_time = []
        self.__name_card = ""
        self.__special_time = True

    # 이미 만들어진 bias 주는애
    def set_bias_with_bias_data(self, bias:Bias):
        try:
            self._bias = bias
            return
        except Exception as e:
            raise CoreControllerLogicError(error_type="set_bias_with_bias_data | " + str(e))
    
    # 최애 인증 시도 함수
    def try_daily_check(self):
        try:
            point = 60

            if self._bias.type == "solo":
                self._bias.point = self._bias.point + point + self._user.solo_combo * 10
                self._user.solo_combo += 1
                self._user.solo_daily = True
            elif self._bias.type == "group":
                self._bias.point = self._bias.point + point + self._user.group_combo * 10
                self._user.group_combo += 1
                self._user.group_daily = True
            else:
                self.__result = "error"
                raise CoreControllerLogicError(error_type="try_daily_check | bias type error")
        except Exception as e:
            raise CoreControllerLogicError(error_type="set_bias_with_bias_data | " + str(e))
        
    # 네임카드를 만들고 업로드 하고 url을 name_card로 돌려줘야함
    def make_name_card(self):
        # 네임카드 만드는 부분
        # 네임카드 포함 내용은 아래와 같다
        # 내용 : user.uid, bias.name, bias.fanname, user.solo_point(group_point), 최애 사진
        #        user.solo_combo(group_combo), 오늘 날짜 등... 넣고싶은거 아무거나 넣어도댐

        # 네임카드 파일 이름은 bid-uid-날짜
        # 예시 : 1001-1234-abcd-5678-24-08-21.png
        
        # 호출문은 아래와 같음 (날짜는 알아서 모율 내에서 계산할것)
        # modul.make_name_card(self._bias, self._user)

        # 함수 반환값을 파일 주소를 반환 할것

        # 아래는 모듈 내부 예시
        #name_card_url = f"https://kr.object.ncloudstorage.com/nova-name-card/{card_name}.png"
        # 파일 이름 뽑는 함수도 하나 만들어 둘것

        # 아래가 실제 사용 예시
        #self.__name_card_url = modul.get_name_card_url()

        return True

    # 이미 만들어진 name카드를 호출하는 함수
    # 이미 호출한 사람이 다시 호출을 시도할 때 줄 내용
    def get_name_card(self):

        # 이것도 모듈에서 제공하는것으로합니다
        # 호출문 예시 (함수이름은 바꿔도 됨)
        # self.name_card_url = self.get_name_card_url_with_uid_n_bid(self._user.uid, self._bias.bid)
        return True
    
    def get_special_check_time(self):
        try:
            special_time = set()
            if self._bias.birthday != "":
                convert_result = self.__convert_date_to_time(date_string=self._bias.birthday)
                special_time.update(convert_result)

            if self._bias.debut != "":
                convert_result = self.__convert_date_to_time(date_string=self._bias.debut)
                special_time.update(convert_result)

            self.__special_time = list(special_time)
            return True
        except Exception as e:
            raise CoreControllerLogicError(error_type="get_special_check_time | " + str(e))

    # 스페셜 체크가능 시간 리스트 만들기
    def __convert_date_to_time(self, date_string):
        # 날짜 문자열을 연, 월, 일로 분리
        year, month, day = map(int, date_string.split('/'))

        # 월을 24시간 기준으로 변환 (0시부터 시작)
        month_as_hour = (month % 12) * 2

        # 일에 따라 시간 조정 (일이 16일보다 작으면 0, 크거나 같으면 1을 추가)
        adjusted_hour = month_as_hour + (1 if day >= 16 else 0)

        return [month % 12, adjusted_hour]
    
    def get_shared_url(self):
        try:
            self.__shared_url = f"http://nova-platform.kr/home_check/shared/{self.__name_card}"
            return
        except Exception as e:
            raise CoreControllerLogicError(error_type="get_shared_url | " + str(e))

    # 특별시 인증 가능한지 여부 조사
    def is_special_time_check(self):
        try:
            if self._bias.type == "solo":
                self.__special_check_valid = self._user.solo_special
            elif self._bias.type == "group":
                self.__special_check_valid = self._user.group_special
            else:
                self.__special_check_valid = False
                raise CoreControllerLogicError(error_type="is_special_time_chekc| bias type error")
            return
        except Exception as e:
            raise CoreControllerLogicError(error_type="is_special_time_check | " + str(e))

    def get_response_form_data(self, head_parser):
        try:
            body = {
                'bias' : self._bias.get_dict_form_data(),   # 이건 팬카페 주소 보려고 보냄
                'user' : self._user.get_dict_form_data(),   # 이건 왜 필요한지 모르긴함
                'shared_url' : self.__shared_url,  # 공유용 url
                'special_check_valid' : self.__special_check_valid,  # 특별시 인증 가능한지 여부 조사
                'special_time' : self.__special_time,  # 특별시 인증 시간 리스트
                'name_card_url' : self.__name_card_url, # 명함 사진 ncloud 주소
                'result' : self.__result
            }

            response = self._get_response_data(head_parser=head_parser, body=body)
            return response

        except Exception as e:
            raise CoreControllerLogicError("response making error | " + e)