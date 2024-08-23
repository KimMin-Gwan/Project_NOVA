import requests
import json
import pprint

#HOST = '223.130.157.23'
#PORT = 80
HOST = '175.106.99.34'
PORT = 6000

 #요청을 보낼 URL
 #get
#url = "http://127.0.0.1:6000/home/banner"  # banner 정보 
#url = "http://127.0.0.1:6000/home/league_data?league_type=solo"  # 리그 매타 정보
#url = "http://127.0.0.1:6000/home/show_league?league_name=양자리"  # 리그 랭킹 순위
#url = "http://175.106.99.34/home/show_league?league_name=양자리"  # 리그 랭킹 순위
#url = "http://175.106.99.34/home/search_bias?bias_name=김"  # bias 검색
#url = "http://127.0.0.1:6000/home/search_bias?bias_name=김"  # bias 검색

#url = "http://127.0.0.1:6000/nova_check/shared/1001-5678-efgh-1234-2024-08-23"# 공유 페이지

url = "http://127.0.0.1:6000/bias_info/user_contribution?bias_id=1003"  # 최애 페이지 기여도 랭킹 
#url = "http://175.106.99.34/bias_info/user_contribution?bias_id=9999"  # 최애 페이지 기여도  랭킹 순위

 ##post
#url = "http://127.0.0.1:6000/home/my_bias"  # 리그 랭킹 순위
#url = "http://175.106.99.34/home/my_bias"  # 리그 랭킹 순위
#url = "http://175.106.99.34/home/my_bias_league"  # 최애 리그 랭킹 순위
#url = "http://127.0.0.1:8888/home/my_bias_league"  # 최애 리그 랭킹 순위
#url = "http://127.0.0.1:6000/home/try_select_my_bias"  # 최애 정하기

#url = "http://175.106.99.34/user_home/try_login"  # 로그인 시도
#url = "http://127.0.0.1:6000/user_home/try_send_email"  # 이메일 보내기
#url = "http://127.0.0.1:6000/user_home/try_sign_in"  # 로그인 시도

#url = "http://127.0.0.1:6000/nova_check/server_info/check_page"  
#url = "http://175.106.99.34/nova_check/server_info/check_page"  
#url = "http://127.0.0.1:6000/nova_check/server_info/try_daily_check"  # 로그인 시도
#url = "http://127.0.0.1:6000/nova_check/server_info/try_special_check"  # 로그인 시도
#url = "http://175.106.99.34/nova_check/shared/1001-5678-efgh-1234-2024-08-23" # 로그인 시도

#url = "http://127.0.0.1:6000/bias_info/my_contribution"  # 리그 랭킹 순위
#url = "http://175.106.99.34/bias_info/my_contribution"  # 리그 랭킹 순위




# # GET 요청 보내기
response = requests.get(url)

# # 상태 코드 확인
print(f"Status Code: {response.status_code}")

 # 응답 데이터 (JSON) 출력
if response.status_code == 200:
    result = response.json()
    #result = response.text
    pprint.pprint(result)
else:
     print("Failed to retrieve data")
exit()


## make_jwt.py 실행시켜서 token 발급 받을 것
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InJhbmRvbVVzZXIxQG5hdmVyLmNvbSIsImlhdCI6MTcyNDI1MjA0MywiZXhwIjoxNzI0MjUzODQzfQ.iKh_X-p68ngTn5Xrg8YX1DGIf4sVqxwtl_ebuLlrDJw"


header = {
    "request-type" : "default",
    "client-version" : 'v1.0.1',
    "client-ip" : '127.0.0.1',
    "uid" : '1234-abcd-5678', 
    "endpoint" : "/core_system/", 
}

## home/my_bias
#send_data = {
    #"header" : header,
    #"body" : {
        #'token' : token
    #}
#}

## home/my_bias_league
## nova-check/server/check_page
#send_data = {
    #"header" : header,
    #"body" : {
        #'token' : token,
        #'type' : "group"
    #}
#}

# home/try_select_my_bias
# bias_info/my_contribution
send_data = {
    "header" : header,
    "body" : {
        'token' : token,
        'bid' : "1002"
    }
}


#user/try_login 
#send_data = {
    #"header" : header,
    #"body" : {
        #'email' : 'randomUser1@naver.com',
        #'password' : "sample122"
    #}
#}


## user/try_send_email
#send_data = {
    #"header" : header,
    #"body" : {
        #'email' : 'alsrhks2508@yu.ac.kr',
    #}
#}

## user/try_Sign_in
#send_data = {
    #"header" : header,
    #"body" : {
            #'email' : 'alsrhks2508@yu.ac.kr',
            #'verification_code' : 1872,
            #'password' : 'sample1234',
            #'age' : "24",
            #'gender' : 'male',
        #}
#}


#post 전송용
headers = {
    'Content-Type': 'application/json'
}
send_data = json.dumps(send_data)
send_data.encode()

response = requests.post(url=url, data = send_data, headers=headers)
response.encoding = 'utf-8'
print(response)

result = response.json()
pprint.pprint(result)