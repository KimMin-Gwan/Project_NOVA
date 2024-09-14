from model import HomeFeedModel, Local_Database
from fastapi import HTTPException, status
from others import CustomError, FeedManager

class Feed_Controller:
    def get_home_feed_data(self, database:Local_Database,
                            request , feed_manager:FeedManager):
        model = HomeFeedModel(database=database)
        try:
            # 유저가 있으면 세팅
            model.set_user_with_email(request=request.jwt_payload)
            model.get_feed_data(self, request.data_payload.key , feed_manager)

        except CustomError as e:
            print("Error Catched : ", e.error_type)
            model.set_state_code(e.error_code) # 종합 에러

        except Exception as e:
            print("Error Catched : ", e.error_type)
            model.set_state_code(e.error_code) # 종합 에러

        finally:
            return model
            










