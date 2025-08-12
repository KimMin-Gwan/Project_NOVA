def sample_func(self, database:Mongo_Database, request) -> BaseModel: 
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
        
        def get_user_contribution(self, database:Mongo_Database, request) -> UserContributionModel: 
        model = UserContributionModel(database=database)

        try:
            if not model.set_bias_data():
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
        
            # 최애 페이지의 지지자 본인의 기여도 정보
    def get_my_contribution(self, database:Mongo_Database, request) -> MyContributionModel: 
        model = MyContributionModel(database=database)
        try:
            if not model.set_user_with_email(request=request.jwt_payload):
                raise UserNotExist("Can not find User with uid")
        except UserNotExist as e:
            print("Error Catched : ", e)
            model.set_state_code(e.error_code) # 종합 에러
            return model

        try:
            if not model.set_bias_data():
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
        
        
    def try_get_community_side_box(self, database:Mongo_Database, data_payload):
        model = CommunitySideBoxModel(database=database)

        # 유저가 있는지 확인
        if model.get_boards_of_bias_community(bid=data_payload.bid):
            model.get_urls_of_bias()
        return model

    def try_change_users_age(self, database:Mongo_Database, request):
        model = ChangeUserAgeModel(database=database)

        model.change_users_age()
        return model