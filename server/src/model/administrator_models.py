from model.base_model import AdminModel
from model import Local_Database
from others.data_domain import League, User, Bias, Banner, NameCard, Item, Feed
from others import CoreControllerLogicError

import boto3
import datetime
import uuid

import time

class ResetDatasModel(AdminModel):
    def __init__(self, database:Local_Database) -> None:
        super().__init__(database)
        self.__response = 'failed'
    
        self.__users = []
        self.__biases = []
    #json파일 버킷에 업로드
    def upload_data(self):
        try:
            now = datetime.datetime.now()
            date = now.strftime('%Y-%m-%d')
            data = ['bias','user']
            for i in data:
                self._s3.upload_file(f'{self._path}{i}.json', f"nova-{i}", f"{i}{date}.json")
            return True
        
        except Exception as e:
            raise CoreControllerLogicError(error_type="upload_league_data | " + str(e))
    #유저 불러오기
    def set_users(self) -> bool: 
        try:
            user_data = self._database.get_all_data(target="user")

            if not user_data:
                return False

            for data in user_data:
                user = User()
                user.make_with_dict(data)
                self.__users.append(user)
            
            return True
        except Exception as e:
            raise CoreControllerLogicError(error_type="set_leagues | " + str(e))
    #bias 불러오기
    def set_biases(self) -> bool: 
        try:
            bias_data = self._database.get_all_data(target="bias")

            if not bias_data:
                return False

            for data in bias_data:
                bias = Bias()
                bias.make_with_dict(data)
                self.__biases.append(bias)
            
            return True
        except Exception as e:
            raise CoreControllerLogicError(error_type="set_leagues | " + str(e))
    #포인트랑 콤보 초기화 ( 함수 이름 변경 필요 )
    def reset_point(self) -> bool:
        try:
            if not self.__users:
                return False
            if not self.__biases:
                return False
            
            for user in self.__users:
                user.solo_point = 0
                user.group_point = 0
                user.solo_combo = 0
                user.group_combo = 0
                self._database.modify_data_with_id(target_id='uid',target_data=user.get_dict_form_data())
            
            for bias in self.__biases:
                bias.point  = 0
                self._database.modify_data_with_id(target_id='bid',target_data=bias.get_dict_form_data())

            self.__set_response()
            return True
        except Exception as e:
            raise CoreControllerLogicError(error_type="reset_point | " + str(e))
    
    def __set_response(self):
        self.__response = 'success'

    def reset_daily(self):
        try:
            if not self.__users:
                return False
            
            for user in self.__users:
                user.solo_daily = False
                user.group_daily = False
                self._database.modify_data_with_id(target_id='uid',target_data=user.get_dict_form_data())

            self.__set_response()
            return True
        except Exception as e:
            raise CoreControllerLogicError(error_type="reset_point | " + str(e))

    def get_response_form_data(self, head_parser):
        try:
            body = {
                'response' : self.__response
            }

            response = self._get_response_data(head_parser=head_parser, body=body)
            return response

        except Exception as e:
            raise CoreControllerLogicError("response making error | " + e)

