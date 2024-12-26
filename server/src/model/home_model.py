from model.base_model import BaseModel
from model import Local_Database
from others.data_domain import Bias, League
from others import CoreControllerLogicError, FeedSearchEngine

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

    # 바이어스 데이터를 모두 받아와서 만들기
    def set_bias_list(self):
        bias_datas = self._database.get_datas_with_ids(target_id="bid", ids=self._user.bids)

        for bias_data in bias_datas:
            bias = Bias()
            bias.make_with_dict(bias_data)
            self.__bias_list.append(bias)

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
        self.__biases = []

    def try_search_bias(self, request):
        try:
            bias_list = []

            dict_bias_list = self._database.get_all_data(target="bias")
            
            for bias_data in dict_bias_list:
                bias = Bias()
                bias.make_with_dict(bias_data)
                bias_list.append(bias)

            result:list = self._search_similar_data(data_list=bias_list,
                                       key_word=request.bias_name, key_attr="bname")
            
            self.__biases = result
            #self.__set_biases(bias_data_list=result)

        except Exception as e:
            raise CoreControllerLogicError(error_type="set_search_bias| " + str(e))
        
        return

    def __set_biases(self, bias_data_list):
        for bias_data in bias_data_list:
            bias = Bias()
            bias.make_with_dict(bias_data)
            self.__biases.append(bias)
        return

    def get_response_form_data(self, head_parser):
        try:
            body = {
                'biases' : self._make_dict_list_data(list_data=self.__biases)
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

    def find_bias(self, request):
        try:
            raw_bias_data = self._database.get_data_with_id(target="bid", id=request.bid)
            if not raw_bias_data:
                return False
            self.__bias.make_with_dict(raw_bias_data)

        except Exception as e:
            raise CoreControllerLogicError(error_type="find_bias | " + str(e))
        return True
    
    # 내 최애를 누구로 할지 최종 결정하는 부분
    def set_my_bias(self, feed_search_engine:FeedSearchEngine):
        try:
            if self.__bias.bid in self._user.bids:
                self._user.bids.remove(self.__bias.bid)
                feed_search_engine.add_new_user_to_bias(bid=self.__bias.bid, uid=self._user.uid)
            else:
                self._user.bids.append(self.__bias.bid)
                feed_search_engine.remove_user_to_bias(bid=self.__bias.bid, uid=self._user.uid)

            self._database.modify_data_with_id(target_id="uid", target_data=self._user.get_dict_form_data())
            self.__result = True

        except Exception as e:
            raise CoreControllerLogicError(error_type="set_my_bias| " + str(e))
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
