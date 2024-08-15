from model.base_model import BaseModel
from model import Local_Database
from others.data_domain import League, Bias
from others import CoreControllerLogicError

class GroupLeaguesModel(BaseModel):
    def __init__(self, database:Local_Database) -> None:
        super().__init__(database)
        self.__group_league = League()
        self.__biases = []

    def set_group_leagues(self,request) -> bool: 
        try:
            
            league_data = self._database.get_data_with_id(target="lid", id=request) #type = group

            if not league_data:
                return False

            self.__group_league.make_with_dict(league_data)
            
            return True
        
        except Exception as e:
            raise CoreControllerLogicError(error_type="set_group_leagues | " + str(e))
    
    def set_group_biases(self) -> bool:
        try:

            if not self.__group_league:
                return False
            
            self.__biases = self._database.get_datas_with_ids(target_id="bid", ids=self.__group_league.bid_list)


            return True
        except Exception as e:
            raise CoreControllerLogicError(error_type="set_group_biases | " + str(e))
    
    def set_list_alignment(self):
        try:
            self.__biases = super()._set_list_alignment(self.__biases,'point')

        except Exception as e:
            raise CoreControllerLogicError(error_type="_set_list_alignment error | " + str(e))


    def get_response_form_data(self, head_parser):
        try:
            body = {
                'group_biases' : self.__biases
            }

            response = self._get_response_data(head_parser=head_parser, body=body)
            return response

        except Exception as e:
            raise CoreControllerLogicError("response making error | " + e)