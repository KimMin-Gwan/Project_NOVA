from model import *

class Core_Controller:
    def get_banner_data(self, database:Mongo_Database) -> BannerModel: 
        model = BannerModel(database=database)
        model.set_banner_data()
        return model
        
    # 홈 화면에서 토큰 발급  시도하는동작
    def get_token(self, database:Mongo_Database) -> TokenModel: 
        model = TokenModel(database=database)
        return model
    
    # 홈 화면에서 토큰 발급  시도하는동작
    def get_token_need_user(self, request, database:Mongo_Database) -> TokenModel: 
        model = TokenModel(database=database)
        model.set_user_with_email(request=request.jwt_payload)
        return model
    
    # 홈 화면의 bias 정보 
    def get_my_bias_data(self, database:Mongo_Database, request) -> MyBiasModel: 
        model = MyBiasModel(database=database)

        # 유저가 있으면 그 유저의 bias_list로 세팅
        if request.jwt_payload != "":
            model.set_user_with_email(request=request.jwt_payload)
            model.set_bias_list()
        # 유저가 아니면 랜덤하게
        else:
            model.set_random_bias()
        
        return model

    def search_bias(self, database:Mongo_Database, request):
        model = BiasSearchModel(database=database)

        if not model.try_search_bias(request=request):
            model.set_state_code("210")

        return model
