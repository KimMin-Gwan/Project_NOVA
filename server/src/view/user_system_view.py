from typing import Any, Optional, Union
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request, UploadFile, File
from view.master_view import Master_View, RequestHeader
from view.parsers import Head_Parser
from controller import Home_Controller, Core_Controller, UserController
from view.jwt_decoder import RequestManager
from pprint import pprint

class User_Service_View(Master_View):
    def __init__(self, app:FastAPI, endpoint:str, database, head_parser:Head_Parser,
                 nova_verification, feed_manager, feed_search_engine, jwt_secret_key) -> None:
        super().__init__(head_parser=head_parser)
        self.__app = app
        self._endpoint = endpoint
        self.__database = database
        self.__nova_verification = nova_verification
        self.__feed_manager = feed_manager
        self.__feed_search_engine = feed_search_engine
        self.__jwt_secret_key = jwt_secret_key
        self.user_route(endpoint)
        self.my_page_route()

    def user_route(self, endpoint:str):
        @self.__app.get(endpoint+'/user')
        def home():
            return 'Hello, This is User system'

        #로그인
        @self.__app.post('/user_home/try_login')
        def try_login(raw_request:dict):
            request_manager = RequestManager(secret_key=self.__jwt_secret_key)
            data_payload = LoginRequest(request=raw_request)

            user_controller=UserController()
            model = user_controller.try_login(database=self.__database,
                                              request=data_payload,
                                              secret_key=self.__jwt_secret_key
                                              )
            body_data = model.get_response_form_data(self._head_parser)
            response = request_manager.make_json_response(body_data=body_data,
                                                           token=body_data['body']['token'])
            return response

        # 로그아웃
        @self.__app.get('/user_home/try_logout')
        def try_logout(request:Request):
            request_manager = RequestManager(secret_key=self.__jwt_secret_key)
            request_manager.try_view_management_need_authorized(data_payload=None, cookies=request.cookies)
            response = request_manager.try_clear_cookies(request=request)
            return response

        # 이메일 전송
        # response 포함 정보 -> 'result' : True or False
        #                    -> 'detail' : "실패 사유"
        @self.__app.post('/user_home/try_send_email')
        def try_send_email(raw_request:dict):
            request = EmailSendRequest(request=raw_request)
            user_controller=UserController()
            model = user_controller.try_send_email(database=self.__database,
                                                   request = request,
                                              nova_verification=self.__nova_verification)
            response = model.get_response_form_data(self._head_parser)
            return response

        # 비밀번호 찾기에서 이메일 보내기
        @self.__app.post('/user_home/try_find_password_send_email')
        def try_find_password_send_email(raw_request:dict):
            request = EmailSendRequest(request=raw_request)
            user_controller=UserController()
            model = user_controller.try_send_email_password(database=self.__database,
                                                            request = request,
                                                            nova_verification=self.__nova_verification)
            response = model.get_response_form_data(self._head_parser)
            return response

        # 비밀번호 찾기
        # response 포함 정보 -> 'result' : True or False
        @self.__app.post('/user_home/try_login_temp_user')
        async def try_login_temp_user(raw_request:dict):
            request_manager = RequestManager(secret_key=self.__jwt_secret_key)
            request_manager.data_payload = TempLoginRequest(request=raw_request)

            user_controller=UserController()
            model = await user_controller.try_login_with_temp_user(database=self.__database,
                                                            request=request_manager,
                                                            nova_verification=self.__nova_verification,
                                                            secret_key=self.__jwt_secret_key
                                                            )
            body_data = model.get_response_form_data(self._head_parser)
            response = request_manager.make_json_response(body_data=body_data,
                                                           token=body_data['body']['token'],)
            return response

        # 임시 로그인 상태에서 비밀번호 변경하기
        @self.__app.post('/user_home/try_find_password')
        def try_find_password(request:Request, raw_request:dict):
            request_manager = RequestManager(secret_key=self.__jwt_secret_key)
            data_payload = ChangePasswordRequest(request=raw_request)

            request_manager.try_view_management_authorized_with_temp_user(data_payload=data_payload, cookies=request.cookies)
            if not request_manager.jwt_payload.result:
                raise request_manager.credentials_exception

            user_controller=UserController()
            model = user_controller.try_find_password(database=self.__database,
                                                            request=request_manager)

            body_data = model.get_response_form_data(self._head_parser)
            # 임시 유저 토큰을 지워버림
            response = request_manager.make_json_response_in_password_find(
                request=request, body_data=body_data)
            
            return response

        # 이메일 중복 검사 기능
        @self.__app.post('/user_home/try_check_email_duplicate')
        def try_check_email_duplicate(request:Request, raw_request:dict):
            request_manager = RequestManager(secret_key=self.__jwt_secret_key)
            request_manager.data_payload = EmailCheckRequest(raw_request)

            user_controller=UserController()
            model = user_controller.try_check_email_duplicate(database=self.__database,
                                                              request=request_manager)
            body_data = model.get_response_form_data(self._head_parser)
            response = request_manager.make_json_response(body_data=body_data, request=request)
            return response

        # 회원가입 시도
        # response 포함 정보 -> 'result' : True or False
        #                    -> 'detail' : "실패 사유"
        @self.__app.post('/user_home/try_sign_up')
        async def try_sign_up(raw_request:dict):
            request = SignInRequest(request=raw_request)
            # pprint(raw_request)
            user_controller=UserController()
            model = await user_controller.try_sign_up(database=self.__database,
                                                   request = request,
                                              nova_verification=self.__nova_verification,
                                              feed_search_engine=self.__feed_search_engine
                                              )
            response = model.get_response_form_data(self._head_parser)
            return response


        # 회원탈퇴
        @self.__app.get('/user_home/try_resign')
        def try_resign(request:Request):
            request_manager = RequestManager(secret_key=self.__jwt_secret_key)
            data_payload = DummyRequest()
            
            user_controller=UserController()
            request_manager.try_view_management_need_authorized(data_payload=data_payload, cookies=request.cookies)
            model = user_controller.try_resign(database=self.__database, request=request_manager)

            response = request_manager.try_clear_cookies(request=request)
            return response

