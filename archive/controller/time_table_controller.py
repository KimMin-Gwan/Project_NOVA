    # 이벤트 추가하기
    def try_add_event(self, database:Mongo_Database, request:RequestManager) -> BaseModel:
        model = AddScheduleModel(database=database)
        if request.jwt_payload!= "":
            model.set_user_with_email(request=request.jwt_payload)
            # 이건 뭔가 이상한 상황일때 그냥 모델 리턴하는거
            if not model._set_tuser_with_tuid():
                return model
        else:
            return model

        model.add_event(seid=request.seid)
        return model

    # 이번주 타임테이블에 추가하기
    def try_select_my_time_table_schedule(self, schedule_search_engine:SSE, database:Mongo_Database, request:RequestManager) -> BaseModel:
        model = AddScheduleModel(database=database)
        
        if request.jwt_payload!= "":
            model.set_user_with_email(request=request.jwt_payload)
            # 이건 뭔가 이상한 상황일때 그냥 모델 리턴하는거
            if not model._set_tuser_with_tuid():
                return model
        else:
            return model
        
        model.select_schedule_in_showcase(schedule_search_engine=schedule_search_engine,
                                          date=request.data_payload.date, bid=request.data_payload.bid)
        
        return model

    # 키워드를 통해 바이어스를 검색
    # 유이하게 Search Engine을 사용하지 않음
    def try_search_bias_with_keyword(self, database:Mongo_Database, request:RequestManager, num_biases=10) -> BaseModel:
        # model = TimeTableBiasModel(database=database)
        model = MultiScheduleModel(database=database)

        if request.jwt_payload!= "":
            model.set_user_with_email(request=request.jwt_payload)
            # 이건 뭔가 이상한 상황일때 그냥 모델 리턴하는거
            if not model._set_tuser_with_tuid():
                return model

        model.search_bias_with_keyword(keyword=request.data_payload.keyword,
                                       last_index=request.data_payload.key,
                                       num_biases=num_biases)

        return model

    # 이번 주 일정을 들고 올 것 (전체에서)
    def try_get_weekday_schedules(self, schedule_search_engine:SSE, database:Mongo_Database, request:RequestManager) -> BaseModel:
        model = MultiScheduleModel(database=database)

        if request.jwt_payload!= "":
            model.set_user_with_email(request=request.jwt_payload)
            # 이건 뭔가 이상한 상황일때 그냥 모델 리턴하는거
            if not model._set_tuser_with_tuid():
                return model

        model.get_weekday_schedules(schedule_search_engine=schedule_search_engine)

        return model

    # 내가 선택한 일정을 들고 옴
    def try_get_my_selected_schedules(self,schedule_search_engine:SSE, database:Mongo_Database,
                                      request:RequestManager, num_schedules=6):
        model = MultiScheduleModel(database)

        if request.jwt_payload!= "":
            model.set_user_with_email(request=request.jwt_payload)
            if not model._set_tuser_with_tuid():
                return model

        model.get_my_selected_schedules(schedule_search_engine=schedule_search_engine,
                                        bid=request.data_payload.bid,
                                        last_index=request.data_payload.key,
                                        num_schedules=num_schedules)

        return model

    # 작성한 스케줄 번들을 보내기
    # 하나만 가지고 오므로 Search Engine을 쓰지 않음
    def try_get_written_bundle(self, database:Mongo_Database, request:RequestManager):
        model = MultiScheduleModel(database)

        if request.jwt_payload!= "":
            model.set_user_with_email(request=request.jwt_payload)
            if not model._set_tuser_with_tuid():
                return model

        model.get_written_bundle(sbid=request.data_payload.sbid)

        return model

    # 스케줄 번들 편집
    def try_modify_bundle(self, schedule_search_engine:SSE, database:Mongo_Database, request:RequestManager):
        model = AddScheduleModel(database)

        if request.jwt_payload!= "":
            model.set_user_with_email(request=request.jwt_payload)
            if not model._set_tuser_with_tuid():
                return model

        # model.set_user_with_email(request=request.data_payload)
        # model._set_tuser_with_tuid()

        schedule_object = model.modify_multiple_schedule(schedule_search_engine=schedule_search_engine,
                                                         schedules=request.data_payload.schedules,
                                                         sname=request.data_payload.sname,
                                                         sbid=request.data_payload.sbid,
                                                         bid=request.data_payload.bid,
                                                         data_type=request.data_payload.type)

        model.save_modified_multiple_schedule_object_with_type(schedule_object=schedule_object, data_type=request.data_payload.type)

        return model

    # 스케줄 번들 삭제
    def try_delete_bundle(self, schedule_search_engine:SSE, database:Mongo_Database, request:RequestManager):
        model = AddScheduleModel(database)

        if request.jwt_payload!= "":
            model.set_user_with_email(request=request.jwt_payload)
            if not model._set_tuser_with_tuid():
                return model

        model.delete_bundle(schedule_search_engine=schedule_search_engine, sbid=request.data_payload.sbid)

        return model