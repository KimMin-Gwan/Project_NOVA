from model.base_model import BaseModel
from model import Local_Database
from others.data_domain import User, Bias
from others import CoreControllerLogicError
import time
import datetime
import boto3
import cv2
import glob
import os

import warnings

# Boto3의 경고 메시지 무시
warnings.filterwarnings("ignore", module='boto3.compat')


class CheckPageModel(BaseModel):
    def __init__(self, database:Local_Database) -> None:
        super().__init__(database)
        self._bias = Bias()
        self._combo = 0
        self._point = 0
        self._contribution = 0.0
        self._result = "default"

    # type에 맞는 bias 세팅
    def set_bias(self, request):
        try:
            bid = ""
            if request.type == "solo":
                bid = self._user.solo_bid
            elif request.type == "group":
                bid = self._user.group_bid
            else:
                raise CoreControllerLogicError(error_type="set bias | request type error")

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
                self._result = "invalid"
                return False
        except Exception as e:
            raise CoreControllerLogicError(error_type="is_validate_user | " + str(e))

    # 이미 체크 했는지 확인해야됨
    def is_already_check(self) -> bool:
        try:
            if self._bias.type == "solo":
                if self._user.solo_daily:
                    self._result = "done"
                    return False
            elif self._bias.type == "group":
                if self._user.group_daily:
                    self._result = "done"
                    return False
            else: 
                self._result = "error"
                return False
            
            self._result = "valid"
            return True

        except Exception as e:
            raise CoreControllerLogicError(error_type="is_validate_user | " + str(e))

    # 인증 시도 페이지에 나올 내용 -> 전체 포인트중 현재까지 기여도 퍼센트(소숫점 2자리)
    def check_page_info(self) -> bool:
        total = 1680

        # 누구 대상인지 확인
        if self._bias.type == "solo":
            self._point = self._user.solo_point
            self._combo = self._user.solo_combo
        elif self._bias.type == "group":
            self._point = self._user.group_point
            self._combo = self._user.group_combo
        else:
            self._result = "error"
            raise CoreControllerLogicError(error_type="is_check_page_info | bias_type error")
        
        percentage = (self._point / total) * 100 # 퍼센트 계산
        self._contribution = round(percentage, 2) # 소숫점 2자리
        return True

    # 바이어스 호출
    def get_data_memebers(self):
        return self._user, self._bias, self._point, self._combo, self._contribution

    def get_response_form_data(self, head_parser):
        try:
            body = {
                'bias' : self._bias.get_dict_form_data(),
                'point' : self._point,
                'combo' : self._combo,
                'contribution' : self._contribution,
                'result' : self._result  # done error invalid valid
            }

            response = self._get_response_data(head_parser=head_parser, body=body)
            return response

        except Exception as e:
            raise CoreControllerLogicError("response making error | " + e)


