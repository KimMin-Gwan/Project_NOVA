from model.base_model import BaseModel
from model import Local_Database
from others.data_domain import Bias
from others import CoreControllerLogicError

class RequestDailyCheck(BaseModel):
    def __init__(self, database:Local_Database) -> None:
        super().__init__(database)
        self.__point = 0

    def request_daily(self,request) -> bool: 
        try:
            self._database.modify_data_with_id(target_id=request.uid,target_data={'daily':True})
            self.__point = 1 + request.combo
            self._database.modify_data_with_id(target_id=request.uid,target_data={'point':request.point + self.__point})
            if request.combo < 4:
                self._database.modify_data_with_id(target_id=request.uid,target_data={'combo':request.combo + 1}) 

            return True
        
        except Exception as e:
            raise CoreControllerLogicError(error_type="request_daily | " + str(e))

    def add_solo_bias_point(self,request):
        try:
            bias_data = self._database.get_data_with_id(target='bid',id=request)
            bias = Bias()
            bias.make_with_dict(bias_data)
            self._database.modify_data_with_id(target_id=request,target_data={'point':bias.point+self.__point})

            return True
        
        except Exception as e:
            raise CoreControllerLogicError(error_type="set_group_leagues | " + str(e))
        
    def add_group_bias_point(self,request):
        try:
            bias_data = self._database.get_data_with_id(target='bid',id=request)
            bias = Bias()
            bias.make_with_dict(bias_data)
            self._database.modify_data_with_id(target_id=request,target_data={'point':bias.point+self.__point})

            return True
        
        except Exception as e:
            raise CoreControllerLogicError(error_type="set_group_leagues | " + str(e))


    def get_response_form_data(self, head_parser):
        try:
            body = {
                'res':'ok'
            }

            response = self._get_response_data(head_parser=head_parser, body=body)
            return response

        except Exception as e:
            raise CoreControllerLogicError("response making error | " + e)