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
        
                # Bias 서치
        # 팔로워 서치부분과는 다르게  둠
        # New Model에 대한 테스트 완료
        @self.__app.get('/time_table_server/try_search_bias')
        def try_search_bias_with_keyword(request:Request,  keyword:Optional[str]="", key:Optional[int]=-1):
            request_manager = RequestManager(secret_key=self.__jwt_secret_key)
            data_payload = SearchRequest(keyword=keyword, key=key, search_type="bias")
            request_manager.try_view_management(data_payload=data_payload, cookies=request.cookies)

            time_table_controller =TImeTableController()
            model = time_table_controller.try_search_bias_with_keyword(database=self.__database,
                                                                       request=request_manager,
                                                                       num_biases=15)

            body_data = model.get_response_form_data(self._head_parser)
            response = request_manager.make_json_response(body_data=body_data)
            return response
        
                # 테스트용
        # 날짜에 따라 잘되는지 테스트
        # @self.__app.get('/time_table_server/get_specific_schedules')
        # def try_get_specific_schedules(request:Request, target_date:Optional[str], num_schedules:Optional[int], key:Optional[int]=-1):
        #     request_manager = RequestManager(secret_key=self.__jwt_secret_key)
        #     data_payload = TestGetSpecificRequest(target_date=target_date, num_schedules=num_schedules, key=key)
        #     request_manager.try_view_management(data_payload=data_payload, cookies=request.cookies)
        #
        #     time_table_controller =TImeTableController()
        #     model = time_table_controller.try_get_specific_schedules(database=self.__database,
        #                                                              schedule_search_engine=self.__schedule_search_engine,
        #                                                              request=request_manager)
        #
        #     body_data = model.get_response_form_data(self._head_parser)
        #     response = request_manager.make_json_response(body_data=body_data)
        #     return response
        
                # 1.5버전까지 반려됨
        # 이벤트는 이곳으로 추가함
        #@self.__app.get('/time_table_server/try_add_event')
        #def try_add_event(request:Request, seid:Optional[str]):
            #request_manager = RequestManager(secret_key=self.__jwt_secret_key)
            #data_payload = AddNewEventRequest(seid=seid)
            #request_manager.try_view_management_need_authorized(data_payload=data_payload, cookies=request.cookies)

            #time_table_controller =TImeTableController()
            #model = time_table_controller.try_add_event(database=self.__database,
                                                        #request=request_manager)
            
            #body_data = model.get_response_form_data(self._head_parser)
            #response = request_manager.make_json_response(body_data=body_data)
            #return response
            
                    
        ## 완료
        ## 홈화면에 노출될 스케줄 정하는건 여기서 함
        #@self.__app.get('/time_table_server/try_select_my_time_table_schedule')
        #def try_select_my_time_table_schedule(request:Request, date:Optional[str],bid:Optional[str]=""):
            #request_manager = RequestManager(secret_key=self.__jwt_secret_key)
            #data_payload = SelectMyTimeTableRequest(date=date, bid=bid)
            #request_manager.try_view_management_need_authorized(data_payload=data_payload, cookies=request.cookies)

            #time_table_controller =TImeTableController()
            #model = time_table_controller.try_select_my_time_table_schedule(database=self.__database,
                                                                            #request=request_manager)
            
            #body_data = model.get_response_form_data(self._head_parser)
            #response = request_manager.make_json_response(body_data=body_data)
            #return response
        
        
                # 완료
        # bid에서 내가 선택했는 스케줄들 볼때 쓰는 엔드 포인트. 로그인 필수
        # 테스트는 아직 못함
        # @self.__app.get('/time_table_server/try_search_my_schedule_with_bid')
        # def try_search_my_schedule_with_bid(request:Request, bid:Optional[str]="", key:Optional[int]=-1):
        #     request_manager = RequestManager(secret_key=self.__jwt_secret_key)
        #     data_payload = ScheduleWithBidRequest(bid=bid, key=key)
        #     request_manager.try_view_management_need_authorized(data_payload=data_payload, cookies=request.cookies)
        #
        #     time_table_controller =TImeTableController()
        #     model = time_table_controller.try_search_my_schedule_with_bid(database=self.__database,
        #                                                                 request=request_manager)
        #
        #     body_data = model.get_response_form_data(self._head_parser)
        #     response = request_manager.make_json_response(body_data=body_data)
        #     return response
        
        
        # 내가 담아놓은 스케줄들을 볼 수 있습니다.
        # 테스트 완료
        @self.__app.get('/time_table_server/try_search_my_schedule_with_bid')
        def try_get_my_selected_schedules(request:Request, bid:Optional[str]="", key:Optional[int]=-1):
            request_manager = RequestManager(secret_key=self.__jwt_secret_key)
            data_payload = ScheduleWithBidRequest(bid=bid, key=key)
            request_manager.try_view_management_need_authorized(data_payload=data_payload, cookies=request.cookies)
            # request_manager.try_view_management(data_payload=data_payload, cookies=request.cookies)

            time_table_controller =TImeTableController()
            model = time_table_controller.try_get_my_selected_schedules(schedule_search_engine=self.__schedule_search_engine,
                                                                        database=self.__database,
                                                                        request=request_manager)

            body_data = model.get_response_form_data(self._head_parser)
            response = request_manager.make_json_response(body_data=body_data)
            return response
        
        
        # 이번 주 일정 불러오기
        @self.__app.get('/time_table_server/try_get_weekday_schedules')
        def try_get_weekday_schedules(request:Request ):
            request_manager = RequestManager(secret_key=self.__jwt_secret_key)
            data_payload = DummyRequest()
            request_manager.try_view_management_need_authorized(data_payload=data_payload, cookies=request.cookies)
            # request_manager.try_view_management(data_payload=data_payload, cookies=request.cookies)

            time_table_controller =TImeTableController()
            model = time_table_controller.try_get_weekday_schedules(schedule_search_engine=self.__schedule_search_engine,
                                                                    database=self.__database,
                                                                    request=request_manager)

            body_data = model.get_response_form_data(self._head_parser)
            response = request_manager.make_json_response(body_data=body_data)
            return response
        
                # 수정할 번들 데이터 불러오기
        @self.__app.get('/time_table_server/try_get_written_bundle')
        def try_get_written_bundle(request:Request, sbid:Optional[str]=""):
            request_manager = RequestManager(secret_key=self.__jwt_secret_key)
            data_payload = ScheduleBundleRequest(sbid=sbid)
            # request_manager.try_view_management(data_payload=data_payload, cookies=request.cookies)
            request_manager.try_view_management_need_authorized(data_payload=data_payload, cookies=request.cookies)

            time_table_controller =TImeTableController()
            model = time_table_controller.try_get_written_bundle(database=self.__database,
                                                                   request=request_manager)

            body_data = model.get_response_form_data(self._head_parser)
            response = request_manager.make_json_response(body_data=body_data)
            return response
        
                # 스케줄 번들 수정
        @self.__app.post('/time_table_server/try_modify_schedule_bundle')
        def try_modify_bundle(request:Request, raw_request:dict):
            request_manager = RequestManager(secret_key=self.__jwt_secret_key)

            pprint(raw_request['body'])
            data_payload = ModifyMultipleScheduleRequest(request=raw_request)
            # request_manager.try_view_management(data_payload=data_payload, cookies=request.cookies)
            request_manager.try_view_management_need_authorized(data_payload=data_payload, cookies=request.cookies)

            time_table_controller =TImeTableController()
            model = time_table_controller.try_modify_bundle(schedule_search_engine=self.__schedule_search_engine,
                                                            database=self.__database,
                                                            request=request_manager)

            body_data = model.get_response_form_data(self._head_parser)
            response = request_manager.make_json_response(body_data=body_data)
            return response
        
                # 번들 데이터 삭제
        # Managed_Table에 대해 테스트 완료
        @self.__app.get('/time_table_server/try_delete_bundle')
        def try_delete_bundle(request:Request, sbid:Optional[str]=""):
            request_manager = RequestManager(secret_key=self.__jwt_secret_key)
            data_payload = DeleteScheduleBundleRequest(sbid=sbid)
            request_manager.try_view_management_need_authorized(data_payload=data_payload, cookies=request.cookies)

            time_table_controller = TImeTableController()
            model = time_table_controller.try_delete_bundle(schedule_search_engine=self.__schedule_search_engine,
                                                            database=self.__database,
                                                            request=request_manager)

            body_data = model.get_response_form_data(self._head_parser)
            response = request_manager.make_json_response(body_data=body_data)
            return response