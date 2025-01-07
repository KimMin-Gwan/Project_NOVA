from model import *
from others import UserNotExist, CustomError

class Sub_Controller:
    def sample_func(self, database:Local_Database, request) -> BaseModel: 
        model = BaseModel(database=database)
        try:
            # 유저가 있는지 확인
            if not model.set_user_with_uid(request=request.jwt_payload):
                raise UserNotExist("Can not find User with uid")
        except UserNotExist as e:
            print("Error Catched : ", e)
            model.set_state_code(e.error_code) # 종합 에러
            return model
        try:
            """
            if not model.set_biases_with_bids():
                model.set_state_code("210")
                return model
            """
        except CustomError as e:
            print("Error Catched : ", e.error_type)
            model.set_state_code(e.error_code) # 종합 에러

        except Exception as e:
            print("Error Catched : ", e.error_type)
            model.set_state_code(e.error_code) # 종합 에러

        finally:
            return model

    def try_get_image_tag(self, database:Local_Database, data_payload) -> BaseModel: 
        model = ImageTagModel(database=database)

        model.get_image(url = data_payload.url)

        return model

    def get_notice_list(self, database:Local_Database) -> BaseModel: 
        model = NoticeListModel(database=database)
        try:
            model.get_notice_list()

        except CustomError as e:
            print("Error Catched : ", e.error_type)
            model.set_state_code(e.error_code) # 종합 에러

        except Exception as e:
            print("Error Catched : ", e.error_type)
            model.set_state_code(e.error_code) # 종합 에러

        finally:
            return model

    def get_notice_detail(self, database:Local_Database, request) -> BaseModel: 
        model = NoticeModel(database=database)
        try:
            model.get_notice(nid = request.nid)

        except CustomError as e:
            print("Error Catched : ", e.error_type)
            model.set_state_code(e.error_code) # 종합 에러

        except Exception as e:
            print("Error Catched : ", e.error_type)
            model.set_state_code(e.error_code) # 종합 에러

        finally:
            return model
        
    # 최애 페이지의 배너 정보
    # 배너가 없으면 뭘 보여줄래?
    def get_bias_banner(self, database:Local_Database, request) -> BaseModel: 
        model = BiasBannerModel(database=database)
        try:
            """
            if not model.set_biases_with_bids():
                model.set_state_code("210")
                return model
            """
        except CustomError as e:
            print("Error Catched : ", e.error_type)
            model.set_state_code(e.error_code) # 종합 에러

        except Exception as e:
            print("Error Catched : ", e.error_type)
            model.set_state_code(e.error_code) # 종합 에러

        finally:
            return model

    # 최애 페이지의 지지자 기여도 랭크 
    def get_user_contribution(self, database:Local_Database, request) -> UserContributionModel: 
        model = UserContributionModel(database=database)

        try:
            if not model.set_bias_data(request=request):
                model.set_state_code("571") # 실패하면 571
                return model

            # 유저 데이터들 만들기
            if not model.set_user_datas():
                model.set_state_code("572") # 실패하면 572
                return model

            # 순위 만들기
            if not model.set_user_alignment():
                model.set_state_code("573") # 실패하면 573
                return model

        except CustomError as e:
            print("Error Catched : ", e.error_type)
            model.set_state_code(e.error_code) # 종합 에러

        except Exception as e:
            print("Error Catched : ", e.error_type)
            model.set_state_code(e.error_code) # 종합 에러

        finally:
            return model

    # 최애 페이지의 지지자 기여도 랭크 
    def get_bias_n_league_data(self, database:Local_Database, request) -> UserContributionModel: 
        model = BiasNLeagueModel(database=database)

        try:
            model.set_bias_data(request.bid)

            # 리그 세팅 (오버라이드)
            model.set_leagues()

            # 리그 참여 바이어스 정렬
            model.set_biases()

            # 리그 정렬하고 딕셔너리 형태로 만들어야됨
            model.set_list_alignment()

            # 리그 통계정보
            model.get_my_league_data()

        except CustomError as e:
            print("Error Catched : ", e.error_type)
            model.set_state_code(e.error_code) # 종합 에러

        except Exception as e:
            print("Error Catched : ", e.error_type)
            model.set_state_code(e.error_code) # 종합 에러

        finally:
            return model

    # 최애 페이지의 지지자 본인의 기여도 정보
    def get_my_contribution(self, database:Local_Database, request) -> MyContributionModel: 
        model = MyContributionModel(database=database)
        try:
            if not model.set_user_with_email(request=request.jwt_payload):
                raise UserNotExist("Can not find User with uid")
        except UserNotExist as e:
            print("Error Catched : ", e)
            model.set_state_code(e.error_code) # 종합 에러
            return model

        try:
            if not model.set_bias_data(request=request):
                model.set_state_code("571") # 실패하면 571
                return model
            
            # 본인이 지지하는지 검토해야됨
            if not model.is_my_bias():
                model.set_state_code("274") # 실패하면 271
                return model

            # 유저 데이터들 만들기
            if not model.set_user_datas():
                model.set_state_code("572") # 실패하면 572
                return model

            # 정렬
            if not model.set_user_alignment():
                model.set_state_code("573") # 실패하면 573
                return model

        except CustomError as e:
            print("Error Catched : ", e.error_type)
            model.set_state_code(e.error_code) # 종합 에러

        except Exception as e:
            print("Error Catched : ", e.error_type)
            model.set_state_code(e.error_code) # 종합 에러

        finally:
            return model

    def try_select_bias(self, database:Local_Database, request, feed_search_engine):
        model = SelectBiasModel(database=database)
        try:
            # 유저가 있는지 확인
            model.set_user_with_email(request=request.jwt_payload)
            
            if model.find_bias(request=request.data_payload.bid):
                model.set_my_bias(feed_search_engine=feed_search_engine)

        except CustomError as e:
            print("Error Catched : ", e.error_type)
            model.set_state_code(e.error_code) # 종합 에러

        except Exception as e:
            print("Error Catched : ", e.error_type)
            model.set_state_code(e.error_code) # 종합 에러

        finally:
            return model
    
    # bias를 문자열로 검색
    def try_search_bias(self, database:Local_Database, request,
                                    feed_search_engine,): 
        model = BiasSearchModel(database=database)

        model.try_search_bias(bname=request.bname, feed_search_engine=feed_search_engine)

        return model
        
    # bias follow페이지에 노출될 최애들의 리스트
    def try_get_bias_follow_page(self, database:Local_Database):
        model = BiasFollowPageModel(database=database)

        if model.set_biases():
            model.try_get_bias_follow_page_data()

        return model
    
    # bias follow페이지에 노출될 최애들의 리스트
    def try_search_bias_with_category(self, database:Local_Database, request):
        model = BiasSearchModel(database=database)

        if model.set_biases():
            model.try_search_bias_with_category(category=request.data_payload.category)

        return model