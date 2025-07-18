import requests
import json
import pprint

#HOST = '223.130.157.23'
#PORT = 80
HOST = '175.106.99.34'
PORT = 6000

 #요청을 보낼 URL
 #get
url = "https://supernova.io.kr/nova_sub_system/image_tag"  # 이미지 태그?




##GET 요청 보내기
#response = requests.get(url)

## # 상태 코드 확인
#print(f"Status Code: {response.status_code}")

 ## 응답 데이터 (JSON) 출력
#if response.status_code == 200:
    #result = response.json()
    ##result = response.text
    #pprint.pprint(result)
#else:
     #print("Failed to retrieve data")
#exit()


# make_jwt.py 실행시켜서 token 발급 받을 것


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

# home/my_bias_league
# nova-check/server/check_page
send_data = {
    "header" : header,
    "body" : {
        'url' : "https://smartstore.naver.com/kuksosu/products/9795815241?NaPm=ci%3D26KXiANZdyRJqg5J9SUvpFIg%7Ctr%3Dgfa%7Cct%3Dm6sztdcc%7Chk%3Dc70e722bcc94efb1bb0248f1d66c8584eaac8d3c%7Cnacn%3DC4a4BcQbqfpxA"
    }
}

## home/try_select_my_bias
## bias_info/my_contribution
#send_data = {
    #"header" : header,
    #"body" : {
        #'token' : token,
        #'bid' : "1001"
    #}
#}


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