from typing import Any, Optional
from fastapi import FastAPI, Request
from view.master_view import Master_View, RequestHeader
from view.parsers import Head_Parser
from controller import Administrator_Controller
from view.jwt_decoder import RequestManager

class Administrator_System_View(Master_View):
    def __init__(self, app:FastAPI, endpoint:str, database, head_parser:Head_Parser) -> None:
        super().__init__(head_parser=head_parser)
        self.__app = app
        self._endpoint = endpoint
        self.__database = database
        self.admin_route(endpoint)

    def admin_route(self, endpoint:str):
        # 임시 URL주소. 바꾸면 됨
        # 사이드박스에서 각 BIAS별 설정된 Board_type(게시판들)과, BIAS의 플랫폼, 인스타 등 주소를 보내야 함.
        # 펀딩부분은 뭐.. 프론트에서 URL로 이어주겠죠?
        @self.__app.get('/admin_system/try_insert_new_bias')
        def try_insert_new_bias(request:Request, raw_request:dict):
            request_manager = RequestManager(secret_key=self.__jwt_secret_key)

            data_payload = BiasInsertRequest(request=raw_request)

            request_manager.try_view_management(data_payload=data_payload, cookies=request.cookies)

            administrator_controller=Administrator_Controller()
            model = administrator_controller.bias_editor(database=self.__database,
                                                        request=request_manager,
                                                         order='add'
                                                         )
            body_data = model.get_response_form_data(self._head_parser)
            response = request_manager.make_json_response(body_data=body_data)
            return response
        
        
        

class BiasInsertRequest(RequestHeader):
    def __init__(self, request) -> None:
        super().__init__(request)
        body = request['body']
        data = body['data']
        self.admin_key = body['admin_key']
        
        self.bname = data['bname']
        self.gender = data['gender']
        self.category = data['category']
        self.birthday = data['birthday']
        self.debut = data['debut']
        self.agency = data['agency']
        self.group = data['group']
        self.num_user = data['num_user']
        self.board_types = data['board_types']
        self.x_account = data['x_account']
        self.insta_account = data['insta_account']
        self.tictok_account = data['tictok_account']
        self.youtube_account = data['youtube_account']
        self.homepage = data['homepage']
        self.fan_cafe = data['fan_cafe']
        self.country = data['country']
        self.fanname = data['fanname']
