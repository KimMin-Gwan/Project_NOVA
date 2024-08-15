from model.local_database_model import Local_Database
from others.data_domain import User
from view.parsers import Head_Parser
import json
from others import CoreControllerLogicError

import editdistance
from jamo import h2j, j2hcj

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

    def _get_response_data(self, head_parser:Head_Parser, body):
        header = head_parser.get_header()
        header['state-code'] = self._state_code
        form = {
            'header' : header,
            'body' : body
        }

        response = json.dumps(form, ensure_ascii=False)
        return response

    def set_state_code(self, state_code):
        self._state_code = state_code
        return


class BaseModel(HeaderModel):
    def __init__(self, database) -> None:
        self._database:Local_Database = database
        self._user = User()  # 이거 고려해야됨
        super().__init__()

    # 유저의 정보를 검색하는 함수
    def set_user_with_uid(self, request):
        # uid를 기반으로 user table 데이터와 userbias 데이터를 가지고 올것
        try:
            user_data = self._database.get_data_with_id(target="uid", id=request.uid)
        except:
            user_data = self._database.get_data_with_id(target="uid", id=request['uid'])

        if not user_data:
            return False
        self._user.make_with_dict(user_data)
        return True
    
    def set_user_with_email(self, request):
        # email 기반으로 user table 데이터와 userbias 데이터를 가지고 올것
        try:
            user_data = self._database.get_data_with_key(target='user', key='email', key_data=request.email)
        except:
            user_data = self._database.get_data_with_key(target='user', key='email', key_data=request['email'])
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
    def _set_list_alignment(self, league_list, align): #정렬
        if align == "type":
            sorted_products = sorted(league_list, key=lambda x: x.type , reverse=False)
        elif align == "point":
            sorted_products = sorted(league_list, key=lambda x: x.point, reverse=True)
        elif align == "lid":
            sorted_products = sorted(league_list, key=lambda x: x.lid, reverse=True)
        else:
            sorted_products = sorted(league_list, key=lambda x: x.bid, reverse=True)
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

