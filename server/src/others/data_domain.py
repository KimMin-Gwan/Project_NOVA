from typing import Any, List
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

    
class Schedule(SampleDomain):
    def __init__(self, sid="", sname="", uid="", uname="",
                 bid="", bname="", start_date="", end_date="", start_time="",
                 end_time="", platform=[], code="", update_datetime="",
                 num_usage=0, state=True, color_code="", tags=[], url=""
                 ):
        self.sid:str = sid                          # schedule id
        self.sname:str = sname                      # schedule name
        self.uid:str = uid                          # maker's id
        self.uname:str = uname                      # maker's name
        self.bid:str = bid                          # target bias
        self.bname:str = bname                      # target bias's name
        self.start_date:str = start_date            # 시작 날짜
        self.start_time:str = start_time            # 시작 시간 
        self.end_date:str = end_date                # 종료 날짜
        self.end_time:str = end_time                # 종료 시간
        self.platform:list = copy.copy(platform)    # 송출 장소
        self.code:str = code                        # 스케줄 코드
        self.update_datetime:str = update_datetime  # 등록된 시간
        self.num_usage:int = num_usage              # 추가된 횟수
        self.state:bool = state                     # 공개 비공개 여부
        self.color_code = color_code                # 색깔 코드
        self.subscribe = False
        self.is_owner = False                       # 글쓴이 여부
        self.tags = tags
        self.url = url
    
    def make_with_dict(self, dict_data:dict):
        self.sid = dict_data.get('sid', "")
        self.sname = dict_data.get('sname', "")
        self.uid = dict_data.get('uid', "")
        self.uname = dict_data.get('uname', "")
        self.bid = dict_data.get('bid', "")
        self.bname = dict_data.get('bname', "")
        self.start_date = dict_data.get('start_date', "")
        self.start_time = dict_data.get('start_time', "")
        self.end_date = dict_data.get('end_date', "")
        self.end_time = dict_data.get('end_time', "")
        self.platform = copy.copy(dict_data.get('platform'))
        self.code = dict_data.get('code', "")
        self.update_datetime = dict_data.get('update_datetime', "")
        self.num_usage = dict_data.get('num_usage', 0)  # 기본값 0 설정
        self.state:bool = dict_data.get('state')
        self.color_code:str= dict_data.get('color_code', "")
        self.tags:list = dict_data.get('tags', [])
        self.url:list = dict_data.get('url', "")
        return self

    def get_dict_form_data(self):
        return {
            "sid": self.sid,
            "sname": self.sname,
            "uid": self.uid,
            "uname": self.uname,
            "bid": self.bid,
            "bname": self.bname,
            "start_date": self.start_date,
            "start_time": self.start_time,
            "end_date": self.end_date,
            "end_time": self.end_time,
            "platform": copy.copy(self.platform),
            "code": self.code,
            "update_datetime": self.update_datetime,
            "num_usage": self.num_usage,
            "state":self.state,
            "color_code": self.color_code,
            "subscribe" : self.subscribe,
            "is_owner" : self.is_owner,
            "tags" : self.tags,
            "url" : self.url
        }

    

class User(SampleDomain):
    def __init__(self, uid = "", uname = "지지자", birth_year=0, 
                 email = "", gender = "d" ,
                 bids=[], num_long_feed=0, num_comment=0,
                 password = "", like=[], my_comment=[],
                 my_feed = []):

        self.uid = uid
        self.uname = uname
        self.birth_year = birth_year
        self.email = email
        self.password = password
        self.gender = gender
        self.bids:list = copy.copy(bids)
        self.num_feed:int = num_long_feed
        self.num_comment:int = num_comment
        self.like:list = copy.copy(like)
        self.my_comment:list = copy.copy(my_comment)
        self.my_feed:list = copy.copy(my_feed)

    # database로 부터 받아온 데이터를 사용해 내용 구성
    def make_with_dict(self, dict_data:dict):
        try:
            self.uid = dict_data['uid']
            self.uname = dict_data['uname']
            self.birth_year= dict_data['birth_year']
            self.email= dict_data['email']
            self.password = dict_data['password']
            self.gender= dict_data['gender']
            self.bids = copy.copy(dict_data['bids'])
            self.num_feed = dict_data['num_long_feed']
            self.num_comment = dict_data.get("num_comment", len(self.my_comment))
            self.like = copy.copy(dict_data["like"])
            self.my_comment = copy.copy(dict_data["my_comment"])
            self.my_feed = copy.copy(dict_data["my_feed"])
            return self
        except Exception as e:
            print(e)
            raise DictMakingError(error_type=e)
    
    # response에 사용되는 json형태로 만들기 위한 dict 데이터
    def get_dict_form_data(self):
        return {
            "uid" : self.uid,
            "uname" : self.uname,
            "birth_year" : self.birth_year,
            "email" : self.email,
            "password" : self.password,
            "gender" : self.gender,
            "bids" : copy.copy(self.bids),
            "num_feed" : self.num_feed,
            "num_comment" : self.num_comment,
            "like" : copy.copy(self.like),
            "my_comment" : copy.copy(self.my_comment),
            "my_feed" : copy.copy(self.my_feed),
        }
        
        
