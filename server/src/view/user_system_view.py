from typing import Any, Optional
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request
from view.master_view import Master_View, RequestHeader
from view.parsers import Head_Parser
from controller import Home_Controller, Core_Controller, UserController
from view.jwt_decoder import RequestManager

class User_Service_View(Master_View):
    def __init__(self, app:FastAPI, endpoint:str, database, head_parser:Head_Parser,
                 nova_verification, feed_manager, feed_search_engine) -> None:
        super().__init__(head_parser=head_parser)
        self.__app = app
        self._endpoint = endpoint
        self.__database = database
        self.__nova_verification = nova_verification
        self.__feed_manager = feed_manager
        self.__feed_search_engine = feed_search_engine
        self.user_route(endpoint)
        self.my_page_route()
        self.new_page_route()

    def user_route(self, endpoint:str):
        @self.__app.get(endpoint+'/user')
        def home():
            return 'Hello, This is User system'

        #로그인
        @self.__app.post('/user_home/try_login')
        def try_login(raw_request:dict):
            request_manager = RequestManager()
            data_payload = LoginRequest(request=raw_request)

            user_controller=UserController()
            model = user_controller.try_login(database=self.__database,
                                              request=data_payload)
            body_data = model.get_response_form_data(self._head_parser)
            response = request_manager.make_json_response(body_data=body_data,
                                                           token=body_data['body']['token'])
            return response

        # 로그아웃
        @self.__app.get('/user_home/try_logout')
        def try_login(request:Request):
            request_manager = RequestManager()
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
        def try_find_passwrod_send_email(raw_request:dict):
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
            request_manager = RequestManager()
            request_manager.data_payload = TempLoginRequest(request=raw_request)

            user_controller=UserController()
            model = await user_controller.try_login_with_temp_user(database=self.__database,
                                                            request=request_manager,
                                                            nova_verification=self.__nova_verification)
            body_data = model.get_response_form_data(self._head_parser)
            response = request_manager.make_json_response(body_data=body_data,
                                                           token=body_data['body']['token'],)
            return response

        # 임시 로그인 상태에서 비밀번호 변경하기
        @self.__app.post('/user_home/try_find_password')
        def try_find_password(request:Request, raw_request:dict):
            request_manager = RequestManager()
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

        # 회원가입 시도
        # response 포함 정보 -> 'result' : True or False
        #                    -> 'detail' : "실패 사유"
        @self.__app.post('/user_home/try_sign_up')
        async def try_sign_up(raw_request:dict):
            request = SignInRequest(request=raw_request)
            user_controller=UserController()
            model = await user_controller.try_sign_up(database=self.__database,
                                                   request = request,
                                              nova_verification=self.__nova_verification,
                                              feed_search_engine=self.__feed_search_engine
                                              )
            response = model.get_response_form_data(self._head_parser)
            return response

