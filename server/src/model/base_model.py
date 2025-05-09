from model.local_database_model import Local_Database
from others.data_domain import User
from view.parsers import Head_Parser
from others import CoreControllerLogicError
from pprint import pprint

import editdistance
from jamo import h2j, j2hcj

import boto3
from datetime import datetime
import random

class FindSimilarData:
    def __decompose(self, text:str):
        return ''.join(j2hcj(h2j(text.replace(" ", ""))))

    def search_similar(self, data_list:list, key_word:str, key_attr:str):
        results = []
        decomposed_key_data = self.__decompose(key_word)
        for item in data_list:
            target_item = getattr(item, key_attr)
            decomposed_item = self.__decompose(target_item)
            distance = editdistance.eval(decomposed_item, decomposed_key_data)
            if distance <= len(decomposed_item) - len(decomposed_key_data):
                results.append(item)
        return results

class HeaderModel:
    def __init__(self) -> None:
        self._state_code = '500'
        self._new_token = ""

    def _get_response_data(self, head_parser:Head_Parser, body):
        header = head_parser.get_header()
        header['state-code'] = self._state_code
        header['new_token'] = self._new_token
        form = {
            'header' : header,
            'body' : body
        }

        #response = json.dumps(form, ensure_ascii=False)
        response = form
        return response

    def set_state_code(self, state_code):
        self._state_code = state_code
        return
    
    def set_token_data(self, new_token):
        self._new_token = new_token
        return

import string
class BaseModel(HeaderModel):
    def __init__(self, database) -> None:
        self._database:Local_Database = database
        self._user = User()  # 이거 고려해야됨
        super().__init__()
        
    def get_user(self):
        return self._user

    def _make_new_id(self):
        characters = string.ascii_letters + string.digits
        
        random_string = ''.join(random.choice(characters) for _ in range(6))
        
        return random_string
    
    def _get_datetime(self, date_str):
        return datetime.strptime(date_str, "%Y/%m/%d-%H:%M:%S")

    def _set_datetime(self):
        return datetime.now().strftime("%Y/%m/%d-%H:%M:%S")

    # 유저의 정보를 검색하는 함수
    def set_user_with_uid(self, request):
        
        # uid를 기반으로 user table 데이터와 userbias 데이터를 가지고 올것
        user_data = self._database.get_data_with_id(target="uid", id=request.uid)

        if not user_data:
            return False
        self._user.make_with_dict(user_data)
        return True
    
    def set_user_with_email(self, request):
        # email 기반으로 user table 데이터와 userbias 데이터를 가지고 올것
        user_data = self._database.get_data_with_key(target='user', key='email', key_data=request.email)
        if not user_data:
            return False
        self._user.make_with_dict(user_data)
        return True

    # 가장 근접한 문자열을 찾는 함수
    def _search_similar_data(self, data_list:list, key_word:str, key_attr:str):
        find_similar_data = FindSimilarData()
        result = find_similar_data.search_similar(data_list=data_list,
                                          key_word=key_word, key_attr=key_attr)
        return result
    
    # 정렬 함수
    # self._set_list_alignment(image_list = images, align = request.ordering)
    def _set_list_alignment(self, bias_list, align): #정렬
        if align == "type":
            sorted_products = sorted(bias_list, key=lambda x: x.type , reverse=False)
        elif align == "point":
            sorted_products = sorted(bias_list, key=lambda x: x.point, reverse=True)
        elif align == "bid":
            sorted_products = sorted(bias_list, key=lambda x: x.bid, reverse=True)
        else:
            sorted_products = sorted(bias_list, key=lambda x: x.bid, reverse=True)
        #sorted_products = sorted(product_list, key=lambda x: datetime.strptime(x.date, "%Y/%m/%d"))
        return sorted_products
    
    # 추상
    def get_response_form_data(self,head_parser):
        try:
            body = {
                "default" : "Default state get_response_form_data func"
            }

            response = self._get_response_data(head_parser=head_parser, body=body)
            return response

        except Exception as e:
            raise CoreControllerLogicError(error_type="response making error | " + str(e))

    # 리스트 인스턴스를 딕셔너리형태로 변경시켜줌
    def _make_dict_list_data(self, list_data:list)-> list:
        dict_list_data = []
        for data in list_data:
            dict_list_data.append(data.get_dict_form_data())
        return dict_list_data

class AdminModel(HeaderModel):
    def __init__(self, database) -> None:
        self._database:Local_Database = database

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
        
        #서버에 저장된 관리자 키
        self.__key = 'nMjzkWLUCI0GfEPbkTut3qcWSxz2KVFx6jXQT4mVpbIV9CisdweCieYcC9AA3JuOYcPSIaT8ey7V9zSX'
        super().__init__()
        
    #관리자 키가 맞는지 확인
    def check_admin_key(self, request):
        # uid를 기반으로 user table 데이터와 userbias 데이터를 가지고 올것
        if self.__key == request.admin_key:
            return True
        else:
            return False
    def _upload_data(self, data_type):
        now = datetime.now()
        date = now.strftime('%Y-%m-%d-%H:%M:%S')
        self._s3.upload_file(f'{self.__path}{data_type}.json', f"nova-{data_type}", f"{data_type}{date}.json")
    
    def get_response_form_data(self,head_parser):
        try:
            body = {
                "default" : "Default state get_response_form_data func"
            }

            response = self._get_response_data(head_parser=head_parser, body=body)
            return response

        except Exception as e:
            raise CoreControllerLogicError(error_type="response making error | " + str(e))