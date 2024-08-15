import requests
import json
import pprint

#HOST = '223.130.157.23'
#PORT = 80
HOST = '127.0.0.1'
PORT = 6000

 #요청을 보낼 URL
 #get
#url = "http://127.0.0.1:6000/home/banner"  # banner 정보 
#url = "http://127.0.0.1:6000/home/league_data?league_type=solo"  # 리그 매타 정보
#url = "http://127.0.0.1:6000/home/show_league?league_name=폴라리스"  # 리그 랭킹 순위
#url = "http://127.0.0.1:6000/home/search_bias?bias_name=김"  # bias 검색

 ##post
#url = "http://127.0.0.1:6000/home/my_bias"  # 리그 랭킹 순위
#url = "http://127.0.0.1:6000/home/my_bias_league"  # 최애 리그 랭킹 순위
url = "http://127.0.0.1:6000/home/try_select_my_bias"  # 최애 정하기

## GET 요청 보내기
#response = requests.get(url)

## 상태 코드 확인
#print(f"Status Code: {response.status_code}")

## 응답 데이터 (JSON) 출력
#if response.status_code == 200:
    #result = response.json()
    #result = json.loads(result)
    #pprint.pprint(result)
#else:
    #print("Failed to retrieve data")

# make_jwt.py 실행시켜서 token 발급 받을 것
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InRlc3RVc2VyQG5hdmVyLmNvbSIsImlhdCI6MTcyMzc1NjM0MiwiZXhwIjoxNzIzNzU4MTQyfQ.8oaBhl2__EWCtZ57uF8W6Jnvv70u5H_JxECsf_pmM_4"


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
#send_data = {
    #"header" : header,
    #"body" : {
        #'token' : token,
        #'type' : "solo"
    #}
#}

# home/try_select_my_bias
send_data = {
    "header" : header,
    "body" : {
        'token' : token,
        'bid' : "1001"
    }
}


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
result = json.loads(result)
pprint.pprint(result)