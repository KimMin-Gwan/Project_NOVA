from model.base_model import BaseModel
from model import Local_Database
from others.data_domain import League, Bias
from others import CoreControllerLogicError

class LeagueModel(BaseModel):
    def __init__(self, database:Local_Database) -> None:
        super().__init__(database)
        self.__bias = Bias()  # 목표 선택용 bias
        self.__league = League()
        self.__biases = []   # 랭크 집계를 위한 bias 리스트

    def get_user(self):
        return self._user
    
    def get_bias(self):
        return self.__bias

    # 리그를 찾기 위해 bias 정보를 검색하기 위한 세팅
    def set_bias_data(self, bid):
        bias_data = self._database.get_data_with_id(target="bid", id=bid)
        self.__bias.make_with_dict(bias_data)
        return
    
    # 리그 정보 세팅
    def set_leagues(self,request) -> bool: 
        try:

            if request.league_id:
                league_data = self._database.get_data_with_id(target="lid", id=request.league_id)#type = solo
            elif request.league_name:
                league_data = self._database.get_data_with_key(target="lid", key="lname", key_data=request.league_name)

            if not league_data:
                return False

            self.__league.make_with_dict(league_data)
            
            return True
        
        except Exception as e:
            raise CoreControllerLogicError(error_type="set_solo_leagues | " + str(e))
    
    # 바이어스 데이터 전부다 가지고오기
    def set_biases(self) -> bool:
        try:
            if not self.__league:
                return False
            
            dict_bias_list= self._database.get_datas_with_ids(target_id="bid", ids=self.__league.bid_list)

            for dict_bias in dict_bias_list:
                bias = Bias()
                bias.make_with_dict(dict_data=dict_bias)
                self.__biases.append(bias)


            return True
        except Exception as e:
            raise CoreControllerLogicError(error_type="set_solo_biases | " + str(e))
    
    # 정렬함수(이게 랭크임)
    def set_list_alignment(self):
        try:
            # bias 리스트를 정렬 (point 기준으로)
            self.__biases = self._set_list_alignment(bias_list=self.__biases, align='point')

        except Exception as e:
            raise CoreControllerLogicError(error_type="_set_list_alignment error | " + str(e))


    def get_response_form_data(self, head_parser):
        try:
            body = {
                'league_data' : self.__league.get_dict_form_data(),
                'rank' : self._make_dict_list_data(self.__biases)  # 순서대로 1등부터 꼴등임
            }

            response = self._get_response_data(head_parser=head_parser, body=body)
            return response

        except Exception as e:
            raise CoreControllerLogicError("response making error | " + e)