from model import *
from others import UserNotExist
from view.jwt_decoder import RequestManager

class Sub_Controller:
    def get_single_bias(self, database:Mongo_Database, request:RequestManager) -> BiasModel:
        model = BiasModel(database=database)
        
        if request.jwt_payload!= "":
            model.set_user_with_email(request=request.jwt_payload)
            
        model.set_bias_data(bid=request.data_payload.bid)
        model.set_is_following()
        return model
        
    
    def try_add_new_bias(self, database:Mongo_Database, request:RequestManager, feed_search_engine) -> BaseModel:
        model = MakeNewBiasModel(database=database)
        
        if not model.set_user_with_email(request=request.jwt_payload):
            raise request.get_bad_request_exception()
        
        result = model.try_make_new_bias(
            name=request.data_payload.name,
            platform=request.data_payload.platform
            )
        
        if result:
            model.add_new_bias_in_engine(feed_search_engine=feed_search_engine)
            model.try_alert_to_admin(info=request.data_payload.info)
            model.auto_follow(feed_search_engine=feed_search_engine)
            
        return model
        
    # 최애 기반 커뮤니티 페이지에서 노출될 공지시항 리스트
    def try_get_notice_sample(self, database:Mongo_Database, data_payload) -> BaseModel: 
        model = NoticeModel(database=database)
        
        # bid가 선택되었는지 확인
        # 만약 bid가 선택되었다면 -> bid 포함된 공지 리스트
        # bid가 없다면 -> bid가 포함되지 않은 공지 리스트
        model.set_base_notices_data()

        ## 2. BIAS 전용 공지와, 전체용 공지를 나누는 작업
        ## BIAS가 선택되지 않았을 경우, BID가 ""로 들어가게 될것이다.
        ## BID가 없는경우라면, NOTICE_FOR_BIAS 찾는 과정에서 BID를 통한 BIAS찾기에서 값이 없을 것(BID=""인 BIAS는 없으니까)
        #model.set_bias_notices_data(bid=data_payload.bid)
        #model.set_none_bias_notices_data()

        ## 전송 데이터를 만드는 과정
        #model.set_send_notice_data(last_nid=data_payload.last_nid)
        return model

    def try_get_image_tag(self, database:Mongo_Database, data_payload) -> BaseModel:
        model = ImageTagModel(database=database)

        model.get_image(url = data_payload.url)

        return model

    # SubModel에 있는 Notice 모델과 NoticeListModel의 기능을 notice_model의 NoticeModel에 통합을 시킴
    # 나누는 이유가 없어보여서 통합 했음.
    def get_notice_list(self, database:Mongo_Database) -> BaseModel:
        # model = NoticeListModel(database=database)
        model = NoticeModel(database=database)

        model.get_notice_list()
        model.set_send_notice_data_for_details()

        return model

    def get_notice_detail(self, database:Mongo_Database, request) -> BaseModel: 
        model = NoticeModel(database=database)
        model.get_notice(nid = request.nid)
        model.set_send_notice_data_for_details()

        return model
        

    def try_follow_bias(self, database:Mongo_Database, request:RequestManager, feed_search_engine):
        model = BiasFollowModel(database=database)
        model.set_user_with_email(request=request.jwt_payload)
            
        if model.find_bias(bid=request.data_payload.bid):
            model.set_my_bias(feed_search_engine=feed_search_engine)

        return model
    
    # bias를 문자열로 검색
    def try_search_bias(self, database:Mongo_Database, request:RequestManager,
                                    feed_search_engine,): 
        model = BiasSearchModel(database=database)

        # managed_bias_list 를 불러옴
        
        # 1. 만약 keyword가 있으면 managed_bias에서 키워드에 필터링 해야함
        # 2. 만약 keyword가 없다면 필터링 할 필요없음
        
        # 2-2. database에서 데이터를 불러옴
        
        # 3. 만약 category가 모두라면 필터링 필요 없음
        # 4. 만약 category가 모두가 아니라면 필터링 해야함

        # 5. 페이징 함
        
        if request.jwt_payload != "":
            model.set_user_with_email(request=request.jwt_payload)
        
        managed_bias_list= model.get_managed_bias_list(feed_search_engine=feed_search_engine)
        
        if request.data_payload.keyword:
            managed_bias_list = model.try_filtering_with_keyword( 
                keyword=request.data_payload.keyword, 
                managed_bias_list=managed_bias_list
                )
            
        bias_list = model.try_get_data_in_database(managed_bias_list=managed_bias_list)
        
        if bias_list:
            if request.data_payload.category != "모두":
                model.try_filetering_bias_with_category(
                    category=request.data_payload.category,
                )
        
            model.try_paging(
                len_bias=request.data_payload.len_bias
            )
            
        return model

    # bias follow페이지에 노출될 최애들의 리스트
    def try_get_bias_follow_page(self, database:Mongo_Database):
        model = BiasFollowPageModel(database=database)

        if model.set_biases():
            model.try_get_bias_follow_page_data()

        return model
    
    # bias follow페이지에 노출될 최애들의 리스트
    def try_search_bias_with_category(self, database:Mongo_Database, request):
        model = BiasSearchModel(database=database)

        if model.set_biases():
            model.try_search_bias_with_category(category=request.data_payload.category)

        return model


    # 바이어스 유효성 검사 인터페이스
    def is_valid_bias(self, database:Mongo_Database, request):
        model = BiasModifyModel(database=database)
        
        if request.jwt_payload!= "":
            model.set_user_with_email(request=request.jwt_payload)

        model.set_bias_data(bid=request.data_payload.bid)
        
        model.is_valid_bias(api_request=True)
        return model

    # 바이어스 자기소개 수정
    def modify_bias_introduce(self, database:Mongo_Database, request):
        model = BiasModifyModel(database=database)

        if request.jwt_payload!= "":
            model.set_user_with_email(request=request.jwt_payload)
        
        model.set_bias_data(bid=request.data_payload.bid)
        
        result = model.modify_bias_introduce(introduce=request.data_payload.introduce)
        
        return model
    
    # 콘텐츠 등록 제한 토글 변경 수정
    def change_open_content_mode(self, database:Mongo_Database, request):
        model = BiasModifyModel(database=database)
        
        if request.jwt_payload!= "":
            model.set_user_with_email(request=request.jwt_payload)

        model.set_bias_data(bid=request.data_payload.bid)
        
        result = model.change_open_content_mode(open_content_mode=request.data_payload.open_content_mode)
        return model

    # 바이어스 프로필 이미지 바꾸기
    def try_change_bias_profile_photo(self, database:Mongo_Database, request):
        model = BiasModifyModel(database=database)

        if request.jwt_payload!= "":
            model.set_user_with_email(request=request.jwt_payload)
        
        model.set_bias_data(bid=request.data_payload.bid)
        
        result = model.try_change_bias_profile_photo(data_payload=request.data_payload)
        return model

    def try_report_post_or_comment(self, database:Mongo_Database, request):
        model = ReportModel(database=database)
        
        if request.jwt_payload != "":
            model.set_user_with_email(request=request.jwt_payload)
        
        # type은 신고인지 버그 리포트인지 구분을 위한 용도임
        # detail은 버그나 신고에 대한 자세한 내용을 기입하기 위한 용도임
        # 나중에 추가될것임
        
        model.try_set_report(data_payload=request.data_payload)
        model.save_report()
        
        return model

    def try_report_bug(self, database:Mongo_Database, request):
        model = ReportModel(database=database)
        
        if request.jwt_payload != "":
            model.set_user_with_email(request=request.jwt_payload)
        
        model.try_set_report(data_payload=request.data_payload)
        model.try_set_bug_report(data_payload=request.data_payload)
        model.save_report()
        
        return model

    # 부정행위 신고 기능 인터페이스
    def try_report_violation(self, database:Mongo_Database, request):
        model = ViolationReportModel(database=database)
        
        model.try_set_violation_report(data_payload=request.data_payload)
        model.save_violation_report()
        model.send_mail_to_manager()

        return model