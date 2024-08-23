from model.base_model import BaseModel
from model import Local_Database
from others.data_domain import League, Bias, User
from others import CoreControllerLogicError

class BaisBannerModel(BaseModel):
    def __init__(self, database:Local_Database) -> None:
        super().__init__(database)
        self.__bias = Bias()  # 목표 선택용 bias
        self.__league = League()
        self.__biases = []   # 랭크 집계를 위한 bias 리스트

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

class UserContributionModel(BaseModel):
    def __init__(self, database:Local_Database) -> None:
        super().__init__(database)
        self.__bias = Bias()  # 목표 선택용 bias
        self.__users = []   # 랭크 집계를 위한 bias 리스트

    def set_bias_data(self, request):
        bias_data = self._database.get_data_with_id(target="bid", id=request.bid)

        if not bias_data:
            return False

        self.__bias.make_with_dict(dict_data=bias_data)
        return True
    
    # 유저 정보 받아오기
    def set_user_datas(self):

        if self.__bias.type == "solo":
            user_datas = self._database.get_datas_with_key(target="uid", key="solo_bid", key_datas=[self.__bias.bid])
        elif self.__bias.type == "group":
            user_datas = self._database.get_datas_with_key(target="uid", key="group_bid", key_datas=[self.__bias.bid])
        else:
            return False
        
        for user_data in user_datas:
            user = User()
            user.make_with_dict(dict_data=user_data)
            self.__users.append(user)

        return True

    def set_user_alignment(self):
        if self.__bias.type == "solo":
            self.__users = sorted(self.__users, key=lambda x: x.solo_point, reverse=True)
        elif self.__bias.type == "group":
            self.__users = sorted(self.__users, key=lambda x: x.group_point, reverse=True)
        else:
            return False
        
        return True
    
    def __get_dict_user_data_with_rank(self):
        dict_user_form_list = []
        priv_point = 10000
        now_rank = 0
        set_rank = 0 

        if self.__bias.type == "solo":
            for user in self.__users:
                now_point = user.solo_point
                if now_point < priv_point:
                    now_rank = now_rank + set_rank + 1
                    set_rank = 0
                    priv_point = now_point
                elif now_point == priv_point:
                    set_rank += 1
                else:
                    print("data align set badly")
                user_data = user.get_dict_form_data()
                user_data['rank'] = now_rank
                dict_user_form_list.append(user_data)
        elif self.__bias.type == "group":
            for user in self.__users:
                now_point = user.group_point
                if now_point < priv_point:
                    now_rank = now_rank + set_rank + 1
                    set_rank = 0
                    priv_point = now_point
                elif now_point == priv_point:
                    set_rank += 1
                else:
                    print("data align set badly")
                user_data = user.get_dict_form_data()
                user_data['rank'] = now_rank
                dict_user_form_list.append(user_data)
        else:
            print("bias_type error")

        return dict_user_form_list

    def get_response_form_data(self, head_parser):
        try:
            body = {
                'user_contribution' : self.__get_dict_user_data_with_rank(),
            }

            response = self._get_response_data(head_parser=head_parser, body=body)
            return response

        except Exception as e:
            raise CoreControllerLogicError("response making error | " + e)
        
