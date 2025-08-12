    # comment 지우기
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