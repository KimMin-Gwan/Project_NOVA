from model.base_model import BaseModel
from model import Local_Database
from others.data_domain import  Bias
from others import CoreControllerLogicError

class MyBiasLeagueModel(BaseModel):
    def __init__(self, database:Local_Database) -> None:
        super().__init__(database)
        self.__solo_bias = Bias()
        self.__group_bias = Bias()

    def set_solo_bias(self,request) -> bool: 
        try:
            
            bias_data = self._database.get_data_with_id(target="bid", id=request)

            if not bias_data:
                return False

            self.__solo_bias.make_with_dict(bias_data)
            
            return True
        
        except Exception as e:
            raise CoreControllerLogicError(error_type="set_group_leagues | " + str(e))
        
    def set_group_bias(self,request) -> bool: 
        try:
            
            bias_data = self._database.get_data_with_id(target="bid", id=request)

            if not bias_data:
                return False

            self.__group_bias.make_with_dict(bias_data)
            
            return True
        
        except Exception as e:
            raise CoreControllerLogicError(error_type="set_group_leagues | " + str(e))
    


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