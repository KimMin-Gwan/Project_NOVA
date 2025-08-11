from model.base_model import AdminModel
from model import Local_Database
from others.data_domain import League, User, Bias, Banner, NameCard, Feed, Comment
from others import CoreControllerLogicError, FeedManager, FeedSearchEngine
import string, random
import boto3
import datetime
import uuid
import time

class BiasEditorModel(AdminModel):
    def __init__(self, database:Local_Database) -> None:
        super().__init__(database)
        self.__bias = Bias()

    def load_bias(self, bid):
        bias_data = self._database.get_data_with_id(target="bid", id=bid)
        self.__bias.make_from_data(bias_data)
        return

    def set_bias_data(self, body_data):
        if not body_data.bid : pass
        else : self.__bias.bid = body_data.bid
        if not body_data.bname : pass
        else : self.__bias.bname = body_data.bname
        if not body_data.gender : pass
        else : self.__bias.gender = body_data.gender
        if not body_data.category : pass
        else : self.__bias.category = body_data.category
        if not body_data.birthday : pass
        else : self.__bias.birthday = body_data.birthday
        if not body_data.debut : pass
        else : self.__bias.debut = body_data.debut
        if not body_data.agency : pass
        else :self.__bias.agency = body_data.agency
        if not body_data.group : pass
        else : self.__bias.group = body_data.group
        if not body_data.num_user : pass
        else : self.__bias.num_user = body_data.num_user
        if not body_data.board_types : pass
        else : self.__bias.board_types = body_data.board_types

        if not body_data.x_account : pass
        else : self.__bias.x_account = body_data.x_account
        if not body_data.insta_account : pass
        else : self.__bias.insta_account = body_data.insta_account
        if not body_data.tiktok_account : pass
        else : self.__bias.tiktok_account = body_data.tiktok_account
        if not body_data.youtube_account : pass
        else : self.__bias.youtube_account = body_data.youtube_account
        if not body_data.homepage : pass
        else : self.__bias.homepage = body_data.homepage
        if not body_data.fan_cafe : pass
        else : self.__bias.fan_cafe = body_data.fan_cafe
        if not body_data.country : pass
        else : self.__bias.country = body_data.country
        if not body_data.fanname : pass
        else : self.__bias.fanname = body_data.fanname

    def add_bias(self):
        num_bias = str(self._database.get_num_list_with_id(target_id='bid'))
        bid = f'{num_bias}'
        if self._database.get_data_with_id(target="bid", id=bid):
            return
        self._database.add_new_data(target_id="bid", new_data=self.__bias.get_data_form_data())

    def modify_bias(self):
        self._database.modify_data_with_id(target_id="bid", target_data=self.__bias.get_data_form_data())

    def delete_bias(self, bid):
        self._database.delete_data_with_id(target="bid", id=bid)

    def get_response_form_data(self, head_parser):
        try:
            body = {
                'response' : self.__bias.get_data_form_data()
            }
            response = self._get_response_data(head_parser=head_parser, body=body)
            return response

        except Exception as e:
            raise CoreControllerLogicError("response making error | " + e)

