import jwt
from jwt import ExpiredSignatureError
from datetime import datetime, timedelta, timezone

# 이전에 생성한 JWT 토큰
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InJhbmRvbVVzZXIxQG5hdmVyLmNvbSIsImlhdCI6MTcyNDcyMTI1MC4wOTg5NTMsImV4cCI6MTcyNDc1MzY2MCwicmVmcmVzaF9leHAiOjE3MjQ3MjIwOTAuMDk4OTUzfQ.bBHwoucTtoBClymiIf7x-zKDJCnFJ1OsryYMmKI3Oa0"

# 비밀 키 설정 (토큰을 생성할 때 사용한 것과 동일한 키)
secret_key = "your_secret_key"

try:

    # 토큰 디코드
    decoded_payload = jwt.decode(token, secret_key, algorithms=["HS256"])
except ExpiredSignatureError:
    decoded_payload = jwt.decode(token, secret_key, algorithms=["HS256"],
                                    options={"verify_exp":False})
    current_time = datetime.utcnow().timestamp()
    #current_time = datetime.now(timezone.utc).timestamp()
    print(current_time)
    if current_time < decoded_payload.get("refresh_exp"):
        print("Access token expired, but refresh token is still valid. Issuing new access token...")

        # 새로운 access token 발급
        new_payload = {
            "email": decoded_payload["email"],
            "iat": datetime.now(timezone.utc).timestamp(),
            "exp": (datetime.now(timezone.utc) + timedelta(minutes=10)).timestamp(),
            "refresh_exp": (datetime.now(timezone.utc) + timedelta(seconds=14)).timestamp()  # refresh 토큰 만료 시간 (Unix 타임스탬프)
        }

        new_token = jwt.encode(new_payload, secret_key, algorithm="HS256")
        print(f"New Token: {new_token}")
    else:
        print("Refresh token has also expired. Please log in again.")



# 페이로드의 'name' 값 출력
print(decoded_payload)
payload = {}
# Unix 타임스탬프를 datetime 객체로 변환
payload["iat"] = datetime.fromtimestamp(decoded_payload["iat"])
payload["exp"] = datetime.fromtimestamp(decoded_payload["exp"])
payload["refresh_exp"] = datetime.fromtimestamp(decoded_payload["refresh_exp"])


