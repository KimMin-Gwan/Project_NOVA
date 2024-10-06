from model.base_model import BaseModel
from model.league_model import LeagueModel
from model import Local_Database
from others.data_domain import League, Bias, User, Notice
from others import CoreControllerLogicError

class BiasBannerModel(BaseModel):
    def __init__(self, database:Local_Database) -> None:
        super().__init__(database)

    def get_response_form_data(self, head_parser):
        try:
            body = {
                'result' : []
            }

            response = self._get_response_data(head_parser=head_parser, body=body)
            return response

        except Exception as e:
            raise CoreControllerLogicError("response making error | " + e)

class BiasNLeagueModel(LeagueModel):
    def __init__(self, database:Local_Database) -> None:
        super().__init__(database)
        self.__my_league_data = {}
    
    # 리그 정보 세팅
    # @override
    def set_leagues(self) -> bool: 
        try:
            league_data = self._database.get_data_with_id(target="lid", id=self._bias.lid)#type = solo

            if not league_data:
                return False

            self._league.make_with_dict(league_data)
            return True
        
        except Exception as e:
            raise CoreControllerLogicError(error_type="set_solo_leagues | " + str(e))
    
    # 리그 통계정보를 받아야됨
    def get_my_league_data(self):
        for dict_data in self._dict_bias_data:
            if dict_data['bid'] == self._bias.bid:
                self.__my_league_data = dict_data

        #self.__my_league_data['total_user'] = self._bias.num_user

        if self._bias.type == "solo":
            user_datas = self._database.get_datas_with_key(target="uid", key="solo_bid", key_datas=[self._bias.bid])
        elif self._bias.type == "group":
            user_datas = self._database.get_datas_with_key(target="uid", key="group_bid", key_datas=[self._bias.bid])

        num_user = 0

        if self._bias.type == "solo":
            for user_data in user_datas:
                user = User()
                user.make_with_dict(user_data)
                if user.solo_point!= 0:
                    num_user += 1
        elif self._bias.type == "group":
            for user_data in user_datas:
                user = User()
                user.make_with_dict(user_data)
                if user.group_point!= 0:
                    num_user += 1
        else:
            False
        self.__my_league_data['lname'] = self._league.lname
        self.__my_league_data['contributed_user'] = num_user

        return True

    def get_response_form_data(self, head_parser):
        try:
            body = {
                "result" : self.__my_league_data
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
        
        
class NoticeListModel(UserContributionModel):
    def __init__(self, database:Local_Database) -> None:
        super().__init__(database)
        self.__notice = []

    # rank와 point를 포함한 데이터
    def get_notice_list(self):
        notice_datas = self._database.get_all_data(target="nid")

        for notice_data in notice_datas:
            notice = Notice()
            notice.get_dict_form_data(notice_data)
            notice.body = ""
            self.__notice.append(notice)

    def get_response_form_data(self, head_parser):
        try:
            body = {
                'notice_list' : self._make_dict_list_data(list_data=self.__notice)
            }

            response = self._get_response_data(head_parser=head_parser, body=body)
            return response

        except Exception as e:
            raise CoreControllerLogicError("response making error | " + e)
        
class NoticeModel(UserContributionModel):
    def __init__(self, database:Local_Database) -> None:
        super().__init__(database)
        self.__notice = Notice()

    # rank와 point를 포함한 데이터
    def get_notice(self, id):
        notice_data = self._database.get_data_with_id(target="nid", id=id)
        self.__notice.get_dict_form_data(notice_data)
        return

    def get_response_form_data(self, head_parser):
        try:
            body = {
                'notice_list' : self._make_dict_list_data(list_data=self.__notice)
            }

            response = self._get_response_data(head_parser=head_parser, body=body)
            return response

        except Exception as e:
            raise CoreControllerLogicError("response making error | " + e)