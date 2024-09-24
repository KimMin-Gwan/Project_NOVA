from typing import Any
from others.error_lib import DictMakingError

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
                 group_bid = "", items = None,
                 solo_daily = False, solo_special = False,
                 group_daily = False, group_special = False,
                 sign = "", password = "", select_name_card = "",
                 solo_daily_check_date = "", group_daily_check_date = "",
                 name_card_list= []
                 ):
        if items == None:
            items = Item()

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
        self.items = items
        self.solo_daily = solo_daily
        self.solo_special = solo_special
        self.group_daily = group_daily
        self.group_special = group_special
        self.sign = sign
        self.select_name_card = select_name_card
        self.name_card_list = name_card_list
        self.solo_daily_check_date = solo_daily_check_date
        self.group_daily_check_date = group_daily_check_date

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
            self.items = Item(init_data = dict_data['items'])
            self.sign = dict_data['sign']
            self.select_name_card = dict_data['select_name_card']
            self.name_card_list = dict_data['name_card_list']
            self.solo_daily_check_date = dict_data['solo_daily_check_date']
            self.group_daily_check_date = dict_data['group_daily_check_date']
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
            "items" : self.items.get_dict_form_data(),
            "solo_daily" :self.solo_daily,
            "solo_special" :self.solo_special,
            "group_daily" :self.group_daily,
            "group_special" :self.group_special,
            "sign" : self.sign,
            "select_name_card" : self.select_name_card,
            "name_card_list": self.name_card_list,
            "solo_daily_check_date" : self.solo_daily_check_date,
            "group_daily_check_date" : self.group_daily_check_date
        }

class Item(SampleDomain):
    def __init__(self, init_data = {"chatting" : 0, "saver":0}):
        self.chatting  = init_data["chatting"]
        self.saver = init_data["saver"]

    def get_dict_form_data(self):
        return {
            "chatting" : self.chatting,
            "saver": self.saver
        }



class Bias(SampleDomain):
    def __init__(self, bid="", type="", bname="", category=[], birthday="", debut="",
                 agency="", group=[], lid="", point=0, num_user=0, x_account="",
                 insta_account="", tiktok_account="", youtube_account="", homepage="",
                 fan_cafe="", country=[], nickname=[], fanname = [], group_member_bids=[]):
        self.bid = bid
        self.type = type
        self.bname = bname
        self.category = category
        self.birthday = birthday
        self.debut = debut
        self.agency = agency
        self.group = group
        self.lid = lid
        self.point = point
        self.num_user = num_user
        self.x_account = x_account
        self.insta_account = insta_account
        self.tiktok_account = tiktok_account
        self.youtube_account = youtube_account
        self.homepage = homepage
        self.fan_cafe = fan_cafe
        self.country = country
        self.nickname = nickname
        self.fanname = fanname
        self.group_memeber_bids = group_member_bids


    def make_with_dict(self, dict_data):
        try:
            self.bid = dict_data['bid']
            self.type = dict_data['type']
            self.bname = dict_data['bname']
            self.category = dict_data['category']
            self.birthday = dict_data['birthday']
            self.debut = dict_data['debut']
            self.agency = dict_data['agency']
            self.group = dict_data['group']
            self.lid = dict_data['lid']
            self.point = dict_data['point']
            self.num_user = dict_data['num_user']
            self.x_account = dict_data['x_account']
            self.insta_account = dict_data['insta_account']
            self.tiktok_account = dict_data['tiktok_account']
            self.youtube_account = dict_data['youtube_account']
            self.homepage = dict_data['homepage']
            self.fan_cafe = dict_data['fan_cafe']
            self.country = dict_data['country']
            self.nickname = dict_data['nickname']
            self.fanname = dict_data['fanname']
            self.group_memeber_bids = dict_data['group_member_bids']
        except Exception as e:
            print(e)
            raise DictMakingError(error_type=e)

    def get_dict_form_data(self):
        return {
            "bid": self.bid,
            "type": self.type,
            "bname": self.bname,
            "category": self.category,
            "birthday": self.birthday,
            "debut": self.debut,
            "agency": self.agency,
            "group": self.group,
            "lid": self.lid,
            "point": self.point,
            "num_user": self.num_user,
            "x_account": self.x_account,
            "insta_account": self.insta_account,
            "tiktok_account": self.tiktok_account,
            "youtube_account": self.youtube_account,
            "homepage": self.homepage,
            "fan_cafe": self.fan_cafe,
            "country": self.country,
            "nickname": self.nickname,
            'fanname':self.fanname,
            'group_member_bids':self.group_memeber_bids
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
        self.bid_list = bid_list
        self.tier = tier
        self.num_bias = num_bias
        self.state = state
        self.type=type

    def make_with_dict(self, dict_data):
        try:
            self.lid = dict_data['lid']
            self.lname = dict_data['lname']
            self.bid_list = dict_data['bid_list']
            self.tier = dict_data['tier']
            self.num_bias = dict_data['num_bias']
            self.state = dict_data['state']
            self.type = dict_data['type']
        except Exception as e:
            raise DictMakingError(error_type=e)

    def get_dict_form_data(self):
        return {
            "lid": self.lid,
            "lname": self.lname,
            "bid_list": self.bid_list,
            "tier": self.tier,
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
        self.choice = choice
        self.result = result
        self.state = state  # feed 의 상태 
        self.attend = attend
        self.category = category
        self.comment =comment 
        self.star = star

    def make_with_dict(self, dict_data):
        try:
            self.fid = dict_data['fid']
            self.uid = dict_data['uid']
            self.nickname = dict_data['nickname']
            self.body = dict_data['body']
            self.date = dict_data['date']
            self.fclass = dict_data['fclass']
            self.class_name = dict_data['class_name']
            self.choice = dict_data['choice']
            self.result = dict_data['result']
            self.state = dict_data['state']
            self.attend = dict_data['attend']
            self.category = dict_data['category']
            self.comment = dict_data['comment']
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
            "choice": self.choice,
            "result": self.result,
            "state": self.state,
            "attend": self.attend,
            "category":self.category,
            "comment":self.comment,
            "star":self.star
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
