from model.base_model import BaseModel
from model import Mongo_Database
from others import CoreControllerLogicError,FeedManager, FeedSearchEngine , ObjectStorageConnection
from others import Comment, Feed, User, FeedLink
from pprint import pprint
import time 


class FeedModel(BaseModel):
    def __init__(self, database:Mongo_Database) -> None:
        super().__init__(database)
        self._feeds = []
        self._key = -1
        self._comments = []
        self._send_data = []
        self._links = []
    
    # 단일 피드 데이터 전송
    def set_single_feed_data(self, fid:str):
        feed_data = self._database.get_data_with_id(target="fid", id=fid)

        if feed_data:
            feed = Feed()
            feed.make_with_dict(feed_data)
            
            # 노출 현황 이 1 이하면 죽어야됨
            # 0: 삭제됨 1 : 비공개 2: 차단 3: 댓글 작성 X 4 : 정상(전체 공개)
            if feed.display < 3:
                return
            
            self._feeds.append(feed)
            
            if feed.lid:
                feed_link_datas = self._database.get_datas_with_ids(target_id="lid", ids=feed.lid)
                
                for feed_link_data in feed_link_datas:
                    feed_link = FeedLink()
                    feed_link.make_with_dict(feed_link_data)
                    self._links.append(feed_link)
                
            # 포인터로 동작함
            self._feeds = self._set_feed_json_data(user=self._user, feeds=self._feeds)
        return
    
    # 좋아요 누르기
    # 완료
    def try_like_feed(self, feed_manager:FeedManager, data_payload):
        self._feeds = feed_manager.try_like_feed(user=self._user,
                                                fid=data_payload.fid)
        
        
        self._feeds = self._set_feed_json_data(user=self._user, feeds=self._feeds)
        return

    
    # send_data를 만들때 사용하는 함수임
    def _make_feed_data(self, fid_list):
        feed_datas = self._database.get_datas_with_ids(target_id="fid", ids=fid_list)
        feeds = []

        for feed_data in reversed(feed_datas):
            feed = Feed()
            feed.make_with_dict(feed_data)
            feeds.append(feed)

        feeds = self._set_feed_json_data(user=self._user, feeds=feeds)
        
        send_data = self.__set_send_data(feeds=feeds)
        return send_data
    
    # 피드 내용을 다듬어서 전송가능한 형태로 세팅
    # 포인터로 동작함
    
    def _set_feed_json_data(self, user:User, feeds:list):

        wusers = []
        uids = []
        result_feeds = []

        for single_feed in feeds:
            single_feed:Feed = single_feed
            uids.append(single_feed.uid)

        user_datas = self._database.get_datas_with_ids(target_id="uid", ids=uids)

        user_datas = list(filter(lambda x: x is not None, user_datas))

        for user_data in user_datas:
            single_user = User()
            single_user.make_with_dict(user_data)
            wusers.append(single_user)

        for feed in feeds:
            feed:Feed = feed
            if feed.display < 3:
                continue

            feed.raw_body = ObjectStorageConnection().get_feed_body(fid=feed.fid)

            feed.num_comment = len(feed.comment)

            for fid_n_date in user.like:
                target_fid = fid_n_date.split('=')[0]
                if target_fid == feed.fid:
                    feed.star_flag = True

            for wuser in wusers:
                if wuser.uid == feed.uid:
                    feed.nickname = wuser.uname

            if user.uid == feed.uid:
                feed.is_owner = True

            result_feeds.append(feed)

        return result_feeds
    
    # 전송 데이터 만들기
    def __set_send_data(self, feeds:list):
        send_data = []

        for feed in feeds:
            feed:Feed = feed

            # 0: 삭제됨 1 : 비공개 2: 차단 3: 댓글 작성 X 4 : 정상(전체 공개)
            if feed.display < 3:
                continue

            dict_data={}
            dict_data['feed'] = feed.get_dict_form_data()

            send_data.append(dict_data)
        return send_data

    def get_response_form_data(self, head_parser):
        try:
            body = {
                'feed' : self._make_dict_list_data(list_data=self._feeds),
                'key' : self._key,
                'comments' : self._make_dict_list_data(list_data=self._comments),
                'send_data' : self._send_data,
                'links' : self._make_dict_list_data(list_data=self._links)
            }

            response = self._get_response_data(head_parser=head_parser, body=body)
            return response

        except Exception as e:
            raise CoreControllerLogicError("response making error | " + e)

