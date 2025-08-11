from model.base_model import BaseModel
from typing import List
import random

from model import Mongo_Database
#from others.data_domain import Alert
from pprint import pprint

class Content():
    def __init__(self, id):
        self.id = id
    
    def make_with_dict(self, dict_data:dict):
        self.id = dict_data.get("id", "")
        return self

    def get_dict_form_data(self):
        return {
            "id" : self.id
        }


class MusicContent(Content):
    def __init__(self, id="", title="", answer=[], url="", artist="", tag=""):
        self.id = id
        self.title = title
        self.answer:list =answer 
        self.url = url
        self.artist = artist
        self.tag = tag
        
    def make_with_dict(self, dict_data:dict):
        self.id = dict_data.get("id", "")
        self.title = dict_data.get("title", "")
        self.answer = dict_data.get("answer", [self.title])
        self.url= dict_data.get("url", "")
        self.artist = dict_data.get("artist", "")
        self.tag= dict_data.get("tag", "")
        return self

    def get_dict_form_data(self):
        return {
            "id" : self.id,
            "title" : self.title,
            "answer" : self.answer,
            "url" : self.url,
            "artist" : self.artist,
            "tag" : self.tag
        }

class DiffImageContent(Content):
    def __init__(self, id="", title="", right_answer=[]):
        self.id = id
        self.title= title
        self.right_answer = right_answer
        
    def make_with_dict(self, dict_data:dict):
        self.id = dict_data.get("id", "")
        self.title = dict_data.get("title", "")
        self.right_answer = dict_data.get("right_answer", [self.title])
        return self

    def get_dict_form_data(self):
        return {
            "id" : self.id,
            "title" : self.title,
            "right_answer" : self.right_answer,
        }


class ContentModel(BaseModel):
    def __init__(self, database:Mongo_Database) -> None:
        super().__init__(database)
        self.__contents:List[Content] = []
        self.__meta_data = {}


    # 뮤직 컨텐츠에서 뮤직의 갯수를 알아야 문제 갯수를 정할 수 있음
    def get_num_music_content( self):
        music_datas = self._database.get_datas_with_key(target="content", key="type", key_datas=["music"])
        
        dict_data:dict = {
            "전체" : 0
        }
        
        for music_data in music_datas:
            music_content = MusicContent().make_with_dict(dict_data=music_data)
            
            # 찾아서 1 올리기
            tag_flag = False
            for tag, _ in dict_data.items():
                if music_content.tag == tag:
                    dict_data[tag] += 1
                    tag_flag = True
                
            # 만약에 못찾으면 생성하고 1 올려주면됨
            if not tag_flag:
                dict_data[music_content.tag] = 1
            
            # 전체 갯수도 1씩 올려줘라
            dict_data["전체"] += 1
            
        self.__meta_data = dict_data
        return 

    # 노래 맞추기 컨텐츠 불러오는곳
    # type은 노래 타입임. 대충 무슨 장르, 특징 같은거
    def get_music_content(
            self, data_payload
        ):  
        music_datas = self._database.get_datas_with_key(target="content", key="type", key_datas=["music"])
        
        # 랜덤하게 섞어주자
        random.shuffle(music_datas)
        
        
        
        
        for music_data in music_datas:
            music_content = MusicContent().make_with_dict(dict_data=music_data)
            # 타입이 default면 그냥 싹다 보내주면됨
            if music_content.tag == data_payload.type or data_payload.type == "전체":
                self.__contents.append(music_content)
            
            if data_payload.num_content != 0:
                if len(self.__contents) >= data_payload.num_content:
                    break
                
        return
    
    

    #---------------------------------------------------------------------
    
    
    
    def get_diff_music_image_content(
            self 
        ):  
        image_datas = self._database.get_datas_with_key(target="content", key="type", key_datas=["image"])
        
        for image_data in image_datas:
            image_content= DiffImageContent().make_with_dict(dict_data=image_data)
            self.__contents.append(image_content)
        return
    
    
    
    
    #--------------------------------------------------------------------
    
    
    

    def get_response_form_data(self, head_parser):
        body = {
            "content" : self._make_dict_list_data(list_data=self.__contents),
            "meta_data" : self.__meta_data
        }

        response = self._get_response_data(head_parser=head_parser, body=body)
        return response
