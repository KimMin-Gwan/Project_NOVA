        @self.__app.get('/home/hot_hashtag')
        def get_hot_hashtag(request:Request):
            request_manager = RequestManager(secret_key=self.__jwt_secret_key)
            data_payload = DummyRequest()
            request_manager.try_view_management(data_payload=data_payload, cookies=request.cookies)

            home_controller=Home_Controller(feed_manager=self.__feed_manager)

            # 만약 인기 해시태그의 리스트가 0이면 어떻게 다른걸 해야됨!!
            model = home_controller.get_hot_hashtag(database=self.__database,
                                                        request=request_manager,
                                                        feed_search_engine=self.__feed_search_engine)
            body_data = model.get_response_form_data(self._head_parser)
            response = request_manager.make_json_response(body_data=body_data)
            return response
        
        
        
        @self.__app.get('/home/realtime_best_hashtag')
        def get_realtime_best_hashtag(request:Request):
            request_manager = RequestManager(secret_key=self.__jwt_secret_key)
            data_payload = DummyRequest()
            request_manager.try_view_management(data_payload=data_payload, cookies=request.cookies)
            #if not request_manager.jwt_payload.result:
                #raise request_manager.credentials_exception

            home_controller=Home_Controller(feed_manager=self.__feed_manager)
            model = home_controller.get_realtime_best_hashtag(database=self.__database,
                                                        request=request_manager,
                                                        feed_search_engine=self.__feed_search_engine)
            body_data = model.get_response_form_data(self._head_parser)
            response = request_manager.make_json_response(body_data=body_data)
            return response

        @self.__app.get('/home/today_spiked_hot_hashtag')
        def get_today_hot_hashtag(request:Request):
            request_manager = RequestManager(secret_key=self.__jwt_secret_key)
            data_payload = DummyRequest()
            request_manager.try_view_management(data_payload=data_payload, cookies=request.cookies)

            # if not request_manager.jwt_payload.result:
            #     raise request_manager.credentials_exception
            home_controller=Home_Controller(feed_manager=self.__feed_manager)
            model = home_controller.get_today_best_hashtag(database=self.__database,
                                                           request=request_manager,
                                                           feed_search_engine=self.__feed_search_engine)
            body_data = model.get_response_form_data(self._head_parser)
            response = request_manager.make_json_response(body_data=body_data)

            return response

        # 이거 까지
        @self.__app.get('/home/weekly_spiked_hot_hashtag')
        def get_weekly_hot_hashtag(request:Request):
            request_manager = RequestManager(secret_key=self.__jwt_secret_key)
            data_payload = DummyRequest()
            request_manager.try_view_management(data_payload=data_payload, cookies=request.cookies)

            # if not request_manager.jwt_payload.result:
            #     raise request_manager.credentials_exception
            home_controller=Home_Controller(feed_manager=self.__feed_manager)
            model = home_controller.get_weekly_best_hashtag(database=self.__database,
                                                            request=request_manager,
                                                            feed_search_engine=self.__feed_search_engine)
            body_data = model.get_response_form_data(self._head_parser)
            response = request_manager.make_json_response(body_data=body_data)

            return response
                # /home/search_feed_with_hashtag?hashtag=뭐
        @self.__app.get('/home/search_feed_with_hashtag')
        def get_hot_hashtag_feed(request:Request, hashtag:Optional[str], target_time:Optional[str]=""):

            request_manager = RequestManager(secret_key=self.__jwt_secret_key)

            data_payload = HashtagFeedRequest(hashtag=hashtag, target_time=target_time)

            request_manager.try_view_management(data_payload=data_payload, cookies=request.cookies)
            #if not request_manager.jwt_payload.result:
                #raise request_manager.credentials_exception

            feed_controller=Feed_Controller(feed_manager=self.__feed_manager)
            model = feed_controller.get_feed_with_hashtag(database=self.__database,
                                                        request=request_manager,
                                                        feed_search_engine=self.__feed_search_engine,
                                                        feed_manager=self.__feed_manager,
                                                        num_feed=5)

            body_data = model.get_response_form_data(self._head_parser)
            #pprint(body_data)
            response = request_manager.make_json_response(body_data=body_data)
            return response
        
        # /home/search_feed_with_bid?bid=뭐
        @self.__app.get('/home/search_feed_with_bid')
        def get_feed_with_bid(request:Request, bid:Optional[str]=""):

            request_manager = RequestManager(secret_key=self.__jwt_secret_key)

            data_payload = GetFeedBidRequest(bid=bid)

            request_manager.try_view_management(data_payload=data_payload, cookies=request.cookies)
            #if not request_manager.jwt_payload.result:
                #raise request_manager.credentials_exception

            feed_controller=Feed_Controller(feed_manager=self.__feed_manager)
            model = feed_controller.get_feed_with_bid(database=self.__database,
                                                        request=request_manager,
                                                        feed_search_engine=self.__feed_search_engine,
                                                        num_feed=5)

            body_data = model.get_response_form_data(self._head_parser)
            #pprint(body_data)
            response = request_manager.make_json_response(body_data=body_data)
            return response
        
        # 추천 키워드 시스템.
        # 현재는 일부러 주간 핫태그를 내보내도록 했습니다.
        @self.__app.get('/home_search/get_recommend_keyword')
        def get_recommend_keyword(request:Request):
            request_manager = RequestManager(secret_key=self.__jwt_secret_key)
            data_payload = DummyRequest()
            request_manager.try_view_management(data_payload=data_payload, cookies=request.cookies)

            home_controller = Home_Controller(feed_manager=self.__feed_manager)
            model = home_controller.get_recommend_keyword(database=self.__database,
                                                          request=request_manager,
                                                          feed_search_engine=self.__feed_search_engine,
                                                          )
            body_data = model.get_response_form_data(self._head_parser)
            response = request_manager.make_json_response(body_data=body_data)
            return response
        
        
        # 오늘의 인기 게시글
        @self.__app.get('/home/today_best')
        def get_feed_data(request:Request, key:Optional[int] = -1):
            request_manager = RequestManager(secret_key=self.__jwt_secret_key)
            data_payload = HomeFeedRequest(key=-1)
            request_manager.try_view_management(data_payload=data_payload, cookies=request.cookies)
            #if not request_manager.jwt_payload.result:
                #raise request_manager.credentials_exception

            feed_controller =Feed_Controller(feed_manager=self.__feed_manager)
            model = feed_controller.get_today_best(database=self.__database,
                                                    request=request_manager,
                                                    feed_search_engine=self.__feed_search_engine,
                                                    num_feed=4)

            body_data = model.get_response_form_data(self._head_parser)
            response = request_manager.make_json_response(body_data=body_data)
            return response

        # 주간 베스트 피드
        @self.__app.get('/home/weekly_best')
        def get_feed_data(request:Request, key:Optional[int] = -1):
            request_manager = RequestManager(secret_key=self.__jwt_secret_key)
            data_payload = HomeFeedRequest(key=-1)
            request_manager.try_view_management(data_payload=data_payload, cookies=request.cookies)
            #if not request_manager.jwt_payload.result:
                #raise request_manager.credentials_exception

            feed_controller =Feed_Controller(feed_manager=self.__feed_manager)
            model = feed_controller.get_weekly_best(database=self.__database,
                                                    request=request_manager,
                                                    feed_search_engine=self.__feed_search_engine,
                                                    num_feed=4)

            body_data = model.get_response_form_data(self._head_parser)
            response = request_manager.make_json_response(body_data=body_data)
            return response
        
        
        # 피드 자세히 보기 (피드 페이지)의 피드 데이터 -> AI가 필터링 한거 무시하고 원본 보기 
        @self.__app.get('/feed_explore/original_feed_data')
        def get_original_feed_data(fid:Optional[str]):
            data_payload = GetFeedRequest(fid=fid)

            feed_controller =Feed_Controller(feed_manager=self.__feed_manager)
            model = feed_controller.get_original_feed_data(database=self.__database,
                                                           data_payload=data_payload)

            body_data = model.get_response_form_data(self._head_parser)
            # pprint(body_data)
            return body_data
        
                # 피드 자세히 보기 (피드 페이지)의 피드 데이터
        @self.__app.get('/feed_explore/original_comment_data')
        def get_original_comment_data(cid:Optional[str]):
            data_payload = CommentRequest(cid=cid)

            feed_controller =Feed_Controller(feed_manager=self.__feed_manager)
            model = feed_controller.get_original_comment_data(database=self.__database,
                                                            data_payload=data_payload)

            body_data = model.get_response_form_data(self._head_parser)
            return body_data
        
          #      # 피드 자세히 보기의 댓글 데이터
        #@self.__app.get('/feed_explore/feed_detail/comment_data')
        #def get_feed_detail(request:Request, fid:Optional[str]):
            #request_manager = RequestManager(secret_key=self.__jwt_secret_key)
            #data_payload = GetFeedRequest(fid=fid)

            #request_manager.try_view_management(data_payload=data_payload, cookies=request.cookies)
            ##if not request_manager.jwt_payload.result:
                ##raise request_manager.credentials_exception

            #feed_controller =Feed_Controller(feed_manager=self.__feed_manager)
            #model = feed_controller.get_all_comment_on_feed(database=self.__database,
                                                        #request=request_manager)

            #body_data = model.get_response_form_data(self._head_parser)

            ## pprint("댓글데이터")
            ## pprint(body_data)
            #response = request_manager.make_json_response(body_data=body_data)
            #return response
            
        # 해시태그로 검색
        @self.__app.get('/feed_explore/search_feed_with_hashtag')
        def search_feed_with_hashtag(request:Request, hashtag:Optional[str], target_time:Optional[str]="", key:Optional[int]=-1):
            request_manager = RequestManager(secret_key=self.__jwt_secret_key)
            data_payload = HashtagFeedRequest(hashtag=hashtag, target_time=target_time, key=key)
            request_manager.try_view_management(data_payload=data_payload, cookies=request.cookies)
            #if not request_manager.jwt_payload.result:
                #raise request_manager.credentials_exception

            feed_controller =Feed_Controller(feed_manager=self.__feed_manager)
            model = feed_controller.get_feed_with_hashtag(database=self.__database,
                                                        request=request_manager,
                                                        feed_search_engine=self.__feed_search_engine,
                                                        feed_manager=self.__feed_manager,
                                                        num_feed=5)

            body_data = model.get_response_form_data(self._head_parser)
            response = request_manager.make_json_response(body_data=body_data)
            return response
        
                # /home/search_feed_with_bid?bid=뭐
        @self.__app.get('/feed_explore/search_feed_with_bid')
        def search_feed_with_bid(request:Request, bid:Optional[str]="", key:Optional[int] = -1):

            request_manager = RequestManager(secret_key=self.__jwt_secret_key)

            data_payload = GetFeedBidRequest(bid=bid, key=key)

            request_manager.try_view_management(data_payload=data_payload, cookies=request.cookies)
            #if not request_manager.jwt_payload.result:
                #raise request_manager.credentials_exception

            home_controller=Feed_Controller(feed_manager=self.__feed_manager)
            model = home_controller.get_feed_with_bid(database=self.__database,
                                                        request=request_manager,
                                                        feed_search_engine=self.__feed_search_engine,
                                                        num_feed=3)

            body_data = model.get_response_form_data(self._head_parser)
            #pprint(body_data)
            response = request_manager.make_json_response(body_data=body_data)
            return response
        
                # 전체 게시글 불러오기
        @self.__app.get('/home/all_feed')
        def get_feed_data(request:Request, key:Optional[int] = -1):
            request_manager = RequestManager(secret_key=self.__jwt_secret_key)
            data_payload = HomeFeedRequest(key=key)
            request_manager.try_view_management(data_payload=data_payload, cookies=request.cookies)
            #if not request_manager.jwt_payload.result:
                #raise request_manager.credentials_exception

            feed_controller =Feed_Controller(feed_manager=self.__feed_manager)
            model = feed_controller.get_all_feed(database=self.__database,
                                                request=request_manager,
                                                feed_search_engine=self.__feed_search_engine,
                                                num_feed=6)

            body_data = model.get_response_form_data(self._head_parser)
            response = request_manager.make_json_response(body_data=body_data)
            return response
        
                # 오늘의 인기 게시글
        @self.__app.get('/feed_explore/today_best')
        def get_today_best_in_search(request:Request, key:Optional[int] = -1):
            request_manager = RequestManager(secret_key=self.__jwt_secret_key)
            data_payload = HomeFeedRequest(key=key)
            request_manager.try_view_management(data_payload=data_payload, cookies=request.cookies)
            #if not request_manager.jwt_payload.result:
                #raise request_manager.credentials_exception

            feed_controller =Feed_Controller(feed_manager=self.__feed_manager)
            model = feed_controller.get_today_best(database=self.__database,
                                                    request=request_manager,
                                                    feed_search_engine=self.__feed_search_engine,
                                                    num_feed=10)

            body_data = model.get_response_form_data(self._head_parser)
            response = request_manager.make_json_response(body_data=body_data)
            return response
        
        

        # 주간 베스트 피드
        @self.__app.get('/feed_explore/weekly_best')
        def get_weekly_best_in_search(request:Request, key:Optional[int] = -1):
            request_manager = RequestManager(secret_key=self.__jwt_secret_key)
            data_payload = HomeFeedRequest(key=key)
            request_manager.try_view_management(data_payload=data_payload, cookies=request.cookies)
            #if not request_manager.jwt_payload.result:
                #raise request_manager.credentials_exception

            feed_controller =Feed_Controller(feed_manager=self.__feed_manager)
            model = feed_controller.get_weekly_best(database=self.__database,
                                                    request=request_manager,
                                                    feed_search_engine=self.__feed_search_engine,
                                                    num_feed=10)

            body_data = model.get_response_form_data(self._head_parser)
            response = request_manager.make_json_response(body_data=body_data)
            return response
        
                # 임시 인터페이스.
        # 필터링 옵션을 통해 글들을 필터링 합니다.
        # 1차 필터링 (위 함수로 동작된 결과)를 끌고오지 않고, 이 함수에서 새롭게 시동합니다.
        # 1차 필터링 (BIAS, 커뮤니티 필터링), 2차 필터링 (옵션 필터링)으로 최종적으로 선별된 Feed를 반환합니다.
        # @self.__app.get('/feed_explore/feed_filtering_with_options')
        # def get_feed_filtering_with_options(request:Request, raw_request:dict):
        #     request_manager = RequestManager(secret_key=self.__jwt_secret_key)
        #     data_payload = CommunityFilteredRequest(request=raw_request)
        #     request_manager.try_view_management(data_payload=data_payload, cookies=request.cookies)
        #
        #     feed_controller =Feed_Controller(feed_manager=self.__feed_manager)
        #     # get_all_feed와 혼용할 계획
        #     model = feed_controller.get_all_feed(database=self.__database,
        #                                         request=request_manager,
        #                                         feed_search_engine=self.__feed_search_engine)
        #
        #
        #     body_data = model.get_response_form_data(self._head_parser)
        #     response = request_manager.make_json_response(body_data=body_data)
        #     return response
        
                # 숏피드에서 맨처음에 feed 데이터를 fid로 검색하기
        @self.__app.get('/feed_explore/get_feed')
        def get_feed_data(request:Request, fid:Optional[str]="" ):
            request_manager = RequestManager(secret_key=self.__jwt_secret_key)
            data_payload = GetFeedRequest(fid=fid)
            request_manager.try_view_management(data_payload=data_payload, cookies=request.cookies)
            #if not request_manager.jwt_payload.result:
                #raise request_manager.credentials_exception

            feed_controller =Feed_Controller(feed_manager=self.__feed_manager)
            model = feed_controller.try_search_in_fid(database=self.__database,
                                                      request=request_manager,
                                                      feed_search_engine=self.__feed_search_engine,
                                                      feed_manager=self.__feed_manager)

            body_data = model.get_response_form_data(self._head_parser)
            response = request_manager.make_json_response(body_data=body_data)
            return response
        
        
        # feed 랑 상호작용 -> 버튼을 눌렀을 때 ( 홈 또는 위성 탐색 페이지에서 사용) -> 투표기능? 뭐 그런거임
        @self.__app.get('/feed_explore/interaction_feed')
        def try_interaction_feed(request:Request, fid:Optional[str], action:Optional[int]):
            request_manager = RequestManager(secret_key=self.__jwt_secret_key)
            data_payload = FeedInteractionRequest(fid=fid, action=action)
            request_manager.try_view_management_need_authorized(data_payload=data_payload, cookies=request.cookies)
            if not request_manager.jwt_payload.result:
                raise request_manager.credentials_exception

            feed_controller =Feed_Controller(feed_manager=self.__feed_manager)
            model = feed_controller.try_interact_feed(database=self.__database,
                                                        request=request_manager,
                                                        feed_manager=self.__feed_manager)
            
            body_data = model.get_response_form_data(self._head_parser)
            response = request_manager.make_json_response(body_data=body_data)
            return response
        
               # feed 랑 상호작용 -> 댓글 달기
        @self.__app.post('/feed_explore/make_comment')
        def try_make_comment(request:Request, raw_requset:dict):
            request_manager = RequestManager(secret_key=self.__jwt_secret_key)
            data_payload = MakeFeedCommentRequest(request=raw_requset)

            request_manager.try_view_management_need_authorized(data_payload=data_payload, cookies=request.cookies)
            if not request_manager.jwt_payload.result:
                raise request_manager.credentials_exception

            feed_controller =Feed_Controller(feed_manager=self.__feed_manager)
            model = feed_controller.try_make_comment(database=self.__database,
                                                        request=request_manager,
                                                        feed_manager=self.__feed_manager,
                                                        ai_manager=self.__ai_manager
                                                        )
            body_data = model.get_response_form_data(self._head_parser)
            response = request_manager.make_json_response(body_data=body_data)
            return response
        
                # feed 랑 상호작용 -> 댓글 지우기
        @self.__app.get('/feed_explore/remove_comment')
        def try_remove_comment(request:Request, fid:Optional[str], cid:Optional[str]):
            request_manager = RequestManager(secret_key=self.__jwt_secret_key)

            data_payload = RemoveCommentRequest(fid=fid, cid=cid)
            request_manager.try_view_management_need_authorized(data_payload=data_payload, cookies=request.cookies)
            if not request_manager.jwt_payload.result:
                raise request_manager.credentials_exception

            feed_controller =Feed_Controller(feed_manager=self.__feed_manager)
            model = feed_controller.try_remove_comment(database=self.__database,
                                                        request=request_manager,
                                                        feed_manager=self.__feed_manager)
            body_data = model.get_response_form_data(self._head_parser)
            response = request_manager.make_json_response(body_data=body_data)
            return response
        
                # def try_make_reply_comment(request:Request, raw_requset:dict):
        #     request_manager = RequestManager(secret_key=self.__jwt_secret_key)
        #     data_payload = MakeFeedCommentRequest(request=raw_requset)
        #
        #     request_manager.try_view_management_need_authorized(data_payload=data_payload, cookies=request.cookies)
        #     if not request_manager.jwt_payload.result:
        #         raise request_manager.credentials_exception
        #
        #     feed_controller =Feed_Controller(feed_manager=self.__feed_manager)
        #     model = feed_controller.try_make_comment(database=self.__database,
        #                                              request=request_manager,
        #                                              feed_manager=self.__feed_manager)
        #     body_data = model.get_response_form_data(self._head_parser)
        #     response = request_manager.make_json_response(body_data=body_data)
        #     return response
        
                # feed 랑 상호작용 -> 댓글 좋아요 하기
        @self.__app.get('/feed_explore/like_comment')
        def try_like_comment(request:Request, fid:Optional[str], cid:Optional[str]):
            request_manager = RequestManager(secret_key=self.__jwt_secret_key)

            data_payload = RemoveCommentRequest(fid=fid, cid=cid)
            request_manager.try_view_management_need_authorized(data_payload=data_payload, cookies=request.cookies)
            if not request_manager.jwt_payload.result:
                raise request_manager.credentials_exception

            feed_controller =Feed_Controller(feed_manager=self.__feed_manager)
            model = feed_controller.try_like_comment(database=self.__database,
                                                        request=request_manager,
                                                        feed_manager=self.__feed_manager)
            body_data = model.get_response_form_data(self._head_parser)
            response = request_manager.make_json_response(body_data=body_data)
            return response
        
                ##채팅서버
        ##  @self.__app.get('/chatting_list')
        ##def get_chatting_list():
            ##core_controller=Core_Controller()
            ##model = core_controller.get_chatting_data(database=self.__database,)
            ##response = model.get_response_form_data(self._head_parser)
            ##return response
            
        #@self.__app.websocket('/chatting')
        #async def chatting_socket(websocket:WebSocket):
            #self.manager = ConnectionManager()
            #core_controller=Core_Controller()
            #await self.manager.connect(websocket)
            #try:
                #while True:
                    ##{"token":"token"."message":"msg"}
                    #request = await websocket.receive_text()
                    #model = core_controller.chatting(database=self.__database, request=request)
                    #if model.get_check() == True:
                        #await self.manager.broadcast(f"{model._user.uname} :{model.get_chat_data().message}")
                    #else:
                        #continue
                
            #except WebSocketDisconnect:
                #self.manager.disconnect(websocket)
            #    await self.manager.broadcast("client disconnected")

        # 최애를 검색하는 보편적인 함수
        # 목적 : 나의 최애 선택하기, 홈화면의 최애 검색 기능
        #"http://127.0.0.1:6000/home/search_bias?bias_name=김"  # bias 검색
        #@self.__app.get('/league_detail/league_meta_data')
        #def get_league_meta_data():
            #home_controller=Home_Controller()
            #model = home_controller.get_league_meta_data(database=self.__database, league_manager=self.__league_manager)
            #response = model.get_response_form_data(self._head_parser)
            #return response
            
        #@self.__app.websocket('/league_detail/league_data')
        #async def league_socket(websocket:WebSocket, league_name:Optional[str] = ""):
            #try:
                #if league_name == "":
                    #return
                #observer = await self.__connection_manager.connect(lname=league_name,
                                                                     #websocket=websocket,
                                                                     #league_manager=self.__league_manager,
                                                                     #)
                #result = await observer.send_operation()
                #if not result:
                    #self.__connection_manager.disconnect(observer=observer)

            #except ConnectionClosedError:
                #self.__connection_manager.disconnect(observer=observer)
                
            #except WebSocketDisconnect:
                #self.__connection_manager.disconnect(observer=observer)
                
                        # feed 랑 상호작용 -> 댓글 모두보기
        @self.__app.get('/feed_explore/view_comment')
        def get_all_comment(request:Request, fid:Optional[str], cid:Optional[str]):
            request_manager = RequestManager(secret_key=self.__jwt_secret_key)

            data_payload = GetAllCommentRequest(fid=fid, cid=cid)
            request_manager.try_view_management(data_payload=data_payload, cookies=request.cookies)
            #if not request_manager.jwt_payload.result:
                #raise request_manager.credentials_exception

            feed_controller =Feed_Controller(feed_manager=self.__feed_manager)
            model = feed_controller.get_all_comment_on_feed(database=self.__database,
                                                        request=request_manager)
            body_data = model.get_response_form_data(self._head_parser)
            response = request_manager.make_json_response(body_data=body_data)
            return response
        
        # 나의 최애 선택하기 (다시 누르면 취소하기됨0)
        @self.__app.post('/home/try_select_my_bias')
        def try_select_my_bias(request:Request, raw_request:dict):
            request_manager = RequestManager(secret_key=self.__jwt_secret_key)

            data_payload = BiasSelectRequest(request=raw_request)
            request_manager.try_view_management_need_authorized(data_payload=data_payload, cookies=request.cookies)

            home_controller=Home_Controller()
            model = home_controller.select_bias(database=self.__database,
                                                 request=request_manager,
                                                 feed_search_engine=self.__feed_search_engine)
            body_data = model.get_response_form_data(self._head_parser)
            response = request_manager.make_json_response(body_data=body_data)
            return response

class ConnectionManager:
    def __init__(self):
        self.active_connection: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connection.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connection.remove(websocket)

    async def broadcast(self, message:str):
        for connection in self.active_connection:
            await connection.send_text(message)