from typing import Any, Optional
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request
from view.master_view import Master_View, RequestHeader
from view.parsers import Head_Parser
from controller import Home_Controller, Core_Controller, UserController
from view.jwt_decoder import RequestManager

class User_Service_View(Master_View):
    def __init__(self, app:FastAPI, endpoint:str, database, head_parser:Head_Parser,
                 nova_verification
                 ) -> None:
        super().__init__(head_parser=head_parser)
        self.__app = app
        self._endpoint = endpoint
        self.__database = database
        self.__nova_verification = nova_verification
        self.user_route(endpoint)

    def user_route(self, endpoint:str):
        @self.__app.get(endpoint+'/user')
        def home():
            return 'Hello, This is User system'
        
        # 로그인 시도
        # response 포함 정보 -> 'result' : True or False
        #                    -> 'detail' : "실패 사유"
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

        # 회원가입 시도
        # response 포함 정보 -> 'result' : True or False
        #                    -> 'detail' : "실패 사유"
        @self.__app.post('/user_home/try_sign_in')
        def try_sign_in(raw_request:dict):
            request = SignInRequest(request=raw_request)
            user_controller=UserController()
            model = user_controller.try_sign_in(database=self.__database,
                                                   request = request,
                                              nova_verification=self.__nova_verification)
            response = model.get_response_form_data(self._head_parser)
            return response

class LoginRequest(RequestHeader):
    def __init__(self, request) -> None:
        super().__init__(request)
        body = request['body']
        self.email = body['email']
        self.password = body['password']

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
        self.verification_code = body['verification_code']
        self.age = body['age']
        self.gender = body['gender']