class UserEditModel(AdminModel):
    def __init__(self, database: Local_Database) -> None:
        super().__init__(database)
        self.__user = User()

    def load_user(self,request,type): #load
        if type == 'uid':
            user_data = self._database.get_data_with_id(target='uid', id=request.uid)
        if type == 'email':
            user_data = self._database.get_data_with_key(target='uid',key='email',key_data=request.email)
        self.__user.make_with_dict(user_data)
        return 
        
    def set_user_data(self,request):
        #item = Item()
        if not request.uname : pass
        else : self.__user.uname = request.uname
        if not request.age : pass
        else : self.__user.age = request.age
        if not request.email : pass
        else : self.__user.email = request.email
        if not request.password : pass
        else : self.__user.password = request.password
        if not request.gender : pass
        else : self.__user.gender = request.gender
        if not request.solo_point : pass
        else : self.__user.solo_point = request.solo_point
        if not request.group_point : pass
        else : self.__user.group_point = request.group_point
        if not request.solo_combo : pass
        else : self.__user.solo_combo = request.solo_combo
        if not request.group_combo : pass
        else : self.__user.group_combo = request.group_combo
        if not request.credit : pass
        else : self.__user.credit = request.credit
        if not request.solo_bid : pass
        else : self.__user.solo_bid = request.solo_bid
        if not request.group_bid : pass
        else : self.__user.group_bid = request.group_bid

        #아이템 설정
        if not request.chatting : pass
        else : self.__user.item.chatting = request.chatting
        if not request.chatting : pass
        else : self.__user.item.saver = request.saver
        #self.__user.items = item

        if not request.solo_daily : pass
        else : self.__user.solo_daily = request.solo_daily
        if not request.solo_special : pass
        else : self.__user.solo_special = request.solo_special
        if not request.group_daily : pass
        else : self.__user.group_daily = request.group_daily
        if not request.group_special : pass
        else : self.__user.group_special = request.group_special
        if not request.sign : pass
        else : self.__user.sign = request.sign
        if not request.select_name_card : pass
        else : self.__user.select_name_card = request.select_name_card
        if not request.name_card_list : pass
        else : self.__user.name_card_list = request.name_card_list

    def add_user(self): #add
        self.__user.uid = self.__make_uid()
        
        self._database.add_new_data(target_id='uid',new_data=self.__user.get_dict_form_data())
        return

    def modify_user(self,request):
        self.__user.uid = request.uid
        self._database.modify_data_with_id(target_id='uid',target_data=self.__user.get_dict_form_data())
        return
    
    def delete_user(self,request):
        self._database.delete_data_With_id(target='uid',id=request.uid)
    
    def __generate_uid(self):
        uid = str(uuid.uuid4())
        # uuid4()는 형식이 "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"인 UUID를 생성합니다.
        # 이를 "1234-abcd-5678" 형태로 변형하려면 일부 문자만 선택하여 조합합니다.
        uid_parts = uid.split('-')
        return f"{uid_parts[0][:4]}-{uid_parts[1][:4]}-{uid_parts[2][:4]}"

    def __make_uid(self):
        uid = ""
        while True:
            uid = self.__generate_uid()
            if not self._database.get_data_with_id(target="uid", id=uid):
                break
        return uid
    
    def get_response_form_data(self, head_parser):
        try:
            body = {
                'response' : self.__user.get_dict_form_data()
            }

            response = self._get_response_data(head_parser=head_parser, body=body)
            return response

        except Exception as e:
            raise CoreControllerLogicError("response making error | " + e)

class NamecardEditModel(AdminModel):
    def __init__(self, database: Local_Database) -> None:
        super().__init__(database)
        self.__namecard = NameCard()

    def load_namecard(self,request): #load
        namecard_data = self._database.get_data_with_id(target='ncid', id=request.ncid)
        self.__namecard.make_with_dict(namecard_data)
        return 
        
    def set_namecard_data(self,request):
        if not request.ncid : pass
        else : self.__namecard.ncid = request.ncid
        if not request.ncname : pass
        else : self.__namecard.ncname = request.ncname
        if not request.nccredit : pass
        else : self.__namecard.nccredit = request.nccredit

    def add_namecard(self): #add
        self.__namecard.ncid = str(self._database.get_num_list_with_id(target_id='ncid')+1)
        self._database.add_new_data(target_id='ncid',new_data=self.__namecard.get_dict_form_data())
        return

    def modify_namecard(self):
        self._database.modify_data_with_id(target_id='ncid',target_data=self.__namecard.get_dict_form_data())
        return
    
    def delete_namecard(self,request):
        self._database.delete_data_With_id(target='ncid',id=request.ncid)

    def get_response_form_data(self, head_parser):
        try:
            body = {
                'response' : self.__namecard.get_dict_form_data()
            }

            response = self._get_response_data(head_parser=head_parser, body=body)
            return response

        except Exception as e:
            raise CoreControllerLogicError("response making error | " + e)

