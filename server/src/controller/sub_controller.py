from model import *
from others import UserNotExist, CustomError

class Sub_Controller:
    
    def try_add_new_bias(self, database:Mongo_Database, request) -> BaseModel:
        model = MakeNewBiasModel(database=database)
        
        if not model.set_user_with_email(request=request.jwt_payload):
            raise UserNotExist("Can not find User With uid")
        
        result = model.try_make_new_bias(
            name=request.data_payload.name,
            platform=request.data_payload.platform
            )
        
        if result:
            model.try_alert_to_admin(info=request.data_payload.info)
        
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
        

    def try_select_bias(self, database:Mongo_Database, request, feed_search_engine):
        model = SelectBiasModel(database=database)
        model.set_user_with_email(request=request.jwt_payload)
            
        if model.find_bias(bid=request.data_payload.bid):
            model.set_my_bias(feed_search_engine=feed_search_engine)

        return model
    
    # bias를 문자열로 검색
    def try_search_bias(self, database:Mongo_Database, request,
                                    feed_search_engine,): 
        model = BiasSearchModel(database=database)

        model.try_search_bias(bname=request.data_payload.bname, feed_search_engine=feed_search_engine)

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