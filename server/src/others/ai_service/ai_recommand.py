from model.local_database_model import Local_Database
from others.data_domain import Feed
from others.feed_manager import FeedManager
from others.ai_service.feed_analyzer import FeedAnalyzer


#
class AnalyzedBias:
    def __init__(self, bid="", tag=[], target_fid=[]):
        self.bid = bid
        self.tag = tag
        self.target_fid = target_fid
        self.batch_bodies = []

class AIRecommender:
    def __init__(self, database:Local_Database, feed_manager:FeedManager= None,
                 ai_manager=None, feed_analyzer:FeedAnalyzer= None):
        self._database = database
        self._feed_manager = feed_manager
        self.__feed_analyzer = feed_analyzer
        self._analyzed_biases = []

        self.__init_bias()

    def __init_bias(self):
        bias_datas = self._database.get_all_data(target="bid")

        for bias_data in bias_datas:
            analyzed_bias = AnalyzedBias(bid=bias_data["bid"])
            self._analyzed_biases.append(analyzed_bias)
        return

    def __search_bias(self, target_bid):
        for analyzed_bias in self._analyzed_biases:
            if analyzed_bias.bid == target_bid:
                return analyzed_bias
        return None

    def __set_batch_body_by_feed(self, target_bid, batch_body, batch_size=4, batch_token=4096):
        # 배치사이즈를 이미 넘긴 경우, 넣지 않고 반환한다.
        analyzed_bias = self.__search_bias(target_bid)

        if len(analyzed_bias.batched_bodies) >= batch_size:
            return

        # 배치 사이즈를 넘기지 않은 경우, 글을 추가했을 때, batch_token을 넘기는지 확인한다.
        # 만약 넘겼다면 추가하지 않는다.
        length = 0
        for batch_body in batch_body:
            length += len(batch_body)

        if length >= batch_token:
            return

        analyzed_bias.batch_bodies.append(batch_body)
        return

    def __set_analyzed_bias(self, batch_size=4, batch_token=4096):
        batched_body_length = 0
        for analyzed_bias in self._analyzed_biases:
            for batch_body in analyzed_bias.batch_bodies:
                batched_body_length += len(batch_body)
            if len(analyzed_bias.batch_bodies) >= batch_size or batched_body_length >= batch_token:
                return analyzed_bias

    def pipeline_feed_recommend(self, feed:Feed, batch_token=4096, batch_size=4):
        # 작성한 Feed를 받아서
        # 글 전체에 대해 분석을 진행합니다.
        # FeedAnalyzer로 분석한 글들을 바탕으로 Writer가 재구성합니다.
        # 이를 반환합니다.
        # 다른 사항은 Feed Analyzer를 참고합니다.

        # 여기서 중요한 건 batch를 분석할 때, 시간상으로 분류할 것인가? 아니면.. batch stack으로 분류할 것인가.

        self.__set_batch_body_by_feed(target_bid=feed.bid, batch_body=feed.body,
                                      batch_size=batch_size, batch_token=batch_token)

        analyzed_bias = self.__set_analyzed_bias(batch_size=batch_size, batch_token=batch_token)

        # AI를 이용해서 Feed를 작성합니다.
        # FeedManager에 AI가 스스로 작성하는 기능이 없네요
        #ai_feed_body = self._ai_manager.try_make_new_ai_feed_body()
        
        # AI가 짠 Feed
        ai_feed = self._feed_manager.create_ai_feed(body=ai_feed_body)

        # 이 feed를 반환합니다.

        return ai_feed





