from model.base_model import BaseModel
from model import Local_Database
#from others.data_domain import Alert
from others import CoreControllerLogicError,FeedManager, FeedSearchEngine, ObjectStorageConnection
from others import Comment, Feed, User, Interaction, Notice, Bias
from pprint import pprint
from datetime import datetime

class NoticeModel(BaseModel):
    def __init__(self, database:Local_Database) -> None:
        super().__init__(database)
        self._notices = []
        self._all_notice = []
        self._bias_notice = []
        self._simple_notice = []

    # 반응형 데이터 만들기
    def get_response_form_data(self, head_parser):
        try:
            body = {
                'notice': self._make_dict_list_data(list_data=self._notices),
            }

            response = self._get_response_data(head_parser=head_parser, body=body)
            return response

        except Exception as e:
            raise CoreControllerLogicError("response making error | " + e)
        
    def _paging_notices(self, notices:list, num_notices=5, last_nid=""):
        start_index = 0

        if last_nid != "":
            for index, notice in enumerate(notices):
                if notice.nid == last_nid:
                    start_index = index
                    break

        if len(notices) < num_notices:
            paging_notices = notices[start_index:]
        else:
            paging_notices = notices[start_index:start_index+num_notices]

        return paging_notices
    
    def set_base_notices_data(self):
        notice_datas = self._database.get_all_data(target="notice")
    
        for notice_data in notice_datas:
            notice = Notice()
            notice.make_with_dict(notice_data)
            self._notices.append(notice)
            
        return
    
    def set_bias_notices_data(self, bid=""):
        # BID를 받지 않았다면 return을 하도록 한다.
        if bid == "":
            return

        bias_data = self._database.get_data_with_id(target="bid", id=bid)
        
        if bias_data:
            bias = Bias()
            bias.make_with_dict(bias_data)
            
        else:
            return
        
        for notice in self._notices:
            
            # 표현할 공지가 아니라면 스킵
            if not notice.displayOpt:
                continue
            
            if notice.bid == bid:
                notice.bname = bias.bname
                self._bias_notice.append(notice)
        
        return

    def set_none_bias_notices_data(self):
        for notice in self._notices:
            # 표현할 공지가 아니라면 스킵
            if not notice.displayOpt:
                continue
            
            if notice.bid == "":
                self._all_notice.append(notice)
        return

    def get_notice_detail(self, nid):
        notice:Notice = Notice()
        notice_data = self._database.get_data_with_id(target="nid", id=nid)

        if not notice_data:
            notice.title = "없는 공지사항 입니다."
        else:
            notice.make_with_dict(notice_data)

        # simple_notice 전용
        self.simple_notice.append(notice)

    # 보낼 데이터 만들기
    def get_notice_list(self):
    # rank와 point를 포함한 데이터
        notice_datas = self._database.get_all_data(target="nid")
        for notice_data in notice_datas:
            notice = Notice()
            notice.make_with_dict(notice_data)
            notice.body = ""
            # notice_detail 전용
            self._simple_notice.append(notice)


    def set_send_notice_data(self, last_nid:str=""):
        self._notices.clear()
        self._notices.extend(self._bias_notice)
        self._notices.extend(self._all_notice)

        # 페이징 시작
        # paging_notices = self._paging_notices(notices=self._notices, last_nid=last_nid)
        
        # for notice in paging_notices:
        
        # 당장에는 주석처리
        #for notice in self._notices:
            #body_data = ObjectStorageConnection().get_notice_body(nid=notice.nid)
            #notice.body = body_data
            
        return

    def set_send_notice_data_for_details(self, last_nid:str=""):
        self._notices.clear()
        self._notices.extend(self._simple_notice)

        # 페이징 시작
        # paging_notices = self._paging_notices(notices=self._notices, last_nid=last_nid)

        # for notice in paging_notices:
        
        # 당장에는 주석처리
        #for notice in self._notices:
            #body_data = ObjectStorageConnection().get_notice_body(nid=notice.nid)
            #notice.body = body_data

        return
        
    # def try_get_notices(self, bid="", last_nid="", num_notices=5):
    #
    #     notice_datas = self._database.get_all_data(target="notice")
    #
    #     for notice_data in notice_datas:
    #         notice = Notice()
    #         notice.make_with_dict(notice_data)
    #         # 표현할 공지가 아니라면 스킵
    #         if not notice.displayopt:
    #             continue
    #
    #         # 만약 BID가 없다면 얘는 전체 공지용
    #         if bid=="":
    #             self._notices.append(notice)
    #
    #         # BID가 있다면 개별 공지
    #         else :
    #             if bid == notice.bid :
    #                 self._notices.append(notice)
    #
    #     self._notices = sorted(self._notices, key=lambda n:datetime.strptime(n.date, "%Y/%m/%d"), reverse=True)
    #     self._notices = self._paging_notices(self._notices, num_notices, last_nid)
    #     return


