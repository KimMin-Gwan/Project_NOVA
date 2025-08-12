from model import *
from fastapi import HTTPException, status
from others import CustomError, FeedManager, FeedSearchEngine

class Feed_Controller:
    def __init__(self, feed_manager:FeedManager):
        self.__feed_manager = feed_manager
        
    def init_chatting(self, request, database:Mongo_Database) ->BaseModel:
        model = BaseModel(database=database)
        # 유저가 있으면 세팅
        model.set_user_with_uid(request=request.data_payload)
        return model


    # Bias 기반 커뮤니티 피드 검색
    def get_feed_in_bias_feed_page(self, database:Mongo_Database,
                                request, feed_search_engine: FeedSearchEngine):
        # model = CommunityFeedModel(database=database)
        model = FilteredFeedModel(database=database)
        
        # 유저가 있으면 세팅
        if request.jwt_payload != "":
            model.set_user_with_email(request=request.jwt_payload)
                
        #model.is_bids_data_empty(data_payload=request.data_payload)

        model.try_filtered_feed_community(
            feed_search_engine=feed_search_engine,
            feed_manager=self.__feed_manager,
            bid = request.data_payload.bid,
            category = request.data_payload.category,
            last_index=request.data_payload.key
        )


        # # board를 선택하지 않은 경우
        # if request.data_payload.board_type == "":
        #     model.try_search_feed_with_bid(
        #         bid = request.data_payload.bid,
        #         last_fid = request.data_payload.last_fid,
        #         feed_search_engine=feed_search_engine,
        #         feed_manager=self.__feed_manager)
        #
        # # board를 선택한 경우
        # else:
        #     model.try_search_feed_with_bid_n_board_type(
        #         bid = request.data_payload.bid,
        #         last_fid = request.data_payload.last_fid,
        #         board_type = request.data_payload.board_type,
        #         feed_search_engine=feed_search_engine,
        #         feed_manager=self.__feed_manager)

        return model


    # 필터링 인터페이스
    # 옵션들을 모두 받아와서 여러번 필터링을 거치게 됩니다.
    # 신규) ->> 사실 당장에 필터링은 안함
    def get_all_feed_filtered(self, database:Mongo_Database,
                              request, feed_search_engine: FeedSearchEngine,
                              num_feed=4):

        model = FilteredFeedModel(database=database)

        # 유저가 있으면 세팅
        if request.jwt_payload != "":
            model.set_user_with_email(request=request.jwt_payload)

        model.try_filtered_feed_with_options(feed_search_engine=feed_search_engine,
                                             feed_manager=self.__feed_manager,
                                             category=request.data_payload.category,
                                             fclass=request.data_payload.fclass,
                                             last_index=request.data_payload.key,
                                             num_feed=num_feed
                                             )
        return model


    # 숏피드에서 다음 피드 요청할 때
    def get_feed_with_recommend(self, database:Mongo_Database,
                        request, feed_search_engine: FeedSearchEngine):
        model = FeedSearchModel(database=database)

        # 유저가 있으면 세팅
        if request.jwt_payload != "":
            model.set_user_with_email(request=request.jwt_payload)

        model.set_recommend_feed(feed_search_engine,
                                fid=request.data_payload.fid,
                                history=request.data_payload.history,
                                feed_manager=self.__feed_manager
                                )
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
                                               feed_manager=self.__feed_manager,
                                               search_columns="bid",
                                               last_index=request.data_payload.key,
                                               num_feed=num_feed)

        # model.try_search_feed_with_bid(feed_search_engine=feed_search_engine,
        #                                feed_manager=self.__feed_manager,
        #                                target=request.data_payload.target,
        #                                last_index=request.data_payload.last_index,
        #                                num_feed=num_feed)


        return model

   

    def search_feed_with_keyword(self, database:Mongo_Database,
                                 request, feed_search_engine:FeedSearchEngine,
                                 num_feed=15):
        model = FeedSearchModelNew(database=database)

        # 유저 세팅
        if request.jwt_payload != "":
            model.set_user_with_email(request=request.jwt_payload)

        # 키워드 데이터를 저장하는 로직. 현재는 pass 상태로 있습니다.
        # 데이터 도메인에다가 추가된다면 만들겁니다.
        model.save_keyword(
            target=request.data_payload.keyword,
            feed_search_engine=feed_search_engine,
        )
        
        model.try_search_feed_with_keyword(feed_search_engine=feed_search_engine,
                                               feed_manager=self.__feed_manager,
                                               target=request.data_payload.keyword,
                                               search_columns=request.data_payload.search_columns,
                                               fclass=request.data_payload.fclass,
                                               last_index=request.data_payload.key,
                                               num_feed=num_feed)

        # model.try_search_feed_with_keyword(
        #     target=request.data_payload.keyword,
        #     fclass=request.data_payload.fclass,
        #     last_index=request.data_payload.key,
        #     feed_search_engine=feed_search_engine,
        #     feed_manager=self.__feed_manager,
        #     num_feed=num_feed
        # )

        return model

    def search_comment_with_keyword(self, database:Mongo_Database,
                                    request, feed_search_engine:FeedSearchEngine,
                                    num_comments=10):
        model = CommentSearchModel(database=database)

        # 유저 세팅
        if request.jwt_payload != "":
            model.set_user_with_email(request=request.jwt_payload)

        # 키워드를 통해 서치함
        model.try_search_comment_with_keyword(
            target=request.data_payload.keyword,
            last_index=request.data_payload.key,
            feed_manager=self.__feed_manager,
            num_comments=num_comments
        )
        return model

    # 피드 자세히 보기
    def get_specific_feed_data(self, database:Mongo_Database,
                               request):
        model = FeedModel(database=database)

        # 유저가 있으면 세팅
        if request.jwt_payload != "":
            model.set_user_with_email(request=request.jwt_payload)

        model.set_single_feed_data(fid=request.data_payload.fid, feed_manager=self.__feed_manager)

        return model


    # 피드 관심 버튼 누르기
    def try_staring_feed(self, database:Mongo_Database,
                               request, feed_manager:FeedManager):
        model = FeedModel(database=database)
        # 유저가 있으면 세팅
        if request.jwt_payload != "":
            model.set_user_with_email(request=request.jwt_payload)
        model.try_staring_feed(feed_manager=feed_manager,
                                        data_payload=request.data_payload)

        return model

    
    # comment 모두 요청
    def get_target_comment_on_feed(self, database:Mongo_Database,
                               request) -> BaseModel:
        model = CommentModel(database=database)
        
        # 유저가 있으면 세팅
        if request.jwt_payload != "":
            model.set_user_with_email(request=request.jwt_payload)
            
        model.set_target_comment(fid=request.data_payload.fid,
                                target_cid=request.data_payload.cid)

        return model
    

    # comment 좋아요 누르기
    def try_like_comment(self, database:Mongo_Database,
                               request, feed_manager:FeedManager):
        model = FeedModel(database=database)
        # 유저가 있으면 세팅
        if request.jwt_payload != "":
            model.set_user_with_email(request=request.jwt_payload)
        model.try_like_comment(feed_manager=feed_manager,
                                        data_payload=request.data_payload)

        return model

    # Feed 편집
    def try_edit_feed(self, database:Mongo_Database,
                               request, feed_manager:FeedManager,
                               ai_manager
                               ) -> FeedEditModel:
        model = FeedEditModel(database=database)

        if request.jwt_payload != "":
            model.set_user_with_email(request=request.jwt_payload)

        model.set_feed_link(data_payload= request.data_payload)
        
        model.try_edit_feed(feed_manager=feed_manager,
                            data_payload=request.data_payload,
                            ai_manager=ai_manager
                            )
        model.check_result(request_manager=request)

        return model

    def try_remove_feed(self, database:Mongo_Database,
                        request, feed_manager:FeedManager) -> FeedEditModel:

        model = FeedEditModel(database=database)
        if request.jwt_payload != "":
            model.set_user_with_email(request=request.jwt_payload)

        model.try_remove_feed(feed_manager=feed_manager,
                              data_payload=request.data_payload)
        model.check_result(request_manager=request)

        return model