import pandas as pd

# 검색엔진이 해야하는일

# 1. 키워드를 통한 피드 검색
# 2. 특정 피드 다음으로 제시할 피드 검색
# 3. 피드 분석 및 최신화
# 4. 추천 피드 제공

# 아래는 검색 엔진
class MagicBoxSearchEngine:
    def __init__(self):
        self.__feed_data_frame = pd.DataFrame()
        self.__algorithm_manager = FeedFindAlgorithmManager(self.__feed_data_frame)

    # 1. 키워드를 통한 피드 검색
    # option은 본문 내용, 해쉬태그, 댓글, 작성자 등
    def search_feed_with_keyword(self, keyword, option="all"):
        pass

    # 2. 다음으로 올 피드 검색 -> short_feed에서 사용될 예정
    def search_next_feed(self, fid, managed_user):
        pass

    # 3. 피드 분석 및 최신화
    def set_new_feed(self, fid, managed_user):
        pass

    # 4. 추천 피드 제공
    # 홈화면에서 제공하는 추천 피드 항목
    def recommend_now_trend_feed(self, fid, managed_user):
        pass

    # 5. 피드에 해쉬태그 달아주기
    # 피드에 자동으로 해쉬태그 달아주기
    def __make_hashtag_itself(self, feed):
        pass

    # 6. 해쉬태그 분석
    # 해쉬태그간의 유사성 파악을 위함
    def __analize_hashtag(self, hashtag):
        pass


# 추천피드 알고리즘
class KNNAlgorithmManger:
    def __init__(self):
        pass

# 여러가지 알고리즘을 적당히 섞어서 만들어야됨
# 기준은 피드 기준이되, 사용자의 성향을 함께 고려할것
class FeedFindAlgorithmManager:
    def __init__(self, dataframe):
        self._dataframe = dataframe
        pass



# hash