# 피드를 생성하거나 수정하는 모델, 삭제에도 사용될 것
class FeedEditModel(BaseModel):
    def __init__(self, database:Mongo_Database) -> None:
        super().__init__(database)
        self._result= False
        self._detail = "Somthing goes Bad| Error Code = 422"
    
    # dict 형태로 들어온 feed link의 데이터를 사용가능한 형태로 변환
    def set_feed_link(self, data_payload):
        feed_links = []
        for link_data in data_payload.link:
            feed_link = FeedLink(url=link_data['url'], explain=link_data['explain'])
            if feed_link.url == '':
                continue
            feed_links.append(feed_link)
        
        data_payload.link = feed_links
        return
        
    def try_edit_feed(self, feed_manager:FeedManager, data_payload):
        # 만약 fid가 ""가 아니면 수정이나 삭제 요청일것임
        # 근데 삭제 요청은 여기서 처리 안하니까 반드시 수정일것
        if data_payload.fid != "":
            detail, flag = feed_manager.try_modify_feed(
                user=self._user,
                data_payload = data_payload,
                fid=data_payload.fid,)
        else:
            detail, flag = feed_manager.try_make_new_feed(
                user=self._user,
                data_payload = data_payload,
                )

        self._result = flag
        self._detail = detail
        return

    def try_remove_feed(self, feed_manager:FeedManager, data_payload):
        detail, flag = feed_manager.try_remove_feed(user=self._user, fid=data_payload.fid)

        self._result = flag
        self._detail = detail
        return
    
    def check_result(self, request_manager):
        if not self._detail:
            if self._result == "NOT_FIT_IN":
                raise request_manager.image_size_exception
            elif self._result == "NOT_OWNER":
                raise request_manager.credentials_exception
            else:
                raise request_manager.system_logic_exception

    def get_response_form_data(self, head_parser):
        try:
            body = {
                "result" : self._result,
                }

            response = self._get_response_data(head_parser=head_parser, body=body)
            return response

        except Exception as e:
            raise CoreControllerLogicError("response making error | " + e)

class FeedSearchModelNew(FeedModel):
    def __init__(self, database:Mongo_Database) -> None:
        super().__init__(database)
        self.__history = []

    def _make_comment_data(self, cid_list):
        comment_datas = self._database.get_data_with_ids(target_id="cid", ids=cid_list)
        comments = []

        for comment_data in comment_datas:
            comment=Comment()
            comment.make_with_dict(comment_data)
            comments.append(comment)

        return comments

    def save_keyword(self, feed_search_engine:FeedSearchEngine, target=""):
        feed_search_engine.try_save_keyword_data(keyword=target)
        return

    def try_search_feed_with_keyword(self, feed_search_engine:FeedSearchEngine, feed_manager:FeedManager,
                                        search_columns:str, target="", target_time="", last_index=-1, num_feed=8):
        if search_columns == "":
            search_columns_list= []
        else:
            search_columns_list = [i.strip() for i in search_columns.split(",")]

        searched_fid_list = feed_search_engine.try_search_feed_new(target=target, search_columns=search_columns_list,
                                                                    target_time=target_time)

        # 페이징
        searched_fid_list, self._key = feed_manager.paging_fid_list(fid_list=searched_fid_list,
                                                                    last_index=last_index,
                                                                    page_size=num_feed)

        self._send_data = self._make_feed_data(fid_list=searched_fid_list)
        return


    def try_search_comment_with_keyword(self, feed_search_engine:FeedSearchEngine,
                                        feed_manager:FeedManager, target="", last_index=-1, num_feed=8):
        search_cid_list = feed_search_engine.try_search_comment_new(target=target)

        search_cid_list, self._key = feed_manager.paging_fid_list(fid_list=search_cid_list,
                                                                  last_index=last_index,
                                                                  page_size=num_feed)

        self._send_data = self._make_comment_data(cid_list=search_cid_list)

        return

    def get_response_form_data(self, head_parser):
        try:
            body = {
                'feed' : self._feeds,
                'comments' : self._comments,
                'key' : self._key,
                'send_data' : self._send_data,
            }

            response = self._get_response_data(head_parser=head_parser, body=body)
            return response

        except Exception as e:
            raise CoreControllerLogicError("response making error | " + e)