class UserEditorModel(AdminModel):
    def __init__(self, database:Local_Database) -> None:
        super().__init__(database)
        self.__user = User()

    def load_user(self, target, target_type):
        user_data = self._database.get_data_with_key(target_id="uid", key=target_type, key_data=target)
        self.__user.make_from_data(user_data)
        return

    def set_user_data(self, body_data):
        if not body_data.uname : pass
        else : self.__user.uname = body_data.uname
        if not body_data.uid: pass
        else : self.__user.uid = body_data.uid
        if not body_data.age: pass
        else : self.__user.age = body_data.age
        if not body_data.email: pass
        else : self.__user.email = body_data.email
        if not body_data.password: pass
        else : self.__user.password = body_data.password
        if not body_data.gender: pass
        else : self.__user.gender = body_data.gender
        if not body_data.bids: pass
        else : self.__user.bids = body_data.bids
        if not body_data.credit: pass
        else : self.__user.credit = body_data.credit
        if not body_data.num_long_feed: pass
        else : self.__user.num_long_feed = body_data.num_long_feed
        if not body_data.num_short_feed: pass
        else : self.__user.num_short_feed = body_data.num_short_feed
        if not body_data.level: pass
        else : self.__user.level = body_data.level
        if not body_data.alert: pass
        else : self.__user.alert = body_data.alert
        if not body_data.like: pass
        else : self.__user.like = body_data.like
        if not body_data.my_comment: pass
        else : self.__user.my_comment = body_data.my_comment
        if not body_data.my_feed: pass
        else : self.__user.my_feed = body_data.my_feed
        if not body_data.active_feed: pass
        else : self.__user.active_feed = body_data.active_feed
        if not body_data.feed_history: pass
        else : self.__user.feed_history = body_data.feed_history
        if not body_data.feed_searce_history: pass
        else : self.__user.feed_search_history = body_data.feed_search_history

    def __make_uid(self):
        uid = ""
        while True:
            uid = self.__generate_uid()
            if not self._database.get_data_with_id(target="uid", id=uid):
                break
        return uid

    def __generate_uid(self):
        uid = str(uuid.uuid4())
        # uuid4()는 형식이 "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"인 UUID를 생성합니다.
        # 이를 "1234-abcd-5678" 형태로 변형하려면 일부 문자만 선택하여 조합합니다.
        uid_parts = uid.split('-')
        return f"{uid_parts[0][:4]}-{uid_parts[1][:4]}-{uid_parts[2][:4]}"

    def add_user(self):
        self.__user.uid = self.__make_uid()
        self._database.add_new_data(target_id="uid", new_data=self.__user.get_data_form_data())
        return

    def modify_user(self):
        self._database.modify_data_with_id(target_id="uid", target_data=self.__user.get_data_form_data())
        return

    # 회원탈퇴 기능은 User_deleted 옵션을 추가해볼까 싶은데

    def delete_user(self, uid):
        deleted_user_data = self._database.get_data_with_id(target="uid", id=uid)
        deleted_user = User().make_from_data(deleted_user_data)

        cleaned_user = User(uid=deleted_user.uid, uname="탈퇴한유저")

        # 유저 데이터를 덮어씌워서 UID만 남김
        self._database.modify_data_with_id(target_id="uid", target_data=cleaned_user.get_data_form_data())

        # 삭제된 유저는 다른 DB로 저장됩니다. UID, 닉네임, 개인 정보 등을 저장합니다. (추후에 쓰입니다.)
        self._database.add_new_data(target_id="duid", new_data=self.__user.get_data_form_data())
        return



    def get_response_form_data(self, head_parser):
        try:
            body = {
                'response' : self.__bias.get_data_form_data()
            }
            response = self._get_response_data(head_parser=head_parser, body=body)
            return response

        except Exception as e:
            raise CoreControllerLogicError("response making error | " + e)

