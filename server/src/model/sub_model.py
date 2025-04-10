from model.base_model import BaseModel
from model.league_model import LeagueModel
from model import Local_Database
from others.data_domain import Bias, User, Report
from others import CoreControllerLogicError, HTMLEXtractor, ImageDescriper
import copy
from urllib.parse import urlparse
import datetime

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


        # solo_bid 같은건 없어졌는데 왜 여기 있음?

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
        if self._bias.bid in self._user.bids:
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

# class NoticeListModel(UserContributionModel):
#     def __init__(self, database:Local_Database) -> None:
#         super().__init__(database)
#         self.__notice = []
#
#     # rank와 point를 포함한 데이터
#     def get_notice_list(self):
#         notice_datas = self._database.get_all_data(target="nid")
#         for notice_data in notice_datas:
#             notice = Notice()
#             notice.make_with_dict(notice_data)
#             notice.body = ""
#             self.__notice.append(notice)
#
#     def get_response_form_data(self, head_parser):
#         try:
#             body = {
#                 'notice_list' : self._make_dict_list_data(list_data=self.__notice)
#             }
#
#             response = self._get_response_data(head_parser=head_parser, body=body)
#             return response
#
#         except Exception as e:
#             raise CoreControllerLogicError("response making error | " + e)
#
# class NoticeModel(UserContributionModel):
#     def __init__(self, database:Local_Database) -> None:
#         super().__init__(database)
#         self.__notice = Notice()
#
#     def get_notice(self, nid):
#         notice_data = self._database.get_data_with_id(target="nid", id=nid)
#         if not notice_data:
#             self.__notice.title = "없는 공지사항 입니다"
#         else:
#             self.__notice.make_with_dict(notice_data)
#         return
#
#     def get_response_form_data(self, head_parser):
#         try:
#             body = {
#                 'notice' : self.__notice.get_dict_form_data()
#             }
#
#             response = self._get_response_data(head_parser=head_parser, body=body)
#             return response
#
#         except Exception as e:
#             raise CoreControllerLogicError("response making error | " + e)

class ImageTagModel(BaseModel):
    def __init__(self, database:Local_Database) -> None:
        super().__init__(database)
        self.__url = ""
        self.__image = ""

    def get_image(self, url):
        self.__url = url
        self.__image = HTMLEXtractor().extract_external_webpage_image_data(url=url)

    def get_response_form_data(self, head_parser):
        try:
            body = {
                'url' : self.__url,
                'image' : self.__image
            }

            response = self._get_response_data(head_parser=head_parser, body=body)
            return response

        except Exception as e:
            raise CoreControllerLogicError("response making error | " + e)


