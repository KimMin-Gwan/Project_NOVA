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

            payload = JWTPayload(result = True , email=payload['email'],
                                 exp=payload['exp'], refresh_exp=payload['refresh_exp'])
        else:
            payload = JWTPayload(result=False)

        return payload, new_token


    # 토큰 제작
    def make_token(self, email):
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
            "iat": datetime.now(timezone.utc).timestamp(),
            "exp": (datetime.now(timezone.utc) + timedelta(hours=3)).timestamp(),
            "refresh_exp": (datetime.now(timezone.utc) + timedelta(days=7)).timestamp()  # refresh 토큰 만료 시간 (예: 7일)
        }

        token = jwt.encode(payload, self._secret_key, algorithm="HS256", headers=headers)
        return token

    
class JWTPayload:
    def __init__(self, result=False, email=None, exp=None, refresh_exp=None):
        self.result = result
        self.email=email
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

    # 쿠키 지우는 마법
    def try_clear_cookies(self):
        response = Response(
            media_type="application/json",
            status_code=status.HTTP_401_UNAUTHORIZED,
        )
        response.delete_cookie()
        return response

    # 404
    def get_bad_request_exception(self):
        return self.bad_request_exception

    # 로그인이 필수일때
    def try_view_management_need_authorized(self, data_payload = None, cookies = None):
        self.data_payload= data_payload
        try:
            payload, new_token = self.home_decode(token=cookies["nova_token"])
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
