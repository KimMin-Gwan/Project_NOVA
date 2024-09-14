from model.base_model import BaseModel
from model import Local_Database
from others.data_domain import Bias, League
from others import CoreControllerLogicError,FeedManager 

class HomeFeedModel(BaseModel):
    def __init__(self, database:Local_Database) -> None:
        super().__init__(database)
        self._feeds = []
        self._key = -1

    def get_feed_data(self, league_manager:FeedManager, key= -1):
        self._feeds, self._key = league_manager.get_feed_in_home(user=self._user, key=key)
        return

    def get_response_form_data(self, head_parser):
        try:
            body = {
                'feed' : self._make_dict_list_data(list_data=self._feeds),
                'key' : self._key
            }

            response = self._get_response_data(head_parser=head_parser, body=body)
            return response

        except Exception as e:
            raise CoreControllerLogicError("response making error | " + e)

