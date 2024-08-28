# post 요청
 + json의 필수 입력 사항은 아래와 같다.
```
header = {
    "request-type" : "default",
    "client-version" : 'v1.0.1',
    "client-ip" : '127.0.0.1',
    "uid" : '1234-abcd-5678', 
    "endpoint" : "/user_system/", 
}
```
```
send_data = {
    "header" : header,
    "body" : {
        'token' : token,
        'type' : 'group'  # 'solo'
    }
}
 ```
## 최애 인증 페이지 접근
 + 목적 :  최애 인증 페이지에 데이터를 불러오기 위한 목적
 + url : http://nova-platform.kr/nova_check/server_info/check_page
 + 기타 : 이미 인증을 수행한 사람과 아닌 사람의 결과값이 다름, result를 보고 판단할 것(valid -> 아직 안함, done -> 이미 했음, invalid -> 비정상 요청, error -> 죽음)
 + send_data 예시
```
send_data = {
    "header" : header,
    "body" : {
        'token' : token,
        'type' : 'group'  # 'solo'
    }
}
```
 + 응답 예시
![캡처2](https://github.com/user-attachments/assets/dc90bbf0-681f-4ab7-a52b-8bdf59e95a3d)
- 아직 인증을 수행하지 않은 사람의 경우

 - 이미 인증을 수행한 사람의 경우
![캡처](https://github.com/user-attachments/assets/8bfcdf88-b586-4472-962a-47a102f127a4)


## 최애 인증 요청
 + 목적 :  최애 인증 페이지에서 최애 인증 버튼을 눌러 최애 인증을 시도할 때
 + url : http://nova-platform.kr/nova_check/server_info/try_daily_check
 + 기타 : result를 보고 판단해야함 (valid -> 아직 안함, done -> 이미 했음, invalid -> 비정상 요청, error -> 죽음)
 + send_data 예시
```
send_data = {
    "header" : header,
    "body" : {
        'token' : token,
        'type' : 'group'  # 'solo'
    }
}
```
 + 응답 예시
![캡처3](https://github.com/user-attachments/assets/eb65bce2-9c36-48d1-8ecb-4ce884f49d33)
 - 정상적인 인증 성공 


![캡처4](https://github.com/user-attachments/assets/cdef41fe-8a24-4cad-ad5a-d70c1d97d51f)
 - 이미 인증을 했는데 또 시도하면

## 특별 인증 요청
 + 목적 :  최애 인증 페이지에서 특별 인증을 시도할 때
 + url : http://nova-platform.kr/nova_check/server_info/try_special_check
 + 기타 : 기존에 보내준 special_time리스트에 현재 시간(시)가 포함되어 있는지 판단 후 전송 혹은 전송 안 함(alert로 경고)
 + send_data 예시
```
send_data = {
    "header" : header,
    "body" : {
        'token' : token,
        'type' : 'group'  # 'solo'
    }
}
```
 + 응답 예시
![캡처5](https://github.com/user-attachments/assets/7eb601bf-66c6-4096-af3d-15121d5078dd)
 - 성공

![캡처6](https://github.com/user-attachments/assets/f9a8b3e9-1107-463e-8936-902b5edba7cd)
 - 실패