# 운영자의 Feed는 따로 관리되어야 합니다.
# 그 이유는.. 기존 사용자와의 동일한 Feed 작동방식을 취하면 위험하다고 판단
class FeedEditorModel(AdminModel):
    def __init__(self, database:Local_Database) -> None:
        super().__init__(database)
        self.__feed = Feed()
        self.__comment = Comment()

    def load_feed(self, fid):
        feed_data = self._database.get_data_with_id(target="fid", id=fid)
        self.__feed.make_from_data(feed_data)
        return

    def load_comment(self, cid):
        comment_data = self._database.get_data_with_id(target="cid", id=cid)
        self.__comment.make_from_data(comment_data)
        return

    def set_feed_data(self, body_data):
        if not body_data.fid: pass
        else : self.__feed.fid = body_data.fid
        if not body_data.uid: pass
        else : self.__feed.uid = body_data.uid
        if not body_data.body: pass
        else : self.__feed.body = body_data.body
        if not body_data.fclass: pass
        else : self.__feed.fclass = body_data.fclass
        if not body_data.display: pass
        else : self.__feed.display = body_data.display
        if not body_data.date: pass
        else : self.__feed.date = body_data.date
        if not body_data.star: pass
        else : self.__feed.star = body_data.star
        if not body_data.board_type: pass
        else : self.__feed.board_type = body_data.board_type
        if not body_data.image: pass
        else : self.__feed.image = body_data.image
        if not body_data.hashtag: pass
        else : self.__feed.hashtag = body_data.hashtag
        if not body_data.comment: pass
        else : self.__feed.comment = body_data.comment
        # if not body_data.iid: pass
        # else : self.__feed.iid = body_data.iid
        if not body_data.lid: pass
        else : self.__feed.lid = body_data.lid
        if not body_data.bid: pass
        else : self.__feed.bid = body_data.bid
        if not body_data.raw_body: pass
        else : self.__feed.raw_body = body_data.raw_body
        if not body_data.reworked_body: pass
        else : self.__feed.reworked_body = body_data.reworked_body
        if not body_data.level : pass
        else : self.__feed.level = body_data.level
        if not body_data.p_body: pass
        else : self.__feed.p_body = body_data.p_body

    def __make_fid(self):
        random_string = "default"
        while True:
            # 사용할 문자들: 대문자, 소문자, 숫자
            characters = string.ascii_letters + string.digits
            # 8자리 랜덤 문자열 생성
            random_string = ''.join(random.choice(characters) for _ in range(6))

            fid = "admin"+"-"+random_string
            if not self._database.get_data_with_id(target="fid", id=fid):
                break
        return fid

    def add_feed(self):
        self.__feed.fid = str(self._database.get_num_list_with_id(target_id="fid")+1)
        self._database.add_new_data(target_id="fid", new_data=self.__feed.get_data_form_data())
        return

    def modify_feed(self):
        self._database.modify_data_with_id(target_id="fid", target_data=self.__feed.get_data_form_data())
        return

    def delete_feed(self):
        self.__feed.display = 0
        self.modify_feed()
        return

    def set_private_feed(self):
        self.__feed.display = 1
        self.modify_feed()
        return

    def set_block_feed(self):
        self.__feed.display = 2
        self.modify_feed()
        return

    def set_unblock_feed(self):
        self.__feed.display = 4
        self.modify_feed()
        return

    def delete_comment(self):
        self.__comment.display = 0
        self._database.modify_data_with_id(target_id="cid", target_data=self.__comment.get_data_form_data())

    def set_block_comment(self):
        self.__comment.display = 2
        self._database.modify_data_with_id(target_id="cid", target_data=self.__comment.get_data_form_data())

    def set_unblock_comment(self):
        self.__comment.display = 4
        self._database.modify_data_with_id(target_id="cid", target_data=self.__comment.get_data_form_data())


    def get_response_form_data(self, head_parser):
        try:
            body = {
                'response' : self.__bias.get_data_form_data()
            }
            response = self._get_response_data(head_parser=head_parser, body=body)
            return response

        except Exception as e:
            raise CoreControllerLogicError("response making error | " + e)

class NameCardEditorModel(AdminModel):
    def __init__(self, database: Local_Database) -> None:
        super().__init__(database)
        self.__namecard = NameCard()

    def load_namecard(self, ncid): #load
        namecard_data = self._database.get_data_with_id(target='ncid', id=ncid)
        self.__namecard.make_with_dict(namecard_data)
        return

    def set_namecard_data(self, body_data):
        if not body_data.ncid : pass
        else : self.__namecard.ncid = body_data.ncid
        if not body_data.ncname : pass
        else : self.__namecard.ncname = body_data.ncname
        if not body_data.nccredit : pass
        else : self.__namecard.nccredit = body_data.nccredit

    def add_namecard(self): #add
        self.__namecard.ncid = str(self._database.get_num_list_with_id(target_id='ncid')+1)
        self._database.add_new_data(target_id='ncid',new_data=self.__namecard.get_dict_form_data())
        return

    def modify_namecard(self):
        self._database.modify_data_with_id(target_id='ncid',target_data=self.__namecard.get_dict_form_data())
        return

    def delete_namecard(self, ncid):
        self._database.delete_data_With_id(target='ncid',id=ncid)

    def get_response_form_data(self, head_parser):
        try:
            body = {
                'response' : self.__namecard.get_dict_form_data()
            }

            response = self._get_response_data(head_parser=head_parser, body=body)
            return response

        except Exception as e:
            raise CoreControllerLogicError("response making error | " + e)