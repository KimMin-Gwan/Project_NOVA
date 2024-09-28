from typing import Any
from others.error_lib import DictMakingError
import copy

# 추상 클래스
class SampleDomain:
    def get_dict_form_data(self):
        pass

    def make_with_dict(self, dict_data):
        pass

class TempUser:
    def __init__(self, email="", verification_code = "",
                exp = "",
                 ):
        self.email = email
        self.verification_code = verification_code
        self.exp = exp

    def __call__(self):
        print(self.email)
        print(self.verification_code)
        print(self.exp)
        return

class User(SampleDomain):
    def __init__(self, uid = "", uname = "", age=14, 
                 email = "", gender = "d" , solo_point = 0, group_point = 0,
                 solo_combo = 0, group_combo = 0,
                 credit = 0, solo_bid = "",
                 group_bid = "", 
                 solo_daily = False, solo_special = False,
                 group_daily = False, group_special = False,
                 sign = "", password = "", select_name_card = "",
                 solo_daily_check_date = "", group_daily_check_date = "",
                 name_card_list= [], alert = []):

        self.uid = uid
        self.uname = uname
        self.age = age
        self.email = email
        self.password = password
        self.gender = gender
        self.solo_point = solo_point
        self.group_point = group_point
        self.solo_combo = solo_combo
        self.group_combo = group_combo
        self.credit = credit
        self.solo_bid = solo_bid
        self.group_bid = group_bid
        self.solo_daily = solo_daily
        self.solo_special = solo_special
        self.group_daily = group_daily
        self.group_special = group_special
        self.sign = sign
        self.select_name_card = select_name_card
        self.name_card_list = copy.copy(name_card_list)
        self.solo_daily_check_date = solo_daily_check_date
        self.group_daily_check_date = group_daily_check_date
        self.alert = copy.copy(alert)

    # database로 부터 받아온 데이터를 사용해 내용 구성
    def make_with_dict(self, dict_data):
        try:
            self.uid = dict_data['uid']
            self.uname = dict_data['uname']
            self.age= dict_data['age']
            self.email= dict_data['email']
            self.password = dict_data['password']
            self.gender= dict_data['gender']
            self.solo_bid = dict_data['solo_bid']
            self.group_bid = dict_data['group_bid']
            self.solo_point = dict_data['solo_point']
            self.group_point = dict_data['group_point']
            self.solo_combo= dict_data['solo_combo']
            self.group_combo= dict_data['group_combo']
            self.credit= dict_data['credit']
            self.solo_daily = dict_data['solo_daily']
            self.solo_special = dict_data['solo_special']
            self.group_daily = dict_data['group_daily']
            self.group_special = dict_data['group_special']
            self.sign = dict_data['sign']
            self.select_name_card = dict_data['select_name_card']
            self.name_card_list = copy.copy(dict_data['name_card_list'])
            self.solo_daily_check_date = dict_data['solo_daily_check_date']
            self.group_daily_check_date = dict_data['group_daily_check_date']
            self.alert = copy.copy(dict_data['alert'])
            return
        except Exception as e:
            raise DictMakingError(error_type=e)
    
    # response에 사용되는 json형태로 만들기 위한 dict 데이터
    def get_dict_form_data(self):
        return {
            "uid" : self.uid,
            "uname" : self.uname,
            "age" : self.age,
            "email" : self.email,
            "password" : self.password,
            "gender" : self.gender,
            "solo_point" : self.solo_point,
            "group_point" : self.group_point,
            "solo_combo" : self.solo_combo,
            "group_combo" : self.group_combo,
            "credit" : self.credit,
            "solo_bid" : self.solo_bid,
            "group_bid" : self.group_bid,
            "solo_daily" :self.solo_daily,
            "solo_special" :self.solo_special,
            "group_daily" :self.group_daily,
            "group_special" :self.group_special,
            "sign" : self.sign,
            "select_name_card" : self.select_name_card,
            "name_card_list": copy.copy(self.name_card_list),
            "solo_daily_check_date" : self.solo_daily_check_date,
            "group_daily_check_date" : self.group_daily_check_date,
            "alert" : copy.copy(self.alert)
        }