#---------------------------------구 형------------------------------------------------------------------------
    def my_page_route(self):
        # @self.__app.get('/user_home/my_data')
        # def get_my_page(request:Request):
        #     request_manager = RequestManager()
        #
        #     data_payload = DummyRequest()
        #     request_manager.try_view_management_need_authorized(data_payload=data_payload, cookies=request.cookies)
        #     if not request_manager.jwt_payload.result:
        #         raise request_manager.credentials_exception
        #
        #     home_controller=UserController()
        #     model = home_controller.get_user_page(database=self.__database,
        #                                                 request=request_manager)
        #     body_data = model.get_response_form_data(self._head_parser)
        #     response = request_manager.make_json_response(body_data=body_data)
        #     return response

        # 비밀번호 변경하기
        @self.__app.post('/user_home/try_change_password')
        def try_change_password(request:Request, raw_request:dict):
            request_manager = RequestManager()

            data_payload = ChangePasswordRequest(request=raw_request)
            request_manager.try_view_management_need_authorized(data_payload=data_payload, cookies=request.cookies)
            if not request_manager.jwt_payload.result:
                raise request_manager.credentials_exception

            home_controller=UserController()
            model = home_controller.try_change_password(database=self.__database,
                                                        request=request_manager)
            body_data = model.get_response_form_data(self._head_parser)
            response = request_manager.make_json_response(body_data=body_data)
            return response

        # 닉네임 바꾸기
        @self.__app.get('/user_home/try_change_nickname')
        def try_chagne_nickname(request:Request, index:Optional[int], custom:Optional[str]=""):
            request_manager = RequestManager()

            data_payload  = ChangeNicknameRequest(index=index, custom=custom)
            request_manager.try_view_management_need_authorized(data_payload=data_payload, cookies=request.cookies)
            if not request_manager.jwt_payload.result:
                raise request_manager.credentials_exception

            home_controller=UserController()
            model = home_controller.try_change_nickname(database=self.__database,
                                                        request=request_manager)
            body_data = model.get_response_form_data(self._head_parser)
            response = request_manager.make_json_response(body_data=body_data)
            return response

        # 종류가 나뉘어진다.
        # 포스트 (Long), 모멘트(Short)를 따로둡니다. (인터페이스를 분리할까 고민 중)
        # 댓글은 이미 동작이 O, 좋아요는 좋아요한 것만 뜨게

        # 내가 쓴 글
        @self.__app.get('/user_home/get_my_feed')
        def get_my_feed(request:Request, fid:Optional[str] = ""):
            request_manager = RequestManager()

            data_payload = MyFeedRequest(fid=fid)
            request_manager.try_view_management_need_authorized(data_payload=data_payload, cookies=request.cookies)
            if not request_manager.jwt_payload.result:
                raise request_manager.credentials_exception

            # home_controller=UserController()
            # # model = home_controller.get_my_feed(database=self.__database,
            # #                                             request=request_manager,
            # #                                             feed_manager=self.__feed_manager)
            # body_data = model.get_response_form_data(self._head_parser)
            response = request_manager.make_json_response(body_data=body_data)
            return response

        # 내가 좋아요 한 거
        @self.__app.get('/user_home/get_stared_feed')
        def get_stared_feed(request:Request, fid:Optional[str] = ""):
            request_manager = RequestManager()

            data_payload = MyFeedRequest(fid=fid)
            request_manager.try_view_management_need_authorized(data_payload=data_payload, cookies=request.cookies)
            if not request_manager.jwt_payload.result:
                raise request_manager.credentials_exception

            # home_controller=UserController()
            # model = home_controller.get_staring_feed(database=self.__database,
            #                                          request=request_manager,
            #                                          feed_manager=self.__feed_manager)
            # body_data = model.get_response_form_data(self._head_parser)
            response = request_manager.make_json_response(body_data=body_data)
            return response

        # 내가 상호작용한 거
        # @self.__app.get('/user_home/get_interactied_feed')
        # def get_interactied_feed(request:Request, fid:Optional[str] = ""):
        #     request_manager = RequestManager()
        #
        #     data_payload = MyFeedRequest(fid=fid)
        #     request_manager.try_view_management_need_authorized(data_payload=data_payload, cookies=request.cookies)
        #     if not request_manager.jwt_payload.result:
        #         raise request_manager.credentials_exception
        #
        #     home_controller=UserController()
        #     model = home_controller.get_interacted_feed(database=self.__database,
        #                                                  request=request_manager,
        #                                                  feed_manager=self.__feed_manager)
        #     body_data = model.get_response_form_data(self._head_parser)
        #     response = request_manager.make_json_response(body_data=body_data)
        #     return response

        # 내 댓글
        @self.__app.get('/user_home/get_my_comments')
        def get_my_comment(request:Request, cid:Optional[str] = ""):
            request_manager = RequestManager()

            data_payload = MyCommentRequest(cid=cid)
            request_manager.try_view_management_need_authorized(data_payload=data_payload, cookies=request.cookies)
            if not request_manager.jwt_payload.result:
                raise request_manager.credentials_exception

            home_controller=UserController()
            model = home_controller.get_my_comments(database=self.__database,
                                                        request=request_manager,
                                                        feed_manager=self.__feed_manager)
            body_data = model.get_response_form_data(self._head_parser)
            response = request_manager.make_json_response(body_data=body_data)
            return response

        # @self.__app.get('/user_home/get_my_alert')
        # def get_my_alert(request:Request, aid:Optional[str] = ""):
        #     request_manager = RequestManager()
        #
        #     data_payload = MyAlertRequest(aid=aid)
        #     request_manager.try_view_management_need_authorized(data_payload=data_payload, cookies=request.cookies)
        #     if not request_manager.jwt_payload.result:
        #         raise request_manager.credentials_exception
        #
        #     home_controller=UserController()
        #     model = home_controller.get_my_alert(database=self.__database,
        #                                                 request=request_manager)
        #     body_data = model.get_response_form_data(self._head_parser)
        #     response = request_manager.make_json_response(body_data=body_data)
        #     return response

