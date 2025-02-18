from model.base_model import BaseModel
from model import Local_Database
from model.feed_model import FeedModel
from others.data_domain import User, Bias, Alert, ManagedUser
from others import CoreControllerLogicError, FeedManager, FeedSearchEngine, ObjectStorageConnection
from view.jwt_decoder import JWTManager
import jwt
import datetime
import uuid
from pprint import pprint

class LoginModel(BaseModel):
    def __init__(self, database:Local_Database) -> None:
        super().__init__(database)
        self.__result = "email"
        self.__token = ''
        self.__detail = '존재하지 않는 이메일 입니다'

    def request_login(self,request,user_data):
        try:
            if request.email == user_data.email and request.password == user_data.password:
                self.__result = "done"
            elif request.password != user_data.password:
                self.__result = "password"
                self.__detail = '일치하지 않는 비밀번호 입니다'

        except Exception as e:
            raise CoreControllerLogicError(error_type="request_login | " + str(e))
    
    def make_token(self,request):
        try:
            jwtManager = JWTManager()
            self.__token = jwtManager.make_token(email=request.email)

        except Exception as e:
            raise CoreControllerLogicError(error_type="login make_token | " + str(e))
        
    def set_login_state(self, result):
        self.__result = result
        return
        
    def make_temp_user_token(self, request):
        jwtManager = JWTManager()
        self.__token = jwtManager.make_token(email=request.email, usage="temp")
        return

    def get_response_form_data(self, head_parser):
        try:
            body = {
                'result' : self.__result,
                'detail' : self.__detail,
                'token' : self.__token
            }

            response = self._get_response_data(head_parser=head_parser, body=body)
            return response

        except Exception as e:
            raise CoreControllerLogicError("response making error | " + e)
    
    def get_result(self):
        return self.__result

class SendEmailModel(BaseModel):
    def __init__(self, database:Local_Database) -> None:
        super().__init__(database)
        self.__result = True
        self.__detail = ''
        #self.__token = ''

    def make_token(self,request):
        try:
            # 비밀 키 설정
            secret_key = "your_secret_key"
            # 헤더 설정
            headers = {
                "alg": "HS256",
                "typ": "JWT"
            }
            # 페이로드 설정
            payload = {
                "email": request.email,
                "iat": datetime.datetime.utcnow(),
                "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30)  # 만료 시간 30분
            }
            # 토큰 생성
            #self.__token = jwt.encode(payload, secret_key, algorithm="HS256", headers=headers)

        except Exception as e:
            raise CoreControllerLogicError(error_type="make_token | " + str(e))
        
    def save_user(self,request, feed_search_engine:FeedSearchEngine):
        try:
            uid = self.__make_uid()
            user = User(uid=uid,
                        age=request.age,
                        email=request.email,
                        gender=request.gender,
                        password=request.password)
            managedUser = ManagedUser(
                uid=uid
            )

            self._database.add_new_data(target_id="uid",
                                        new_data=user.get_dict_form_data())
            
            feed_search_engine.try_add_user(user=user)
            #self._database.add_new_data(target_id="muid",
                                        #new_data=managedUser.get_dict_form_data())


        except Exception as e:
            raise CoreControllerLogicError(error_type="save_response | " + str(e))
        
    def set_response(self,):
        try:
            self.__result = False
            self.__detail = "이미 존재하는 이메일 입니다."
        except Exception as e:
            raise CoreControllerLogicError(error_type="set_response | " + str(e))

    def set_response_in_reverse(self,):
        try:
            self.__result = False
            self.__detail = "존재하지 않는 이메일 입니다."
        except Exception as e:
            raise CoreControllerLogicError(error_type="set_response | " + str(e))

    def check_email_duplicate(self, email:str):
        user_data = self._database.get_data_with_key(target="uid", key="email", key_data=email)
        if user_data is not None:
            self.set_response()
        else:
            self.__detail = "사용 가능한 이메일 입니다."

    def get_response_form_data(self, head_parser):
        try:
            body = {
                'result' : self.__result,
                #'token' : self.__token,
                'detail' : self.__detail
            }

            response = self._get_response_data(head_parser=head_parser, body=body)
            return response

        except Exception as e:
            raise CoreControllerLogicError("response making error | " + e)
    
    def get_result(self):
        return self.__result
    
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
   
