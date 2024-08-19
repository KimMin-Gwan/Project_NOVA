from model.base_model import BaseModel
from model import Local_Database
from others.data_domain import Bias, League
from others import CoreControllerLogicError

class SampleModel(BaseModel):
    def __init__(self, database:Local_Database) -> None:
        super().__init__(database)
        self.__result = False

    def set_function(self):
        try:
            data = self._database.get_all_data(target="banner")
            self.__result = True 

        except Exception as e:
            raise CoreControllerLogicError(error_type="set_group_leagues | " + str(e))

    def get_response_form_data(self, head_parser):
        try:
            body = {
                'result ': self.__result
            }

            response = self._get_response_data(head_parser=head_parser, body=body)
            return response

        except Exception as e:
            raise CoreControllerLogicError("response making error | " + e)