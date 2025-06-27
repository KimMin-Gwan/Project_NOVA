from model.base_model import BaseModel
from typing import List

from model import Local_Database
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
    def __init__(self, id="", title="",
                 right_answer=[], music_id="", type=""):
        self.id = id
        self.title = title
        self.right_answer:list = right_answer
        self.music_id = music_id
        self.type = type
        
    def make_with_dict(self, dict_data:dict):
        self.id = dict_data.get("id", "")
        self.title = dict_data.get("title", "")
        self.right_answer = dict_data.get("right_answer", [self.title])
        self.music_id = dict_data.get("music_id", "")
        self.type = dict_data.get("type", "")
        return self

    def get_dict_form_data(self):
        return {
            "id" : self.id,
            "title" : self.title,
            "right_answer" : self.right_answer,
            "music_id" : self.music_id,
            "type" : self.type
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
    def __init__(self, database:Local_Database) -> None:
        super().__init__(database)
        self.__contents:List[Content] = []

    # 노래 맞추기 컨텐츠 불러오는곳
    # type은 노래 타입임. 대충 무슨 장르, 특징 같은거
    def get_music_content(
            self, data_payload
        ):  
        music_datas = self._database.get_datas_with_key(target="content", key="type", key_datas=["music"])
        
        for music_data in music_datas:
            music_content = MusicContent().make_with_dict(dict_data=music_data)
            # 타입이 default면 그냥 싹다 보내주면됨
            if music_content.type == data_payload.type or data_payload.type == "default":
                self.__contents.append(music_content)
        return
    
    
    def get_diff_music_image_content(
            self 
        ):  
        image_datas = self._database.get_datas_with_key(target="content", key="type", key_datas=["image"])
        
        for image_data in image_datas:
            image_content= DiffImageContent().make_with_dict(dict_data=image_data)
            self.__contents.append(image_content)
        return

    def get_response_form_data(self, head_parser):
        body = {
            self._make_dict_list_data(list_data=self.__contents)
        }

        response = self._get_response_data(head_parser=head_parser, body=body)
        return response
