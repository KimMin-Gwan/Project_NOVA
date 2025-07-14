from view.jwt_decoder import JWTManager, JWTPayload, RequestManager
from model import Local_Database, BaseModel, ContentModel
from others import ScheduleSearchEngine as SSE
from datetime import datetime


class ContentController:
    
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
        
    