#----------------------------------------신형(만)--------------------------------------------------
    def new_my_page_route(self):
        @self.__app.get('/user_home/my_data')
        def try_get_my_page(request, raw_request:dict):
            request_manager = RequestManager()

            data_payload = DummyRequest()
            request_manager.try_view_management_need_authorized(data_payload=data_payload, cookies=request.cookies)
            if not request_manager.jwt_payload.result:
                raise request_manager.credentials_exception

            user_controller = UserController()
            model = user_controller.try_get_user_page(database=self.__database,request=request_manager)
            body_data = model.get_response_form_data(self._head_parser)
            response = request_manager.make_json_response(body_data=body_data)
            return response

        # 비밀번호 변경하기
        @self.__app.post('/user_home/try_change_password')
        def try_change_password(request:Request, raw_request:dict):
            request_manager = RequestManager()

            data_payload = ChangePasswordRequest(request=raw_request)
            request_manager.try_view_management_need_authorized(data_payload=data_payload, cookies=request.cookies)
            if not request_manager.jwt_payload.result:
                raise request_manager.credentials_exception

            home_controller=UserController()
            model = home_controller.try_change_password(database=self.__database,
                                                        request=request_manager)
            body_data = model.get_response_form_data(self._head_parser)
            response = request_manager.make_json_response(body_data=body_data)
            return response

        # 닉네임 바꾸기
        @self.__app.get('/user_home/try_change_nickname')
        def try_chagne_nickname(request:Request, index:Optional[int], custom:Optional[str]=""):
            request_manager = RequestManager()

            data_payload  = ChangeNicknameRequest(index=index, custom=custom)
            request_manager.try_view_management_need_authorized(data_payload=data_payload, cookies=request.cookies)
            if not request_manager.jwt_payload.result:
                raise request_manager.credentials_exception

            home_controller=UserController()
            model = home_controller.try_change_nickname(database=self.__database,
                                                        request=request_manager)
            body_data = model.get_response_form_data(self._head_parser)
            response = request_manager.make_json_response(body_data=body_data)
            return response

        # 종류가 나뉘어진다.
        # 포스트 (Long), 모멘트(Short)를 따로둡니다. (인터페이스를 분리할까 고민 중)
        # 댓글은 이미 동작이 O, 좋아요는 좋아요한 것만 뜨게

        # 내가 쓴 글
        @self.__app.get('/user_home/get_my_feed')
        def get_my_feed(request:Request, fid:Optional[str] = ""):
            request_manager = RequestManager()

            data_payload = MyFeedRequest(fid=fid)
            request_manager.try_view_management_need_authorized(data_payload=data_payload, cookies=request.cookies)
            if not request_manager.jwt_payload.result:
                raise request_manager.credentials_exception

            # home_controller=UserController()
            # # model = home_controller.get_my_feed(database=self.__database,
            # #                                             request=request_manager,
            # #                                             feed_manager=self.__feed_manager)
            # body_data = model.get_response_form_data(self._head_parser)
            response = request_manager.make_json_response(body_data=body_data)
            return response

        # 내가 좋아요 한 거
        @self.__app.get('/user_home/get_stared_feed')
        def get_stared_feed(request:Request, fid:Optional[str] = ""):
            request_manager = RequestManager()

            data_payload = MyFeedRequest(fid=fid)
            request_manager.try_view_management_need_authorized(data_payload=data_payload, cookies=request.cookies)
            if not request_manager.jwt_payload.result:
                raise request_manager.credentials_exception

            # home_controller=UserController()
            # model = home_controller.get_staring_feed(database=self.__database,
            #                                          request=request_manager,
            #                                          feed_manager=self.__feed_manager)
            # body_data = model.get_response_form_data(self._head_parser)
            response = request_manager.make_json_response(body_data=body_data)
            return response

        # 내가 상호작용한 거
        # @self.__app.get('/user_home/get_interactied_feed')
        # def get_interactied_feed(request:Request, fid:Optional[str] = ""):
        #     request_manager = RequestManager()
        #
        #     data_payload = MyFeedRequest(fid=fid)
        #     request_manager.try_view_management_need_authorized(data_payload=data_payload, cookies=request.cookies)
        #     if not request_manager.jwt_payload.result:
        #         raise request_manager.credentials_exception
        #
        #     home_controller=UserController()
        #     model = home_controller.get_interacted_feed(database=self.__database,
        #                                                  request=request_manager,
        #                                                  feed_manager=self.__feed_manager)
        #     body_data = model.get_response_form_data(self._head_parser)
        #     response = request_manager.make_json_response(body_data=body_data)
        #     return response

        # 내 댓글
        @self.__app.get('/user_home/get_my_comments')
        def get_my_comment(request:Request, cid:Optional[str] = ""):
            request_manager = RequestManager()

            data_payload = MyCommentRequest(cid=cid)
            request_manager.try_view_management_need_authorized(data_payload=data_payload, cookies=request.cookies)
            if not request_manager.jwt_payload.result:
                raise request_manager.credentials_exception

            home_controller=UserController()
            model = home_controller.get_my_comments(database=self.__database,
                                                    request=request_manager,
                                                    feed_manager=self.__feed_manager)
            body_data = model.get_response_form_data(self._head_parser)
            response = request_manager.make_json_response(body_data=body_data)
            return response


class DummyRequest():
    def __init__(self) -> None:
        pass

class ChangeNicknameRequest():
    def __init__(self, index, custom) -> None:
        self.index = index
        self.custom =custom
        pass

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

class ChangePasswordRequest(RequestHeader):
    def __init__(self, request) -> None:
        super().__init__(request)
        body = request['body']
        self.password = body['password']
        self.new_password= body['new_password']

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

class MyFeedRequest():
    def __init__(self, fid) -> None:
        self.fid= fid

class MyCommentRequest():
    def __init__(self, cid) -> None:
        self.cid=cid 

class MyAlertRequest():
    def __init__(self, aid) -> None:
        self.aid = aid