class MyFeedsModel(FeedModel):
    def __init__(self, database:Mongo_Database) -> None:
        super().__init__(database)

    def __search_user_nickname(self, uid:str, uids:list, wusers:list):
        if uid not in uids:
            return ""

        # uid가 존재함. 그러면 리스트에서 찾는다
        for user in wusers:
            if user.uid == uid:
                return user.uname

        return ""

    def __set_send_data(self):
        result_feeds = []
        uids = []
        wusers = []

        for single_feed in self._feeds:
            if single_feed.uid in uids:
                continue
            uids.append(single_feed.uid)

        user_datas = self._database.get_datas_with_ids(target_id="uid", ids=uids)
        for user_data in user_datas:
            single_user = User()
            single_user.make_with_dict(user_data)
            wusers.append(single_user)

        for feed in self._feeds:
            feed:Feed = feed
            # 삭제된거 지우고
            if feed.display < 3:
                continue
            
            feed.raw_body = ObjectStorageConnection().get_feed_body(fid = feed.fid)

            # comment 길이 & image 길이
            feed.num_comment = len(feed.comment)

            # 좋아요를 누를 전적
            for fid_n_date in self._user.like:
                target_fid = fid_n_date.split('=')[0]
                if target_fid == feed.fid:
                    feed.star_flag = True

            # 피드 작성자 이름
            # 나중에 nickname으로 바꿀것
            feed.nickname = self.__search_user_nickname(feed.uid, uids, wusers)
            feed.is_owner = True
            result_feeds.append(feed)
        return result_feeds

    def get_my_feeds(self, feed_manager:FeedManager, last_index:int=-1):
        # 이게 가능한게, 리스트에서, 인덱스로만 사용해서 참조 하기 때문에 이거 써도 된다.
        self._feeds = feed_manager.get_my_feeds(user=self._user)
        self._feeds, self._key = feed_manager.paging_fid_list(fid_list=self._feeds, last_index=last_index, page_size=3)
        self._feeds = self.__set_send_data()
        return


    def get_liked_feeds(self, feed_manager:FeedManager, last_index:int=-1):
        self._feeds = feed_manager.get_liked_feeds(user=self._user)
        self._feeds, self._key = feed_manager.paging_fid_list(fid_list=self._feeds, last_index=last_index, page_size=3)
        self._feeds = self.__set_send_data()
        return


class FilteredFeedModel(FeedModel):
    def __init__(self, database:Mongo_Database):
        super().__init__(database)
        
    def is_bids_data_empty(self, data_payload):
        if not data_payload.bids:
            data_payload.bids = data_payload.cookie_bid_list
        return

    def try_filtered_feed_with_options(self,
                                       feed_search_engine:FeedSearchEngine,
                                       feed_manager:FeedManager,
                                       category:list,
                                       last_index:int=-1,
                                       num_feed:int=4,
                                       ):

        # 필터링 전 Feeds 들을 가져옵니다.
        # 모든 Feed를 가져온 다음. 게시글을 하나하나씩 쳐내는 방식을 씁니다.
        fid_list = feed_manager.get_all_fids()

        # 1차 필터링 : FClass를 통한 분류를 먼저 진행합니다.
        #   왜 FClass 부터 먼저 진행하나요? -> 간단한 것부터 먼저 분류합니다.
        #
        fid_list = feed_search_engine.try_filtered_feed_with_option(fid_list=fid_list, option="feed", keys=[])
        # pprint(len(fid_list))
        # 2차 필터링 : Category 별 분류를 진행합니다.
        # AD의 경우, 생각중
        fid_list = feed_search_engine.try_filtered_feed_with_option(fid_list=fid_list, option="category", keys=category)
        # pprint(len(fid_list))
        # 마지막, 분류가 끝이 났으면 페이징을 진행합니다.
        fid_list, self._key = feed_manager.paging_fid_list(fid_list=fid_list, last_index=last_index, page_size=num_feed)

        self._send_data = self._make_feed_data(fid_list=fid_list)

        return

    # BID와 카테고리를 통한 필터링 기능
    def try_filtered_feed_community(self,
                                    feed_search_engine:FeedSearchEngine,
                                    feed_manager:FeedManager,
                                    bid:str,
                                    category:str,
                                    last_index:int=-1,
                                    num_feed:int=4,):

        # 넘겨주는 값
        # 기본 : bid == "" (선택하지않음.), 선택 시, 선택된 BID를 가져옴
        # 기본 : category == "" (선택하지않음). BID 커뮤니티에 있는 게시글 중 카테고리 필터링을 거치지 않는다
        #       선택 시, 추가로 카테고리 필터링을 거치게됨

        fid_list = feed_search_engine.try_feed_with_bid_n_filtering(target_bid=bid, category=category)

        fid_list, self._key = feed_manager.paging_fid_list(fid_list=fid_list, last_index=last_index, page_size=num_feed)
        # pprint(fid_list)
        self._send_data = self._make_feed_data(fid_list=fid_list)
        return

    def get_response_form_data(self, head_parser):
        try:
            body = {
                'send_data' : self._send_data,
                'key' : self._key
            }

            response = self._get_response_data(head_parser=head_parser, body=body)
            return response

        except Exception as e:
            raise CoreControllerLogicError("response making error | " + e)
