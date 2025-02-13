from model.local_database_model import Local_Database
from others.feed_manager import FeedManager


class AnalyzedBias():
    def __init__(self, bid="", tag=[]):
        self.bid = ""
        self.tag = tag


class AIRecommander:
    def __init__(self, database:Local_Database, feed_manager:FeedManager= None):
        self._database = database
        
    def __init_bias(self):
        pass
    

