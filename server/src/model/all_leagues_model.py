from model.base_model import BaseModel
from model import Local_Database
from others.data_domain import League
from others import CoreControllerLogicError

class AllLeaguesModel(BaseModel):
    def __init__(self, database:Local_Database) -> None:
        super().__init__(database)
        self.__leagues = []
        self.__solo_league_list = []
        self.__group_league_list = []

    def set_leagues(self) -> bool: 
        try:
            league_data = self._database.get_all_data(target="league")

            if not league_data:
                return False

            for data in league_data:
                self.__leagues.append(data)
            
            return True
        except Exception as e:
            raise CoreControllerLogicError(error_type="set_leagues | " + str(e))
    
    
    def set_league_list(self) -> bool:
        try:

            if not self.__leagues:
                return False
            
            for i in self.__leagues:
                if i['type']=='solo':
                    self.__solo_league_list.append(i['lid'])
                else:
                    self.__group_league_list.append(i['lid'])
            
            return True
        except Exception as e:
            raise CoreControllerLogicError(error_type="set_leagues | " + str(e))


    def get_response_form_data(self, head_parser):
        try:
            body = {
                'solo_leagues' : self.__solo_league_list,
                'group_leagues' : self.__group_league_list
            }

            response = self._get_response_data(head_parser=head_parser, body=body)
            return response

        except Exception as e:
            raise CoreControllerLogicError("response making error | " + e)