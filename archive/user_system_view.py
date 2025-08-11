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
        
        
        