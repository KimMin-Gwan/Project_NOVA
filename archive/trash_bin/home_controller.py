from model import BannerModel, HomeBiasModel, BiasSearchModel, Mongo_Database, SelectBiasModel, LeagueMetaModel, TokenModel, HashTagModel, RecommendKeywordModel
from others import UserNotExist, CustomError, FeedManager


#from server.src.view.jwt_decoder import JWTManager, JWTPayload
#from view import RequestManager

class Home_Controller:
    def __init__(self, feed_manager = None):
        self.__feed_manager:FeedManager = feed_manager









