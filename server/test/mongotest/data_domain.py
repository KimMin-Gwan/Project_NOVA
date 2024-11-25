from typing import Any
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
    def __init__(self, uid = "", uname = "지지자", age=0, 
                 email = "", gender = "d" ,
                 credit = 0, solo_bid = "", group_bid = "", 
                 password = "", alert= [], like=[], my_comment=[],
                 my_feed = [], active_feed = [], feed_history = [],
                 feed_search_history=[]):

        self.uid = uid
        self.uname = uname
        self.age = age
        self.email = email
        self.password = password
        self.gender = gender
        self.solo_bid = solo_bid
        self.group_bid = group_bid
        self.credit = credit
        self.alert:list = copy.copy(alert)
        self.like:list = copy.copy(like)
        self.my_comment:list = copy.copy(my_comment)
        self.my_feed:list = copy.copy(my_feed)
        self.active_feed:list = copy.copy(active_feed)
        self.feed_history:list = copy.copy(feed_history)
        self.feed_search_history:list =copy.copy(feed_search_history)


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
            self.credit= dict_data['credit']
            self.alert = copy.copy(dict_data['alert'])
            self.like = copy.copy(dict_data["like"])
            self.my_comment = copy.copy(dict_data["my_comment"])
            self.my_feed = copy.copy(dict_data["my_feed"])
            self.active_feed = copy.copy(dict_data["active_feed"])
            self.feed_history = copy.copy(dict_data["feed_history"])
            self.feed_search_history = copy.copy(dict_data["feed_search_history"])
            return
        except Exception as e:
            raise e
    
    # response에 사용되는 json형태로 만들기 위한 dict 데이터
    def get_dict_form_data(self):
        return {
            "uid" : self.uid,
            "uname" : self.uname,
            "age" : self.age,
            "email" : self.email,
            "password" : self.password,
            "gender" : self.gender,
            "credit" : self.credit,
            "solo_bid" : self.solo_bid,
            "group_bid" : self.group_bid,
            "alert" : copy.copy(self.alert),
            "like" : copy.copy(self.like),
            "my_comment" : copy.copy(self.my_comment),
            "my_feed" : copy.copy(self.my_feed),
            "active_feed" : copy.copy(self.active_feed),
            "feed_history" : copy.copy(self.feed_history),
            "feed_search_history" : copy.copy(self.feed_search_history)
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
            raise e

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
            raise e

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
            raise e

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
    def __init__(self, fid="", uid="", nickname="", star=60,
                 body="", date="", fclass="", class_name="",
                 choice=None, result=None, state="d", attend=None,
                 category = None, comment = None, image = None,
                 hashtag = None):
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
        if image is None:
            image = []
        if hashtag is None:
            hashtag = []

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
        self.image = copy.copy(image)
        self.hashtag = copy.copy(hashtag)
        self.num_image = len(self.image)

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
            self.image= copy.copy(dict_data['image'])
            self.hashtag = copy.copy(dict_data['hashtag'])
            self.num_image = len(self.image)
            self.num_comment = len(self.comment)
        except KeyError as e:
            raise e

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
            "star_flag" : self.star_flag,
            "image":copy.copy(self.image),
            "hashtag":copy.copy(self.hashtag),
            "num_image": self.num_image
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
            raise e

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
            raise e

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
                 my_feed = [], my_comment = [], active_feed=[],
                 feed_key = 0, comment_key = 0):
        self.uid = uid
        self.option = copy.copy(option)
        self.history:list = copy.copy(history)
        self.ttl= 0
        self.star:list= copy.copy(star)
        self.my_feed:list= copy.copy(my_feed)
        self.my_comment:list = copy.copy(my_comment)
        self.active_feed:list = copy.copy(active_feed)
        self.feed_key = feed_key
        self.comment_key = comment_key

    def make_with_dict(self, dict_data):
        try:
            self.uid = dict_data['muid']
            self.option = copy.copy(dict_data['option'])
            self.history:list = copy.copy(dict_data['history'])
            self.star:list = copy.copy(dict_data['star'])
            self.my_feed:list = copy.copy(dict_data['my_feed'])
            self.my_comment:list =copy.copy(dict_data['my_comment'])
            self.active_feed:list =copy.copy(dict_data['active_feed'])
            self.feed_key = dict_data['feed_key']
            self.comment_key = dict_data['comment_key']
        except KeyError as e:
            e

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
            "active_feed" : copy.copy(self.active_feed),
            "feed_key" : self.feed_key,
            "comment_key" : self.comment_key
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
            raise e

    def get_dict_form_data(self):
        return {
            "aid" : self.aid,
            "uid" : self.uid,
            "body" : self.body,
            "date" : self.date
        }

# 유저 특화 시스템 구성을 위한 관리 유저
class Notice:
    def __init__(self, nid="", date="", title="", body=""):
        self.nid = nid 
        self.date =date 
        self.title=title
        self.body=body

    def make_with_dict(self, dict_data):
        try:
            self.nid= dict_data['nid']
            self.date= dict_data['date']
            self.title= dict_data['title']
            self.body = dict_data['body']
        except KeyError as e:
            raise e

    def get_dict_form_data(self):
        return {
            "nid" : self.nid,
            "date" : self.date,
            "title" : self.title,
            "body" : self.body
        }