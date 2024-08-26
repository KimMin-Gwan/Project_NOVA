from typing import Any, Optional
from fastapi import FastAPI
from view.master_view import Master_View, RequestHeader
from view.parsers import Head_Parser
from controller import Administrator_Controller

class Administrator_Service_View(Master_View):
    def __init__(self, app:FastAPI, endpoint:str, database, head_parser:Head_Parser) -> None:
        super().__init__(head_parser=head_parser)
        self.__app = app
        self._endpoint = endpoint
        self.__database = database
        self.admin_route(endpoint)

    def admin_route(self, endpoint:str):
        @self.__app.get(endpoint+'/admin')

        def home():
            return 'Hello, This is Admin System'
        
        @self.__app.post('/admin/reset_league_point')
        def reset_league_point(raw_request:dict):
            request = ResetLeaguesPointRequest(raw_request)
            administrator_controller=Administrator_Controller()
            model = administrator_controller.reset_leagues_point(database=self.__database,
                                                                 requset=request)
            response = model.get_response_form_data(self._head_parser)
            return response
        

class ResetLeaguesPointRequest(RequestHeader):
    def __init__(self, request) -> None:
        super().__init__(request)
        body = request['body']
        self.admin_key = body['admin_key']



