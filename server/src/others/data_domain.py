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
    
class TimeTableUser(SampleDomain):
    def __init__(self, tuid="", uid="", sids=None, this_week_sids=None,
                 seids=None, my_sids=None,
                 my_sbids=None, my_seids=None, category=None):
        self.tuid: str = tuid               # Time table user ID == User.uid
        self.sids: list = sids if sids is not None else []         # Schedule IDs
        self.seids: list = seids if seids is not None else []      # Schedule event IDs
        self.this_week_sids = this_week_sids if this_week_sids is not None else []  # 이번주에 체크한거
        self.my_sids: list = my_sids if my_sids is not None else []  # My schedule IDs
        self.my_sbids: list = my_sbids if my_sbids is not None else []  # My schedule bundle IDs
        self.my_seids: list = my_seids if my_seids is not None else []  # My schedule event IDs
        self.category: list = category if category is not None else []  # interest category tag

    def make_with_dict(self, dict_data:dict):
        self.tuid = dict_data.get('tuid', "")
        self.sids = dict_data.get('sids', [])
        self.seids = dict_data.get('seids', [])
        self.my_sids = dict_data.get('my_sids', [])
        self.my_sbids = dict_data.get('my_sbids', [])
        self.my_seids = dict_data.get('my_seids', [])
        self.category = dict_data.get('category', [])
        return self

    def get_dict_form_data(self):
        return {
            "tuid": self.tuid,
            "sids": self.sids,
            "seids": self.seids,
            "my_sids": self.my_sids,
            "my_sbids": self.my_sbids,
            "my_seids": self.my_seids,
            "category" : self.category
        }


    
class ScheduleEvent(SampleDomain):
    def __init__(self, seid="", sename="", bid="",
                 bname="", uid="", uname="", update_datetime="",
                 location="", start_time="", end_time="", date="",
                 code="", sids=[]
                 ):
        
        self.seid: str = seid                   # Schedule event ID
        self.sename: str = sename               # Schedule event name
        self.bid: str = bid                     # Bias ID
        self.bname: str = bname                 # Bias name
        self.uid: str = uid                     # Maker's ID
        self.uname: str = uname                 # Maker's name
        self.update_datetime: str = update_datetime  # Update date and time
        self.location: str = location           # Event location
        self.start_time: str = start_time       # Event start time
        self.end_time: str = end_time           # Event end time
        self.date: str = date                   # Event date
        self.code: str = code                   # Schdeul Code
        self.sids: list = sids

    def make_with_dict(self, dict_data:dict):
        self.seid = dict_data.get('seid', "")
        self.sename = dict_data.get('sename', "")
        self.bid = dict_data.get('bid', "")
        self.bname = dict_data.get('bname', "")
        self.uid = dict_data.get('uid', "")
        self.uname = dict_data.get('uname', "")
        self.update_datetime = dict_data.get('update_datetime', "")
        self.location = dict_data.get('location', "")
        self.start_time = dict_data.get('start_time', "")
        self.end_time = dict_data.get('end_time', "")
        self.date = dict_data.get('date', "")
        self.code = dict_data.get('code', "")
        self.sids= dict_data.get('sids', "")
        return self

    def get_dict_form_data(self):
        return {
            "seid": self.seid,
            "sename": self.sename,
            "bid": self.bid,
            "bname": self.bname,
            "uid": self.uid,
            "uname": self.uname,
            "update_datetime": self.update_datetime,
            "location": self.location,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "date": self.date,
            "code": self.code,
            "sids": self.sids
        }

# 스케쥴 번들
class ScheduleBundle(SampleDomain):
    def __init__(self, sbid="", sbname="", bid="",
                 bname="", uid="", uname="",
                 update_datetime="", code="", sids=None):
        self.sbid: str = sbid                # Schedule bundle ID
        self.sbname: str = sbname            # Schedule bundle name
        self.bid: str = bid                  # Bias ID
        self.bname: str = bname              # Bias name
        self.uid: str = uid                  # Maker's ID
        self.uname: str = uname              # Maker's name
        self.update_datetime: str = update_datetime  # Update time
        self.code: str = code                # Bundle code
        self.sids: list = sids if sids is not None else []  # List of schedule IDs

    def make_with_dict(self, dict_data:dict):
        self.sbid = dict_data.get('sbid', "")
        self.sbname = dict_data.get('sbname', "")
        self.bid = dict_data.get('bid', "")
        self.bname = dict_data.get('bname', "")
        self.uid = dict_data.get('uid', "")
        self.uname = dict_data.get('uname', "")
        self.update_datetime = dict_data.get('update_datetime', "")
        self.code = dict_data.get('code', "")
        self.sids = dict_data.get('sids', [])
        return self

    def get_dict_form_data(self):
        return {
            "sbid": self.sbid,
            "sbname": self.sbname,
            "bid": self.bid,
            "bname": self.bname,
            "uid": self.uid,
            "uname": self.uname,
            "update_datetime": self.update_datetime,
            "code": self.code,
            "sids": self.sids
        }
    
