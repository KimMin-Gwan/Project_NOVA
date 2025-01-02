from model import FeedModel, Local_Database, FeedEditModel, FeedSearchModel
from fastapi import HTTPException, status
from others import CustomError, FeedManager, FeedSearchEngine

class Feed_Controller:
    def __init__(self, feed_manager:FeedManager):
        self.__feed_manager = feed_manager

    # fid를 통한 피드 검색
    def try_search_in_fid(self, database:Local_Database,
                        request, feed_search_engine: FeedSearchEngine,
                        num_feed= 1):
        model = FeedSearchModel(database=database)
        # 유저가 있으면 세팅
        if request.jwt_payload != "":
            model.set_user_with_email(request=request.jwt_payload)
        model.try_search_feed_with_fid(feed_search_engine=feed_search_engine,
                                       feed_manager=self.__feed_manager,
                                        fid=request.data_payload.fid)

        return model
    

    # 키워드를 통한 피드 검색
    def try_search_in_keyword(self, database:Local_Database,
                        request, feed_search_engine: FeedSearchEngine,
                        num_feed= 4):
        model = FeedSearchModel(database=database)
        try:
            # 유저가 있으면 세팅
            if request.jwt_payload != "":
                model.set_user_with_email(request=request.jwt_payload)
            model.try_search_feed(feed_search_engine=feed_search_engine,
                                  feed_manager=self.__feed_manager,
                                target=request.data_payload.keyword,
                                num_feed=num_feed)

        except CustomError as e:
            print("Error Catched : ", e.error_type)
            model.set_state_code(e.error_code) # 종합 에러

        except Exception as e:
            print("Error Catched : ", e.error_type)
            model.set_state_code(e.error_code) # 종합 에러

        finally:
            return model

    # 키워드를 통한 피드 검색
    def try_search_in_hashtag(self, database:Local_Database,
                        request, feed_search_engine: FeedSearchEngine,
                        num_feed= 4):
        model = FeedSearchModel(database=database)
        try:
            # 유저가 있으면 세팅
            if request.jwt_payload != "":
                model.set_user_with_email(request=request.jwt_payload)
            model.try_search_feed_with_hashtag(feed_search_engine=feed_search_engine,
                                               feed_manager=self.__feed_manager,
                                                target=request.data_payload.hashtag,
                                                index=request.data_payload.key,
                                                num_feed=num_feed)

        except CustomError as e:
            print("Error Catched : ", e.error_type)
            model.set_state_code(e.error_code) # 종합 에러

        except Exception as e:
            print("Error Catched : ", e.error_type)
            model.set_state_code(e.error_code) # 종합 에러

        finally:
            return model

    # 오늘의 인기 게시글
    def get_today_best(self, database:Local_Database,
                        request, feed_search_engine: FeedSearchEngine,
                        num_feed= 4):
        model = FeedModel(database=database)
        try:
            # 유저가 있으면 세팅
            if request.jwt_payload != "":
                model.set_user_with_email(request=request.jwt_payload)
            model.set_today_best_feed(feed_search_engine=feed_search_engine,
                                        feed_manager=self.__feed_manager,
                                        index=request.data_payload.key,
                                       num_feed=num_feed)

        except CustomError as e:
            print("Error Catched : ", e.error_type)
            model.set_state_code(e.error_code) # 종합 에러

        except Exception as e:
            print("Error Catched : ", e.error_type)
            model.set_state_code(e.error_code) # 종합 에러

        finally:
            return model

    # 주간 인기 게시글
    def get_weekly_best(self, database:Local_Database,
                        request, feed_search_engine: FeedSearchEngine,
                        num_feed= 4):
        model = FeedModel(database=database)
        try:
            # 유저가 있으면 세팅
            if request.jwt_payload != "":
                model.set_user_with_email(request=request.jwt_payload)
            model.set_weekly_best_feed(feed_search_engine=feed_search_engine,
                                       feed_manager=self.__feed_manager,
                                        index=request.data_payload.key,
                                       num_feed=num_feed)

        except CustomError as e:
            print("Error Catched : ", e.error_type)
            model.set_state_code(e.error_code) # 종합 에러

        except Exception as e:
            print("Error Catched : ", e.error_type)
            model.set_state_code(e.error_code) # 종합 에러

        finally:
            return model
        
    # 전체 개시글(최신순)
    def get_all_feed(self, database:Local_Database,
                        request, feed_search_engine: FeedSearchEngine,
                        num_feed= 4):
        model = FeedModel(database=database)
        try:
            # 유저가 있으면 세팅
            if request.jwt_payload != "":
                model.set_user_with_email(request=request.jwt_payload)
            model.set_all_feed(feed_search_engine=feed_search_engine,
                               feed_manager=self.__feed_manager,
                                        index=request.data_payload.key,
                                       num_feed=num_feed)

        except CustomError as e:
            print("Error Catched : ", e.error_type)
            model.set_state_code(e.error_code) # 종합 에러

        except Exception as e:
            print("Error Catched : ", e.error_type)
            model.set_state_code(e.error_code) # 종합 에러

        finally:
            return model

    # 해시태그로 피드 검색하기
    def get_feed_with_hashtag(self, database:Local_Database,
                        request, feed_search_engine: FeedSearchEngine,
                        num_feed= 4):
        model = FeedModel(database=database)

        try:
            # 유저가 있으면 세팅
            if request.jwt_payload != "":
                model.set_user_with_email(request=request.jwt_payload)
            model.set_feed_data(feed_search_engine=feed_search_engine,
                                target_type="hashtag",
                                target=request.data_payload.hashtag,
                                num_feed=num_feed,
                                index=request.data_payload.key,
                                feed_manager=self.__feed_manager
                                )

        except CustomError as e:
            print("Error Catched : ", e.error_type)
            model.set_state_code(e.error_code) # 종합 에러

        except Exception as e:
            print("Error Catched : ", e.error_type)
            model.set_state_code(e.error_code) # 종합 에러

        finally:
            return model



    # 숏피드에서 다음 피드 요청할 때
    def get_feed_with_recommend(self, database:Local_Database,
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


    def get_home_hot_hashtag_feed(self, database:Local_Database,
                            request , feed_manager:FeedManager):
        model = FeedModel(database=database)
        try:

            # 유저가 있으면 세팅
            if request.jwt_payload != "":
                model.set_user_with_email(request=request.jwt_payload)
            model.set_feed_data(
                target_type="hashtag", target=request.data_payload.target,
                feed_manager=self.__feed_manager,
                num_feed=4, index= request.data_payload.key)

        except CustomError as e:
            print("Error Catched : ", e.error_type)
            model.set_state_code(e.error_code) # 종합 에러

        except Exception as e:
            print("Error Catched : ", e.error_type)
            model.set_state_code(e.error_code) # 종합 에러

        finally:
            return model           
        


    ## 예전에 쓰던거
    #def get_home_feed_data(self, database:Local_Database,
                            #request , feed_manager:FeedManager):
        #model = FeedModel(database=database)
        #try:
            ## 유저가 있으면 세팅
            #if request.jwt_payload != "":
                #model.set_user_with_email(request=request.jwt_payload)
            #model.set_home_feed_data(feed_manager=feed_manager, key=request.data_payload.key)

        #except CustomError as e:
            #print("Error Catched : ", e.error_type)
            #model.set_state_code(e.error_code) # 종합 에러

        #except Exception as e:
            #print("Error Catched : ", e.error_type)
            #model.set_state_code(e.error_code) # 종합 에러

        #finally:
            #return model

    # 피드 자세히 보기
    def get_specific_feed_data(self, database:Local_Database,
                               request):
        model = FeedModel(database=database)

        # 유저가 있으면 세팅
        if request.jwt_payload != "":
            model.set_user_with_email(request=request.jwt_payload)

        model.set_single_feed_data(fid=request.data_payload.fid, feed_manager=self.__feed_manager)

        return model

    # 피드 상호작용 누르기
    def try_interact_feed(self, database:Local_Database,
                               request, feed_manager:FeedManager):
        model = FeedModel(database=database)
        try:
            # 유저가 있으면 세팅
            model.set_user_with_email(request=request.jwt_payload)
            model.try_interact_feed(feed_manager=feed_manager,
                                         data_payload=request.data_payload)

        except CustomError as e:
            print("Error Catched : ", e.error_type)
            model.set_state_code(e.error_code) # 종합 에러

        except Exception as e:
            print("Error Catched : ", e.error_type)
            model.set_state_code(e.error_code) # 종합 에러

        finally:
            return model

    # 피드 관심 버튼 누르기
    def try_staring_feed(self, database:Local_Database,
                               request, feed_manager:FeedManager):
        model = FeedModel(database=database)
        try:
            # 유저가 있으면 세팅
            model.set_user_with_email(request=request.jwt_payload)
            model.try_staring_feed(feed_manager=feed_manager,
                                         data_payload=request.data_payload)

        except CustomError as e:
            print("Error Catched : ", e.error_type)
            model.set_state_code(e.error_code) # 종합 에러

        except Exception as e:
            print("Error Catched : ", e.error_type)
            model.set_state_code(e.error_code) # 종합 에러

        finally:
            return model

    # comment 만들기
    def try_make_comment(self, database:Local_Database,
                               request, feed_manager:FeedManager):
        model = FeedModel(database=database)
        try:
            # 유저가 있으면 세팅
            model.set_user_with_email(request=request.jwt_payload)
            model.try_make_new_comment(feed_manager=feed_manager,
                                         data_payload=request.data_payload)

        except CustomError as e:
            print("Error Catched : ", e.error_type)
            model.set_state_code(e.error_code) # 종합 에러

        except Exception as e:
            print("Error Catched : ", e.error_type)
            model.set_state_code(e.error_code) # 종합 에러

        finally:
            return model

    # comment 모두 요청
    def get_all_comment_on_feed(self, database:Local_Database,
                               request, feed_manager:FeedManager):
        model = FeedModel(database=database)
        try:
            # 유저가 있으면 세팅
            model.set_user_with_email(request=request.jwt_payload)
            model.get_all_comment_on_feed(feed_manager=feed_manager,
                                         data_payload=request.data_payload)

        except CustomError as e:
            print("Error Catched : ", e.error_type)
            model.set_state_code(e.error_code) # 종합 에러

        except Exception as e:
            print("Error Catched : ", e.error_type)
            model.set_state_code(e.error_code) # 종합 에러

        finally:
            return model

    # comment 지우기
    def try_remove_comment(self, database:Local_Database,
                               request, feed_manager:FeedManager):
        model = FeedModel(database=database)
        try:
            # 유저가 있으면 세팅
            model.set_user_with_email(request=request.jwt_payload)
            model.try_remove_comment(feed_manager=feed_manager,
                                         data_payload=request.data_payload)

        except CustomError as e:
            print("Error Catched : ", e.error_type)
            model.set_state_code(e.error_code) # 종합 에러

        except Exception as e:
            print("Error Catched : ", e.error_type)
            model.set_state_code(e.error_code) # 종합 에러

        finally:
            return model

    # comment 좋아요 누르기
    def try_like_comment(self, database:Local_Database,
                               request, feed_manager:FeedManager):
        model = FeedModel(database=database)
        try:
            # 유저가 있으면 세팅
            model.set_user_with_email(request=request.jwt_payload)
            model.try_like_comment(feed_manager=feed_manager,
                                         data_payload=request.data_payload)

        except CustomError as e:
            print("Error Catched : ", e.error_type)
            model.set_state_code(e.error_code) # 종합 에러

        except Exception as e:
            print("Error Catched : ", e.error_type)
            model.set_state_code(e.error_code) # 종합 에러

        finally:
            return model

    # comment 좋아요 누르기
    def try_edit_feed(self, database:Local_Database,
                               request, feed_manager:FeedManager) -> FeedEditModel:
        model = FeedEditModel(database=database)
        model.set_user_with_email(request=request.jwt_payload)
        model.try_edit_feed(feed_manager=feed_manager,
                                        data_payload=request.data_payload)
        model.check_result(request_manager=request)

        return model