class TryCheckModel(CheckPageModel):
    def __init__(self, database:Local_Database) -> None:
        super().__init__(database)
        self.__name_card_url = ""
        self._special_time = []
        self.__name_card = ""
        self.__shared_url = ""
        self.__special_check_valid = False

    # 부모 클래스로 만들때 사용할 초기화 함수
    def init_with_mother_model(self, model:CheckPageModel):
        user, bias ,point, combo, contribution = model.get_data_memebers()
        self._user = user
        self._bias = bias
        self._point = point
        self._combo = combo
        self._contribution = contribution
        self._result = "done"
        return
    
    # 중복 최애 인증은 invalid 임
    def set_result_invalid(self):
        self._result="invalid"

    # 최애 인증 시도 함수
    def try_daily_check(self):
        try:
            point = 60
            if self._bias.type == "solo":
                self._bias.point = self._bias.point + point + self._user.solo_combo * 10
                self._user.solo_combo += 1
                self._user.solo_daily = True
                self._result = "done"
                self._save_datas()
            elif self._bias.type == "group":
                self._bias.point = self._bias.point + point + self._user.group_combo * 10
                self._user.group_combo += 1
                self._user.group_daily = True
                self._result = "done"
                self._save_datas()
            else:
                self._result = "error"
                raise CoreControllerLogicError(error_type="try_daily_check | bias type error")
        except Exception as e:
            print(e)
            raise CoreControllerLogicError(error_type="try_daily_check | " )
        
    def _save_datas(self):
        self._database.modify_data_with_id(target_id="bid", target_data=self._bias.get_dict_form_data())
        self._database.modify_data_with_id(target_id="uid", target_data=self._user.get_dict_form_data())
        return
        
    # 네임카드를 만들고 업로드 하고 url을 name_card로 돌려줘야함
    def make_name_card(self):
        try:
            name_card_maker = NameCardMaker()
            name_card_maker.make_name_card(bias=self._bias, user=self._user)
        except Exception as e:
            raise CoreControllerLogicError(error_type="make_name_card | " + str(e))
        return True

    # 명함의 url 생성
    def set_name_card_url(self):
        try:
            name_card_maker = NameCardMaker()
            self.__name_card_url = name_card_maker.get_name_card_url(bias=self._bias, user=self._user)
        except Exception as e:
            raise CoreControllerLogicError(error_type="make_name_card | " + str(e))
        return
        
    # 이미 만들어진 name카드를 호출하는 함수
    def set_name_card_name(self):
        try:
            name_card_maker = NameCardMaker()
            self.__name_card = name_card_maker.get_name_card_name(bias=self._bias, user=self._user)
        except Exception as e:
            raise CoreControllerLogicError(error_type="make_name_card | " + str(e))

    # 스페셜 체크 시간 리스트
    def get_special_check_time(self):
        try:
            special_time = set()
            if self._bias.birthday != "":
                convert_result = self._convert_date_to_time(date_string=self._bias.birthday)
                special_time.update(convert_result)

            if self._bias.debut != "":
                convert_result = self._convert_date_to_time(date_string=self._bias.debut)
                special_time.update(convert_result)

            self._special_time = list(special_time)
            return True
        except Exception as e:
            raise CoreControllerLogicError(error_type="get_special_check_time | " + str(e))

    # 스페셜 체크가능 시간 리스트 만들기
    def _convert_date_to_time(self, date_string):
        # 날짜 문자열을 연, 월, 일로 분리
        _, month, day = map(int, date_string.split('/'))

        # 월을 24시간 기준으로 변환 (0시부터 시작)
        month_as_hour = (month % 12) * 2

        # 일에 따라 시간 조정 (일이 16일보다 작으면 0, 크거나 같으면 1을 추가)
        adjusted_hour = month_as_hour + (1 if day >= 16 else 0)

        return [month % 12, adjusted_hour]
    
    # 공유 전용 url
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
                #'user' : self._user.get_dict_form_data(),   # 이건 왜 필요한지 모르긴함
                'shared_url' : self.__shared_url,  # 공유용 url
                'special_check_valid' : self.__special_check_valid,  # 특별시 인증 가능한지 여부 조사
                'special_time' : self._special_time,  # 특별시 인증 시간 리스트
                'name_card_url' : self.__name_card_url, # 명함 사진 ncloud 주소
                'point' : self._point,
                'combo' : self._combo,
                'contribution' : self._contribution,
                'result' : self._result
            }

            response = self._get_response_data(head_parser=head_parser, body=body)
            return response

        except Exception as e:
            raise CoreControllerLogicError("response making error | " + e)
        
class TrySpecialCheckModel(TryCheckModel):
    def __init__(self, database:Local_Database) -> None:
        super().__init__(database)
        self.__result = "default"

    # 이미 스페셜 체크 했는지 확인해야됨
    # Override
    def is_already_check(self) -> bool:
        try:
            if self._bias.type == "solo":
                if self._user.solo_special:
                    self._result = "error"
                    return False
            elif self._bias.type == "group":
                if self._user.group_special:
                    self._result = "error"
                    return False
            else: 
                self._result = "type error"
                return False
            
            self._result = "valid"
            return True

        except Exception as e:
            raise CoreControllerLogicError(error_type="is_validate_user | " + str(e))

    # 최애 인증 시도 함수
    def try_special_check(self):
        try:
            point = 20
            self._bias.point += point
            if self._bias.type == "solo":
                self._user.solo_special = True
                self.__result = "done"
                self._save_datas()
            elif self._bias.type == "group":
                self._user.group_special = True
                self.__result = "done"
                self._save_datas()
            else:
                self.__result = "error"
                raise CoreControllerLogicError(error_type="try_daily_check | bias type error")
        except Exception as e:
            raise CoreControllerLogicError(error_type="set_bias_with_bias_data | " + str(e))
    
    # 특별시 인지 체크
    def check_special_time(self):
        self.get_special_check_time()
        now = datetime.datetime.now()
        hour = now.hour
        hour = 10
        if hour in self._special_time:
            return True
        else:
            self.__result = "time invalid"
            return False
        
    # 스페셜 체크가능 시간 리스트 만들기
    def _convert_date_to_time(self, date_string):
        # 날짜 문자열을 연, 월, 일로 분리
        _, month, day = map(int, date_string.split('/'))

        # 월을 24시간 기준으로 변환 (0시부터 시작)
        month_as_hour = (month % 12) * 2

        # 일에 따라 시간 조정 (일이 16일보다 작으면 0, 크거나 같으면 1을 추가)
        adjusted_hour = month_as_hour + (1 if day >= 16 else 0)

        return [month % 12, adjusted_hour]

    def get_response_form_data(self, head_parser):
        try:
            body = {
                'result' : self.__result
            }

            response = self._get_response_data(head_parser=head_parser, body=body)
            return response

        except Exception as e:
            raise CoreControllerLogicError("response making error | " + e)

