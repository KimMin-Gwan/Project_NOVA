from model.base_model import BaseModel
from model import Mongo_Database
from others.data_domain import Bias, User, Report
from others import CoreControllerLogicError, HTMLEXtractor, ImageDescriper, MailSender, FeedSearchEngine
import uuid

class BannerModel(BaseModel):
    def __init__(self, database:Mongo_Database) -> None:
        super().__init__(database)
        self.__banner = []

    def set_banner_data(self):
        try:
            self.__banner = self._database.get_all_data(target="banner")

        except Exception as e:
            raise CoreControllerLogicError(error_type="set_group_leagues | " + str(e))

    def get_response_form_data(self, head_parser):
        try:
            body = {
                'banner' : self.__banner
            }

            response = self._get_response_data(head_parser=head_parser, body=body)
            return response

        except Exception as e:
            raise CoreControllerLogicError("response making error | " + e)
        
        
class ImageTagModel(BaseModel):
    def __init__(self, database:Mongo_Database) -> None:
        super().__init__(database)
        self.__url = ""
        self.__image = ""

    def get_image(self, url):
        self.__url = url
        self.__image = HTMLEXtractor().extract_external_webpage_image_data(url=url)

    def get_response_form_data(self, head_parser):
        try:
            body = {
                'url' : self.__url,
                'image' : self.__image
            }

            response = self._get_response_data(head_parser=head_parser, body=body)
            return response

        except Exception as e:
            raise CoreControllerLogicError("response making error | " + e)


class ReportModel(BaseModel):
    def __init__(self, database):
        super().__init__(database)
        self.__report = Report()
        self.__result = False
        
    # 리포트 만들기
    def try_set_report(self, data_payload):
        if data_payload.cid != "":
            self.__report.cid = data_payload.cid
        else:
            self.__report.fid = data_payload.fid    
            
        self.__report.date = self._set_datetime()
        self.__report.rid = self._make_new_id()
        self.__report.type = "wicked"
        self.__report.result = False
        return
    
    # 버그 리포트 일때
    def try_set_bug_report(self, data_payload):
        self.__report.detail = data_payload.detail
        self.__report.type = "bug"
        
        if data_payload.images:
            ImageDescriper().try_report_image_upload(rid=self.__report.rid,
                                                    image_names=data_payload.image_names,
                                                    images=data_payload.images
                                                    )
        return
    
    # 리포트 저장
    def save_report(self):
        self._database.add_new_data(target_id="rid", new_data=self.__report.get_dict_form_data())
        self.__result = True
        return
    
    def get_response_form_data(self, head_parser):
        try:
            body = {
                'result' : self.__result
            }

            response = self._get_response_data(head_parser=head_parser, body=body)
            return response

        except Exception as e:
            raise CoreControllerLogicError("response making error | " + e)

# bias.state => "DEFAULT", "TEMP", "CONFIRMED", "APPROVED"

class MakeNewBiasModel(BaseModel):
    def __init__(self, database:Mongo_Database) -> None:
        super().__init__(database)
        self._info = ""
        self._bias = Bias(state="TEMP")
        self._result = False

    def get_response_form_data(self, head_parser):
        try:
            body = {
                'result' : self._result,
            }

            response = self._get_response_data(head_parser=head_parser, body=body)
            return response

        except Exception as e:
            raise CoreControllerLogicError("response making error | " + e)


    def try_make_new_bias(self, name, platform):
        if name == "NONE" or name == "":
            return False
        
        if platform == "NONE" or platform == "":
            return False
        
        self._bias.bid = str(uuid.uuid4())
        self._bias.bname = name
        self._bias.platform = platform
        return True
    
    def try_alert_to_admin(self, info:str):
        MailSender().alert_new_bias(user=self._user, bias=self._bias, info=info)
        MailSender().send_email_new_bias_added(
            receiver_email=self._user.email,
            bias=self._bias, info=info
            )
        
        self._database.add_new_data(target_id="bid", new_data=self._bias.get_dict_form_data())
        self._result = True
        return
    
class MyBiasModel(BaseModel):
    def __init__(self, database:Mongo_Database) -> None:
        super().__init__(database)
        self.__bias_list = []
        
    def get_bid_list(self):
        bid_list = []
        for bias in self.__bias_list:
            bid_list.append(bias.bid)
        return bid_list
    
    def get_bias_list(self):
        return self.__bias_list

    # 바이어스 데이터를 모두 받아와서 만들기
    def set_bias_list(self):
        if self._user.bids:
            bias_datas = self._database.get_datas_with_ids(target_id="bid", ids=self._user.bids)

            for bias_data in bias_datas:
                bias = Bias()
                bias.make_with_dict(bias_data)
                self.__bias_list.append(bias)
        return
        

    def get_response_form_data(self, head_parser):
        try:
            body = {
                "bias_list" : self._make_dict_list_data(list_data=self.__bias_list)
            }

            response = self._get_response_data(head_parser=head_parser, body=body)
            return response

        except Exception as e:
            raise CoreControllerLogicError("response making error | " + e)
    
