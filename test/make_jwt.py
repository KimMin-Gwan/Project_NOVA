import jwt
from datetime import datetime, timezone, timedelta

# 비밀 키 설정
secret_key = "your_secret_key"

# 헤더 설정
headers = {
    "alg": "HS256",
    "typ": "JWT"
}

# 페이로드
payload = {
    "email": "randomUser1@naver.com",
    "iat": datetime.now(timezone.utc).timestamp(),
    "exp": (datetime.now(timezone.utc)+ timedelta(hours=3)).timestamp(),
    "refresh_exp": (datetime.now(timezone.utc) + timedelta(days=7)).timestamp()  # refresh 토큰 만료 시간 (예: 7일)
}

# 토큰 생성
token = jwt.encode(payload, secret_key, algorithm="HS256", headers=headers)

# 생성된 토큰 출력
print(token)





