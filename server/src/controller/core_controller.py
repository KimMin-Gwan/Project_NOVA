from model import *
from others import UserNotExist, CustomError

class Core_Controller:
    def sample_func(self, database:Local_Database, request) -> BaseModel: 
        model = BaseModel(database=database)

        try:
            # 유저가 있는지 확인
            if not model.set_user_with_uid(request=request):
                raise UserNotExist("Can not find User with uid")
        except UserNotExist as e:
            print("Error Catched : ", e)
            model.set_state_code(e.error_code) # 종합 에러
            return model

        try:
            """
            if not model.set_biases_with_bids():
                model.set_state_code("210")
                return model
            """

        except CustomError as e:
            print("Error Catched : ", e.error_type)
            model.set_state_code(e.error_code) # 종합 에러

        except Exception as e:
            print("Error Catched : ", e.error_type)
            model.set_state_code(e.error_code) # 종합 에러

        finally:
            return model
    
    def request_login(self, database:Local_Database, request) -> BaseModel: 
        model = RequestLogin(database=database)

        try:
            # 유저가 있는지 확인
            if not model.set_user_with_email(request=request):
                raise UserNotExist("Can not find User with uid")
        except UserNotExist as e:
            print("Error Catched : ", e)
            model.set_state_code(e.error_code) # 종합 에러
            return model

        try:
            model.request_login(request=request,token=model._user.token)

        except CustomError as e:
            print("Error Catched : ", e.error_type)
            model.set_state_code(e.error_code) # 종합 에러

        finally:
            return model
        
    def requese_daily_check(self, database:Local_Database, request) -> BaseModel: 
        model = RequestDailyCheck(database=database)
        
        try:
            # 유저가 있는지 확인
            if not model.set_user_with_email(request=request):
                raise UserNotExist("Can not find User with email")
        except UserNotExist as e:
            print("Error Catched : ", e)
            model.set_state_code(e.error_code) # 종합 에러
            return model

        try:
            model.request_daily(model._user)
            model.add_solo_bias_point(model._user.solo_bid)
            model.add_group_bias_point(model._user.group_bid)

            

        except CustomError as e:
            print("Error Catched : ", e.error_type)
            model.set_state_code(e.error_code) # 종합 에러

        finally:
            return model
        
    def get_my_bias_league(self, database:Local_Database, request) -> BaseModel: 

        model = MyBiasLeagueModel(database=database)

        try:
            # 유저가 있는지 확인
            if not model.set_user_with_email(request=request):
                raise UserNotExist("Can not find User with email")
        except UserNotExist as e:
            print("Error Catched : ", e)
            model.set_state_code(e.error_code) # 종합 에러
            return model

        try:
            model.set_solo_bias(model._user.solo_bid)
            model.set_group_bias(model._user.group_bid)

        except CustomError as e:
            print("Error Catched : ", e.error_type)
            model.set_state_code(e.error_code) # 종합 에러

        finally:
            return model
        
    def get_all_leagues(self, database:Local_Database) -> BaseModel: 
        
        model = AllLeaguesModel(database=database)

        try:
            model.set_leagues()
            model.set_league_list()

        except CustomError as e:
            print("Error Catched : ", e.error_type)
            model.set_state_code(e.error_code) # 종합 에러

        finally:
            return model
        
    def get_solo_league(self, database:Local_Database, request) -> BaseModel: 
        
        model = SoloLeaguesModel(database=database)

        try:
            model.set_solo_leagues(request)
            model.set_solo_biases()
            model._set_list_alignment()

        except CustomError as e:
            print("Error Catched : ", e.error_type)
            model.set_state_code(e.error_code) # 종합 에러

        finally:
            return model
        
    def get_group_league(self, database:Local_Database, request) -> BaseModel: 
        
        model = GroupLeaguesModel(database=database)

        try:
            model.set_group_leagues(request)
            model.set_group_biases()
            model._set_list_alignment()

        except CustomError as e:
            print("Error Catched : ", e.error_type)
            model.set_state_code(e.error_code) # 종합 에러

        finally:
            return model