import json
import requests
import pprint
import boto3

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

        self._path = './model/local_database/'
        self.__service_name = 's3'
        self.__endpoint_url = 'https://kr.object.ncloudstorage.com'
        self.__region_name = 'kr-standard'
        self.__access_key = 'eeJ2HV8gE5XTjmrBCi48'
        self.__secret_key = 'zAGUlUjXMup1aSpG6SudbNDzPEXHITNkEUDcOGnv'
        self._s3 = boto3.client(self.__service_name,
                           endpoint_url=self.__endpoint_url,
                           aws_access_key_id=self.__access_key,
                      aws_secret_access_key=self.__secret_key)

    def _check_data(self, data):
        print('완료 전 데이터를 다시 확인해 주세요')
        print(data)
        print('입력한 데이터가 맞으면 y 잘못된 데이터가 입력되었을 시 n')
        control = input('입력: ')
        if control == 'y':
            return True
        elif control == 'n':
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