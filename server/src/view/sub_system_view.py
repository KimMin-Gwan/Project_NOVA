from typing import Any, Optional
from fastapi import FastAPI
from view.master_view import Master_View, RequestHeader
from view.parsers import Head_Parser
from controller import Sub_Controller
from fastapi.responses import HTMLResponse
from others import FeedSearchEngine
from pprint import pprint

class Sub_Service_View(Master_View):
    def __init__(self, app:FastAPI, endpoint:str, database, head_parser:Head_Parser,
                 feed_search_engine:FeedSearchEngine) -> None:
        super().__init__(head_parser=head_parser)
        self.__app = app
        self._endpoint = endpoint
        self.__database = database
        self.__feed_search_engine=feed_search_engine
        self.notice_route()
        #self.bias_page_route("/bias_info")
        self.test_route()



    def test_route(self):
        @self.__app.get("/testing/try_get_feed")
        def try_get_feed():

            result = "default"
            result_index = "index"

            # 여기다가 조건을 작성

            target_type = "uname"
            target = "버튜버"
            num_feed= 10
            index = 240
            fid = 10

            # 여기서 만든 함수 실행
            #result , result_index = self.__feed_search_engine.try_get_feed_in_recent(target_type=target_type, target = target, num_feed=num_feed, index=index)
            #result , result_index = self.__feed_search_engine.try_get_feed_in_recent(search_type ="today", num_feed= 6, index=-2)
            
            result = self.__feed_search_engine.try_test_graph_recommnad_system(
                fid=fid)
               


            feed_data = self.__database.get_datas_with_ids(target_id="fid", ids=result)

            pprint(feed_data)

            return True
        



    def notice_route(self):
        @self.__app.get("/nova_notice/notice_list")
        def get_notice_list():
            sub_controller = Sub_Controller()
            model = sub_controller.get_notice_list(database=self.__database)
            response = model.get_response_form_data(self._head_parser)
            return response

        @self.__app.get("/nova_notice/notice_detail")
        def get_notice_detail(nid:Optional[str]):
            sub_controller = Sub_Controller()
            request = NoticeDetailRequest(nid=nid)
            model = sub_controller.get_notice_detail(database=self.__database, request=request)
            response = model.get_response_form_data(self._head_parser)
            return response


    #def bias_page_route(self, endpoint:str):
        #@self.__app.get(endpoint+'/home')
        #def home():
            #return 'Hello, This is Root of Core-System Service'
        
        ## 최애 페이지에 배너 정보
        #@self.__app.get(endpoint + '/banner')
        #def get_bias_banner(bias_id:Optional[str] = "solo"):
            #home_controller=Sub_Controller()
            #model = home_controller.get_bias_banner(database=self.__database,)
            #response = model.get_response_form_data(self._head_parser)
            #return response

        ## 최애 페이지에 지지자 순위 정보
        #@self.__app.get(endpoint + '/bias_n_league')
        #def get_bias_n_legue(bias_id:Optional[str] = ""):
            #request = BiasPageInfoRequest(bid=bias_id)
            #sub_controller =Sub_Controller()
            #model = sub_controller.get_bias_n_league_data(database=self.__database,
                                                          #request=request)
            #response = model.get_response_form_data(self._head_parser)
            #return response
        
        ## 최애 페이지에 지지자 순위 정보
        #@self.__app.get(endpoint + '/user_contribution')
        #def get_user_contribution(bias_id:Optional[str] = ""):
            #request = BiasPageInfoRequest(bid=bias_id)
            #sub_controller =Sub_Controller()
            #model = sub_controller.get_user_contribution(database=self.__database,
                                                          #request=request)
            #response = model.get_response_form_data(self._head_parser)
            #return response

        ## 최애 페이지에 지지자의 본인 기여도 정보
        #@self.__app.post(endpoint + '/my_contribution')
        #def get_my_contribution(raw_request:dict):
            #request = MyContributionRequest(request=raw_request)
            #sub_controller=Sub_Controller()
            #model = sub_controller.get_my_contribution(database=self.__database,
                                                          #request=request)
            #response = model.get_response_form_data(self._head_parser)
            #return response

class NoticeDetailRequest():
    def __init__(self, nid = None) -> None:
        self.nid=nid
        
class BiasPageInfoRequest():
    def __init__(self, bid = None) -> None:
        self.bid=bid  


class MyContributionRequest(RequestHeader):
    def __init__(self, request) -> None:
        super().__init__(request)
        body = request['body']
        self.token = body['token']
        self.bid = body['bid']



