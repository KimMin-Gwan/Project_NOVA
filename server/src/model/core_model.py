from model.base_model import BaseModel
from model import Mongo_Database
from others import CoreControllerLogicError
from pprint import pprint


class TokenModel(BaseModel):
    def __init__(self, database:Mongo_Database) -> None:
        super().__init__(database)

    def get_response_form_data(self, head_parser):
        try:
            body = {
                'result' : True,
                'user' : self._user.uid,
                'uimage' : self._user.uimage
            }

            response = self._get_response_data(head_parser=head_parser, body=body)
            return response

        except Exception as e:
            raise CoreControllerLogicError("response making error | " + e)




