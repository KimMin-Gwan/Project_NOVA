from model.base_model import BaseModel
from model import Local_Database
from others.data_domain import Bias, League
from others import CoreControllerLogicError, FeedSearchEngine
from random import sample

class TokenModel(BaseModel):
    def __init__(self, database:Local_Database) -> None:
        super().__init__(database)

    def get_response_form_data(self, head_parser):
        try:
            body = {
                'result' : True
            }

            response = self._get_response_data(head_parser=head_parser, body=body)
            return response

        except Exception as e:
            raise CoreControllerLogicError("response making error | " + e)



class BannerModel(BaseModel):
    def __init__(self, database:Local_Database) -> None:
        super().__init__(database)
        self.__banner = []

    def set_banner_data(self):
        try:
            self.__banner = self._database.get_all_data(target="banner")

        except Exception as e:
            raise CoreControllerLogicError(error_type="set_group_leagues | " + str(e))

    def get_response_form_data(self, head_parser):
        try:
            body = {
                'banner' : self.__banner
            }

            response = self._get_response_data(head_parser=head_parser, body=body)
            return response

        except Exception as e:
            raise CoreControllerLogicError("response making error | " + e)

class HomeBiasModel(BaseModel):
    def __init__(self, database:Local_Database) -> None:
        super().__init__(database)
        self.__bias_list = []
        
    def get_bid_list(self):
        bid_list = []
        for bias in self.__bias_list:
            bid_list.append(bias.bid)
        return bid_list
    
    def get_bias_list(self):
        return self.__bias_list
        
    def set_random_bias(self):
        bias_datas = self._database.get_all_data(target="bid")
        
        num_bias = len(bias_datas)
        
        if num_bias >= 1 or num_bias < 4:
            random_index = sample(range(num_bias), 1)
        elif num_bias >= 4 and num_bias < 10: 
            random_index = sample(range(num_bias), 2)
        elif num_bias >= 10 and num_bias < 20:
            random_index = sample(range(num_bias), 3)
        elif num_bias >= 20:
            random_index = sample(range(num_bias), 4)
        else:
            return
        
        for index in random_index:
            bias = Bias()
            bias.make_with_dict(bias_datas[index])
            self.__bias_list.append(bias)
            
        return

    # 바이어스 데이터를 모두 받아와서 만들기
    def set_bias_list(self):
        if self._user.bids:
            bias_datas = self._database.get_datas_with_ids(target_id="bid", ids=self._user.bids)

            for bias_data in bias_datas:
                bias = Bias()
                bias.make_with_dict(bias_data)
                self.__bias_list.append(bias)
        else:
            self.set_random_bias()
        return
        

    def get_response_form_data(self, head_parser):
        try:
            body = {
                "bias_list" : self._make_dict_list_data(list_data=self.__bias_list)
            }

            response = self._get_response_data(head_parser=head_parser, body=body)
            return response

        except Exception as e:
            raise CoreControllerLogicError("response making error | " + e)

class BiasSearchModel(BaseModel):
    def __init__(self, database:Local_Database) -> None:
        super().__init__(database)
        self._biases = []
        
    # 바이어스 전체 데이터 세팅
    def set_biases(self):
        bias_datas = self._database.get_all_data(target="bias")
        
        for bias_data in bias_datas:
            bias = Bias()
            bias.make_with_dict(dict_data=bias_data)
            self._biases.append(bias)
            
        if len(self._biases):
            return True
        else:
            return False
            
    
    def try_search_bias_with_category(self, category:str, biases=[]):
        self._biases=self._try_search_bias_with_category(category=category, biases=biases)
        return
        
    # 카테고리를 바탕으로 검색 -> 반드시 set_biases가 선행해도됨
    def _try_search_bias_with_category(self, category:str, biases=[]):
        result = []
        
        if len(biases):
            for bias in biases:
                if category in bias.category:
                    result.append(bias)
        else:
            for bias in self._biases:
                if category in bias.category:
                    result.append(bias)
                    
        return result

    def try_search_bias(self, bname, feed_search_engine):
        # ManagedBias 전체 호출
        managed_bias_list = feed_search_engine.get_all_managed_bias()

        # 코사인 유사도 평가를 통한 가장 비슷한 이름 검색
        result:list = self._search_similar_data(data_list=managed_bias_list,
                                    key_word=bname, key_attr="bname")
            
        # 검색 결과가 있으면 데이터 베이스에서 찾아서 보내줌
        if result:
            bids = []
                
            # ManagedBias에서 bid 추출
            for managed_bias in result:
                bids.append(managed_bias.bid)
                    
            # 검색 후 만들기
            bias_datas = self._database.get_datas_with_ids(target_id="bid", ids=bids)
            for bias_data in bias_datas:
                bias = Bias()
                bias.make_with_dict(bias_data)
                self._biases.append(bias)
        return

    def get_response_form_data(self, head_parser):
        try:
            body = {
                'biases' : self._make_dict_list_data(list_data=self._biases)
            }

            response = self._get_response_data(head_parser=head_parser, body=body)
            return response

        except Exception as e:
            raise CoreControllerLogicError("response making error | " + e)