class Schedule(SampleDomain):
    def __init__(self, sid="", sname="", uid="", uname="",
                 bid="", bname="", date="", start_time="",
                 end_time="", location="", code="", update_datetime="",
                 num_usage=0, state=True
                 ):
        self.sid:str = sid                          # schedule id
        self.sname:str = sname                      # schedule name
        self.uid:str = uid                          # maker's id
        self.uname:str = uname                      # maker's name
        self.bid:str = bid                          # target bias
        self.bname:str = bname                      # target bias's name
        self.date:str = date                        # 시작 날짜
        self.start_time:str = start_time            # 시작 시간 
        self.end_time:str = end_time                # 종료 시간
        self.location:str = location                # 시작 장소
        self.code:str = code                        # 스케줄 코드
        self.update_datetime:str = update_datetime  # 등록된 시간
        self.num_usage:int = num_usage              # 추가된 횟수
        self.state:bool = state
    
    def make_with_dict(self, dict_data:dict):
        self.sid = dict_data.get('sid', "")
        self.sname = dict_data.get('sname', "")
        self.uid = dict_data.get('uid', "")
        self.uname = dict_data.get('uname', "")
        self.bid = dict_data.get('bid', "")
        self.bname = dict_data.get('bname', "")
        self.date = dict_data.get('date', "")
        self.start_time = dict_data.get('start_time', "")
        self.end_time = dict_data.get('end_time', "")
        self.location = dict_data.get('location', "")
        self.code = dict_data.get('code', "")
        self.update_datetime = dict_data.get('update_datetime', "")
        self.num_usage = dict_data.get('num_usage', 0)  # 기본값 0 설정
        self.state:bool = dict_data.get('state', "")
        return self

    def get_dict_form_data(self):
        return {
            "sid": self.sid,
            "sname": self.sname,
            "uid": self.uid,
            "uname": self.uname,
            "bid": self.bid,
            "bname": self.bname,
            "date": self.date,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "location": self.location,
            "code": self.code,
            "update_time": self.update_datetime,
            "num_usage": self.num_usage,
            "state":self.state
        }

    

class User(SampleDomain):
    def __init__(self, uid = "", uname = "지지자", age=0, 
                 email = "", gender = "d" ,
                 credit = 0, bids=[], num_long_feed=0, num_short_feed=0, num_comment=0,
                 password = "", alert= [], like=[], my_comment=[],
                 my_feed = [], active_feed = [], feed_history = [],
                 feed_search_history=[], level = 3):

        self.uid = uid
        self.uname = uname
        self.age = age
        self.email = email
        self.password = password
        self.gender = gender
        self.bids:list = copy.copy(bids)
        self.credit = credit
        self.num_long_feed:int = num_long_feed
        self.num_short_feed:int = num_short_feed
        self.num_comment:int = num_comment
        self.level:int = level

        self.alert:list = copy.copy(alert)
        self.like:list = copy.copy(like)
        self.my_comment:list = copy.copy(my_comment)
        self.my_feed:list = copy.copy(my_feed)
        self.active_feed:list = copy.copy(active_feed)      # interaction 한 Feed
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
            self.bids = copy.copy(dict_data['bids'])
            self.credit= dict_data['credit']
            self.num_long_feed = dict_data['num_long_feed']
            self.num_short_feed = dict_data['num_short_feed']
            self.num_comment = dict_data['num_comment']
            self.level = dict_data['level']

            self.alert = copy.copy(dict_data['alert'])
            self.like = copy.copy(dict_data["like"])
            self.my_comment = copy.copy(dict_data["my_comment"])
            self.my_feed = copy.copy(dict_data["my_feed"])
            self.active_feed = copy.copy(dict_data["active_feed"])
            self.feed_history = copy.copy(dict_data["feed_history"])
            self.feed_search_history = copy.copy(dict_data["feed_search_history"])
            return self
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
            "credit" : self.credit,
            "bids" : copy.copy(self.bids),
            "num_long_feed" : self.num_long_feed,
            "num_short_feed" : self.num_short_feed,
            "num_comment" : self.num_comment,
            "level" : self.level,

            "alert" : copy.copy(self.alert),
            "like" : copy.copy(self.like),
            "my_comment" : copy.copy(self.my_comment),
            "my_feed" : copy.copy(self.my_feed),
            "active_feed" : copy.copy(self.active_feed),
            "feed_history" : copy.copy(self.feed_history),
            "feed_search_history" : copy.copy(self.feed_search_history)
        }

