import json
import requests
import pprint

class Admin():
    def __init__(self) -> None:
        self.__key = 'nMjzkWLUCI0GfEPbkTut3qcWSxz2KVFx6jXQT4mVpbIV9CisdweCieYcC9AA3JuOYcPSIaT8ey7V9zSX'
        #self.__base_url= 'http://175.106.99.34/admin'
        self.__base_url= 'http://127.0.0.1:6000/admin'
        # HOST = '175.106.99.34'
        # HOST = '127.0.0.1'
        # PORT = 6000
        self.__header = {
            "request-type" : "default",
            "client-version" : 'v1.0.1',
            "client-ip" : '127.0.0.1',
            "uid" : '1234-abcd-5678', 
            "endpoint" : "/administrator_system/", 
    }
    def _check_data(self, data):
        print('완료 전 데이터를 다시 확인해 주세요')
        print(data)
        print('입력한 데이터가 맞으면 yes 잘못된 데이터가 입력되었을 시 no')
        control = input()
        if control == 'yes' or 'YES' or 'Yes':
            return True
        elif control == 'no' or "NO" or 'No':
            return False
        else:
            print('잘못된 응답입니다.')
            return False
    
    def _request(self,data,endpoint):
        send_data = {
        "header" : self.__header,
        "body" : {
            'admin_key' : self.__key,
            'data' : data
            }
        }

        headers = {
            'Content-Type': 'application/json'
        }
        send_data = json.dumps(send_data)
        send_data.encode()

        response = requests.post(url=self.__base_url+endpoint, data = send_data, headers=headers)
        response.encoding = 'utf-8'
        print(response)

        result = response.json()
        pprint.pprint(result)