class Bias(SampleDomain):
    def __init__(self, bid="", bname="", gender="", category=[], tags=[],
                 num_follower=0, platform=[], platform_url="https://supernova.io.kr",
                 state="DEFAULT", schedules = []
                 ):
        self.bid = bid
        self.bname = bname
        self.gender = gender
        self.category = copy.copy(category)
        self.tags = copy.copy(tags)
        self.num_follower = num_follower
        self.platform = copy.copy(platform)
        self.platform_url = platform_url
        self.state = state
        self.schedules = schedules

    def make_with_dict(self, dict_data: dict):
        try:
            self.bid = dict_data.get('bid', "")
            self.bname = dict_data.get('bname', "")
            self.gender = dict_data.get('gender', "")
            self.category = copy.copy(dict_data.get('category', []))
            self.tags = copy.copy(dict_data.get('tags', []))
            self.num_follower = dict_data.get('num_follower', 0)
            self.platform = copy.copy(dict_data.get("platform", []))
            self.state = dict_data.get("state", "DEFAULT")
            self.platform_url = dict_data.get("platform_url", "https://supernova.io.kr")
            self.schedules = copy.copy(dict_data.get('schedules', []))
            
        except Exception as e:
            print(e)
            raise DictMakingError(error_type=e)
        finally:
            return self

    def get_dict_form_data(self):
        return {
            "bid": self.bid,
            "bname": self.bname,
            "gender": self.gender,
            "category": copy.copy(self.category),
            "tags": copy.copy(self.tags),
            "num_follower": self.num_follower,
            "platform" : self.platform,
            "platform_url" : self.platform_url,
            "state" : self.state,
            "schedules" : copy.copy(self.schedules)
        }

class Feed(SampleDomain):
    def __init__(self, fid="", uid="", body="", date="",
                 display=4, like=0, board_type="", image=None, hashtag=None, bname="",
                 comment=None, lid="", bid="", raw_body =""):
        if image is None:
            image = []
        if hashtag is None:
            hashtag = []
        if comment is None:
            comment = []
            
        self.fid = fid
        self.uid = uid
        self.body = body
        # 디스플레이 옵션
        #   0 : 삭제
        #   1 : 비공개
        #   2 : 차단
        #   3 : 댓글 작성 비활성화
        #   4 : 전체 공개
        self.display = display
        self.date = date
        self.like = like
        self.board_type = board_type
        self.hashtag = copy.copy(hashtag)
        self.comment:List[str] = copy.copy(comment)
        self.lid = lid  # link id
        self.bid = bid  # bias id
        self.bname = bname
        self.raw_body = raw_body
        self.level = 0

        self.num_comment = len(self.comment)
        self.star_flag = False
        self.nickname = ""
        self.is_owner = False
        self.is_reworked = False


    def make_with_dict(self, dict_data:dict):
        try:
            self.fid = dict_data["fid"]
            self.uid = dict_data["uid"]
            self.body = dict_data["body"]
            self.display = dict_data["display"]
            self.date = dict_data["date"]
            self.like = dict_data["like"]
            self.board_type = dict_data["board_type"]
            self.hashtag = copy.copy(dict_data["hashtag"])
            self.comment = copy.copy(dict_data["cid"])
            self.lid = dict_data["lid"]
            self.bid = dict_data["bid"]
            self.raw_body = dict_data["raw_body"]
            self.level = dict_data["level"]
            self.bname = dict_data.get("bname", "")

            self.num_comment = len(self.comment)
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
            "display": self.display,
            "date" : self.date,
            "like": self.like,
            "board_type" :self.board_type,
            "hashtag": copy.copy(self.hashtag),
            "cid": copy.copy(self.comment),
            "lid": self.lid,
            "bid": self.bid,
            "raw_body" : self.raw_body,
            "level" : self.level,
            "bname" : self.bname,

            "num_comment":self.num_comment,
            "star_flag":self.star_flag,
            "nickname" : self.nickname,
            "is_owner" : self.is_owner,
            "is_reworked" : self.is_reworked
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
        self.is_reply = False
        
        self.reworked_body = reworked_body
        self.level=level
        self.is_reworked = False

    def make_with_dict(self, dict_data:dict):
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
            self.is_reply = dict_data.get('is_reply', False)
            
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
            "is_reply": self.is_reply,
            
            "reworked_body" : self.reworked_body,
            "level" : self.level,
            "is_reworked" : self.is_reworked
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
    