#----------------------------------------신형--------------------------------------------------

    def my_page_route(self):
        @self.__app.get('/user_home/get_my_page_data')
        def try_get_my_page(request:Request):
            request_manager = RequestManager(secret_key=self.__jwt_secret_key)
            # pprint("프린트 됨")
            data_payload = DummyRequest()
            request_manager.try_view_management_need_authorized(data_payload=data_payload, cookies=request.cookies)
            if not request_manager.jwt_payload.result:
                raise request_manager.credentials_exception

            user_controller = UserController()
            model = user_controller.try_get_user_page(database=self.__database,request=request_manager)
            body_data = model.get_response_form_data(self._head_parser)
            response = request_manager.make_json_response(body_data=body_data)
            return response

        # 타입에 맞게 Feed들을 반환하는 내가쓴 글 찾기
        @self.__app.get('/user_home/get_my_feed')
        def try_get_my_feeds_type(request:Request, type:Optional[str]="post", key:Optional[int]=-1):
            request_manager = RequestManager(secret_key=self.__jwt_secret_key)
            data_payload = MyFeedsRequest(type=type, key=key)

            request_manager.try_view_management_need_authorized(data_payload=data_payload, cookies=request.cookies)

            user_controller = UserController()
            model = user_controller.try_get_my_feeds_with_type(database=self.__database,
                                                               request=request_manager,
                                                               feed_manager=self.__feed_manager)
            body_data = model.get_response_form_data(self._head_parser)
            response = request_manager.make_json_response(body_data=body_data)
            return response

        # 내 댓글
        @self.__app.get('/user_home/get_my_comments')
        def try_get_my_comment(request:Request, key:Optional[int]=-1):
            request_manager = RequestManager(secret_key=self.__jwt_secret_key)

            data_payload = MyCommentsRequest(key=key)

            # request_manager.try_view_management(data_payload=data_payload, cookies=request.cookies)
            request_manager.try_view_management_need_authorized(data_payload=data_payload, cookies=request.cookies)
            if not request_manager.jwt_payload.result:
                raise request_manager.credentials_exception

            user_controller=UserController()
            model = user_controller.try_get_my_comments(database=self.__database,
                                                    request=request_manager,
                                                    feed_manager=self.__feed_manager)
            body_data = model.get_response_form_data(self._head_parser)
            response = request_manager.make_json_response(body_data=body_data)
            return response

        # 프로필 수정 표시 탭
        @self.__app.get('/user_home/get_my_profile_data')
        def try_get_my_profile(request:Request):
            request_manager = RequestManager(secret_key=self.__jwt_secret_key)

            data_payload = DummyRequest()
            request_manager.try_view_management_need_authorized(data_payload=data_payload, cookies=request.cookies)
            if not request_manager.jwt_payload.result:
                raise request_manager.credentials_exception

            user_controller = UserController()
            model = user_controller.try_get_my_profile(database=self.__database,
                                                       request=request_manager)
            body_data = model.get_response_form_data(self._head_parser)
            response = request_manager.make_json_response(body_data=body_data)
            return response

        # 패스워드 변경하기
        @self.__app.post('/user_home/try_change_password')
        def try_change_password(request:Request, raw_request:dict):
            request_manager = RequestManager(secret_key=self.__jwt_secret_key)

            data_payload = ChangePasswordRequest(request=raw_request)
            request_manager.try_view_management_need_authorized(data_payload=data_payload, cookies=request.cookies)

            home_controller=UserController()
            model = home_controller.try_change_password(database=self.__database,
                                                        request=request_manager)
            body_data = model.get_response_form_data(self._head_parser)
            response = request_manager.make_json_response(body_data=body_data)
            return response

        # 닉네임 바꾸기
        @self.__app.post('/user_home/try_change_nickname')
        def try_change_nickname(request:Request, raw_request:dict):
            request_manager = RequestManager(secret_key=self.__jwt_secret_key)

            data_payload  = ChangeNicknameRequest(request=raw_request)
            request_manager.try_view_management_need_authorized(data_payload=data_payload, cookies=request.cookies)

            user_controller=UserController()
            model = user_controller.try_change_nickname(database=self.__database,
                                                        request=request_manager)
            body_data = model.get_response_form_data(self._head_parser)
            response = request_manager.make_json_response(body_data=body_data)
            return response

        # 프로필 사진 바꾸기
        @self.__app.post('/user_home/try_change_profile_photo')
        async def try_change_profile_photo(request:Request, image:Union[UploadFile, None] = File(None)):
            request_manager = RequestManager(secret_key=self.__jwt_secret_key)
            
            if image is None:
                image_name = ""
            else:
                image_name = image.filename
                image = await image.read()
        
            data_payload = ChangeProfilePhotoRequest(image=image, image_name=image_name)
            request_manager.try_view_management_need_authorized(data_payload=data_payload, cookies=request.cookies)
            if not request_manager.jwt_payload.result:
                raise request_manager.credentials_exception

            user_controller=UserController()
            model = user_controller.try_change_profile_photo(database=self.__database,
                                                             request=request_manager)
            body_data = model.get_response_form_data(self._head_parser)
            response = request_manager.make_json_response(body_data=body_data)

            return response