class Bias(SampleDomain):
    def __init__(self, bid="",bname="", category=[], birthday="", debut="",
                 agency="", group=[], num_user=0, x_account="",
                 insta_account="", tiktok_account="", youtube_account="", homepage="",
                 fan_cafe="", country=[], fanname = [], board_types=["선택없음", "자유게시판", "팬아트", "유머게시판"]):
        self.bid = bid
        self.bname = bname
        self.category = copy.copy(category)
        self.birthday = birthday
        self.debut = debut
        self.agency = agency
        self.group = copy.copy(group)
        self.num_user = num_user
        self.board_types = board_types
        self.x_account = x_account
        self.insta_account = insta_account
        self.tiktok_account = tiktok_account
        self.youtube_account = youtube_account
        self.homepage = homepage
        self.fan_cafe = fan_cafe
        self.country = copy.copy(country)
        self.fanname = copy.copy(fanname)

    def make_with_dict(self, dict_data):
        try:
            self.bid = dict_data['bid']
            self.bname = dict_data['bname']
            self.category = copy.copy(dict_data['category'])
            self.birthday = dict_data['birthday']
            self.debut = dict_data['debut']
            self.agency = dict_data['agency']
            self.group = copy.copy(dict_data['group'])
            self.num_user = dict_data['num_user']
            self.board_types = copy.copy(dict_data['board_types'])
            self.x_account = dict_data['x_account']
            self.insta_account = dict_data['insta_account']
            self.tiktok_account = dict_data['tiktok_account']
            self.youtube_account = dict_data['youtube_account']
            self.homepage = dict_data['homepage']
            self.fan_cafe = dict_data['fan_cafe']
            self.country = copy.copy(dict_data['country'])
            self.fanname = copy.copy(dict_data['fanname'])
        except Exception as e:
            print(e)
            raise DictMakingError(error_type=e)
        finally:
            return self

    def get_dict_form_data(self):
        return {
            "bid": self.bid,
            "bname": self.bname,
            "category": copy.copy(self.category),
            "birthday": self.birthday,
            "debut": self.debut,
            "agency": self.agency,
            "group": copy.copy(self.group),
            "num_user": self.num_user,
            "board_types": copy.copy(self.board_types),
            "x_account": self.x_account,
            "insta_account": self.insta_account,
            "tiktok_account": self.tiktok_account,
            "youtube_account": self.youtube_account,
            "homepage": self.homepage,
            "fan_cafe": self.fan_cafe,
            "country": copy.copy(self.country),
            'fanname':copy.copy(self.fanname),
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
            return self
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
    def __init__(self, fid="", uid="", body="", fclass="", date="",
                 display=4, star=0, board_type="", image=None, hashtag=None,
                 comment=None, iid="", lid="", bid="", raw_body ="", p_body=""):
        if image is None:
            image = []
        if hashtag is None:
            hashtag = []
        if comment is None:
            comment = []
            
        self.fid = fid
        self.uid = uid
        self.body = body
        self.fclass = fclass
        # 디스플레이 옵션
        #   0 : 삭제
        #   1 : 비공개
        #   2 : 차단
        #   3 : 댓글 작성 비활성화
        #   4 : 전체 공개
        self.display = display
        self.date = date
        self.star = star
        self.board_type = board_type
        self.image = copy.copy(image)
        self.hashtag = copy.copy(hashtag)
        self.comment = copy.copy(comment)
        self.iid = iid  # interaction id
        self.lid = lid  # link id
        self.bid = bid  # bias id
        self.raw_body = raw_body
        self.reworked_body = ""
        self.level = 0
        self.p_body = p_body

        self.num_comment = len(self.comment)
        self.num_image = len(self.image)
        self.star_flag = False
        self.nickname = ""
        self.is_owner = False
        self.is_reworked = False


    def make_with_dict(self, dict_data):
        try:
            self.fid = dict_data["fid"]
            self.uid = dict_data["uid"]
            self.body = dict_data["body"]
            self.fclass = dict_data["fclass"]
            self.display = dict_data["display"]
            self.date = dict_data["date"]
            self.star = dict_data["star"]
            self.board_type = dict_data["board_type"]
            self.image = copy.copy(dict_data["image"])
            self.hashtag = copy.copy(dict_data["hashtag"])
            self.comment = copy.copy(dict_data["cid"])
            self.iid = dict_data["iid"]
            self.lid = dict_data["lid"]
            self.bid = dict_data["bid"]
            self.raw_body = dict_data["raw_body"]
            self.reworked_body = dict_data["reworked_body"]
            self.level = dict_data["level"]
            self.p_body = dict_data["p_body"]

            self.num_comment = len(self.comment)
            self.num_image = len(self.image)
            self.star_flag = False
            self.nickname = ""
            return self
        except KeyError as e:
            print(e)
            raise DictMakingError(error_type=f"Missing key: {str(e)}")

    def get_dict_form_data(self):
        return {
            "fid": self.fid,
            "uid": self.uid,
            "body": self.body,
            "fclass": self.fclass,
            "display": self.display,
            "date" : self.date,
            "star": self.star,
            "board_type" :self.board_type,
            "image": copy.copy(self.image),
            "hashtag": copy.copy(self.hashtag),
            "cid": copy.copy(self.comment),
            "iid": self.iid,
            "lid": self.lid,
            "bid": self.bid,
            "raw_body" : self.raw_body,
            "reworked_body" :self.reworked_body,
            "level" : self.level,
            "p_body": self.p_body,

            "num_comment":self.num_comment,
            "num_image":self.num_image,
            "star_flag":self.star_flag,
            "nickname" : self.nickname,
            "is_owner" : self.is_owner,
            "is_reworked" : self.is_reworked
        }

class Interaction(SampleDomain):
    def __init__(self, iid="", fid="", choice=[],
                 attend=[]):
        self.iid=iid
        self.fid=fid
        self.choice=choice
        self.attend=attend  # 2차원배열

        self.num_choice = len(self.choice)
        self.result = [len(sublist) for sublist in self.attend] # 참여자 수

        self.my_attend = -1  # 내가 선택한 정보 (-1 이면 참여 안한거임)

    def make_with_dict(self, dict_data):
        try:
            self.iid = dict_data['iid']
            self.fid = dict_data['fid']
            self.choice = copy.copy(dict_data["choice"])
            self.attend = copy.copy(dict_data["attend"])
            self.num_choice = len(self.choice)
            self.result = [len(sublist) for sublist in self.attend] # 참여자 수
            return self
        except Exception as e:
            raise DictMakingError(error_type=e)

    def get_dict_form_data(self):
        return {
            "iid":self.iid,
            "fid":self.fid,
            "choice":self.choice,
            "result":self.result,
            "attend":self.attend,
            "num_choice":self.num_choice,
            "my_attend":self.my_attend,
        }

class FeedLink(SampleDomain):
    def __init__(self, lid="", explain="", url="", domain="", title="", fid=""):
        self.lid = lid
        self.explain = explain
        self.url = url 
        self.domain = domain
        self.title = title
        self.fid = fid

    def make_with_dict(self, dict_data):
        try:
            self.lid = dict_data['lid']
            self.explain= dict_data['explain']
            self.url = dict_data['url']
            self.domain = dict_data['domain']
            self.title= dict_data['title']
            self.fid = dict_data['fid']
            return self
        except Exception as e:
            raise DictMakingError(error_type=e)

    def get_dict_form_data(self):
        return {
            "lid": self.lid,
            "explain": self.explain,
            "url": self.url,
            "domain" : self.domain,
            "title" : self.title,
            "fid" : self.fid
        }

class Banner(SampleDomain):
    def __init__(self, baid="", ba_url=""):
        self.baid = baid
        self.ba_url = ba_url

    def make_with_dict(self, dict_data):
        try:
            self.baid = dict_data['baid']
            self.ba_url = dict_data['ba_url']
            return self
        except Exception as e:
            raise DictMakingError(error_type=e)

    def get_dict_form_data(self):
        return {
            "baid": self.baid,
            "ba_url": self.ba_url
        }

class Comment(SampleDomain):
    def __init__(self, cid="", fid="", uid="", uname="", display=4, reply=[],
                 body="", date="", like=0, state="y", like_user=[], mention="",
                 target_cid="", level = 2, reworked_body =""
                 ):
        self.cid = cid
        self.fid = fid
        self.uid = uid
        # 디스플레이 옵션
        #   0 : 삭제
        #   1 : 비공개
        #   2 : 차단
        #   3 : 댓글 작성 비활성화
        #   4 : 전체 공개
        self.display = display
        self.reply = []      # 대댓글을 담는 공간
        self.uname = uname
        self.body = body
        self.date = date
        self.like = like
        self.state = state
        self.like_user:list = copy.copy(like_user)
        self.num_like_user = len(self.like_user)
        self.target_cid = target_cid            # 대댓글을 달 위치 cid
        self.owner = False
        self.mention = mention
        
        self.reworked_body = reworked_body
        self.level=level
        self.is_reworked = False

    def make_with_dict(self, dict_data):
        try:
            self.cid = dict_data['cid']
            self.fid = dict_data['fid']
            self.uid = dict_data['uid']
            self.uname = dict_data['uname']
            self.display = dict_data['display']
            self.body = dict_data['body']
            self.date = dict_data['date']
            self.like = dict_data['like']
            self.state = dict_data['state']
            self.like_user= copy.copy(dict_data['like_user'])
            self.target_cid = dict_data['target_cid']
            self.owner = dict_data['owner']
            self.mention = dict_data['mention']
            
            self.reworked_body = dict_data['reworked_body']
            self.level = dict_data['level']
            return self
        except KeyError as e:
            raise DictMakingError(error_type=f"Missing key: {str(e)}")

    def get_dict_form_data(self):
        return {
            "cid": self.cid,
            "fid": self.fid,
            "uid": self.uid,
            "display": self.display,
            "uname": self.uname,
            "body": self.body,
            "date": self.date,
            "like": self.like,
            "state": self.state,
            "like_user": copy.copy(self.like_user),
            "target_cid": self.target_cid,
            "owner" : self.owner,
            "mention": self.mention,
            "reply":self.reply,
            
            "reworked_body" : self.reworked_body,
            "level" : self.level,
            "is_reworked" : self.is_reworked
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
            return self
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
            "active_feed" : copy.copy(self.active_feed),
            "feed_key" : self.feed_key,
            "comment_key" : self.comment_key
        }
        
class Report(SampleDomain):
    def __init__(self, rid="", type="", date="", cid="",
                 detail = "", fid="", uid="",
                 result=False, aid_date=""):
        self.rid = rid 
        self.type = type
        self.date = date
        self.cid = cid 
        self.fid = fid
        self.uid = uid
        self.detail = detail  # 자세한 내용
        self.result:bool = result  # 결과
        self.aid_date =aid_date

    def make_with_dict(self, dict_data):
        try:
            self.rid = dict_data['rid']
            self.type= dict_data['type']
            self.date = dict_data['date']
            self.cid = dict_data['cid']
            self.fid = dict_data['fid']
            self.uid = dict_data['uid']
            self.detail = dict_data['detail']
            self.result = dict_data['result']
            self.aid_date = dict_data['aid_date']
            return self
        except KeyError as e:
            raise DictMakingError(error_type=f"Missing key: {str(e)}")

    def get_dict_form_data(self):
        return {
            "rid" : self.rid,
            "type" : self.type,
            "date" : self.date,
            "cid" : self.cid,
            "fid" : self.fid,
            "uid" : self.uid,
            "detail" :self.detail,
            "result" : self.result,
            "aid_date" : self.aid_date
        }
        
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
            return self
        except KeyError as e:
            raise DictMakingError(error_type=f"Missing key: {str(e)}")

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
            return self
        except KeyError as e:
            raise DictMakingError(error_type=f"Missing key: {str(e)}")
        return

    def get_dict_form_data(self):
        return {
            "nid" : self.nid,
            "date" : self.date,
            "title" : self.title,
            "body" : self.body,
        }
    
class Project:
    def __init__(self, pid="", pname="", uid="", uname="", user_info="",
                 make_date="", expire_date="", head_image=[], body_url="",
                 now_progress=0, goal_progress=0, ptype = "", ftype="", introduce="",
                 num_participants=0,
                 ):
        self.pid = pid
        self.pname = pname
        self.uid = uid
        self.uname = uname
        self.user_info = user_info
        self.make_date = make_date
        self.expire_date = expire_date
        self.head_image = head_image
        self.body_url = body_url
        self.now_progress = now_progress
        self.goal_progress = goal_progress
        self.int_progress = 0 # 이건 달성 퍼센트임
        self.ptype = ptype
        self.ftype = ftype
        self.introduce = introduce
        self.num_participants = num_participants

        # 아마 밑에 추가될 내용은 결제 관련인데
        # 결제는 걍 미침... 새로 데이터 도메인 파는게 답임
        # 최애 펀딩인지 덕질 펀딩인지 구분하는거랑
        # 후원 펀딩인지 참여 펀딩인지 구분도 해야됨

    def make_with_dict(self, dict_data):
        try:
            self.pid = dict_data['pid']
            self.pname = dict_data['pname']
            self.uid = dict_data['uid']
            self.uname = dict_data['uname']
            self.user_info = dict_data['user_info']
            self.make_date = dict_data['make_date']
            self.expire_date = dict_data['expire_date']
            self.head_image = copy.copy(dict_data['head_image'])
            self.body_url = dict_data['body_url']
            self.now_progress = dict_data['now_progress']
            self.goal_progress = dict_data['goal_progress']
            self.ptype = dict_data['ptype']
            self.ftype = dict_data['ftype']
            self.introduce = dict_data['introduce']
            self.num_participants = dict_data['num_participants']
            return self
        except KeyError as e:
            raise DictMakingError(error_type=f"Missing key: {str(e)}")

    def get_dict_form_data(self):
        return {
            "pid": self.pid,
            "pname": self.pname,
            "uid": self.uid,
            "uname": self.uname,
            "user_info": self.user_info,
            "make_date": self.make_date,
            "expire_date": self.expire_date,
            "head_image": copy.copy(self.head_image),
            "body_url": self.body_url,
            "now_progress": self.now_progress,
            "goal_progress": self.goal_progress,
            "int_progress" : self.int_progress,
            "ptype" : self.ptype,
            "ftype" : self.ftype,
            "introduce" : self.introduce,
            "num_participants":self.num_participants
        }

class ProjectSales:
    def __init__(self, psid="", pid="", psname="", price=0, detail=None,
                 quantity=0, num_sales=0, tags=None):
        if detail is None:
            detail = []
        if tags is None:
            tags = []
        self.psid = psid
        self.pid = pid
        self.psname = psname
        self.price = price
        self.detail:list = copy.copy(detail)
        self.quantity = quantity
        self.num_sales = num_sales
        self.tags:list = copy.copy(tags)

    def make_with_dict(self, dict_data):
        try:
            self.psid = dict_data['psid']
            self.pid = dict_data['pid']
            self.psname = dict_data['psname']
            self.price = dict_data['price']
            self.detail:list = copy.copy(dict_data['detail'])
            self.quantity = dict_data['quantity']
            self.num_sales = dict_data['num_sales']
            self.tags:list = copy.copy(dict_data['tags'])
            return self
        except KeyError as e:
            raise ValueError(f"Missing key: {str(e)}")

    def __call__(self):
        print(f"psid: {self.psid}")
        print(f"pid: {self.pid}")
        print(f"psname: {self.psname}")
        print(f"price: {self.price}")
        print(f"detail: {self.detail}")
        print(f"quantity: {self.quantity}")
        print(f"num_sales: {self.num_sales}")
        print(f"tags: {self.tags}")

    def get_dict_form_data(self):
        return {
            "psid": self.psid,
            "pid": self.pid,
            "psname": self.psname,
            "price": self.price,
            "detail": copy.copy(self.detail),
            "quantity": self.quantity,
            "num_sales": self.num_sales,
            "tags": copy.copy(self.tags)
        }
    
class ProjectPurchase:
    def __init__(self, ppid="", pid="", psid="", uid="",
                 count=0, total=0, unit_price=0, purchase_date=""
                 ):
        self.ppid = ppid
