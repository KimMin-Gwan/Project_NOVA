from model.base_model import BaseModel
from model import Local_Database
from others.data_domain import User, Bias, Alert, ManagedUser
from others import CoreControllerLogicError, FeedManager, FeedSearchEngine
from view.jwt_decoder import JWTManager
import jwt
import datetime
import uuid

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
        self.__solo_bias = Bias()
        self.__group_bias = Bias()


    def set_solo_bias(self):
        bid = self._user.solo_bid
        if bid != "":
            bias_data = self._database.get_data_with_id(target="bid", id =bid)
            self.__solo_bias.make_with_dict(bias_data)
        return

    def set_group_bias(self):
        bid = self._user.group_bid
        if bid != "":
            bias_data = self._database.get_data_with_id(target="bid", id =bid)
            self.__group_bias.make_with_dict(bias_data)
        return

    def set_user_data_with_no_password(self):
        self._user.password = ""
        return

    def get_response_form_data(self, head_parser):
        try:
            body = {
                'user' : self._user.get_dict_form_data(),
                'solo_bias' : self.__solo_bias.get_dict_form_data(),
                'group_bias' : self.__group_bias.get_dict_form_data(),
            }

            response = self._get_response_data(head_parser=head_parser, body=body)
            return response

        except Exception as e:
            raise CoreControllerLogicError("response making error | " + e)

class MyCommentsModel(BaseModel):
    def __init__(self, database:Local_Database) -> None:
        super().__init__(database)
        self._comments= []
        self._cid = ""

    def get_my_comments(self, feed_manager:FeedManager, data_payload):
        self._comments= feed_manager.get_my_comments(user=self._user,
                                                    cid=data_payload.cid)
        if len(self._comments) != 0:
            self._cid= self._comments[-1].cid
        return

    def get_response_form_data(self, head_parser):
        try:
            body = {
                'comments' : self._make_dict_list_data(list_data=self._comments),
                "cid" : self._cid
            }

            response = self._get_response_data(head_parser=head_parser, body=body)
            return response

        except Exception as e:
            raise CoreControllerLogicError("response making error | " + e)

class MyFeedsModel(BaseModel):
    def __init__(self, database:Local_Database) -> None:
        super().__init__(database)
        self._feeds = []
        self._fid = ""

    def get_my_feed(self, feed_manager:FeedManager, data_payload):
        self._feeds = feed_manager.get_my_feeds(user=self._user,
                                                fid=data_payload.fid)
        if len(self._feeds) != 0:
            self._fid = self._feeds[-1].fid
        return

    #def get_commented_feed(self, feed_manager:FeedManager, data_payload):
        #self._feeds = feed_manager.get_commented_feed(user=self._user,
                                                    #fid=data_payload.fid)
        #if len(self._feeds) != 0:
            #self._fid = self._feeds[-1].fid

    def get_staring_feed(self, feed_manager:FeedManager, data_payload):
        self._feeds = feed_manager.get_stared_feed(user=self._user,
                                                    fid=data_payload.fid)
        if len(self._feeds) != 0:
            self._fid = self._feeds[-1].fid
        return

    def get_interactied_feed(self, feed_manager:FeedManager, data_payload):
        self._feeds = feed_manager.get_stared_feed(user=self._user,
                                                    fid=data_payload.fid)
        if len(self._feeds) != 0:
            self._fid = self._feeds[-1].fid
        return

    def get_response_form_data(self, head_parser):
        try:
            body = {
                'feeds' : self._make_dict_list_data(list_data=self._feeds),
                "fid" : self._fid
            }

            response = self._get_response_data(head_parser=head_parser, body=body)
            return response

        except Exception as e:
            raise CoreControllerLogicError("response making error | " + e)

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
        
    # 비밀번호 변경하기를 임시유저로( 비밀번호 찾기)
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
        self._detail = "Something goes bad | ERROR = 422"

    # 비밀번호 변경하기
    def try_change_nickname(self, data_payload):

        if data_payload.index == 0:
            self._user.uname = "지지자"
            self._detail = "지지자로 변경되었습니다"
            self._result = True
        elif data_payload.index == 1:
            if self._user.solo_bid != "":
                bias_data = self._database.get_data_with_id(target="bid", id=self._user.solo_bid)
                bias = Bias()
                bias.make_with_dict(dict_data=bias_data)
                if len(bias.fanname) == 0:
                    self._detail = f"{bias.bname}님은 팬명칭이 없어요"
                    return
                else:
                    self._user.uname = bias.fanname[0]
                    self._detail = f"{self._user.uname}로 변경되었습니다"
                    self._result =True
            else:
                self._detail = "지지하는 개인 최애가 없어요!"
                return
        elif data_payload.index == 2:
            if self._user.group_bid!= "":
                bias_data = self._database.get_data_with_id(target="bid", id=self._user.group_bid)
                bias = Bias()
                bias.make_with_dict(dict_data=bias_data)
                if len(bias.fanname) == 0:
                    self._detail = f"{bias.bname}님은 팬명칭이 없어요"
                    return
                else:
                    self._user.uname = bias.fanname[0]
                    self._detail = f"{self._user.uname}로 변경되었습니다"
                    self._result =True
            else:
                self._detail = "지지하는 그룹 최애가 없어요!"
                return

        elif data_payload.index == 3:
            # 지지자가 패스 구독중인지 확인하는 함수가 있어야함
            if data_payload.custom != "":
                self._user.uname = data_payload.custom
                self._detail = f"{self._user.uname}로 변경되었습니다"
                self._result =True
            else:
                self._detail = "최소 1글자 이상의 이름을 사용해야합니다!"
                return

        self._database.modify_data_with_id(target_id="uid", target_data=self._user.get_dict_form_data())
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
        

# feed 의 메타 정보를 보내주는 모델
class MyAlertModel(BaseModel):
    def __init__(self, database:Local_Database) -> None:
        super().__init__(database)
        self._alerts= []
        self._aid = -1

    # 알람 정보 세팅
    def set_alert_data(self, aid):
        alert_datas = self._database.get_datas_with_ids(target_id="aid", ids=self._user.alert)

        target = -1
        for i, alert_data in enumerate(reversed(alert_datas)):
            alert= Alert()
            alert.make_with_dict(dict_data=alert_data)
            self._alerts.append(alert)
            if alert.aid == aid:
                target = i

        if target != -1:
            self._alerts = self._alerts[target +1 :]

        if len(self._alerts) > 5:
            self._alerts = self._alerts[:5]
        return
    
    # 마지막 aid 정보
    def set_last_aid(self):
        if len(self._alerts) != 0:
            self._aid = self._alerts[-1].aid
        return
    
    def get_response_form_data(self, head_parser):
        try:
            body = {
                'alert' : self._make_dict_list_data(list_data=self._alerts),
                'aid' : self._aid
            }

            response = self._get_response_data(head_parser=head_parser, body=body)
            return response

        except Exception as e:
            raise CoreControllerLogicError("response making error | " + e)