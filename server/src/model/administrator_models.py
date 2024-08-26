from model.base_model import AdminModel
from model import Local_Database
from others.data_domain import League, User, Bias
from others import CoreControllerLogicError

import boto3
import datetime

class ResetLeaguesModel(AdminModel):
    def __init__(self, database:Local_Database) -> None:
        super().__init__(database)
        self.__response = 'failed'
        self.__path = './model/local_database/'
        self.__service_name = 's3'
        self.__endpoint_url = 'https://kr.object.ncloudstorage.com'
        self.__region_name = 'kr-standard'
        self.__access_key = 'eeJ2HV8gE5XTjmrBCi48'
        self.__secret_key = 'zAGUlUjXMup1aSpG6SudbNDzPEXHITNkEUDcOGnv'
        self.__s3 = boto3.client(self.__service_name,
                           endpoint_url=self.__endpoint_url,
                           aws_access_key_id=self.__access_key,
                      aws_secret_access_key=self.__secret_key)
        self.__users = []
        self.__biases = []
    #json파일 버킷에 업로드
    def upload_data(self):
        try:
            now = datetime.datetime.now()
            date = now.strftime('%Y-%m-%d')
            data = ['bias','user']
            for i in data:
                self.__s3.upload_file(f'{self.__path}{i}.json', f"nova-{i}", f"{i}{date}.json")
            return True
        
        except Exception as e:
            raise CoreControllerLogicError(error_type="upload_league_data | " + str(e))
    #유저 불러오기
    def set_users(self) -> bool: 
        try:
            user_data = self._database.get_all_data(target="user")

            if not user_data:
                return False

            for data in user_data:
                user = User()
                user.make_with_dict(data)
                self.__users.append(user)
            
            return True
        except Exception as e:
            raise CoreControllerLogicError(error_type="set_leagues | " + str(e))
    #bias 불러오기
    def set_biases(self) -> bool: 
        try:
            bias_data = self._database.get_all_data(target="bias")

            if not bias_data:
                return False

            for data in bias_data:
                bias = Bias()
                bias.make_with_dict(data)
                self.__biases.append(bias)
            
            return True
        except Exception as e:
            raise CoreControllerLogicError(error_type="set_leagues | " + str(e))
    #포인트랑 콤보 초기화 ( 함수 이름 변경 필요 )
    def reset_point(self) -> bool:
        try:
            if not self.__users:
                return False
            if not self.__biases:
                return False
            
            for user in self.__users:
                user.solo_point = 0
                user.group_point = 0
                user.combo = 0
                user.solo_combo = 0
                user.group_combo = 0
                self._database.modify_data_with_id(target_id='uid',target_data=user.get_dict_form_data())
            
            for bias in self.__biases:
                bias.point=0
                self._database.modify_data_with_id(target_id='bid',target_data=bias.get_dict_form_data())

            self.__set_response()
            return True
        except Exception as e:
            raise CoreControllerLogicError(error_type="reset_point | " + str(e))
    
    def __set_response(self):
        self.__response = 'success'

    def get_response_form_data(self, head_parser):
        try:
            body = {
                'response' : self.__response
            }

            response = self._get_response_data(head_parser=head_parser, body=body)
            return response

        except Exception as e:
            raise CoreControllerLogicError("response making error | " + e)