       # 임시 URL주소. 바꾸면 됨
        # 사이드박스에서 각 BIAS별 설정된 Board_type(게시판들)과, BIAS의 플랫폼, 인스타 등 주소를 보내야 함.
        # 펀딩부분은 뭐.. 프론트에서 URL로 이어주겠죠?
        @self.__app.get('/nova_sub_system/try_get_community_side_box')
        def try_get_community_side_box(bid:Optional[str] = ""):
            data_payload = CommunitySideBoxRequest(bid=bid)

            sub_controller=Sub_Controller()
            model = sub_controller.try_get_community_side_box(database=self.__database,
                                                              data_payload=data_payload)
            body_data = model.get_response_form_data(self._head_parser)
            return body_data
        
        # 나이변경 기능
        @self.__app.post('/nova_sub_system/try_change_users_age')
        def try_change_users_age(request:Request):
            request_manager = RequestManager(secret_key=self.__jwt_secret_key)
            request_manager.try_view_management(cookies=request.cookies)

            sub_controller=Sub_Controller()
            model = sub_controller.try_change_users_age(database=self.__database,
                                                        request=request_manager)
            body_data = model.get_response_form_data(self._head_parser)
            response = request_manager.make_json_response(body_data=body_data)
            return response
        
        
class CommunitySideBoxRequest(RequestHeader):
    def __init__(self, bid) -> None:
        self.bid=bid