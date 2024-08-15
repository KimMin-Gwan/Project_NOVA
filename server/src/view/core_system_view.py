from typing import Any
from fastapi import FastAPI
from view.master_view import Master_View, RequestHeader
from view.parsers import Head_Parser
from controller import Core_Controller

class Core_Service_View(Master_View):
    def __init__(self, app:FastAPI, endpoint:str, database, head_parser:Head_Parser) -> None:
        super().__init__(head_parser=head_parser)
        self.__app = app
        self._endpoint = endpoint
        self.__database = database
        self.register_route(endpoint)

    def register_route(self, endpoint:str):
        @self.__app.get(endpoint+'/home')
        def home():
            return 'Hello, This is Root of Core-System Service'
        
        @self.__app.get(endpoint+'/{sample}')
        def sample_post(sample:str):
            request = sample
            core_controller=Core_Controller()
            model = core_controller.sample_func(database=self.__database,
                                                             request=request)
            response = model.get_response_form_data(self._head_parser)
            return response
        
        @self.__app.post(endpoint+'/home/login')
        def login(raw_request:dict):
            request = LoginRequest(request=raw_request)
            core_controller=Core_Controller()
            model = core_controller.get_my_bias_league(database=self.__database,
                                                             request=request)
            response = model.get_response_form_data(self._head_parser)
            return response
        
        @self.__app.post(endpoint+'/home/daily')
        def daily_request(raw_request:dict):
            request = DailyRequest(request=raw_request)
            core_controller=Core_Controller()
            model = core_controller.get_my_bias_league(database=self.__database,
                                                             request=request)
            response = model.get_response_form_data(self._head_parser)
            return response
        
        @self.__app.get('/home/my_bias/{email}/{token}')
        def sample_post(email:str, token:str):
            request = {
                'token' : token,
                'email' : email
            }
            core_controller=Core_Controller()
            model = core_controller.get_my_bias_league(database=self.__database,
                                                             request=request)
            response = model.get_response_form_data(self._head_parser)
            return response

        @self.__app.get('/home/show_all_leagues')
        def show_all_leagues():
            core_controller=Core_Controller()
            model = core_controller.get_all_leagues(database=self.__database)
            response = model.get_response_form_data(self._head_parser)
            return response
        
        @self.__app.get('/home/get_solo_leagues/{league_id}')
        def get_solo_leagues(league_id:str):
            request = league_id
            core_controller=Core_Controller()
            model = core_controller.get_solo_league(database=self.__database,
                                                    request=request)
            response = model.get_response_form_data(self._head_parser)
            return response
        
        @self.__app.get('/home/get_group_leagues/{league_id}')
        def get_group_leagues(league_id:str):
            request = league_id
            core_controller=Core_Controller()
            model = core_controller.get_group_league(database=self.__database,
                                                     request=request)
            response = model.get_response_form_data(self._head_parser)
            return response
        

        @self.__app.post(endpoint+'/post_sample')
        def sample_post(raw_request:dict):
            request = SampleRequest(request=raw_request)
            core_controller=Core_Controller()
            model = core_controller.sample_func(database=self.__database,
                                                             request=request)
            response = model.get_response_form_data(self._head_parser)
            return response

class SampleRequest(RequestHeader):
    def __init__(self, request) -> None:
        super().__init__(request)
        body = request['body']
        self.uid = body['uid']
        self.date = body['date']

class LoginRequest(RequestHeader):
    def __init__(self, request) -> None:
        super().__init__(request)
        body = request['body']
        self.email = body['email']
        self.token = body['token']

class DailyRequest(RequestHeader):
    def __init__(self, request) -> None:
        super().__init__(request)
        body = request['body']
        self.email = body['email']
        self.token = body['token']






