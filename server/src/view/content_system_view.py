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
        test_connection_manager:TC, jwt_secret_key
        ):
        super().__init__(head_parser=head_parser)
        self.__app = app
        self._endpoint = endpoint
        self.__database = database
        self.__test_connection_manager = test_connection_manager
        self.__jwt_secret_key = jwt_secret_key
        
    def home_route(self, endpoint:str):
        @self.__app.get(endpoint + "/home")
        def home():
            return "bad request"
        
        @self.__app.get('/content_system/get_music_content')
        def get_music_content(request:Request, type:Optional[str]="default"):
            request_manager = RequestManager(secret_key=self.__jwt_secret_key)

            data_payload = GetContentRequest(type=type)
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
                
                request_manager = RequestManager(secret_key=self.__jwt_secret_key)
                if uid == "-1":
                    uid = ""
                data_payload= GetContentRequest()
                request_manager.try_view_just_data_payload(data_payload=data_payload)
                
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
    def __init__(self, type) -> None:
        self.type = type