class LeagueEditmodel(AdminModel):
    def __init__(self, database: Local_Database) -> None:
        super().__init__(database)
        self.__league = League()

    def load_league(self,request): #load
        league_data = self._database.get_data_with_id(target='lid', id=request.lid)
        self.__league.make_with_dict(league_data)
        return 
        
    def set_league_data(self,request):
        if not request.lid : pass
        else : self.__league.lid = request.lid
        if not request.lname : pass
        else : self.__league.lname = request.lname
        if not request.bid_list : pass
        else : self.__league.bid_list = request.bid_list
        if not request.tier : pass
        else : self.__league.tier = request.tier
        if not request.num_bias : pass
        else :self.__league.num_bias = request.num_bias
        if not request.state : pass
        else :self.__league.state = request.state
        if not request.type : pass
        else : self.__league.type = request.type

    def add_league(self): #add
        self.__league.lid = '100'+str(self._database.get_num_list_with_id(target_id='lid')+1)
        self._database.add_new_data(target_id='lid',new_data=self.__league.get_dict_form_data())
        return

    def modify_league(self):
        self._database.modify_data_with_id(target_id='lid',target_data=self.__league.get_dict_form_data())
        return
    
    def delete_league(self,request):
        self._database.delete_data_With_id(target='lid',id=request.lid)
    
    def get_response_form_data(self, head_parser):
        try:
            body = {
                'response' : self.__league.get_dict_form_data()
            }

            response = self._get_response_data(head_parser=head_parser, body=body)
            return response

        except Exception as e:
            raise CoreControllerLogicError("response making error | " + e)

class FeedEditModel(AdminModel):
    def __init__(self, database: Local_Database) -> None:
        super().__init__(database)
        self.__feed = Feed()

    def load_feed(self,request): #load
        feed_data = self._database.get_data_with_id(target='fid', id=request.fid)
        self.__feed.make_with_dict(feed_data)
        #self._database.delete_data_With_id(target='cid', id=request.cid) #삭제 만든거 테스트용
        return 
        
    def set_feed_data(self,request):
        if not request.fid : pass
        else : self.__feed.fid = request.fid
        if not request.uid : pass
        else : self.__feed.uid = request.uid
        if not request.nickname : pass
        else : self.__feed.nickname = request.nickname
        if not request.body : pass
        else : self.__feed.body = request.body
        if not request.date : pass
        else : self.__feed.date = request.date
        if not request.fclass : pass
        else : self.__feed.fclass = request.fclass
        if not request.class_name : pass
        else : self.__feed.class_name = request.class_name
        if not request.choice : pass
        else : self.__feed.choice = request.choice
        if not request.result : pass
        else : self.__feed.result = request.result
        if not request.state : pass
        else : self.__feed.state = request.state
        if not request.attend : pass
        else : self.__feed.attend = request.attend
        if not request.category : pass
        else : self.__feed.category = request.category
        if not request.comment : pass
        else : self.__feed.comment = request.comment
 

    def add_feed(self): #add
        self.__feed.fid = str(self._database.get_num_list_with_id(target_id='fid')+1)
        self._database.add_new_data(target_id='fid',new_data=self.__feed.get_dict_form_data())
        return

    def modify_feed(self):
        self._database.modify_data_with_id(target_id='fid',target_data=self.__feed.get_dict_form_data())
        return
    
    def delete_feed(self,request):
        self._database.delete_data_With_id(target='fid',id=request.fid)
    
    def get_response_form_data(self, head_parser):
        try:
            body = {
                'response' : self.__feed.get_dict_form_data()
            }

            response = self._get_response_data(head_parser=head_parser, body=body)
            return response

        except Exception as e:
            raise CoreControllerLogicError("response making error | " + e)

