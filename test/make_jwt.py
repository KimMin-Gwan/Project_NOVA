import jwt
import datetime

# 비밀 키 설정
secret_key = "your_secret_key"

# 헤더 설정
headers = {
    "alg": "HS256",
    "typ": "JWT"
}

# 페이로드 설정
payload = {
    "email": "testUser@naver.com",
    "iat": datetime.datetime.utcnow(),
    "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30)  # 만료 시간 30분
}

# 토큰 생성
token = jwt.encode(payload, secret_key, algorithm="HS256", headers=headers)

# 생성된 토큰 출력
print(token)



