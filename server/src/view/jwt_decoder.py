import jwt
from jwt import ExpiredSignatureError
from datetime import datetime, timezone, timedelta
from fastapi import Response, Request
from fastapi import HTTPException, status
import json


class JWTManager:
    def __init__(self):
        self._secret_key = "your_secret_key"
        self._argorithms = ["HS256"]

    # 이건 이제 안씀
    def decode(self, token):
        try:
            # 토큰 디코드
            decoded_payload = jwt.decode(token, self._secret_key, algorithms=self._argorithms)
            payload = JWTPayload(result = True , email=decoded_payload['email'],
                                 exp=decoded_payload['exp'], refresh_exp=decoded_payload['refresh_exp'])
        except ExpiredSignatureError:
            payload = JWTPayload(result=False)

        return payload
    
    # 이걸 써야됨
    def home_decode(self, token):
        flag = False
        new_token = ""
        try:
            # 토큰 디코드
            decoded_payload = jwt.decode(token, self._secret_key, algorithms=self._argorithms)
            flag = True
        except ExpiredSignatureError:
            decoded_payload = jwt.decode(token, self._secret_key, algorithms=self._argorithms,
                                            options={"verify_exp":False})
            current_time = datetime.now(timezone.utc).timestamp()
            if current_time < datetime.fromtimestamp(decoded_payload["refresh_exp"]).timestamp():
                new_token = self.make_token(email = decoded_payload["email"])
                flag = True

        if flag:
            payload = {}

            # Unix 타임스탬프를 datetime 객체로 변환
            payload["iat"] = datetime.fromtimestamp(decoded_payload["iat"])
            payload["email"] = decoded_payload["email"]
            payload["exp"] = datetime.fromtimestamp(decoded_payload["exp"])
            payload["refresh_exp"] = datetime.fromtimestamp(decoded_payload["refresh_exp"])
            
            print(payload)
            payload = JWTPayload(result = True , email=payload['email'],
                                 exp=payload['exp'], refresh_exp=payload['refresh_exp'],
                                 usage=payload['usage'])
        else:
            payload = JWTPayload(result=False)

        return payload, new_token


    # 토큰 제작
    def make_token(self, email, usage="all"):
        # 헤더 설정
        headers = {
            "alg": "HS256",
            "typ": "JWT"
        }

        # 페이로드 설정
        # exp 3시간
        # refresh 7일
        payload = {
            "email": email,
            "usage" : usage,
            "iat": datetime.now(timezone.utc).timestamp(),
            "exp": (datetime.now(timezone.utc) + timedelta(hours=3)).timestamp(),
            "refresh_exp": (datetime.now(timezone.utc) + timedelta(days=7)).timestamp()  # refresh 토큰 만료 시간 (예: 7일)
        }

        token = jwt.encode(payload, self._secret_key, algorithm="HS256", headers=headers)
        return token

    
class JWTPayload:
    def __init__(self, result=False, email=None, exp=None, refresh_exp=None, usage="None"):
        self.result = result
        self.email=email
        self.usage=usage
        self.exp=exp
        self.refresh_exp=refresh_exp

# Request를 분석하는 모듈
class RequestManager(JWTManager):
    def __init__(self):
        super().__init__()
        self.data_payload= None
        self.jwt_payload = JWTPayload()
        self.new_token = ""
        self.credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not Validate credentials",
            headers={"WWW-Authenticate" : "Bearer"}
        )
        self.bad_request_exception= HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not Find Page",
        )
        self.image_size_exception = HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail="The aspect ratio is over 3:1",
        )
        self.system_logic_exception= HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Unprocessable Entity"
        )
        self.forbidden_exception= HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="403 Forbidden"
        )

    # 쿠키 지우는 마법
    def try_clear_cookies(self, request:Request):
        request.cookies.clear()
        response = Response(
            content=json.dumps({"result":True}),
            media_type="application/json",
            status_code=200
        )
        response.delete_cookie(key="nova_token",
                samesite="None",  # Changed to 'Lax' for local testing
                secure=True,  # Local testing; set to True in production
                httponly=True)
        return response

    # 404
    def get_bad_request_exception(self):
        return self.bad_request_exception

    # 임시 유저의 로그인에서
    def try_view_management_authorized_with_temp_user(self, data_payload = None, cookies = None):
        self.data_payload= data_payload
        try:
            payload, new_token = self.home_decode(token=cookies["nova_token"])
            if payload.usage != "temp":
                raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="Could not Validate credentials",
                        headers={"WWW-Authenticate" : "Bearer"})
        except:
            raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Could not Validate credentials",
                    headers={"WWW-Authenticate" : "Bearer"})
        self.jwt_payload= payload
        self.new_token = new_token

    # 로그인이 필수일때
    def try_view_management_need_authorized(self, data_payload = None, cookies = None):
        self.data_payload= data_payload
        try:

            payload, new_token = self.home_decode(token=cookies["nova_token"])
            # 임시사용자에게 제한을 줘야햄
            print(payload.usage)

            if payload.usage == "temp":
                raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="Could not Validate credentials",
                        headers={"WWW-Authenticate" : "Bearer"})
        except:
            raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Could not Validate credentials",
                    headers={"WWW-Authenticate" : "Bearer"})
        self.jwt_payload= payload
        self.new_token = new_token

    # 로그인 필수 아닐때
    def try_view_management(self, data_payload = None, cookies = None):
        self.data_payload= data_payload
        try:
            payload, new_token = self.home_decode(token=cookies["nova_token"])
            # 임시사용자는 굳이 더 줄 필요없음
            if payload.usage == "temp":
                self.jwt_payload = ""
                self.new_token = ""
            else:
                self.jwt_payload= payload
                self.new_token = new_token
        except:
            self.jwt_payload = ""
            self.new_token = ""
        finally:
            return

    # json데이터 보내줘야할때ㅔ response 만드는 곳
    def make_json_response(self, body_data:dict, token = ""):
        if token != "":
            self.new_token = token

        response = Response(
            content=json.dumps(body_data),
            media_type="application/json",
            status_code=200
        )
        if self.new_token != "":
            response.set_cookie(
                key="nova_token", 
                value=self.new_token, 
                max_age=7*60*60*24,
                samesite="None",  # Changed to 'Lax' for local testing
                secure=True,  # Local testing; set to True in production
                httponly=True
            )

        return response

    # 비밀번호 변경하기에서 임시 유저 토큰 지우고 전송 데이터를 세팅
    def make_json_response_in_password_find(self,request:Request, body_data:dict):
        request.cookies.clear()
        response = Response(
            content=json.dumps(body_data),
            media_type="application/json",
            status_code=200
        )

        response.delete_cookie(key="nova_token",
                samesite="None",  # Changed to 'Lax' for local testing
                secure=True,  # Local testing; set to True in production
                httponly=True)

        return response

# 