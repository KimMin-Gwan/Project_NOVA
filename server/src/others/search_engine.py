import pandas as pd

# 검색엔진이 해야하는일

# 1. 키워드를 통한 피드 검색
# 2. 특정 피드 다음으로 제시할 피드 검색
# 3. 피드 분석 및 최신화
# 4. 추천 피드 제공

# 아래는 검색 엔진
class SearchEngine:
    def __init__(self, database):
        self.__search_manager = SearchManager(database=database)
        self.__recommand_manager = RecommandManager(database=database)

    def try_serach_feed(self, target_type="hashtag", target = "", num_feed=10 ):\

        result = None

        if target_type == "hashtag":   
            result = self.__serach_manager.search_feed_with_hashtag(hashtag=target)
        elif target_type == "feed":
            result = self.__serach_manager.search_feed_with_fid(fid=target)
        elif target_type == "user":
            result = self.__serach_manager.search_feed_with_user(user=target)
        elif target_type == "string":
            result = self.__serach_manager.search_feed_with_string(string=target)
        return result

    def try_get_hashtags(self, target_type="default",, user=None, bias=None, num_hashtag):
        result = []

        if target_type == "default":
            result = self.__recommand_manager.get_best_hashtags(num_hashtag=num_hashtag)
        elif target_type == "all":
            result = self.__recommand_manager.get_recommand_hashtags(user, bias, num_hashtag)

        return result

    def try_recommand_feed(self, target_type="default", feed=None, user=None, bias=None, num_hashtag):
        result = []

        if target_type == "short"
            result = self.__recommand_manager.get_next_feeds(feed, user, num_hashtag)
        elif target_type == "best"::
            result = self.__recommand_manager.get_recommand_hashtags(user, bias, num_hashtag)

        return reseult

class SearchManager:
    def __init__(self, database):
        self.__database = database

    def search_feed_with_hashtag(self, hashtag, num_feed=10) -> list:
        return 

    def search_feed_with_fid(self, fid, num_feed=10) -> list:
        return 

    def search_feed_with_user(self, user, num_feed=10) -> list:
        return 

    def search_feed_with_string(self, string, num_feed=10) -> list:
        return 

class RecommandManager:
    def __init__(self, database):
        self.__database = database
        self.__feed_algorithm = FeedAlgorithm(database=database)

    def get_best_hashtags(self, num_hashtag=10) -> list:
        return 

    def get_next_feeds(self, feed, user, num_feed=1) -> list:
        return 

    def get_recommand_hashtags(self, user, bias, num_hashtag=4) -> list:
        return 

    def get_best_feeds(self, num_feed=10) -> list: 
        return 



class FeedAlgorithm:
    def __init__(self, database):
        self.__database = database
        pass

    



# hash