class BiasFollowModel(BaseModel):
    def __init__(self, database:Mongo_Database) -> None:
        super().__init__(database)
        self.__bias= Bias()
        self.__result = False

    def find_bias(self, bid):
        try:
            raw_bias_data = self._database.get_data_with_id(target="bid", id=bid)
            if not raw_bias_data:
                return False
            self.__bias.make_with_dict(raw_bias_data)

        except Exception as e:
            raise CoreControllerLogicError(error_type="find_bias | " + str(e))
        return True
    
    # 내 최애를 누구로 할지 최종 결정하는 부분
    def set_my_bias(self, feed_search_engine:FeedSearchEngine):
        if self.__bias.bid in self._user.bids:
            self._user.bids.remove(self.__bias.bid)
            feed_search_engine.remove_user_to_bias(bid=self.__bias.bid, uid=self._user.uid)
        else:
            self._user.bids.append(self.__bias.bid)
            feed_search_engine.add_new_user_to_bias(bid=self.__bias.bid, uid=self._user.uid)

        self._database.modify_data_with_id(target_id="uid", target_data=self._user.get_dict_form_data())
        self.__result = True

        return True


    def get_response_form_data(self, head_parser):
        try:
            body = {
                'result' : self.__result
            }

            response = self._get_response_data(head_parser=head_parser, body=body)
            return response

        except Exception as e:
            raise CoreControllerLogicError("response making error | " + e)

class BiasSearchModel(BaseModel):
    def __init__(self, database:Mongo_Database) -> None:
        super().__init__(database)
        self._biases = []
        
    # 바이어스 전체 데이터 세팅
    def set_biases(self):
        bias_datas = self._database.get_all_data(target="bias")
        
        for bias_data in bias_datas:
            bias = Bias()
            bias.make_with_dict(dict_data=bias_data)
            self._biases.append(bias)
            
        if len(self._biases):
            return True
        else:
            return False
            
    
    def try_search_bias_with_category(self, category:str, biases=[]):
        self._biases=self._try_search_bias_with_category(category=category, biases=biases)
        return
        
    # 카테고리를 바탕으로 검색 -> 반드시 set_biases가 선행해도됨
    def _try_search_bias_with_category(self, category:str, biases=[]):
        result = []
        
        if len(biases):
            for bias in biases:
                if category in bias.platform:
                    result.append(bias)
        else:
            for bias in self._biases:
                if category in bias.platform:
                    result.append(bias)
                    
        return result

    def try_search_bias(self, bname, feed_search_engine:FeedSearchEngine):
        # ManagedBias 전체 호출
        managed_bias_list = feed_search_engine.get_all_managed_bias()

        # 코사인 유사도 평가를 통한 가장 비슷한 이름 검색
        result:list = self._search_similar_data(data_list=managed_bias_list,
                                    key_word=bname, key_attr="bname")
            
        # 검색 결과가 있으면 데이터 베이스에서 찾아서 보내줌
        if result:
            bids = []
                
            # ManagedBias에서 bid 추출
            for managed_bias in result:
                bids.append(managed_bias.bid)
                    
            # 검색 후 만들기
            bias_datas = self._database.get_datas_with_ids(target_id="bid", ids=bids)
            for bias_data in bias_datas:
                bias = Bias()
                bias.make_with_dict(bias_data)
                self._biases.append(bias)
        return

    def get_response_form_data(self, head_parser):
        try:
            body = {
                'biases' : self._make_dict_list_data(list_data=self._biases)
            }

            response = self._get_response_data(head_parser=head_parser, body=body)
            return response

        except Exception as e:
            raise CoreControllerLogicError("response making error | " + e)
        
class BiasFollowPageModel(BiasSearchModel):
    def __init__(self, database:Mongo_Database) -> None:
        super().__init__(database)
        self.__chzzk= []
        self.__soop= []
        self.__artist= []
        self.__youtube= []
        
    def try_get_bias_follow_page_data(self):
        self.__chzzk = self._try_search_bias_with_category(category="치지직")
        self.__soop = self._try_search_bias_with_category(category="SOOP")
        self.__artist= self._try_search_bias_with_category(category="아티스트")
        self.__youtube= self._try_search_bias_with_category(category="크리에이터")
        return


    def get_response_form_data(self, head_parser):
        try:
            body = {
                'chzzk' : self._make_dict_list_data(list_data=self.__chzzk),
                'soop' : self._make_dict_list_data(list_data=self.__soop),
                'artist' : self._make_dict_list_data(list_data=self.__artist),
                'youtube' : self._make_dict_list_data(list_data=self.__youtube)
            }

            response = self._get_response_data(head_parser=head_parser, body=body)
            return response

        except Exception as e:
            raise CoreControllerLogicError("response making error | " + e)
        
        
        
        
        
        
        
        