class SelectBiasModel(BaseModel):
    def __init__(self, database:Local_Database) -> None:
        super().__init__(database)
        self.__bias= Bias()
        self.__result = False

    def find_bias(self, bid):
        try:
            raw_bias_data = self._database.get_data_with_id(target="bid", id=bid)
            if not raw_bias_data:
                return False
            self.__bias.make_with_dict(raw_bias_data)

        except Exception as e:
            raise CoreControllerLogicError(error_type="find_bias | " + str(e))
        return True
    
    # 내 최애를 누구로 할지 최종 결정하는 부분
    def set_my_bias(self, feed_search_engine:FeedSearchEngine):
        if self.__bias.bid in self._user.bids:
            self._user.bids.remove(self.__bias.bid)
            feed_search_engine.add_new_user_to_bias(bid=self.__bias.bid, uid=self._user.uid)
        else:
            self._user.bids.append(self.__bias.bid)
            feed_search_engine.remove_user_to_bias(bid=self.__bias.bid, uid=self._user.uid)

        self._database.modify_data_with_id(target_id="uid", target_data=self._user.get_dict_form_data())
        self.__result = True

        return True


    def get_response_form_data(self, head_parser):
        try:
            body = {
                'result' : self.__result
            }

            response = self._get_response_data(head_parser=head_parser, body=body)
            return response

        except Exception as e:
            raise CoreControllerLogicError("response making error | " + e)

class LeagueMetaModel(BaseModel):
    def __init__(self, database:Local_Database) -> None:
        super().__init__(database)
        self.__leagues = []

    # 타입에 맞는 리그 다 찾아야됨
    def set_league(self, league_manager):
        try:
            self.__leagues = league_manager.get_league_meta_data()

        except Exception as e:
            raise CoreControllerLogicError(error_type="set_group_leagues | " + str(e))
        return

    def get_response_form_data(self, head_parser):
        try:
            body = {
                'leagues' : self._make_dict_list_data(list_data=self.__leagues)
            }

            response = self._get_response_data(head_parser=head_parser, body=body)
            return response

        except Exception as e:
            raise CoreControllerLogicError("response making error | " + e)
        
class BiasFollowPageModel(BiasSearchModel):
    def __init__(self, database:Local_Database) -> None:
        super().__init__(database)
        self.__chzzk= []
        self.__soop= []
        self.__artist= []
        self.__youtube= []
        
    def try_get_bias_follow_page_data(self):
        self.__chzzk = self._try_search_bias_with_category(category="치지직")
        self.__soop = self._try_search_bias_with_category(category="SOOP")
        self.__artist= self._try_search_bias_with_category(category="아티스트")
        self.__youtube= self._try_search_bias_with_category(category="크리에이터")
        return


    def get_response_form_data(self, head_parser):
        try:
            body = {
                'chzzk' : self._make_dict_list_data(list_data=self.__chzzk),
                'soop' : self._make_dict_list_data(list_data=self.__soop),
                'artist' : self._make_dict_list_data(list_data=self.__artist),
                'youtube' : self._make_dict_list_data(list_data=self.__youtube)
            }

            response = self._get_response_data(head_parser=head_parser, body=body)
            return response

        except Exception as e:
            raise CoreControllerLogicError("response making error | " + e)

class RecommendKeywordModel(BaseModel):
    def __init__(self, database:Local_Database) -> None:
        super().__init__(database)
        self.__keywords = []

    def get_response_form_data(self, head_parser):
        try:
            body = {
                'keywords' : self._make_dict_list_data(list_data=self.__keywords),
            }

            response = self._get_response_data(head_parser=head_parser, body=body)
            return response

        except Exception as e:
            raise CoreControllerLogicError("response making error | " + e)

    # 추천 키워드를 가져옴.
    # 지금은 주간 추천 해시태그를 반환받음
    def get_recommend_keywords(self, feed_search_engine:FeedSearchEngine):
        self.__keywords = feed_search_engine.try_get_recommend_keyword()

        return


