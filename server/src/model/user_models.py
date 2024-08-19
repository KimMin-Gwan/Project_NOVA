from model.base_model import BaseModel
from model import Local_Database
from others.data_domain import User
from others import CoreControllerLogicError
import jwt
import datetime
import uuid

class LoginModel(BaseModel):
    def __init__(self, database:Local_Database) -> None:
        super().__init__(database)
        self.__result = False
        self.__token = ''
        self.__detail = ''

    def request_login(self,request,user_data):
        try:
            if request.email == user_data.email and request.password == user_data.password:
                self.__result = True
            elif request.password != user_data.password:
                self.__detail = 'worng password'

        except Exception as e:
            raise CoreControllerLogicError(error_type="request_login | " + str(e))
    
    def make_token(self,request):
        try:
            # 비밀 키 설정
            secret_key = "your_secret_key"
            # 헤더 설정
            headers = {
                "alg": "HS256",
                "typ": "JWT"
            }
            # 페이로드 설정
            payload = {
                "email": request.email,
                "iat": datetime.datetime.utcnow(),
                "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30)  # 만료 시간 30분
            }
            # 토큰 생성
            self.__token = jwt.encode(payload, secret_key, algorithm="HS256", headers=headers) 

        except Exception as e:
            raise CoreControllerLogicError(error_type="login make_token | " + str(e))

    def get_response_form_data(self, head_parser):
        try:
            body = {
                'resust' : self.__result,
                'detail' : self.__detail,
                'token' : self.__token
            }

            response = self._get_response_data(head_parser=head_parser, body=body)
            return response

        except Exception as e:
            raise CoreControllerLogicError("response making error | " + e)
    
    def get_result(self):
        return self.__result
    

class SendEmailModel(BaseModel):
    def __init__(self, database:Local_Database) -> None:
        super().__init__(database)
        self.__result = True
        self.__detail = ''
        self.__token = ''

    def make_token(self,request):
        try:
            # 비밀 키 설정
            secret_key = "your_secret_key"
            # 헤더 설정
            headers = {
                "alg": "HS256",
                "typ": "JWT"
            }
            # 페이로드 설정
            payload = {
                "email": request.email,
                "iat": datetime.datetime.utcnow(),
                "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30)  # 만료 시간 30분
            }
            # 토큰 생성
            self.__token = jwt.encode(payload, secret_key, algorithm="HS256", headers=headers)

        except Exception as e:
            raise CoreControllerLogicError(error_type="make_token | " + str(e))
        
    def save_user(self,request):
        try:
            uid = self.__make_uid()
            user = User(uid=uid,
                        age=request.age,
                        email=request.email,
                        gender=request.gender,
                        password=request.password)

            self._database.add_new_data(target_id="uid",
                                        new_data=user.get_dict_form_data())

        except Exception as e:
            raise CoreControllerLogicError(error_type="save_response | " + str(e))
        
    def set_response(self,):
        try:
            self.__result = False
        except Exception as e:
            raise CoreControllerLogicError(error_type="set_response | " + str(e))

    def get_response_form_data(self, head_parser):
        try:
            body = {
                'resust' : self.__result,
                'token' : self.__token,
                'detail' : self.__detail
            }

            response = self._get_response_data(head_parser=head_parser, body=body)
            return response

        except Exception as e:
            raise CoreControllerLogicError("response making error | " + e)
    
    def get_result(self):
        return self.__result
    
    def __generate_uid(self):
        uid = str(uuid.uuid4())
        # uuid4()는 형식이 "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"인 UUID를 생성합니다.
        # 이를 "1234-abcd-5678" 형태로 변형하려면 일부 문자만 선택하여 조합합니다.
        uid_parts = uid.split('-')
        return f"{uid_parts[0][:4]}-{uid_parts[1][:4]}-{uid_parts[2][:4]}"

    def __make_uid(self):
        uid = ""
        while True:
            uid = self.__generate_uid()
            if not self._database.get_data_with_id(target="uid", id=uid):
                break
        return uid