class UserPageModel(BaseModel):
    def __init__(self, database:Local_Database) -> None:
        super().__init__(database)
        self.__biases = []
        self._uname = ""
        self._uid = ""
        self._num_long_feed = 0
        self._num_short_feed = 0
        self._num_like = 0
        self._num_comment = 0

    def set_bias_datas(self):
        bids = self._user.bids
        if len(self._user.bids):
            bias_datas = self._database.get_datas_with_ids(target_id="bid", ids=bids)
            for bias_data in bias_datas:
                bias = Bias()
                bias.make_with_dict(bias_data)
                self.__biases.append(bias)
        return

    def set_user_data_with_no_password(self):
        self._user.password = ""
        return

    # 나의 Feed 중 타입에 따라 개수 세기
    def __count_my_feeds_type(self, feed_type:str):
        count = 0
        feed_datas = self._database.get_datas_with_ids(target_id="fid", ids=self._user.my_feed)
        for feed_data in feed_datas:
            if feed_data["fclass"] == feed_type:
                count += 1

        return count


    def get_user_data(self):
        self._uname = self._user.uname
        self._uid = self._user.uid
        self._num_long_feed = self._user.num_long_feed
        self._num_short_feed = self._user.num_short_feed
        self._num_like = len(self._user.like)
        self._num_comment = len(self._user.my_comment)

        return

    def get_response_form_data(self, head_parser):
        try:
            body = {
                'uname' : self._uname,
                'uid' : self._uid,
                'num_long_feed' : self._num_long_feed,
                'num_short_feed' : self._num_short_feed,
                'num_like' : self._num_like,
                'num_comment' : self._num_comment
            }

            response = self._get_response_data(head_parser=head_parser, body=body)
            return response

        except Exception as e:
            raise CoreControllerLogicError("response making error | " + e)

# 통일성을 위해 Comment 까지 재편 합니다.
class MyCommentsModel(BaseModel):
    def __init__(self, database:Local_Database ) -> None:
        super().__init__(database)
        self._comments = []
        self._key = -1

    def get_response_form_data(self, head_parser):
        try:
            body = {
                'comments' : self._make_dict_list_data(list_data=self._comments),
                "key" : self._key
            }

            response = self._get_response_data(head_parser=head_parser, body=body)
            return response

        except Exception as e:
            raise CoreControllerLogicError("response making error | " + e)

    def get_my_comments(self, feed_manager:FeedManager, last_index:int=-1):
        self._comments = feed_manager.get_my_comments(user=self._user)
        self._comments, self._key = feed_manager.paging_fid_list(fid_list=self._comments, last_index=last_index, page_size=3)

        return

class MyFeedsModel(FeedModel):
    def __init__(self, database:Local_Database) -> None:
        super().__init__(database)

    def __search_user_nickname(self, uid:str, uids:list, wusers:list):
        if uid not in uids:
            return ""

        # uid가 존재함. 그러면 리스트에서 찾는다
        for user in wusers:
            if user.uid == uid:
                return user.nickname

        return ""

    def __set_send_data(self):
        result_feeds = []

        uids = []
        wusers = []

        for single_feed in self._feeds:
            if single_feed.uid in uids:
                continue
            uids.append(single_feed.uid)

        user_datas = self._database.get_datas_with_ids(target_id="uid", ids=uids)
        for user_data in user_datas:
            single_user = User()
            single_user.make_with_dict(user_data)
            wusers.append(single_user)

        for feed in self._feeds:
            # 마이페이지에 인터엑션은 표시 없음
            feed.iid = ""
            
            # 삭제된거 지우고
            if feed.display < 3:
                continue
        
            # 롱폼은 바디 데이터를 받아야됨
            if feed.fclass != "short":
                feed.raw_body = ObjectStorageConnection().get_feed_body(fid = feed.fid)
                _, feed.image = ObjectStorageConnection().extract_body_n_image(raw_data=feed.raw_body)

            else:
                feed.raw_body = feed.body
            
            # comment 길이 & image 길이
            feed.num_comment = len(feed.comment)
            feed.num_image = len(feed.image)

            # 좋아요를 누를 전적
            
            for fid_n_date in self._user.like:
                target_fid = fid_n_date.split('=')[0]
                if target_fid == feed.fid:
                    feed.star_flag = True

            # 피드 작성자 이름
            # 나중에 nickname으로 바꿀것
            feed.nickname = self.__search_user_nickname(feed.uid, uids, wusers)
            feed.is_owner = True
            result_feeds.append(feed)
        return result_feeds

    def get_my_long_feeds(self, feed_manager:FeedManager, last_index:int=-1):
        # 이게 가능한게, 리스트에서, 인덱스로만 사용해서 참조 하기 때문에 이거 써도 된다.
        self._feeds = feed_manager.get_my_long_feeds(user=self._user)
        self._feeds, self._key = feed_manager.paging_fid_list(fid_list=self._feeds, last_index=last_index, page_size=3)
        self._feeds = self.__set_send_data()
        return

    def get_my_short_feeds(self, feed_manager:FeedManager, last_index:int=-1):
        # 이게 가능한게, 리스트에서, 인덱스로만 사용해서 참조 하기 때문에 이거 써도 된다.
        self._feeds = feed_manager.get_my_short_feeds(user=self._user)
        self._feeds, self._key = feed_manager.paging_fid_list(fid_list=self._feeds, last_index=last_index, page_size=3)
        self._feeds = self.__set_send_data()

        return

    def get_liked_feeds(self, feed_manager:FeedManager, last_index:int=-1):
        self._feeds = feed_manager.get_liked_feeds(user=self._user)
        self._feeds, self._key = feed_manager.paging_fid_list(fid_list=self._feeds, last_index=last_index, page_size=3)
        self._feeds = self.__set_send_data()

        return

    def get_interacted_feeds(self, feed_manager:FeedManager, last_index:int=-1):
        self._feeds = feed_manager.get_interacted_feeds(user=self._user)
        self._feeds, self._key = feed_manager.paging_fid_list(fid_list=self._feeds, last_index=last_index, page_size=3)
        self._feeds = self.__set_send_data()
        
        return

