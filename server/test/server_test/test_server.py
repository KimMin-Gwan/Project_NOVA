import requests
from pprint import pprint

# 세션 생성
session = requests.Session()

# 로그인 정보
login_url = "https://nova-platform.kr/user_home/try_login"
#login_url = "http://127.0.0.1:4000/user_home/try_login"
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

fid = "6063-qfgh-2540-3URvvc"

test_url = f"http://127.0.0.1:4000/feed_explore/feed_detail/comment_data?fid={fid}"
#test_url = "https://nova-platform.kr/nova_fund_system/project_detail?pid=5"


print("????")
# 쿠키 확인
print("Cookies after login:", session.cookies.get_dict()) 
print("????")


# 헤더 포함 요청 테스트
response = session.get(test_url, cookies=session.cookies.get_dict())

# 결과 확인
if response.status_code == 200:
    pprint(response.json())
else:
    print("실패:", response.status_code, response.text)



