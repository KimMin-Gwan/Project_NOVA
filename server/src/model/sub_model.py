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
        self._bias = Bias()  # 목표 선택용 bias
        self._users = []   # 랭크 집계를 위한 bias 리스트

    def set_bias_data(self, request):
        bias_data = self._database.get_data_with_id(target="bid", id=request.bid)

        if not bias_data:
            return False

        self._bias.make_with_dict(dict_data=bias_data)
        return True
    
    # 유저 정보 받아오기
    def set_user_datas(self):

        if self._bias.type == "solo":
            user_datas = self._database.get_datas_with_key(target="uid", key="solo_bid", key_datas=[self._bias.bid])
        elif self._bias.type == "group":
            user_datas = self._database.get_datas_with_key(target="uid", key="group_bid", key_datas=[self._bias.bid])
        else:
            return False
        
        for user_data in user_datas:
            user = User()
            user.make_with_dict(dict_data=user_data)
            self._users.append(user)

        return True

    def set_user_alignment(self):
        if self._bias.type == "solo":
            self._users = sorted(self._users, key=lambda x: x.solo_point, reverse=True)
        elif self._bias.type == "group":
            self._users = sorted(self._users, key=lambda x: x.group_point, reverse=True)
        else:
            return False
        
        return True
    
    def _get_dict_user_data_with_rank(self):
        dict_user_form_list = []
        priv_point = 10000
        now_rank = 0
        set_rank = 0 

        if self._bias.type == "solo":
            for user in self._users:
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
                user_data['point'] = user.solo_point
                user_data['rank'] = now_rank
                dict_user_form_list.append(user_data)
        elif self._bias.type == "group":
            for user in self._users:
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
                user_data['point'] = user.group_point
                user_data['rank'] = now_rank
                dict_user_form_list.append(user_data)
        else:
            print("bias_type error")

        return dict_user_form_list
    
    def get_response_form_data(self, head_parser):
        try:
            body = {
                'user_contribution' : self._get_dict_user_data_with_rank(),
            }

            response = self._get_response_data(head_parser=head_parser, body=body)
            return response

        except Exception as e:
            raise CoreControllerLogicError("response making error | " + e)
        

        
class MyContributionModel(UserContributionModel):
    def __init__(self, database:Local_Database) -> None:
        super().__init__(database)
        self.__result = False  # 내가 팔로우 중이면 True

    # 내 최애가 맞는지 확인
    def is_my_bias(self) -> bool:
        if self._user.solo_bid == self._bias.bid or self._user.group_bid == self._bias.bid:
            self.__result = True
            return True
        else:
            return False

    # rank와 point를 포함한 데이터
    def _get_my_data(self) -> dict:
        user_data = self._get_dict_user_data_with_rank()
        point = 0
        rank = 0

        for user in user_data:
            if user['uid'] == self._user.uid:
                point = user['point']
                rank = user['rank']

        dict_user = self._user.get_dict_form_data()
        dict_user['point'] = point
        dict_user['rank'] = rank
        return dict_user

    def get_response_form_data(self, head_parser):
        try:
            body = {
                'my_contribution' : self._get_my_data(),
                'result' : self.__result
            }

            response = self._get_response_data(head_parser=head_parser, body=body)
            return response

        except Exception as e:
            raise CoreControllerLogicError("response making error | " + e)