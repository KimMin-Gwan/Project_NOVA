from others.data_domain import Feed, Comment
from others.ai_service.feed_analyzer import FeedAnalyzer
from others.ai_service.ai_recommand import AIRecommander
from model.local_database_model import Local_Database

import time
import asyncio


# 외부 인터페이스
class AIManger:
    def __init__(self, database, model_setting):
        self._database:Local_Database= database
        self.__feed_analyzer = FeedAnalyzer(
            model_setting=model_setting
        )
        #self.__treated_fid = []
        #self.__recommander = AIRecommander(database=database)
    
    # 새로운 게시물이 들어오면 처리하는 부분
    def treat_new_feed(self, feed:Feed, data_payload_body=None):
        feed = self.__feed_analyzer.pipeline_when_feed_created(feed=feed, data_payload_body=data_payload_body)
        return feed
        
    # 새로운 comment가 들어오면 처리하는 부분
    def treat_new_comment(self, comment:Comment):
        comment = self.__feed_analyzer.pipeline_when_comment_created(comment=comment)
        return comment
        
        
    async def apprehend_mood_n_trend(self):
        try:
            last_computed_time = time.time()  # 초기값 설정
            
            while True:
                # 현재 시간 계산
                current_time = time.time()
                time_diff = (current_time - last_computed_time) / 3600  # 시간 단위로 계산

                # 마지막 계산 시간이 1시간 이상일 경우 갱신
                # 나중에는 bias 단위로 잘라서 필요할 때마다 실행 시켜야됨
                if time_diff >= 12:
                    #feeds = []
                    #feed_datas = self._database.get_datas_with_ids(target_id=self.__treated_fid)
                    
                    #for feed_data in feed_datas:
                        #feed = Feed()
                        #feed.make_with_dict(feed_data)
                        #feeds.append(feed)
                    
                    ## 무드 찾기 파이프라인 동작
                    ##self.__feed_analyzer.pipeline_when_apprehend_mood_n_trend(feeds)
                    
                    ## 비우기
                    #self.__treated_fid.clear()
                    self.last_computed_time = current_time  # 갱신 완료 시점 기록

                # 60초 대기
                await asyncio.sleep(120)
                
        except KeyboardInterrupt:
            print("Shutting down due to KeyboardInterrupt.")
