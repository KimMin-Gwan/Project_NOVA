from view.jwt_decoder import JWTManager, JWTPayload, RequestManager
from model import Mongo_Database, BaseModel, ContentModel
from others import ScheduleSearchEngine as SSE
from datetime import datetime
from pprint import pprint

import requests


class ContentController:
    def try_subscribe_chat(self, data_payload, content_key_storage):
        Client_Id = content_key_storage.chzzk_client_id
        Client_Secret = content_key_storage.chzzk_client_secret
        url="https://openapi.chzzk.naver.com/open/v1/sessions/events/subscribe/chat"
        
        #  headers = {
            #  "Client-Id": Client_Id,
            #  "Client-Secret": Client_Secret,
            #  "Content-Type": "application/json"
        #  }

        auth = f'Bearer {data_payload.access_token}'

        headers = {
            "Authorization" : auth,
            "Content-Type": "application/json"
        }

        
        requests_data = {
            'sessionKey' : data_payload.session_key
        }
        
        target_url = f'{url}?sessionKey={data_payload.session_key}'
        
        
        result = requests.post(
            url=target_url,
            headers=headers
        )
        
        # if not result:
            #return { "result" : 500 }
        
        
        #url2="https://openapi.chzzk.naver.com/open/v1/users/me"
        #result = requests.get(
            #url=url2,
            #headers=headers
        #)
        
        #pprint(result)
        
        #channelName = result.json()["content"]["channelName"]
        
        if result:
            return { "result" : 200 }
        else:
            return { "result" : 500 }
        
        
    
    
    def try_auth_chzzk(self, data_payload, content_key_storage):
        Client_Id = content_key_storage.chzzk_client_id
        Client_Secret = content_key_storage.chzzk_client_secret
        
        requests_data = {
            "grantType" : "authorization_code",
            "clientId": Client_Id,
            "clientSecret": Client_Secret,
            "code": data_payload.code,
            "state": data_payload.state
        }
        
        headers = {
            "Client-Id": Client_Id,
            "Client-Secret": Client_Secret,
            "Content-Type": "application/json"
        }
        
        token_result = requests.post(
            url="https://openapi.chzzk.naver.com/auth/v1/token",
            headers=headers,
            json=requests_data
        )
        
        token_result_json = token_result.json()
        
        access_token = token_result_json["content"]["accessToken"]
        refresh_token = token_result_json["content"]["refreshToken"]
        expires_in = token_result_json["content"]["expiresIn"]
        


        headers = {
            "Authorization": f"Bearer {access_token}",  # 유저 accessToken
            "Content-Type": "application/json"
        }

        response = requests.get(
            url = "https://openapi.chzzk.naver.com/open/v1/sessions/auth",
            headers=headers
            )

        url = response.json()["content"]["url"]
        
        result={
            'accessToken': access_token,
            'refreshToken': refresh_token,
            'tokenType':"Bearer",
            'expiresIn':"86400",
            'url' : url
        }
        
        return result
        
        
        
    
    
    # 뮤직 컨텐츠에서 초기에 갯수 받아오게 하는 부분
    def get_num_music_content(self, database, request):
        model = ContentModel(database=database)
        
        # 주제 수 찍어주면됨
        model.get_num_music_content()
        return model
    
    # sid 리스트로 스케줄 데이터 뽑아내기
    def get_music_content(self, database, request):
        model = ContentModel(database=database)
        
        # 주제 수 찍어주면됨
        model.get_music_content(data_payload=request.data_payload)
        return model
    
    def get_diff_image_content(self, database, request):
        model = ContentModel(database=database)
        
        # 주제 수 찍어주면됨
        model.get_diff_music_image_content()
        
        return model
        
    