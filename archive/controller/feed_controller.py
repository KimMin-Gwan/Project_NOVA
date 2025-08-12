    # fid를 통한 피드 검색
    def try_search_in_fid(self, database:Mongo_Database,
                        request, feed_search_engine: FeedSearchEngine, feed_manager: FeedManager,
                        num_feed= 1):
        model = FeedSearchModelNew(database=database)
        # 유저가 있으면 세팅
        if request.jwt_payload != "":
            model.set_user_with_email(request=request.jwt_payload)
        model.try_search_feed_with_keyword(feed_search_engine=feed_search_engine,
                                               feed_manager=feed_manager,
                                               search_columns="fid",
                                               target=request.data_payload.fid
                                               )

        # model.try_search_feed_with_fid(feed_search_engine=feed_search_engine,
        #                                feed_manager=self.__feed_manager,
        #                                 fid=request.data_payload.fid)

        return model
    
    
        # 오늘의 인기 게시글
    def get_today_best(self, database:Mongo_Database,
                        request, feed_search_engine: FeedSearchEngine,
                        num_feed=4):
        model = FeedModel(database=database)
        
        # 유저가 있으면 세팅
        if request.jwt_payload != "":
            model.set_user_with_email(request=request.jwt_payload)

        model.set_best_feed_with_time(feed_search_engine=feed_search_engine,
                                      feed_manager=self.__feed_manager,
                                      search_type="best",
                                      time_type="day",
                                      last_index=request.data_payload.key,
                                      num_feed=num_feed)
        #
        # model.set_today_best_feed(feed_search_engine=feed_search_engine,
        #                             feed_manager=self.__feed_manager,
        #                             index=request.data_payload.key,
        #                             num_feed=num_feed)

        return model
    
    
    # 주간 인기 게시글
    def get_weekly_best(self, database:Mongo_Database,
                        request, feed_search_engine: FeedSearchEngine,
                        num_feed= 4):
        model = FeedModel(database=database)
        
        # 유저가 있으면 세팅
        if request.jwt_payload != "":
            model.set_user_with_email(request=request.jwt_payload)

        model.set_best_feed_with_time(feed_search_engine=feed_search_engine,
                                      feed_manager=self.__feed_manager,
                                      search_type="best",
                                      time_type="weekly",
                                      last_index=request.data_payload.key,
                                      num_feed=num_feed)

        # model.set_weekly_best_feed(feed_search_engine=feed_search_engine,
        #                             feed_manager=self.__feed_manager,
        #                             index=request.data_payload.key,
        #                             num_feed=num_feed)
        #
        return model    # comment 지우기
    def try_remove_comment(self, database:Mongo_Database,
                               request, feed_manager:FeedManager):
        model = FeedModel(database=database)
          # 유저가 있으면 세팅
        if request.jwt_payload != "":
            model.set_user_with_email(request=request.jwt_payload)
        model.try_remove_comment(feed_manager=feed_manager,
                                        data_payload=request.data_payload)

        return model

    # comment 모두 요청
    def get_all_comment_on_feed(self, database:Mongo_Database,
                               request):
        model = FeedModel(database=database)
        
        # 유저가 있으면 세팅
        if request.jwt_payload != "":
            model.set_user_with_email(request=request.jwt_payload)
            
        model.get_all_comment_on_feed(feed_manager=self.__feed_manager,
                                        data_payload=request.data_payload)

        return model

    # comment 만들기
    def try_make_comment(self, database:Mongo_Database,
                               request, feed_manager:FeedManager,
                               ai_manager
                               ):
        model = FeedModel(database=database)
        # 유저가 있으면 세팅
        if request.jwt_payload != "":
            model.set_user_with_email(request=request.jwt_payload)
        model.try_make_new_comment(feed_manager=feed_manager,
                                        data_payload=request.data_payload,
                                        ai_manager=ai_manager
                                        )

         return model

    # 피드 상호작용 누르기
    def try_interact_feed(self, database:Mongo_Database,
                               request, feed_manager:FeedManager):
        model = FeedModel(database=database)
        # 유저가 있으면 세팅
        if request.jwt_payload != "":
            model.set_user_with_email(request=request.jwt_payload)
        model.try_interact_feed(feed_manager=feed_manager,
                                        data_payload=request.data_payload)

        return model

 # 해시태그로 피드 검색하기
    def get_feed_with_hashtag(self, database:Mongo_Database,
                              request, feed_search_engine: FeedSearchEngine,
                              feed_manager: FeedManager,
                              num_feed= 4):
        model = FeedSearchModelNew(database=database)

        # 유저가 있으면 세팅
        if request.jwt_payload != "":
            model.set_user_with_email(request=request.jwt_payload)

        model.try_search_feed_with_keyword(feed_search_engine=feed_search_engine,
                                               feed_manager=feed_manager,
                                               search_columns="hashtag",
                                               target=request.data_payload.hashtag,
                                               target_time=request.data_payload.target_time,
                                               last_index=request.data_payload.key,
                                               num_feed=num_feed
        )

        # model.try_search_feed_with_hashtag(feed_search_engine=feed_search_engine,
        #                                    feed_manager=feed_manager,
        #                                    target=request.data_payload.hashtag,
        #                                    target_time=request.data_payload.target_time,
        #                                    last_index=request.data_payload.key,
        #                                    num_feed=num_feed
        #                                    )


        return model