# 명함 제조기
class NameCardMaker:
    def __init__(self):
        self.__path = './model/local_database/'
        self.__service_name = 's3'
        self.__endpoint_url = 'https://kr.object.ncloudstorage.com'
        self.__region_name = 'kr-standard'
        self.__access_key = 'eeJ2HV8gE5XTjmrBCi48'
        self.__secret_key = 'zAGUlUjXMup1aSpG6SudbNDzPEXHITNkEUDcOGnv'
        self.__s3 = boto3.client(self.__service_name,
                           endpoint_url=self.__endpoint_url,
                           aws_access_key_id=self.__access_key,
                      aws_secret_access_key=self.__secret_key)

    def make_name_card(self, bias:Bias, user:User): 
        # 네임카드 만드는 부분
        # 네임카드 포함 내용은 아래와 같다
        # 내용 : user.uid, bias.name, bias.fanname, user.solo_point(group_point), 최애 사진
        #        user.solo_combo(group_combo), 오늘 날짜 등... 넣고싶은거 아무거나 넣어도댐

        # 1. 백그라운드 이미지  불러오기
        img = self.__name_card_backgroud_image(user.select_name_card)

        # 2. 바이어스 이미지 받아오기
        self.__s3.download_file('nova-images',f'{bias.bid}.PNG',f'{self.__path}temp_files/{bias.bid}.png')
        bias_img = cv2.imread(f"{self.__path}temp_files/{bias.bid}.png")
        bias_img = cv2.resize(bias_img, (100, 100))  # 예를 들어 100x100 크기로 리사이즈

        # 3. 글자 붙혀넣기
        cv2.putText(img,f"{user.uid}", (300,200), cv2.FONT_HERSHEY_COMPLEX, 1, (0,150,0), 1)   # 중심 위치 300,200인 폰트가 FONT_HERSHEY_COMPLEX인, 크기 1의, 약한 초록색의 ,두께 3인 글씨
        cv2.putText(img,f"{bias.bname}", (400,400), cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 1)
        #이미지 합성
        img[100:200, 100:200] = bias_img

        # 4. 이미지 이름 만들기
        image_name = self.__make_name_url(bias.bid, user.uid)

        # 4. 이미지 저장
        cv2.imwrite(f'{self.__path}temp_files/{image_name}.png', img)

        # 호출문은 아래와 같음 (날짜는 알아서 모율 내에서 계산할것)
        # modul.make_name_card(self._bias, self._user)
        # 5. 이미지 업로드
        self.__s3.upload_file(f'{self.__path}temp_files/{image_name}.png', "nova-name-card", f"{image_name}.png",ExtraArgs={'ACL':'public-read'})

        #name_card_url = f"https://kr.object.ncloudstorage.com/nova-name-card/{card_name}.png"
        # 함수 반환값을 파일 주소를 반환 할것

        self.delete_temp_image()
        return True
        # 아래가 실제 사용 예시
        #self.__name_card_url = modul.get_name_card_url()

    # 명함의 백그라운드 이미지 선택(name_card_id는 user에서 제공)
    def __name_card_backgroud_image(self, name_card_id):
        path = self.__path + "name_card/" + name_card_id + ".PNG"
        img = cv2.imread(path)
        return img

    # 명함의 파일 이름 생성기
    # 네임카드 파일 이름은 bid-uid-날짜
    # 예시 : 1001-1234-abcd-5678-24-08-21.png
    def __make_name_url(self, bid, uid) -> str:
        now = datetime.datetime.now()
        date = now.strftime('%Y-%m-%d')
        name_card_url = f'{bid}-{uid}-{date}'
        return name_card_url

    # img 이미지 이름 가지고 오기
    def get_name_card_name(self, bias:Bias, user:User) -> str:
        image_name = self.__make_name_url(bias.bid, user.uid)
        return image_name

    # cloud의 url 가지고 오기
    def get_name_card_url(self, bias:Bias, user:User) ->str:
        image_name = self.get_name_card_name(bias, user)
        name_card_url = f"{self.__endpoint_url}/nova-name-card/{image_name}.png"
        return name_card_url

    # 임시 이미지 파일 지우기
    def delete_temp_image(self):
        # 파일이 작성되기 까지 대기 시간
        time.sleep(0.1)

        # 디렉토리 내의 모든 파일을 찾음
        directory_path = self.__path + "/temp_files/"
        files = glob.glob(os.path.join(directory_path, '*'))
        for file in files:
            # 파일인지 확인 후 삭제
            if os.path.isfile(file):
                os.remove(file)
        return