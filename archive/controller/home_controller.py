    # 추천 검색어 시스템. 현재는 주간 핫 해시태그들만 보여줌
    def get_recommend_keyword(self, database:Mongo_Database, request, feed_search_engine) -> RecommendKeywordModel:
        model = RecommendKeywordModel(database=database)
        if request.jwt_payload != "":
            model.set_user_with_email(request=request.jwt_payload)
        # 작동하는 함수는 현재 주간 핫 해시태그들을 보여줍니다
        model.get_recommend_keywords(feed_search_engine=feed_search_engine)

        return model
    def get_monthly_best_hashtag(self, database:Mongo_Database, request, feed_search_engine) -> HashTagModel:
        model = HashTagModel(database=database)
        if request.jwt_payload != "":
            model.set_user_with_email(request=request.jwt_payload)
        model.set_monthly_best_hashtag(feed_search_engine=feed_search_engine, num_hashtags=5)

        return model
    def get_weekly_best_hashtag(self, database:Mongo_Database, request, feed_search_engine) -> HashTagModel:
        model = HashTagModel(database=database)
        if request.jwt_payload != "":
            model.set_user_with_email(request=request.jwt_payload)
            
        model.set_weekly_best_hashtag(feed_search_engine=feed_search_engine, num_hashtags=5)

        return model
    def get_today_best_hashtag(self, database:Mongo_Database, request, feed_search_engine) -> HashTagModel:
        model = HashTagModel(database=database)

        if request.jwt_payload != "":
            model.set_user_with_email(request=request.jwt_payload)

        model.set_today_best_hashtag(feed_search_engine=feed_search_engine, num_hashtags=5)

        return model

    def get_hot_hashtag(self, database:Mongo_Database, request, feed_search_engine) -> HashTagModel:
        model = HashTagModel(database=database)

        if request.jwt_payload != "":
            model.set_user_with_email(request=request.jwt_payload)

        if model.is_user_login():
            model.set_best_hashtag(feed_search_engine=feed_search_engine)
        else:
            model.set_realtime_best_hashtag(feed_search_engine=feed_search_engine, num_hashtags=10)
        return model

    def get_realtime_best_hashtag(self, database:Mongo_Database, request, feed_search_engine) -> HashTagModel:
        model = HashTagModel(database=database)
        # model.set_best_hash_tag()
        model.set_realtime_best_hashtag(feed_search_engine=feed_search_engine, num_hashtag=10)

        return model

