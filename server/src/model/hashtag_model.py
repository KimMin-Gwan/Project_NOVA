from model.base_model import BaseModel
from model import Local_Database
#from others.data_domain import Alert
from others import CoreControllerLogicError,FeedManager, Bias, FeedSearchEngine


class HashTagModel(BaseModel):
    def __init__(self, database:Local_Database) -> None:
        super().__init__(database)
        self._hashtags = []
        self._bias = Bias()
        self._title = ""

    def is_user_login(self):
        if self._user.uid == "":
            return False
        else:
            bias_data = self._database.get_data_with_id(target="bid", id=self._bias.bid)
            if not bias_data:
                return False
            self._bias.make_with_dict(bias_data)
            self._title=self._bias.bname
            return True

    def set_best_hash_tag(self, feed_search_engine:FeedSearchEngine):
        print(self._bias.bid)

        self._hashtags = feed_search_engine.get_recommnad_hashtag(bid=self._bias.bid)
        return

    def set_realtime_best_hash_tag(self, feed_search_engine:FeedSearchEngine, num_hashtag):
        self._hashtags =feed_search_engine.get_best_hashtag(num_hashtag=num_hashtag)

        #self._hashtags = ["에스파", "경민생카", "조슈아생일시", "Mantra", "제니",
                        #"오뱅온", "지스타", "숲인방", "버츄얼하꼬", "가을야구"]

        return

    def get_response_form_data(self, head_parser):
        try:
            body = {
                "hashtags" : self._hashtags,
                "title" : self._title,
                "bid" : self._bias.bid
                }

            response = self._get_response_data(head_parser=head_parser, body=body)
            return response

        except Exception as e:
            raise CoreControllerLogicError("response making error | " + e)
