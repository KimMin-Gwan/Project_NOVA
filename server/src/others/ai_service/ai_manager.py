from others.data_domain import Feed
from others.ai_service.feed_analyzer import FeedAnalyzer

# 외부 인터페이스
class AIManger:
    def __init__(self, model_setting):
        self.__feed_analyzer = FeedAnalyzer(
            model_setting=model_setting
        )
    
    # 새로운 게시물이 들어오면 처리하는 부분
    def treat_new_feed(self, feed:Feed):
        feed = self.__feed_analyzer.pipeline_when_feed_created(feed=feed)
        return feed
        
        
        
        
