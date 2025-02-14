from model.local_database_model import Local_Database
from others.feed_manager import FeedManager
from others.ai_service.feed_analyzer import FeedAnalyzer
from others.ai_service.ai_manager import AIManager


class AnalyzedBias():
    def __init__(self, bid="", tag=[], target_fid=[]):
        self.bid = bid
        self.tag = tag
        self.target_fid = target_fid

class AIRecommender:
    def __init__(self, database:Local_Database, feed_manager:FeedManager= None,
                 ai_manager:AIManager=None, feed_analyzer:FeedAnalyzer= None):
        self._database = database
        self._feed_manager = feed_manager
        self._ai_manager = ai_manager
        self.__feed_analyzer = feed_analyzer
        
    def __init_bias(self, bid, tag, target_fid):
        self.analyzed_bias = AnalyzedBias(bid=bid, tag=tag, target_fid=target_fid)

    async def pipeline_feed_recommend(self, feeds:list):
        # 작성한 Feed를 받아서
        # 글 전체에 대해 분석을 진행합니다.
        # FeedAnalyzer로 분석한 글들을 바탕으로 Writer가 재구성합니다.
        # 이를 반환합니다.
        # 다른 사항은 Feed Analyzer를 참고합니다.

        # 여기서 중요한 건 batch를 분석할 때, 시간상으로 분류할 것인가? 아니면.. batch stack으로 분류할 것인가.

        batched_feeds = []
        self.analyzed_bias.tag = self.__feed_analyzer.pipeline_analyze_tag(batched_feeds)

        # AI를 이용해서 Feed를 작성합니다.
        # FeedManager에 AI가 스스로 작성하는 기능이 없네요
        ai_feed_body = self._ai_manager.try_make_new_ai_feed_body(tags=self.analyzed_bias.tag)
        # AI가 짠 Feed
        ai_feed = self._feed_manager.create_ai_feed(body=ai_feed_body)

        # 이 feed를 반환합니다.

        return ai_feed