class MyProfileModel(BaseModel):
    def __init__(self, database:Local_Database) -> None:
        super().__init__(database)
        self._uname = ""
        self._uid = ""
        self._email = ""
        self._age = ""
        self._gender = ""

    def get_response_form_data(self, head_parser):
        try:
            body = {
                'uname' : self._uname,
                'uid': self._uid,
                "email": self._email,
                "age": self._age,
                "gender": self._gender
            }

            response = self._get_response_data(head_parser=head_parser, body=body)
            return response

        except Exception as e:
            raise CoreControllerLogicError("response making error | " + e)

    def get_my_profile(self):
        self._uname = self._user.uname
        self._uid = self._user.uid
        self._email = self._user.email
        self._age = self._user.age
        self._gender = self._user.gender

        return

class ChangePasswordModel(BaseModel):
    def __init__(self, database:Local_Database) -> None:
        super().__init__(database)
        self._result = False
        self._detail = "Something goes bad | ERROR = 422"

    # 비밀번호 변경하기
    def try_change_password(self, data_payload):
        if self.__check_present_password(present_password=data_payload.password):
            self.__try_change_password(new_password = data_payload.new_password)
            self._result = True
            self._detail = "비밀번호가 변경되었어요"
            return 
        else:
            self._detail = "비밀번호가 틀렸어요"
            return
        
    # 비밀번호 변경하기를 임시유저로 ( 비밀번호 찾기)
    def try_change_password_with_temp_user(self, data_payload):
        self.__try_change_password(new_password = data_payload.new_password)
        self._result = True
        self._detail = "비밀번호가 변경되었어요"


    # 현재 비밀번호가 맞는지 체크
    def __check_present_password(self, present_password):
        if self._user.password != present_password:
            return False
        else:
            return True

    # 비밀번호 바꾸고 저장하기
    def __try_change_password(self, new_password):
        self._user.password = new_password
        self._database.modify_data_with_id(
            target_id="uid",
            target_data=self._user.get_dict_form_data())
        return 

    def get_response_form_data(self, head_parser):
        try:
            body = {
                'result' : self._result,
                "detail" : self._detail
            }

            response = self._get_response_data(head_parser=head_parser, body=body)
            return response

        except Exception as e:
            raise CoreControllerLogicError("response making error | " + e)

class ChangeNickNameModel(BaseModel):
    def __init__(self, database:Local_Database) -> None:
        super().__init__(database)
        self._result = False
        self._uname = ""

    # 달라진 닉네임인지 체크하는 곳
    def __check_new_nickname(self, new_uname:str):
        if self._user.uname != new_uname :
            return True
        else:
            return False

    def __change_nickname(self, new_uname:str):
        # 바꾸게 되면 데이터베이스를 수정합니다.
        self._uname = new_uname
        self._user.uname = new_uname
        self._database.modify_data_with_id(target_id="uid", target_data=self._user.get_dict_form_data())

    # 닉네임 변경하기
    def try_change_nickname(self, data_payload):
        # check uname, 변동사항이 없으면 False를 반환
        self._uname = self._user.uname

        if self.__check_new_nickname(data_payload.new_uname):
            self.__change_nickname(data_payload.new_uname)
            self._result = True

        return

    def get_response_form_data(self, head_parser):
        try:
            body = {
                'result' : self._result,
                "uname" : self._uname
            }

            response = self._get_response_data(head_parser=head_parser, body=body)
            return response

        except Exception as e:
            raise CoreControllerLogicError("response making error | " + e)

class ChangeProfilePhotoModel(BaseModel):
    def __init__(self, database:Local_Database) -> None:
        super().__init__(database)
        self._result = False
        self._detail = "업로드에 문제가 있음"

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

    # 아직 안됨
    def try_change_profile_photo(self, data_payload):
          
        connector = ObjectStorageConnection()
        result = connector.make_new_profile_image(uid=self._user.uid,
                                         image=data_payload.image,
                                         image_name=data_payload.image_name
                                         )
        
        if not result:
            self._detail = "허용되지 않은 확장자를 사용"
        else:
            self._result = True
            self._detail = "업로드 성공"
        
        return
