import requests
import json
import pprint

#HOST = '223.130.157.23'
#PORT = 80
HOST = '127.0.0.1'
PORT = 6000

def send_data():

    url = f'http://{HOST}:{str(PORT)}/core_system/home/daily'


    header = {
        "request-type" : "default",
        "client-version" : 'v1.0.1',
        "client-ip" : '127.0.0.1',
        "uid" : '1234-abcd-5678', 
        "endpoint" : "/core_system/", 
    }


    send_data = {
        "header" : header,
        "body" : {
            'email' : 'testUser@naver.com',
            'token' : '1234'
        }
    }

    headers = {
        'Content-Type': 'application/json'
    }


    # send_data = json.dumps(send_data)
    # send_data.encode()

    # uid = '1234-abcd-5678'
    # token = '1'
    # url = f'http://{HOST}:{str(PORT)}/home/my_bias/testUser@naver.com/1'
    # response = requests.get(url)
    

    # response = requests.post(url=url, data = send_data, headers=headers)

    send_data = json.dumps(send_data)
    send_data.encode()
    response = requests.post(url=url, data = send_data, headers=headers)
    response.encoding = 'utf-8'
    print(response)

    result = response.json()
    result = json.loads(result)
    pprint.pprint(result)



if __name__ == '__main__':
    send_data()
