from model.base_model import BaseModel
from model import Local_Database
#from others.data_domain import Alert

class TimeTableModel(BaseModel):
    def __init__(self, database:Local_Database) -> None:
        super().__init__(database)
        self._feeds = []
        
    def get_response_form_data(self, head_parser):
        body = {
            "result" : self._result,
            }

        response = self._get_response_data(head_parser=head_parser, body=body)
        return response
