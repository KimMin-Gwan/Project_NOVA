from view.jwt_decoder import JWTManager, JWTPayload, RequestManager
from model import Local_Database, BaseModel, ContentModel
from others import ScheduleSearchEngine as SSE
from datetime import datetime
from pprint import pprint

import requests






class ContentController:
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
        
        
        result = requests.post(
            url="https://openapi.chzzk.naver.com/auth/v1/token",
            headers=headers,
            data=requests_data
        )
        
        pprint(result.json())
        
        result={
            'accessToken':"temp",
            'refreshToken':"temp",
            'tokenType':"Bearer",
            'expiresIn':"86400"
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
        
    