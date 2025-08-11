        # 이벤트는 보류
        # 타임 테이블 페이지의 최 상단 이벤트 보드 데이터
        # 비로그인 상태에서는 date를 선택하지 않으면 그날 이벤트를 랜덤하게 3개 줄것
        # 로그인 상태에서는 date를 선택하면 그날 이벤트를 모두 줄것
        # date는 안들어오면 오늘 날짜로 자동 선택될 것임
        # date는 "2025/03/05" 형식
        #@self.__app.get('/time_table_server/try_get_eventboard_data')
        #def get_eventboard_data(request:Request, date:Optional[str]=datetime.now().strftime("%Y/%m/%d")):
            #request_manager = RequestManager(secret_key=self.__jwt_secret_key)
            #data_payload = DateRequest(date=date)
            #request_manager.try_view_management(data_payload=data_payload, cookies=request.cookies)

            #time_table_controller =TImeTableController()
            #model = time_table_controller.get_eventboard_data(database=self.__database,
                                                              #request=request_manager)
            #body_data = model.get_response_form_data(self._head_parser)
            #response = request_manager.make_json_response(body_data=body_data)

            #return response
            
        # 완료
        # 타임 차트에서 데이터 뽑아오기
        # 비로그인 상태에서는 데이터를 반환하지 않아도될듯 -> 아니면 반환할 데이터를 마련해도 될듯
        # 로그인 상태에서는 본인이 추가한 모든 일정(오늘자)이 반환되어야함
        @self.__app.get('/time_table_server/try_get_today_time_chart')
        def try_get_today_time_chart(request:Request, date:Optional[str]=datetime.now().strftime("%Y/%m/%d")):
            request_manager = RequestManager(secret_key=self.__jwt_secret_key)
            data_payload = DateRequest(date=date)
            request_manager.try_view_management(data_payload=data_payload, cookies=request.cookies)

            time_table_controller =TImeTableController()
            model = time_table_controller.get_time_chart(database=self.__database,
                                                              request=request_manager)
            
            body_data = model.get_response_form_data(self._head_parser)
            response = request_manager.make_json_response(body_data=body_data)
            return response
        
                # keyword 추천
        # 본인이 팔로우한 bias의 카테고리 위주로 제시할 듯
        # 로그인을 안했거나 팔로우한 bias가 없으면 랜덤하게 뿌리면됨
        # New Model에 대한 테스트 완료
        @self.__app.get('/time_table_server/try_get_recommend_keyword')
        def try_get_recommend_keyword(request:Request):
            request_manager = RequestManager(secret_key=self.__jwt_secret_key)
            data_payload = DummyRequest()
            request_manager.try_view_management(data_payload=data_payload, cookies=request.cookies)

            time_table_controller =TImeTableController()
            model = time_table_controller.try_get_recommend_keyword(database=self.__database,
                                                                    request=request_manager,
                                                                    num_keywords=6)

            # 반환 데이터 : 'recommend_keywords'
            body_data = model.get_response_form_data(self._head_parser)
            response = request_manager.make_json_response(body_data=body_data)
            return response