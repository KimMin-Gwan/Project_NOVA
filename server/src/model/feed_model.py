from model.base_model import BaseModel
from model import Local_Database
#from others.data_domain import Alert
from others import CoreControllerLogicError,FeedManager 

class FeedModel(BaseModel):
    def __init__(self, database:Local_Database) -> None:
        super().__init__(database)
        self._feeds = []
        self._key = -1
        self._comments = []

    def set_home_feed_data(self, feed_manager:FeedManager, key= -1):
        self._feeds, self._key = feed_manager.get_feed_in_home(user=self._user, key=key)
        return

    def set_specific_feed_data(self, feed_manager:FeedManager, data_payload):
        self._feeds, self._key = feed_manager.get_feed_in_fclass(user=self._user,
                                                                  key=data_payload.key,
                                                                  fclass=data_payload.fclass)
        return
    
    def try_interact_feed(self, feed_manager:FeedManager, data_payload):
        self._feeds = feed_manager.try_interaction_feed(user=self._user,
                                                    fid=data_payload.fid,
                                                    action=data_payload.action)
        return

    def try_staring_feed(self, feed_manager:FeedManager, data_payload):
        self._feeds = feed_manager.try_staring_feed(user=self._user,
                                                    fid=data_payload.fid)
        return

    def try_make_new_comment(self, feed_manager:FeedManager, data_payload):
        self._feeds = feed_manager.make_new_comment_on_feed(user=self._user,
                                                    fid=data_payload.fid,
                                                    body=data_payload.body)
        self._comments = feed_manager.get_all_comment_on_feed( user=self._user,
                                                               fid=data_payload.fid)
        return

    def get_all_comment_on_feed(self, feed_manager:FeedManager, data_payload):
        self._comments = feed_manager.get_all_comment_on_feed( user=self._user,
                                                               fid=data_payload.fid)
        return

    def try_remove_comment(self, feed_manager:FeedManager, data_payload):
        self._feeds= feed_manager.remove_comment_on_feed( user=self._user,
                                                               fid=data_payload.fid,
                                                               cid=data_payload.cid)
        self._comments = feed_manager.get_all_comment_on_feed( user=self._user,
                                                               fid=data_payload.fid)
        return

    def try_like_comment(self, feed_manager:FeedManager, data_payload):
        self._feeds= feed_manager.try_like_comment( user=self._user,
                                                               fid=data_payload.fid,
                                                               cid=data_payload.cid)
        self._comments = feed_manager.get_all_comment_on_feed( user=self._user,
                                                               fid=data_payload.fid)
        return

    def get_response_form_data(self, head_parser):
        try:
            body = {
                'feed' : self._make_dict_list_data(list_data=self._feeds),
                'key' : self._key,
                'comments' : self._make_dict_list_data(list_data=self._comments)
            }

            response = self._get_response_data(head_parser=head_parser, body=body)
            return response

        except Exception as e:
            raise CoreControllerLogicError("response making error | " + e)


# feed 의 메타 정보를 보내주는 모델
class FeedMetaModel(BaseModel):
    def __init__(self, database:Local_Database) -> None:
        super().__init__(database)
        self._feed_meta_data = []

    def set_feed_meta_data(self, feed_manager:FeedManager):
        self._feeds = feed_manager.get_feed_meta_data()
        return
    
    def __make_send_data(self):
        result = []
        for fclass in self._feeds:
            single_data = {
                "fname" : fclass.fname,
                "fclass" : fclass.fclass,
                "specific" : fclass.specific
            }
            result.append(single_data)
        return result

    def get_response_form_data(self, head_parser):
        try:
            body = {
                'feed_meta_data' : self.__make_send_data(),
            }

            response = self._get_response_data(head_parser=head_parser, body=body)
            return response

        except Exception as e:
            raise CoreControllerLogicError("response making error | " + e)

# feed 의 메타 정보를 보내주는 모델
class FeedEditModel(BaseModel):
    def __init__(self, database:Local_Database) -> None:
        super().__init__(database)
        self._result= False
        self._detail = "Somthing goes Bad| Error Code = 422"

    def set_feed_meta_data(self, feed_manager:FeedManager):
        self._feeds = feed_manager.get_feed_meta_data()
        return
    
    def __make_send_data(self):
        result = []
        for fclass in self._feeds:
            single_data = {
                "" : fclass.fname,
            }
            result.append(single_data)
        return result

    def get_response_form_data(self, head_parser):
        try:
            body = {
                'feed_meta_data' : self.__make_send_data(),
            }

            response = self._get_response_data(head_parser=head_parser, body=body)
            return response

        except Exception as e:
            raise CoreControllerLogicError("response making error | " + e)
