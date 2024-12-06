import requests

# 세션 생성
session = requests.Session()

# 로그인 정보
#login_url = "https://nova-platform.kr/user_home/try_login"
login_url = "http://127.0.0.1:4000/user_home/try_login"
login_data = {
    "header": {  # 빈 값이라도 정확히 포함해야 함
        "request-type": "",
        "client-version": "",
        "client-ip": "",
        "uid": "",
        "endpoint": ""
    },
    "body": {
        "email": "randomUser2@naver.com",
        "password": "sample122"
    }
}

# 로그인 요청
response = session.post(login_url, json=login_data)

# 로그인 성공 여부 확인
if response.status_code == 200:
    print("로그인 성공:", response.json())
else:
    print("로그인 실패:", response.status_code, response.text)



test_url = "http://127.0.0.1:4000/nova_fund_system/project_detail?pid=5"

# 로그인 요청
response = session.get(test_url)

# 로그인 성공 여부 확인
if response.status_code == 200:
    print("성공:", response.json())
else:
    print("실패:", response.status_code, response.text)





