from model.base_model import AdminModel
from model import Local_Database
from others.data_domain import League
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
        self.__leagues = []
    
    def upload_league_data(self):
        try:
            now = datetime.datetime.now()
            date = now.strftime('%Y-%m-%d')
            self.__s3.upload_file(f'{self.__path}league.json', "nova-leagues", f"league{date}.json")
            return True
        
        except Exception as e:
            raise CoreControllerLogicError(error_type="upload_league_data | " + str(e))
        
    def set_leagues(self) -> bool: 
        try:
            league_data = self._database.get_all_data(target="league")

            if not league_data:
                return False

            for data in league_data:
                self.__leagues.append(data)
            
            return True
        except Exception as e:
            raise CoreControllerLogicError(error_type="set_leagues | " + str(e))
        
    def reset_point(self) -> bool:
        try:
            if not self.__leagues:
                return False
            
            for league in self.__leagues:
                league.solo_point=0
                league.group_point=0
                self._database.modify_data_with_id(target_id='lid',target_data=league)

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