class BiasEditModel(AdminModel):
    def __init__(self, database: Local_Database) -> None:
        super().__init__(database)
        self.__bias = Bias()

    def load_bias(self,request): #load
        league_data = self._database.get_data_with_id(target='bid', id=request.bid)
        self.__bias.make_with_dict(league_data)
        return 
        
    def set_bias_data(self,request):
        if not request.bid : pass
        else : self.__bias.bid = request.bid
        if not request.type : pass
        else : self.__bias.type = request.type
        if not request.bname : pass
        else : self.__bias.bname = request.bname
        if not request.category : pass
        else : self.__bias.category = request.category
        if not request.birthday : pass
        else : self.__bias.birthday = request.birthday
        if not request.debut : pass
        else : self.__bias.debut = request.debut
        if not request.agency : pass
        else :self.__bias.agency = request.agency
        if not request.group : pass
        else : self.__bias.group = request.group
        if not request.lid : pass
        else : self.__bias.lid = request.lid
        if not request.point : pass
        else : self.__bias.point = request.point
        if not request.num_user : pass
        else : self.__bias.num_user = request.num_user
        if not request.x_account : pass
        else : self.__bias.x_account = request.x_account
        if not request.insta_account : pass
        else : self.__bias.insta_account = request.insta_account
        if not request.tiktok_account : pass
        else : self.__bias.tiktok_account = request.tiktok_account
        if not request.youtube_account : pass
        else : self.__bias.youtube_account = request.youtube_account
        if not request.homepage : pass
        else : self.__bias.homepage = request.homepage
        if not request.fan_cafe : pass
        else : self.__bias.fan_cafe = request.fan_cafe
        if not request.country : pass
        else : self.__bias.country = request.country
        if not request.nickname : pass
        else : self.__bias.nickname = request.nickname
        if not request.fanname : pass
        else : self.__bias.fanname = request.fanname
        if not request.group_memeber_bids : pass
        else : self.__bias.group_memeber_bids = request.group_member_bids

    def add_bias(self): #add
        num_bias = str(self._database.get_num_list_with_id(target_id='bid'))
        while True:
            bid = f'{self.__bias.type}{num_bias}'
            if self._database.get_data_with_id(target='bid',id=bid):
                continue
            else:
                break
        self.__bias.bid = bid
        self._database.add_new_data(target_id='bid',new_data=self.__bias.get_dict_form_data())
        return

    def modify_bias(self):
        print('start')
        self._database.modify_data_with_id(target_id='bid',target_data=self.__bias.get_dict_form_data())
        print('done')
        return
    
    def delete_bias(self,request):
        self._database.delete_data_With_id(target='bid',id=request.bid)
    
    def get_response_form_data(self, head_parser):
        try:
            body = {
                'response' : self.__bias.get_dict_form_data()
            }

            response = self._get_response_data(head_parser=head_parser, body=body)
            return response

        except Exception as e:
            raise CoreControllerLogicError("response making error | " + e)
    
class BannerEditModel(AdminModel):
    def __init__(self, database: Local_Database) -> None:
        super().__init__(database)
        self.__banner = Banner()

    def load_banner(self,request): #load
        league_data = self._database.get_data_with_id(target='baid', id=request.baid)
        self.__banner.make_with_dict(league_data)
        return 
        
    def set_banner_data(self,request):
        if not request.baid : pass
        else : self.__banner.baid = request.baid
        if not request.ba_url : pass
        else : self.__banner.ba_url = request.ba_url

    def add_banner(self): #add
        self.__banner.baid = str(self._database.get_num_list_with_id(target_id='baid')+1)
        self._database.add_new_data(target_id='baid',new_data=self.__banner.get_dict_form_data())
        return

    def modify_banner(self):
        self._database.modify_data_with_id(target_id='baid',target_data=self.__banner.get_dict_form_data())
        return
    
    def delete_banner(self,request):
        self._database.delete_data_With_id(target='baid',id=request.baid)
    
    def get_response_form_data(self, head_parser):
        try:
            body = {
                'response' : self.__banner.get_dict_form_data()
            }

            response = self._get_response_data(head_parser=head_parser, body=body)
            return response

        except Exception as e:
            raise CoreControllerLogicError("response making error | " + e)
    