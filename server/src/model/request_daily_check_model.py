from model.base_model import BaseModel
from model import Local_Database
from others.data_domain import Bias
from others import CoreControllerLogicError

class RequestDailyCheck(BaseModel):
    def __init__(self, database:Local_Database) -> None:
        super().__init__(database)
        self.__point = 0
        self.__combo = 0

    def request_daily(self,request) -> bool: 
        try:

            self.__point = 1 + request.combo

            
            self.__combo = request.combo + 1
            if self.__combo > 4:
                self.__combo = 4
            self._database.modify_data_with_id(target_id='uid',target_data={
                'uid': request.uid,
                "uname": request.uname,
                "age": request.age,
                "email": request.email,
                "gender" : request.gender,
                'point':request.point + self.__point,
                'combo':self.__combo,
                "credit" : request.credit,
                "solo_bid" : request.solo_bid,
                "group_bid" : request.group_bid,
                "items" : request.items,
                'daily':True,
                "special" : request.special
            }) 

            return True
        
        except Exception as e:
            raise CoreControllerLogicError(error_type="request_daily | " + str(e))

    def add_solo_bias_point(self,request):
        try:
            # bias_data = self._database.get_data_with_id(target='bid',id=request)
            bias = self._database.get_data_with_id(target='bid',id=request)
            # if not bias_data:
            #     return False
            if not bias:
                 return False
            # bias = Bias()
            # bias.make_with_dict(bias_data)
            self._database.modify_data_with_id(target_id='bid',target_data={
            #     "bid" : request,
            #     "type" : bias.type,
            #     "bname" : bias.bname,
            #     "category" : bias.category,
            #     "birthday" : bias.birthday,
            #     "debut" :  bias.debut,
            #     "agency" : bias.agency,
            #     "group" : bias.group,
            #     "lid" : bias.lid,
            #     'point':bias.point+self.__point,
            #     "num_user" : bias.num_user,
            #     "x_account" : bias.x_account,
            #     "insta_acoount" : bias.insta_account,
            #     "tiktok_account" : bias.tiktok_account,
            #     "youtube_account" : bias.youtube_account,
            #     "homepage" : bias.homepage,
            #     "fan_cafe" : bias.fan_cafe,
            #     "country" : bias.country,
            #     "nickname" : bias.nickname,
            #     "fanname" : bias.fanname,
            #     "group_memeber_bids" : bias.group_memeber_bids

                "bid" : request,
                "type" : bias['type'],
                "bname" : bias['bname'],
                "category" : bias['category'],
                "birthday" : bias['birthday'],
                "debut" :  bias['debut'],
                "agency" : bias['agency'],
                "group" : bias['group'],
                "lid" : bias['lid'],
                'point':bias['point']+self.__point,
                "num_user" : bias['num_user'],
                "x_account" : bias['x_account'],
                "insta_acoount" : bias['insta_acoount'],
                "tiktok_account" : bias['tiktok_account'],
                "youtube_account" : bias['youtube_account'],
                "homepage" : bias['homepage'],
                "fan_cafe" : bias['fan_cafe'],
                "country" : bias['country'],
                "nickname" : bias['nickname'],
                "fanname" : bias['fanname'],
                "group_memeber_bids" : bias['group_memeber_bids']
                })

            return True
        
        except Exception as e:
            raise CoreControllerLogicError(error_type="add_solo_bias_point | " + str(e))
        
    def add_group_bias_point(self,request):
        try:
            bias_data = self._database.get_data_with_id(target='bid',id=request)
            if not bias_data:
                return False
            bias = Bias()
            bias.make_with_dict(bias_data)
            self._database.modify_data_with_id(target_id='bid',target_data={
                "bid" : request,
                "type" : bias.type,
                "bname" : bias.bname,
                "category" : bias.category,
                "birthday" : bias.birthday,
                "debut" :  bias.debut,
                "agency" : bias.agency,
                "group" : bias.group,
                "lid" : bias.lid,
                'point':bias.point+self.__point,
                "num_user" : bias.num_user,
                "x_account" : bias.x_account,
                "insta_acoount" : bias.insta_account,
                "tiktok_account" : bias.tiktok_account,
                "youtube_account" : bias.youtube_account,
                "homepage" : bias.homepage,
                "fan_cafe" : bias.fan_cafe,
                "country" : bias.country,
                "nickname" : bias.nickname,
                "fanname" : bias.fanname,
                "group_memeber_bids" : bias.group_memeber_bids
                })

            return True
        
        except Exception as e:
            raise CoreControllerLogicError(error_type="add_group_bias_point | " + str(e))


    def get_response_form_data(self, head_parser):
        try:
            body = {
                'res':'ok'
            }

            response = self._get_response_data(head_parser=head_parser, body=body)
            return response

        except Exception as e:
            raise CoreControllerLogicError("response making error | " + e)