from model.local_database_model import Local_Database
from others.feed_manager import FeedManager


class AnalyzedBias():
    def __init__(self, bid="", tag=[], target_fid=[]):
        self.bid = bid
        self.tag = tag
        self.target_fid = target_fid

class AIRecommander:
    def __init__(self, database:Local_Database, feed_manager:FeedManager= None):
        self._database = database
        
    def __init_bias(self):

        analyzed_bias = AnalyzedBias()

    def pipeline_feed_recommend(self):
        #
    

