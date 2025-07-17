from typing import Optional, Union
from fastapi import FastAPI, WebSocket, Request, File, UploadFile, Form, WebSocketDisconnect
from view.master_view import Master_View, RequestHeader
from view.parsers import Head_Parser
from view.jwt_decoder import RequestManager
from controller import ContentController
from fastapi.responses import HTMLResponse
from manager import TestConnectionManager as TC
from others import FeedManager as FM
from websockets.exceptions import ConnectionClosedError


class Content_Service_view(Master_View):
    def __init__(
        self, app:FastAPI, endpoint: str,
        database, head_parser:Head_Parser,
        test_connection_manager:TC, jwt_secret_key,
        content_key_storage
        ):
        super().__init__(head_parser=head_parser)
        self.__app = app
        self._endpoint = endpoint
        self.__database = database
        self.__test_connection_manager = test_connection_manager
        self.__jwt_secret_key = jwt_secret_key
        self.__content_key_storage = content_key_storage
        self.home_route(endpoint=endpoint)
        
    def home_route(self, endpoint:str):
        @self.__app.get(endpoint + "/home")
        def home():
            return "bad request"
        
        
        @self.__app.get('/content_system/try_subscribe_chat')
        def get_num_music_content(sessionKey:Optional[str]):
            content_controller = ContentController()
            data_payload = ChzzkSubscribeRequest(session_key=sessionKey)
            
            result:dict = content_controller.try_subscribe_chat(
                data_payload=data_payload,
                content_key_storage=self.__content_key_storage
            )

            return result
        
        @self.__app.get('/content_system/try_auth_chzzk')
        def get_num_music_content(code:Optional[str], state:Optional[str]):
            content_controller = ContentController()
            data_payload = ChzzkAuthRequest(code=code, state=state)
            
            
            result:dict = content_controller.try_auth_chzzk(
                data_payload=data_payload,
                content_key_storage=self.__content_key_storage
            )
            
            return result
        
        @self.__app.get('/content_system/get_num_music_content')
        def get_num_music_content(request:Request):
            request_manager = RequestManager(secret_key=self.__jwt_secret_key)

            content_controller = ContentController()
            model = content_controller.get_num_music_content(
                database=self.__database,
                request=request_manager,
            )

            body_data = model.get_response_form_data(self._head_parser)
            response = request_manager.make_json_response(body_data=body_data)
            return response
            
        
        
        @self.__app.get('/content_system/get_music_content')
        def get_music_content(request:Request, type:Optional[str]="all", num_content:Optional[int]=0):
            request_manager = RequestManager(secret_key=self.__jwt_secret_key)

            data_payload = GetContentRequest(type=type, num_content=num_content)
            request_manager.try_view_management(data_payload=data_payload, cookies=request.cookies)


            content_controller = ContentController()
            model = content_controller.get_music_content(
                database=self.__database,
                request=request_manager,
            )

            body_data = model.get_response_form_data(self._head_parser)
            response = request_manager.make_json_response(body_data=body_data)
            return response
        
        
        @self.__app.get('/content_system/get_diff_image_content')
        def get_image_content(request:Request):
            request_manager = RequestManager(secret_key=self.__jwt_secret_key)

            data_payload = GetContentRequest(type="")
            request_manager.try_view_management(data_payload=data_payload, cookies=request.cookies)


            content_controller = ContentController()
            model = content_controller.get_diff_image_content(
                database=self.__database,
                request=request_manager,
            )

            body_data = model.get_response_form_data(self._head_parser)
            response = request_manager.make_json_response(body_data=body_data)
            return response       
        
        @self.__app.websocket('/testing_websocket')
        async def try_socket_chatting(websocket:WebSocket): 
            try:
                observer = await self.__test_connection_manager.connect(
                    websocket=websocket,
                    )
                
                result = await observer.observer_operation()
                
                if not result:
                    await self.__test_connection_manager.disconnect(observer=observer)

            except ConnectionClosedError:
                await self.__test_connection_manager.disconnect(observer=observer)
                
            except WebSocketDisconnect:
                await self.__test_connection_manager.disconnect(observer=observer)
        
            
class GetContentRequest(RequestHeader):
    def __init__(self, type="all", num_content=0) -> None:
        self.type = type
        self.num_content = num_content
        
class ChzzkAuthRequest(RequestHeader):
    def __init__(self, code, state):
        self.code = code
        self.state = state
        
class ChzzkSubscribeRequest(RequestHeader):
    def __init__(self, session_key):
        self.session_key=session_key 
        