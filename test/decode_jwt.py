import jwt

# 이전에 생성한 JWT 토큰
token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6InJhbmRvbVVzZXIxQG5hdmVyLmNvbSIsImlhdCI6MTcyNDI1MTIzNCwiZXhwIjoxNzI0MjUzMDM0fQ.6Zt-Aa9VnOLfqrBEL4DRSUAeP5LhdxnxNbrSk8AbUAY"

# 비밀 키 설정 (토큰을 생성할 때 사용한 것과 동일한 키)
secret_key = "your_secret_key"

# 토큰 디코드
decoded_payload = jwt.decode(token, secret_key, algorithms=["HS256"])

# 페이로드의 'name' 값 출력
print(decoded_payload)
