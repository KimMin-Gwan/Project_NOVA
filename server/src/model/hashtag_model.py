from model.base_model import BaseModel
from model import Local_Database
#from others.data_domain import Alert
from others import CoreControllerLogicError,FeedManager, Bias, FeedSearchEngine


class HashTagModel(BaseModel):
    def __init__(self, database:Local_Database) -> None:
        super().__init__(database)
        self._hashtags = []
        self._bias = Bias()
        self._bids = self._user.bids

    # 로그인 확인 함수
    def is_user_login(self):
        if self._user.uid == "":
            return False
        else:
            self.set_bias()
            return True
    
    # 바이어스 데이터 구성
    def set_bias(self):
        if len(self._user.bids):

            # 지금은 어쩔 수 없이 bid를 하나만 세팅함
            # 나중에 고쳐야됨
            bias_data = self._database.get_data_with_id(target="bid", id=self._user.bids[0])
            if not bias_data:
                return False
            self._bias.make_with_dict(bias_data)
            return True
        else:
            return False

    # 유저 추천 해시태그
    def set_best_hashtag(self, feed_search_engine:FeedSearchEngine):
        self._hashtags = feed_search_engine.get_recommend_hashtag(bids=self._bids)
        return

    # 실시간/오늘의/이번 주/이달의 급상승 해시태그 인터페이스
    def set_today_best_hashtag(self, feed_search_engine:FeedSearchEngine, num_hashtags):
        self._hashtags = feed_search_engine.get_spiked_hashtags(target_type="today", num_hashtags=num_hashtags)
        return

    def set_weekly_best_hashtag(self, feed_search_engine:FeedSearchEngine, num_hashtags):
        self._hashtags = feed_search_engine.get_spiked_hashtags(target_type="weekly", num_hashtags=num_hashtags)
        return

    def set_monthly_best_hashtag(self, feed_search_engine:FeedSearchEngine, num_hashtags):
        self._hashtags = feed_search_engine.get_spiked_hashtags(target_type="monthly", num_hashtags=num_hashtags)
        return


    def set_realtime_best_hashtag(self, feed_search_engine:FeedSearchEngine, num_hashtag):
        self._hashtags =feed_search_engine.get_best_hashtag(num_hashtag=num_hashtag)
        return


    def get_response_form_data(self, head_parser):
        try:
            body = {
                "hashtags" : self._hashtags,
                "bid_list" : self._bias.bid
                }

            response = self._get_response_data(head_parser=head_parser, body=body)
            return response

        except Exception as e:
            raise CoreControllerLogicError("response making error | " + e)