class Bias(SampleDomain):
    def __init__(self, bid="", type="", bname="", category=[], birthday="", debut="",
                 agency="", group=[], lid="", point=0, num_user=0, x_account="",
                 insta_account="", tiktok_account="", youtube_account="", homepage="",
                 fan_cafe="", country=[], nickname=[], fanname = [], group_member_bids=[]):
        self.bid = bid
        self.type = type
        self.bname = bname
        self.category = copy.copy(category)
        self.birthday = birthday
        self.debut = debut
        self.agency = agency
        self.group = copy.copy(group)
        self.lid = lid
        self.point = point
        self.num_user = num_user
        self.x_account = x_account
        self.insta_account = insta_account
        self.tiktok_account = tiktok_account
        self.youtube_account = youtube_account
        self.homepage = homepage
        self.fan_cafe = fan_cafe
        self.country = copy.copy(country)
        self.nickname = copy.copy(nickname)
        self.fanname = copy.copy(fanname)
        self.group_memeber_bids = copy.copy(group_member_bids)


    def make_with_dict(self, dict_data):
        try:
            self.bid = dict_data['bid']
            self.type = dict_data['type']
            self.bname = dict_data['bname']
            self.category = copy.copy(dict_data['category'])
            self.birthday = dict_data['birthday']
            self.debut = dict_data['debut']
            self.agency = dict_data['agency']
            self.group = copy.copy(dict_data['group'])
            self.lid = dict_data['lid']
            self.point = dict_data['point']
            self.num_user = dict_data['num_user']
            self.x_account = dict_data['x_account']
            self.insta_account = dict_data['insta_account']
            self.tiktok_account = dict_data['tiktok_account']
            self.youtube_account = dict_data['youtube_account']
            self.homepage = dict_data['homepage']
            self.fan_cafe = dict_data['fan_cafe']
            self.country = copy.copy(dict_data['country'])
            self.nickname = copy.copy(dict_data['nickname'])
            self.fanname = copy.copy(dict_data['fanname'])
            self.group_memeber_bids = copy.copy(dict_data['group_member_bids'])
        except Exception as e:
            print(e)
            raise DictMakingError(error_type=e)

    def get_dict_form_data(self):
        return {
            "bid": self.bid,
            "type": self.type,
            "bname": self.bname,
            "category": copy.copy(self.category),
            "birthday": self.birthday,
            "debut": self.debut,
            "agency": self.agency,
            "group": copy.copy(self.group),
            "lid": self.lid,
            "point": self.point,
            "num_user": self.num_user,
            "x_account": self.x_account,
            "insta_account": self.insta_account,
            "tiktok_account": self.tiktok_account,
            "youtube_account": self.youtube_account,
            "homepage": self.homepage,
            "fan_cafe": self.fan_cafe,
            "country": copy.copy(self.country),
            "nickname": copy.copy(self.nickname),
            'fanname':copy.copy(self.fanname),
            'group_member_bids':copy.copy(self.group_memeber_bids)
        }


class NameCard(SampleDomain):
    def __init__(self, ncid="", ncname="", nccredit=0):
        self.ncid = ncid
        self.ncname = ncname
        self.nccredit = nccredit

    def make_with_dict(self, dict_data):
        try:
            self.ncid = dict_data['ncid']
            self.ncname = dict_data['ncname']
            self.nccredit = dict_data['nccredit']
        except Exception as e:
            raise DictMakingError(error_type=e)

    def get_dict_form_data(self):
        return {
            "ncid": self.ncid,
            "ncname": self.ncname,
            "nccredit": self.nccredit
        }
    
class League(SampleDomain):
    def __init__(self, lid="", lname="", bid_list=None, tier=None, num_bias=0, state="", type="solo"):
        if bid_list is None:
            bid_list = []
        if tier is None:
            tier = []
        self.lid = lid
        self.lname = lname
        self.bid_list = copy.copy(bid_list)
        self.tier = copy.copy(tier)
        self.num_bias = num_bias
        self.state = state
        self.type=type

    def make_with_dict(self, dict_data):
        try:
            self.lid = dict_data['lid']
            self.lname = dict_data['lname']
            self.bid_list = copy.copy(dict_data['bid_list'])
            self.tier = copy.copy(dict_data['tier'])
            self.num_bias = dict_data['num_bias']
            self.state = dict_data['state']
            self.type = dict_data['type']
        except Exception as e:
            raise DictMakingError(error_type=e)

    def get_dict_form_data(self):
        return {
            "lid": self.lid,
            "lname": self.lname,
            "bid_list": copy.copy(self.bid_list),
            "tier": copy.copy(self.tier),
            "num_bias": self.num_bias,
            "state": self.state,
            "type":self.type
        }
    
class Feed(SampleDomain):
    def __init__(self, fid="", uid="", nickname="", star=0,
                 body="", date="", fclass="", class_name="",
                 choice=None, result=None, state="d", attend=None,
                 category = None, comment = None):
        if choice is None:
            choice = []
        if result is None:
            result = []
        if attend is None:
            attend = []
        if category is None:
            category = []
        if comment is None:
            comment = []

        self.fid = fid
        self.uid = uid
        self.nickname = nickname
        self.body = body
        self.date = date
        self.fclass = fclass
        self.class_name = class_name
        self.choice = copy.copy(choice)
        self.result = copy.copy(result)
        self.state = state  # feed 의 상태 
        self.attend = copy.copy(attend)
        self.category = copy.copy(category)
        self.comment = copy.copy(comment)
        self.num_comment = 0
        self.star = star
        self.star_flag = False

    def make_with_dict(self, dict_data):
        try:
            self.fid = dict_data['fid']
            self.uid = dict_data['uid']
            self.nickname = dict_data['nickname']
            self.body = dict_data['body']
            self.date = dict_data['date']
            self.fclass = dict_data['fclass']
            self.class_name = dict_data['class_name']
            self.choice = copy.copy(dict_data['choice'])
            self.result = copy.copy(dict_data['result'])
            self.state = dict_data['state']
            self.attend = copy.copy(dict_data['attend'])
            self.category = copy.copy(dict_data['category'])
            self.comment = copy.copy(dict_data['comment'])
            self.star= dict_data['star']
        except KeyError as e:
            raise DictMakingError(error_type=f"Missing key: {str(e)}")

    def get_dict_form_data(self):
        return {
            "fid": self.fid,
            "uid": self.uid,
            "nickname": self.nickname,
            "body": self.body,
            "date": self.date,
            "fclass": self.fclass,
            "class_name": self.class_name,
            "choice": copy.copy(self.choice),
            "result": copy.copy(self.result),
            "state": self.state,
            "attend": copy.copy(self.attend),
            "category":copy.copy(self.category),
            "comment":copy.copy(self.comment),
            "num_comment" :self.num_comment,
            "star":self.star,
            "star_flag" : self.star_flag
        }


