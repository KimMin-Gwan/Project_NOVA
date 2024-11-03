import pandas as pd


class SearchEngine:
    def __init__(self):
        self.search_module = SearchModule()


    def try_search_feed(self, keyword):
        self.search_module.get_new_feed(keyword=keyword, type="all")



class SearchModule:
    def __init__(self):
        self.feed_data_frame = FeedDataframe()


    def get_new_feed(self, keyword, type):
        if keyword == "":
            return None
        else:
            self.feed_data_frame.search_feed(keyword=keyword, type=type)



class FeedDataframe:
    def __init__(self):
        self.df = pd.DataFrame()

    def search_feed(self, keyword, type):
        result = None
        try:
            result = df.get[keyword]
        finally:
            return result