class DummyRequest():
    def __init__(self) -> None:
        pass

class MyFeedsRequest(RequestHeader):
    def __init__(self, type, key) -> None:
        self.type = type
        self.key = key

class MyCommentsRequest(RequestHeader):
    def __init__(self, key) -> None:
        # self.email = "randomUser4@naver.com"
        self.key = key

class ChangePasswordRequest(RequestHeader):
    def __init__(self, request) -> None:
        super().__init__(request)
        body = request['body']
        self.password = body['password']
        self.new_password= body['new_password']

class ChangeNicknameRequest(RequestHeader):
    def __init__(self, request) -> None:
        super().__init__(request)
        body = request['body']
        self.new_uname = body['uname']

class ChangeProfilePhotoRequest(RequestHeader):
    def __init__(self, image, image_name) -> None:
        self.image = image
        self.image_name =image_name

class LoginRequest(RequestHeader):
    def __init__(self, request) -> None:
        super().__init__(request)
        body = request['body']
        self.email = body['email']
        self.password = body['password']

class TempLoginRequest(RequestHeader):
    def __init__(self, request) -> None:
        super().__init__(request)
        body = request['body']
        self.email = body['email']
        self.verification_code = body['verification_code']

class EmailCheckRequest(RequestHeader):
    def __init__(self, request) -> None:
        super().__init__(request)
        body = request['body']
        self.email = body['email']

class EmailSendRequest(RequestHeader):
    def __init__(self, request) -> None:
        super().__init__(request)
        body = request['body']
        self.email = body['email']

class SignInRequest(RequestHeader):
    def __init__(self, request) -> None:
        super().__init__(request)
        body = request['body']
        self.email = body['email']
        self.password= body['password']
        self.verification_code = int(body['verification_code'])
        self.age = body['age']
        self.gender = body['gender']

class ResignRequest(RequestHeader):
    def __init__(self, request) -> None:
        super().__init__(request)
        body = request['body']

# class MyFeedRequest():
#     def __init__(self, fid) -> None:
#         self.fid= fid
#
# class MyCommentRequest():
#     def __init__(self, cid) -> None:
#         self.cid=cid
#
# class MyAlertRequest():
#     def __init__(self, aid) -> None:
#         self.aid = aid