class Banner(SampleDomain):
    def __init__(self, baid="", ba_url=""):
        self.baid = baid
        self.ba_url = ba_url

    def make_with_dict(self, dict_data):
        try:
            self.baid = dict_data['baid']
            self.ba_url = dict_data['ba_url']
        except Exception as e:
            raise DictMakingError(error_type=e)

    def get_dict_form_data(self):
        return {
            "baid": self.baid,
            "ba_url": self.ba_url
        }

class Comment(SampleDomain):
    def __init__(self, cid="", fid="", uid="", uname="",
                 body="", date="", like=0, state="y", like_user=[]):
        self.cid = cid
        self.fid = fid
        self.uid = uid
        self.uname = uname
        self.body = body
        self.date = date
        self.like = like
        self.state = state
        self.like_user = copy.copy(like_user)
        self.num_like_user = len(self.like_user)
        self.owner = False

    def make_with_dict(self, dict_data):
        try:
            self.cid = dict_data['cid']
            self.fid = dict_data['fid']
            self.uid = dict_data['uid']
            self.uname = dict_data['uname']
            self.body = dict_data['body']
            self.date = dict_data['date']
            self.like = dict_data['like']
            self.state = dict_data['state']
            self.like_user= copy.copy(dict_data['like_user'])
        except KeyError as e:
            raise DictMakingError(error_type=f"Missing key: {str(e)}")

    def get_dict_form_data(self):
        return {
            "cid": self.cid,
            "fid": self.fid,
            "uid": self.uid,
            "uname": self.uname,
            "body": self.body,
            "date": self.date,
            "like": self.like,
            "state": self.state,
            "like_user": copy.copy(self.like_user),
            "owner" : self.owner
        }

# 유저 특화 시스템 구성을 위한 관리 유저
class ManagedUser:
    def __init__(self, uid="", option=[], history=[], star=[],
                 my_feed = [], my_comment = [], active_feed=[]):
        self.uid = uid
        self.option = copy.copy(option)
        self.history = copy.copy(history)
        self.ttl= 0
        self.star= copy.copy(star)
        self.my_feed = copy.copy(my_feed)
        self.my_comment = copy.copy(my_comment)
        self.active_feed = copy.copy(active_feed)

    def make_with_dict(self, dict_data):
        try:
            self.uid = dict_data['muid']
            self.option = copy.copy(dict_data['option'])
            self.history = copy.copy(dict_data['history'])
            self.star = copy.copy(dict_data['star'])
            self.my_feed = copy.copy(dict_data['my_feed'])
            self.my_comment =copy.copy(dict_data['my_comment'])
            self.active_feed =copy.copy(dict_data['active_feed'])
        except KeyError as e:
            raise DictMakingError(error_type=f"Missing key: {str(e)}")

    def __call__(self):
        print(f"uid : {self.uid}")
        print(f"history : {self.history}")
        print(f"TTL : {self.ttl}")

    def get_dict_form_data(self):
        return {
            "muid" : self.uid,
            "option" : copy.copy(self.option),
            "history" : copy.copy(self.history),
            "star" : copy.copy(self.star),
            "my_feed" : copy.copy(self.my_feed),
            "my_comment" : copy.copy(self.my_comment),
            "active_feed" : copy.copy(self.active_feed)
        }
    

# 유저 특화 시스템 구성을 위한 관리 유저
class Alert:
    def __init__(self, aid="", uid="", body="", date =""):
        self.aid = aid
        self.uid = uid
        self.body=body
        self.date=date


    def make_with_dict(self, dict_data):
        try:
            self.aid = dict_data['aid']
            self.uid = dict_data['uid']
            self.body = dict_data['body']
            self.date = dict_data['date']
        except KeyError as e:
            raise DictMakingError(error_type=f"Missing key: {str(e)}")

    def get_dict_form_data(self):
        return {
            "aid" : self.aid,
            "uid" : self.uid,
            "body" : self.body,
            "date" : self.date
        }