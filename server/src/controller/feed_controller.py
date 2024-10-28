from model import FeedModel, Local_Database, FeedMetaModel, FeedEditModel
from fastapi import HTTPException, status
from others import CustomError, FeedManager

class Feed_Controller:
    def get_home_feed_data(self, database:Local_Database,
                            request , feed_manager:FeedManager):
        model = FeedModel(database=database)
        try:
            # 유저가 있으면 세팅
            if request.jwt_payload != "":
                model.set_user_with_email(request=request.jwt_payload)
            model.set_home_feed_data(feed_manager=feed_manager, key=request.data_payload.key)

        except CustomError as e:
            print("Error Catched : ", e.error_type)
            model.set_state_code(e.error_code) # 종합 에러

        except Exception as e:
            print("Error Catched : ", e.error_type)
            model.set_state_code(e.error_code) # 종합 에러

        finally:
            return model

    def get_home_hot_hashtag_feed(self, database:Local_Database,
                            request , feed_manager:FeedManager):
        model = FeedModel(database=database)
        try:
            print("1")

            # 유저가 있으면 세팅
            if request.jwt_payload != "":
                print("2")
                model.set_user_with_email(request=request.jwt_payload)
            print("3")
            model.set_home_feed_data(feed_manager=feed_manager, key=-4)
            print("4")

        except CustomError as e:
            print("Error Catched : ", e.error_type)
            model.set_state_code(e.error_code) # 종합 에러

        except Exception as e:
            print("Error Catched : ", e.error_type)
            model.set_state_code(e.error_code) # 종합 에러

        finally:
            return model           
        

    # 위성 탐색에서 들어오는 요청에 대한 반환값
    def get_specific_feed_data(self, database:Local_Database,
                               request, feed_manager:FeedManager):
        model = FeedModel(database=database)
        try:
            # 유저가 있으면 세팅
            if request.jwt_payload != "":
                model.set_user_with_email(request=request.jwt_payload)
            model.set_specific_feed_data(feed_manager=feed_manager,
                                         data_payload=request.data_payload)

        except CustomError as e:
            print("Error Catched : ", e.error_type)
            model.set_state_code(e.error_code) # 종합 에러

        except Exception as e:
            print("Error Catched : ", e.error_type)
            model.set_state_code(e.error_code) # 종합 에러

        finally:
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
