from model.base_model import BaseModel
from model import Mongo_Database
from others.data_domain import User, Bias
from others import CoreControllerLogicError, FeedSearchEngine, ObjectStorageConnection
from view.jwt_decoder import JWTManager
import uuid
from pprint import pprint
import random
import re

class LoginModel(BaseModel):
    def __init__(self, database:Mongo_Database) -> None:
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
    
    def make_token(self,request, secret_key):
        try:
            jwtManager = JWTManager(secret_key=secret_key)
            self.__token = jwtManager.make_token(email=request.email)

        except Exception as e:
            raise CoreControllerLogicError(error_type="login make_token | " + str(e))
        
    def set_login_state(self, result):
        self.__result = result
        return
        
    def make_temp_user_token(self, request, secret_key):
        jwtManager = JWTManager(secret_key=secret_key)
        self.__token = jwtManager.make_token(email=request.email, usage="temp")
        return
    
    def get_token(self):
        return self.__token

    def get_response_form_data(self, head_parser):
        try:
            body = {
                'result' : self.__result,
                'detail' : self.__detail,
            }

            response = self._get_response_data(head_parser=head_parser, body=body)
            return response

        except Exception as e:
            raise CoreControllerLogicError("response making error | " + e)
    
    def get_result(self):
        return self.__result

class SendEmailModel(BaseModel):
    def __init__(self, database:Mongo_Database) -> None:
        super().__init__(database)
        self.__result = True
        self.__detail = ''

    def __make_user_nickname(self):
        while True:
            random_number = random.randint(0,10000)
            uname = "지지자"+str(random_number)
            # 만약 데이터베이스에 이 이름이 등록되어있다면.. 다시 랜덤숫자를 생성합니다
            if self._database.get_data_with_key(target="uid", key="uname", key_data=uname):
                continue
            else:
                return uname

    def save_user(self,request, feed_search_engine:FeedSearchEngine):
        try:
            uid = self.__make_uid()
            uname = self.__make_user_nickname()
            user = User(uid=uid,
                        uname=uname,
                        birth_year=request.birth_year,
                        email=request.email,
                        gender=request.gender,
                        password=request.password)

            self._database.add_new_data(target_id="uid",
                                        new_data=user.get_dict_form_data())
            
            feed_search_engine.try_add_user(user=user)

        except Exception as e:
            print(e)
            raise CoreControllerLogicError(error_type="save_response | " + str(e))
        
    def set_response(self, result:bool, detail):
        self.__result = result
        self.__detail = detail
        return

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
    def __init__(self, database:Mongo_Database) -> None:
        super().__init__(database)
        self.__biases = []
        self._uname = ""
        self._uid = ""
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

    def get_user_data(self):
        self._uname = self._user.uname
        self._uid = self._user.uid
        self._num_feed = self._user.num_feed
        self._num_like = len(self._user.like)
        self._num_comment = self._user.num_comment
        # self._num_comment = count_my_comments()
        # self._num_comment = len(self._user.my_comment)

        return

    def get_response_form_data(self, head_parser):
        try:
            body = {
                'uname' : self._uname,
                'uid' : self._uid,
                'num_feed' : self._num_feed,
                'num_like' : self._num_like,
                'num_comment' : self._num_comment
            }

            response = self._get_response_data(head_parser=head_parser, body=body)
            return response

        except Exception as e:
            raise CoreControllerLogicError("response making error | " + e)



class MyProfileModel(BaseModel):
    def __init__(self, database:Mongo_Database) -> None:
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
                "birth_year": self._age,
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
        self._age = self._user.birth_year
        self._gender = self._user.gender
        return

class ChangePasswordModel(BaseModel):
    def __init__(self, database:Mongo_Database) -> None:
        super().__init__(database)
        self._result = False
        self._detail = "Something goes bad | ERROR = 422"

    # 비밀번호 변경하기
    def try_change_password(self, data_payload):
        if self.__check_present_password(present_password=data_payload.password):
            if self.check_password_format(password=data_payload.new_password):
                self.__try_change_password(new_password = data_payload.new_password)
                self._result = True
                self._detail = "비밀번호가 변경되었어요."
            else:
                self._detail = "비밀번호 형식이 맞지 않습니다."
            return 
        else:
            self._detail = "비밀번호가 일치하지 않습니다."
            return
        
    def check_password_format(self, password: str) -> bool:
        pattern = re.compile(
            r'^(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{10,}$'
        )
        return bool(pattern.match(password))
        
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
    def __init__(self, database:Mongo_Database) -> None:
        super().__init__(database)
        self._result = False
        self._uname = ""
        self._detail = "default"

    # 달라진 닉네임인지 체크하는 곳
    def __check_new_nickname(self, new_uname:str):
        if self._user.uname != new_uname :
            return True
        else:
            return False

    def __change_nickname(self, new_uname:str):
        # 바꾸게 되면 데이터베이스를 수정합니다.
        self._uname = new_uname
        
        
        pprint(new_uname)
        result = self._database.get_data_with_key(target="uid", key="uname", key_data=new_uname)
        
        print("닉찾기 :", result)
            
            
        if result:
            return False
        else:
            self._user.uname = new_uname
            self._database.modify_data_with_id(target_id="uid", target_data=self._user.get_dict_form_data())
            return True
        
    def check_uname_format(self, uname:str) -> bool:
        if len(uname) == 0 or len(uname) > 7:
            return False
        else:
            return True

    # 닉네임 변경하기
    def try_change_nickname(self, data_payload):
        # check uname, 변동사항이 없으면 False를 반환
        self._uname = self._user.uname

        if self.__check_new_nickname(data_payload.new_uname):
            if self.check_uname_format(data_payload.new_uname):
                if self.__change_nickname(data_payload.new_uname):
                    self._result = True
                    self._detail = "닉네임이 변경되었습니다."
                else:
                    self._detail = "이미 사용중인 닉네임입니다."
            else:
                self._detail = "닉네임은 0자 이상, 7자 이하로 입력해주세요."
                
        else:
            self._detail = "기존 닉네임과 같습니다."

        return

    def get_response_form_data(self, head_parser):
        try:
            body = {
                'result' : self._result,
                "uname" : self._uname,
                "detail" : self._detail
            }

            response = self._get_response_data(head_parser=head_parser, body=body)
            return response

        except Exception as e:
            raise CoreControllerLogicError("response making error | " + e)

class ChangeProfilePhotoModel(BaseModel):
    def __init__(self, database:Mongo_Database) -> None:
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

class DeleteUserModel(BaseModel):
    def __init__(self, database:Mongo_Database) -> None:
        super().__init__(database)
        self._result = False
        self._detail = "Something goes bad | ERROR = 422"

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

    def try_delete_user(self):
        deleted_user_data = self._database.get_data_with_id(target="uid", id=self._user.uid)
        deleted_user = User().make_with_dict(deleted_user_data)

        cleaned_user = User(uid=deleted_user.uid, uname="탈퇴한유저")

        # 유저 데이터를 덮어씌워서 UID만 남김
        self._database.modify_data_with_id(target_id="uid", target_data=cleaned_user.get_dict_form_data())

        # 삭제된 유저는 다른 DB에 저장 됩니다. UID, 닉네임, 개인 정보 등을 저장합니다.
        self._database.add_new_data(target_id="duid", new_data=self._user.get_dict_form_data())
        return
