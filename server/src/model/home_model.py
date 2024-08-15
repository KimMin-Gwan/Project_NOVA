from model.base_model import BaseModel
from model import Local_Database
from others.data_domain import Bias, League
from others import CoreControllerLogicError

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
        self.__solo_bias= Bias()
        self.__group_bias = Bias()

    # 솔로 바이어스 세팅
    def set_solo_bias_with_bid(self):
        if self._user.solo_bid == "":  # 팔로우한 바이어스 없으면 false 반환
            return False
        
        raw_solo_bias = self._database.get_data_with_id(target="bid", id=self._user.solo_bid)

        if not raw_solo_bias:  # 바이어스 정보가 유실되어있으면 false 반환
            return False

        self.__solo_bias.make_with_dict(raw_solo_bias)
        return

    # 그룹 바이어스 세팅
    def set_group_bias_with_bid(self):
        if self._user.group_bid == "":# 팔로우한 바이어스 없으면 false 반환
            return False
        
        raw_group_bias = self._database.get_data_with_id(target="bid", id=self._user.group_bid)

        if not raw_group_bias: # 바이어스 정보가 유실되어있으면 false 반환
            return False

        self.__group_bias.make_with_dict(raw_group_bias)


    def get_response_form_data(self, head_parser):
        try:
            body = {
                'solo_bias' : self.__solo_bias.get_dict_form_data(),
                'group_bias' : self.__group_bias.get_dict_form_data()
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
    def set_my_bias(self):
        try:
            flag = False
            # 솔로인지 그룹인지 확인해야됨
            if self.__bias.type == "solo":
                if self._user.solo_bid == "":
                    self._user.solo_bid = self.__bias.bid
                    flag = True
                else:  # 이미 있는데 선택해? 죽임
                    return flag
            else:
                if self._user.group_bid== "":  # 정상 성택
                    self._user.group_bid= self.__bias.bid
                    flag = True
                else:  # 이미 있는데 선택을 왜하냐고
                    return flag 
            
            if flag:
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
    def set_league(self, request):
        try:
            raw_league_datas = self._database.get_all_data(target="lid")
            for league_data in raw_league_datas:
                league = League()
                league.make_with_dict(league_data)
                print(league_data)
                if league.type == request.league_type:
                    self.__leagues.append(league)

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
