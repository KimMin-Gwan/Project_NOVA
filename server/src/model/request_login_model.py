from model.base_model import BaseModel
from model import Local_Database
from others.data_domain import User
from others import CoreControllerLogicError

class RequestLogin(BaseModel):
    def __init__(self, database:Local_Database) -> None:
        super().__init__(database)
        self.__res = ''

    def request_login(self,request,token) -> bool: 
        try:
            if request.token == token:
                self.__res = 'approved'
            else:
                self.__res = 'access denied'
            
            return True
        
        except Exception as e:
            raise CoreControllerLogicError(error_type="set_group_leagues | " + str(e))


    def get_response_form_data(self, head_parser):
        try:
            body = {
                'response' : self.__res
            }

            response = self._get_response_data(head_parser=head_parser, body=body)
            return response

        except Exception as e:
            raise CoreControllerLogicError("response making error | " + e)