import jwt

# 이전에 생성한 JWT 토큰
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InRlc3RVc2VyQG5hdmVyLmNvbSIsImlhdCI6MTcyMzc0MDUzNiwiZXhwIjoxNzIzNzQyMzM2fQ.nVHdFqWT3cPjYBYl2iLskp0f-jSHAUDNL5XQLb9tJWA"

# 비밀 키 설정 (토큰을 생성할 때 사용한 것과 동일한 키)
secret_key = "your_secret_key"

# 토큰 디코드
decoded_payload = jwt.decode(token, secret_key, algorithms=["HS256"])

# 페이로드의 'name' 값 출력
print(decoded_payload[''])