class CommunitySideBoxModel(BaseModel):
    def __init__(self, database):
        super().__init__(database)
        self.__bias = Bias()
        self.__urls = {}
        self._boards = []

    def get_response_form_data(self, head_parser):
        try:
            body = {
                'bname' : self.__bias.bname,
                'urls' : self.__urls,
                'boards' : self._boards
            }

            response = self._get_response_data(head_parser=head_parser, body=body)
            return response

        except Exception as e:
            raise CoreControllerLogicError("response making error | " + e)

    def get_boards_of_bias_community(self, bid):
        bias_data = self._database.get_data_with_id(target='bid', id=bid)
        
        if bias_data:
            self.__bias.make_with_dict(bias_data)
            self._boards = copy.copy(self.__bias.board_types)
            return True
        else:
            return False

    def get_urls_of_bias(self):
        # URL 패턴. 고정된 패턴들을 포함합니다.
        self.__urls["X"] = self.__bias.x_account
        self.__urls["Instagram"] =  self.__bias.insta_account
        self.__urls["TikTok"]=  self.__bias.tiktok_account
        self.__urls["Youtube"] = self.__bias.youtube_account

        # 홈페이지 패턴, 주요한 곳들을 추가했음. 팝콘, 팬더는 일부러 안넣음 만약 넣어야한다면 넣겠다.

        # 치지직
        if "chzzk" in self.__bias.homepage:
            self.__urls["Chzzk"] = self.__bias.homepage
        # SOOP, 구 아프리카티비
        elif "soop" in self.__bias.homepage or "afreecatv" in self.__bias.homepage:
            self.__urls["SOOP"] = self.__bias.homepage
        # 플렉스 티비. 여기 여캠 비중 압도적인 신생 플랫폼
        elif "flextv" in self.__bias.homepage:
            self.__urls["FlexTV"] = self.__bias.homepage
        # 카카오티비. 구 다음팟 티비
        elif "kakao" in self.__bias.homepage:
            self.__urls["KakaoTV"] = self.__bias.homepage
        # 트위치. 망했지만 넣긴하는게 맞음. 해외시청자가 주인 방송인들은 아직 잔류하는 듯
        elif "twitch" in self.__bias.homepage:
            self.__urls["Twitch"] = self.__bias.homepage

        # 나머지 플랫폼 : Default로 두겠음
        else:
            self.__urls["Default"] = self.__bias.homepage

        # 팬카페 패턴
        if "naver" in self.__bias.fan_cafe:
            self.__urls["Naver"] = self.__bias.fan_cafe
        elif "daum" in self.__bias.fan_cafe:
            self.__urls["Daum"] = self.__bias.fan_cafe

        # 디코로 대화하는 쪽도 있어서 걍 넣음
        elif "discord" in self.__bias.fan_cafe:
            self.__urls["Discord"] = self.__bias.fan_cafe

        # 팬카페는 3가지 경우에 대해서만 하겠음
        # 팬심은 안넣습니다.
        else:
            self.__urls["Default"] = self.__bias.fan_cafe

        # 마지막. 키 순회하면서 ""인 값들을 모두 쳐냄
        for key in list(self.__urls.keys()):
            if self.__urls[key] == "":
                del self.__urls[key]


class ReportModel(BaseModel):
    def __init__(self, database):
        super().__init__(database)
        self.__report = Report()
        self.__result = False
        
    # 리포트 만들기
    def try_set_report(self, data_payload):
        if data_payload.cid != "":
            self.__report.cid = data_payload.cid
        else:
            self.__report.fid = data_payload.fid    
            
        self.__report.date = self._set_datetime()
        self.__report.rid = self._make_new_id()
        self.__report.type = "wicked"
        self.__report.result = False
        return
    
    # 버그 리포트 일때
    def try_set_bug_report(self, data_payload):
        self.__report.detail = data_payload.detail
        self.__report.type = "bug"
        
        if data_payload.images:
            ImageDescriper().try_report_image_upload(rid=self.__report.rid,
                                                    image_names=data_payload.image_names,
                                                    images=data_payload.images
                                                    )
        
        return
    
    # 리포트 저장
    def save_report(self):
        self._database.add_new_data(target_id="rid", new_data=self.__report.get_dict_form_data())
        self.__result = True
        return
    
    def get_response_form_data(self, head_parser):
        try:
            body = {
                'result' : self.__result
            }

            response = self._get_response_data(head_parser=head_parser, body=body)
            return response

        except Exception as e:
            raise CoreControllerLogicError("response making error | " + e)

class ChangeUserAgeModel(BaseModel):
    def __init__(self, database:Local_Database) -> None:
        super().__init__(database)
        self._result = False
        self._detail = ""

    def get_response_form_data(self, head_parser):
        try:
            body = {
                'result' : self._result,
                'detail' : self._detail
            }

            response = self._get_response_data(head_parser=head_parser, body=body)
            return response

        except Exception as e:
            raise CoreControllerLogicError("response making error | " + e)

    def change_users_age(self):
        today = datetime.datetime.now()
        user_datas = self._database.get_all_data(target="uid")
        if today.month == 1 and today.day == 1:
            for user_data in user_datas:
                user_data['age'] += 1

        # 하나하나 저장 함.
        for user_data in user_datas:
            self._database.modify_data_with_id(target_id="uid", target_data=user_data)

        self._result = True
        self._detail = "Complete Change all users age"

        return



