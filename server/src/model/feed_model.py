from model.base_model import BaseModel
from model import Local_Database
#from others.data_domain import Alert
from others import CoreControllerLogicError,FeedManager, FeedSearchEngine, ObjectStorageConnection, HTMLEXtractor
from others import Comment, Feed, User, Interaction, FeedLink
from pprint import pprint


class FeedModel(BaseModel):
    def __init__(self, database:Local_Database) -> None:
        super().__init__(database)
        self._feeds = []
        self._key = -1
        self._comments = []
        self._interaction = Interaction()
        self._send_data = []
        self._links = []
    
    # 단일 피드 데이터 전송
    def set_single_feed_data(self, fid:str, feed_manager:FeedManager):
        feed_data = self._database.get_data_with_id(target="fid", id=fid)

        if feed_data:
            feed = Feed()
            feed.make_with_dict(feed_data)
            
            # 노출 현황 이 1 이하면 죽어야됨
            # 0: 삭제됨 1 : 비공개 2: 차단 3: 댓글 작성 X 4 : 정상(전체 공개)
            if feed.display < 3:
                return
            
            self._feeds.append(feed)
            
            #if feed.iid != "":
                #interaction_data = self._database.get_data_with_id(target="iid", id=feed.iid)
                #self._interaction.make_with_dict(interaction_data)
                
                #self._set_feed_interactied(self._user, interaction=self._interaction)
                
            if feed.lid:
                feed_link_datas = self._database.get_datas_with_ids(target_id="lid", ids=feed.lid)
                
                for feed_link_data in feed_link_datas:
                    feed_link = FeedLink()
                    feed_link.make_with_dict(feed_link_data)
                    self._links.append(feed_link)
                
            # 포인터로 동작함
            self._feeds = self._set_feed_json_data(user=self._user, feeds=self._feeds)
        return
    
    def set_original_feed_data(self, fid:str):
        feed_data = self._database.get_data_with_id(target="fid", id=fid)

        if feed_data:
            feed = Feed()
            feed.make_with_dict(feed_data)
            
            # 노출 현황 이 1 이하면 죽어야됨
            # 0: 삭제됨 1 : 비공개 2: 차단 3: 댓글 작성 X 4 : 정상(전체 공개)
            if feed.display < 3:
                return
            
            # 롱폼은 바디 데이터를 받아야됨
            if feed.fclass != "short":
                feed.raw_body = ObjectStorageConnection().get_feed_body(fid = feed.fid)
                _, feed.image = ObjectStorageConnection().extract_body_n_image(raw_data=feed.raw_body)

            else:
                feed.raw_body = feed.body
                    
            feed.is_reworked = False
            
            feed.p_body = ""
            feed.reworked_body = ""
            self._feeds.append(feed)
        return
    
    def set_original_comment_data(self, cid:str):
        comment_data = self._database.get_data_with_id(target="cid", id=cid)
        new_comment = Comment()
        new_comment.make_with_dict(comment_data)
        
        if new_comment.display == 0:
            return
                
        self._comments.append(new_comment)
        return
    
    # send_data를 만들때 사용하는 함수임
    def _make_feed_data_n_interaction_data(self, feed_manager, fid_list):
        feed_datas = self._database.get_datas_with_ids(target_id="fid", ids=fid_list)

        feeds = []
        #iids = []

        for feed_data in reversed(feed_datas):
            feed = Feed()
            feed.make_with_dict(feed_data)
            feeds.append(feed)
            
            #if feed.iid != "":
                #iids.append(feed.iid)
        feeds = self._set_feed_json_data(user=self._user, feeds=feeds)
        #interaction_datas = self._database.get_datas_with_ids(target_id="iid", ids=iids)
        #interactions = []
        
        #for interaction_data in interaction_datas:
            #interaction = Interaction()
            #interaction.make_with_dict(interaction_data)
            #interactions.append(interaction)
            
        # 인터엑션 넣을 필요 있음
        
        send_data = self.__set_send_data(feeds=feeds)
        return send_data

    def set_feed_data(self, feed_search_engine:FeedSearchEngine, feed_manager:FeedManager,
                      search_columns:str="", target="", last_index=-1, num_feed=1):

        if search_columns == "":
            search_columns_list= []
        else:
            search_columns_list = [i.strip() for i in search_columns.split(",")]


        fid_list = feed_search_engine.try_search_feed_new(target=target, search_columns=search_columns_list)
        fid_list, self._key = feed_manager.paging_fid_list(fid_list, last_index=last_index, page_size=num_feed)

        self._send_data = self._make_feed_data_n_interaction_data(feed_manager=feed_manager, fid_list=fid_list)
        return

    # def set_feed_data(self, feed_search_engine:FeedSearchEngine, feed_manager,
    #                     target_type="default", target="", num_feed=1, index=-1):
    #
    #     fid_list, self._key = feed_search_engine.try_search_feed(
    #         target_type=target_type, target=target, num_feed=num_feed, index=index)
    #
    #     self._send_data = self._make_feed_data_n_interaction_data(feed_manager=feed_manager, fid_list=fid_list)
    #     return

    def set_best_feed_with_time(self, feed_search_engine:FeedSearchEngine, feed_manager:FeedManager,
                                search_type, time_type, last_index=-1, num_feed=4):
        
        fid_list = feed_search_engine.try_get_feed_in_recent(search_type=search_type, time_type=time_type)
        fid_list, self._key = feed_manager.paging_fid_list(fid_list, last_index=last_index, page_size=num_feed)
        self._send_data = self._make_feed_data_n_interaction_data(feed_manager=feed_manager, fid_list=fid_list)

        return

    # def set_today_best_feed(self, feed_search_engine:FeedSearchEngine, feed_manager,
    #                          index=-1, num_feed=4):
    #     fid_list, self._key = feed_search_engine.try_get_feed_in_recent(
    #         search_type="today", num_feed=num_feed, index=index)
    #
    #     self._send_data = self._make_feed_data_n_interaction_data(feed_manager=feed_manager, fid_list=fid_list)
    #     return
    #
    # def set_weekly_best_feed(self, feed_search_engine:FeedSearchEngine, feed_manager,
    #                          index=-1, num_feed=4):
    #     fid_list, self._key = feed_search_engine.try_get_feed_in_recent(
    #         search_type="weekly", num_feed=num_feed, index=index)
    #
    #     self._send_data = self._make_feed_data_n_interaction_data(feed_manager=feed_manager, fid_list=fid_list)
    #     return
    #
    # def set_all_feed(self, feed_search_engine:FeedSearchEngine, feed_manager,
    #                   index=-1, num_feed=4):
    #     fid_list, self._key = feed_search_engine.try_get_feed_in_recent(
    #         search_type="recent", num_feed=num_feed, index=index)
    #
    #     self._send_data = self._make_feed_data_n_interaction_data(feed_manager=feed_manager, fid_list=fid_list)
    #     return
    
    # 상호작용하기
    def try_interact_feed(self, feed_manager:FeedManager, data_payload):
        self._feeds = feed_manager.try_interaction_feed(user=self._user,
                                                    fid=data_payload.fid,
                                                    action=data_payload.action)
        
        if self._feeds:
            interaction_data = self._database.get_data_with_id(target="iid", id=self._feeds[0].iid)
            self._interaction = Interaction()
            self._interaction.make_with_dict(dict_data=interaction_data)
            
        self._set_feed_interactied(user=self._user, interaction=self._interaction)
        
        self._feeds = self._set_feed_json_data(user=self._user, feeds=self._feeds)
        return

    # 좋아요 누르기
    # 완료
    def try_staring_feed(self, feed_manager:FeedManager, data_payload):
        self._feeds = feed_manager.try_staring_feed(user=self._user,
                                                fid=data_payload.fid)
        
        
        self._feeds = self._set_feed_json_data(user=self._user, feeds=self._feeds)
        return

    # 댓글 새로 달기
    # 1. 댓글 달기 -> 2. 댓글 달고나서 전체 댓글 데이터만 제공
    # 파라미터 수정 필요 
    def try_make_new_comment(self, feed_manager:FeedManager, data_payload, ai_manager):
        feed_manager.try_make_comment_on_feed(user=self._user,
                                            fid=data_payload.fid,
                                            target_cid=data_payload.target_cid,
                                            body=data_payload.body,
                                            ai_manager=ai_manager
                                            )
        self._comments = feed_manager.get_all_comment_on_feed( user=self._user,
                                                               fid=data_payload.fid)
        return

    # def try_make_new_reply_comment(self, feed_manager:FeedManager, data_payload):
    #     feed_manager.try_make_reply_on_comment(user=self._user,
    #                                            fid=data_payload.fid,
    #                                            target_cid=data_payload.target_cid,
    #                                            body=data_payload.body)
    #     self._comments = feed_manager.get_all_comment_on_feed(user=self._user,
    #                                                           fid=data_payload.fid)
    #     return

    # 댓글 불러오기
    # 단일 feed에 맞는 댓글 전체 불러오기
    def get_all_comment_on_feed(self, feed_manager:FeedManager, data_payload):
        self._comments = feed_manager.get_all_comment_on_feed( user=self._user,
                                                               fid=data_payload.fid)
        return

    # 댓글 지우기
    # 1. 댓글 지우기 -> 전체 댓글 데이터 제공
    # 파라미터 수정 필요 
    def try_remove_comment(self, feed_manager:FeedManager, data_payload):
        feed_manager.remove_comment_on_feed( user=self._user,
                                                               fid=data_payload.fid,
                                                               cid=data_payload.cid
                                                               )
        self._comments = feed_manager.get_all_comment_on_feed( user=self._user,
                                                               fid=data_payload.fid)
        return

    # 댓글 좋아요
    def try_like_comment(self, feed_manager:FeedManager, data_payload):
        feed_manager.try_like_comment( user=self._user,
                                    fid=data_payload.fid,
                                    cid=data_payload.cid)
        self._comments = feed_manager.get_all_comment_on_feed( user=self._user,
                                                               fid=data_payload.fid)
        return
    
    # 피드 내용을 다듬어서 전송가능한 형태로 세팅
    # 포인터로 동작함
    def _set_feed_json_data(self, user:User, feeds:list):
        wusers = []
        uids=[]
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
            
            # 노출 현황 이 1 이하면 죽어야됨
            # 0: 삭제됨 1 : 비공개 2: 차단 3: 댓글 작성 X 4 : 정상(전체 공개)
            if feed.display < 3:
                continue
            
            feed:Feed = feed
            # level
            # 1: 정상 2: 약간의 욕설과 반말 3: 인신공격 및 성희롱 등
            # 만약 3단계를 선택했다면 모든 글은 원본 데이터를 제공함
            # 만약 2단계를 선택했다면 3단계의 글은 전부다 재구성 된 데이터로 나와야됨
            # 만약 1단계를 선택했다면 2단계와 3단계 글은 전부다 재구성 된 데이터로 나와야됨
            
            # 재구성 할 필요 있음
            if user.level < feed.level:
                # 롱폼은 바디 데이터를 받아야됨
                if feed.fclass != "short":
                    # 원본 긁어와서
                    feed.raw_body = ObjectStorageConnection().get_feed_body(fid = feed.fid)
                    
                    
                    # 재구성된 HTML데이터에 이미지 끼워넣고
                    feed.raw_body = HTMLEXtractor().restore_img_src_data_in_html(raw_html=feed.raw_body, p_html=feed.p_body)
                    
                    # 미리보기용 바디랑 이미지 데이터 만들어줌
                    feed.body, feed.image = ObjectStorageConnection().extract_body_n_image(raw_data=feed.raw_body)

                else:
                    # 미리보기용 바디데이터는 재구성된 데이터로
                    feed.body = feed.reworked_body
                    # 실 데이터도 재구성된 데이터
                    #feed.raw_body = feed.body
                
                # 재구성된 데이터라고 알릴 것
                feed.is_reworked = True
                
            # 필요 없음
            else:
                # 롱폼은 바디 데이터를 받아야됨
                if feed.fclass != "short":
                    feed.raw_body = ObjectStorageConnection().get_feed_body(fid = feed.fid)
                    _, feed.image = ObjectStorageConnection().extract_body_n_image(raw_data=feed.raw_body)

                else:
                    feed.raw_body = feed.body
                    
                feed.is_reworked = False
            
            
            feed.p_body = ""
            feed.reworked_body = ""
            
            # comment 길이 & image 길이
            feed.num_comment = len(feed.comment)
            feed.num_image = len(feed.image)

            # 좋아요를 누를 전적
            
            for fid_n_date in user.like:
                target_fid = fid_n_date.split('=')[0]
                if target_fid == feed.fid:
                    feed.star_flag = True

            # 피드 작성자 이름
            # 나중에 nickname으로 바꿀것
            for wuser in wusers:
                if wuser.uid == feed.uid:
                    feed.nickname = wuser.uname
                    
            if user.uid == feed.uid:
                feed.is_owner = True
                
            
            result_feeds.append(feed)
            
        return result_feeds
    
    # 상호작용에서 내가 상호작용한 내용이 있는지 검토하는 부분
    def _set_feed_interactied(self, user, interaction:Interaction):
        for i, attend in enumerate(interaction.attend):
            for uid in attend:
                if uid == user.uid:
                    interaction.my_attend = i
        return

    # 전송 데이터 만들기
    # feed 데이터와 interaction을 모두 줘야하는 경우에만 사용
    def __set_send_data(self, feeds:list):
        send_data = []

        for feed in feeds:
            feed:Feed = feed

            # 0: 삭제됨 1 : 비공개 2: 차단 3: 댓글 작성 X 4 : 정상(전체 공개)
            if feed.display < 3:
                continue

            #interaction = Interaction()
            #for single_interaction in interactions:
                #if single_interaction.iid == feed.iid:
                    #interaction = single_interaction
                    #self._set_feed_interactied(self._user, interaction=single_interaction)
                    

            dict_data={}
            dict_data['feed'] = feed.get_dict_form_data()
            #dict_data['interaction'] = interaction.get_dict_form_data()

            send_data.append(dict_data)
        return send_data

    def get_response_form_data(self, head_parser):
        try:
            body = {
                'feed' : self._make_dict_list_data(list_data=self._feeds),
                'key' : self._key,
                'interaction' :self._interaction.get_dict_form_data(),
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
    def __init__(self, database:Local_Database) -> None:
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
        
    def try_edit_feed(self, feed_manager:FeedManager, data_payload, ai_manager):
        # 만약 fid가 ""가 아니면 수정이나 삭제 요청일것임
        # 근데 삭제 요청은 여기서 처리 안하니까 반드시 수정일것
        if data_payload.fid != "":
            detail, flag = feed_manager.try_modify_feed(
                user=self._user,
                data_payload = data_payload,
                fid=data_payload.fid,
                ai_manager=ai_manager
                )
        else:
            detail, flag = feed_manager.try_make_new_feed(
                user=self._user,
                data_payload = data_payload,
                ai_manager=ai_manager
                )

        self._result = flag
        self._detail = detail
        return

    def try_remove_feed(self, feed_manager:FeedManager, data_payload):
        detail, flag = feed_manager.try_remove_feed_new(user=self._user, fid=data_payload.fid)

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
    def __init__(self, database:Local_Database) -> None:
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
                                        search_columns:str, fclass="", target="", target_time="", last_index=-1, num_feed=8):
        if search_columns == "":
            search_columns_list= []
        else:
            search_columns_list = [i.strip() for i in search_columns.split(",")]

        searched_fid_list = feed_search_engine.try_search_feed_new(target=target, search_columns=search_columns_list,
                                                                   fclass=fclass, target_time=target_time)

        # 페이징
        searched_fid_list, self._key = feed_manager.paging_fid_list(fid_list=searched_fid_list,
                                                                    last_index=last_index,
                                                                    page_size=num_feed)

        self._send_data = self._make_feed_data_n_interaction_data(feed_manager=feed_manager, fid_list=searched_fid_list)
        return

    # def try_search_feed_with_hashtag(self, feed_search_engine:FeedSearchEngine,
    #                                  feed_manager:FeedManager, fclass="", target="", target_time="",last_index=-1, num_feed=8):
    #     searched_fid_list = feed_search_engine.try_search_feed_new(target_type="hashtag", target=target, fclass=fclass, target_time=target_time)
    #
    #     # 페이징
    #     searched_fid_list, self._key = feed_manager.paging_fid_list(fid_list=searched_fid_list,
    #                                                                 last_index=last_index,
    #                                                                 page_size=num_feed)
    #
    #     self._send_data = self._make_feed_data_n_interaction_data(feed_manager=feed_manager, fid_list=searched_fid_list)
    #     return
    #
    # def try_search_feed_with_keyword(self, feed_search_engine:FeedSearchEngine,
    #                                  feed_manager:FeedManager, fclass="", target="", target_time="", last_index=-1, num_feed=8):
    #     searched_fid_list = feed_search_engine.try_search_feed_new(target_type="keyword", target=target, fclass=fclass)
    #
    #     # 페이징
    #     searched_fid_list, self._key = feed_manager.paging_fid_list(fid_list=searched_fid_list,
    #                                                                 last_index=last_index,
    #                                                                 page_size=num_feed)
    #
    #     self._send_data = self._make_feed_data_n_interaction_data(feed_manager=feed_manager,fid_list=searched_fid_list)
    #
    #     return
    #
    # def try_search_feed_with_uname(self, feed_search_engine:FeedSearchEngine,
    #                                feed_manager:FeedManager, fclass="", target="", last_index=-1, num_feed=8):
    #     searched_fid_list = feed_search_engine.try_search_feed_new(target_type="uname", target=target, fclass=fclass)
    #     # 페이징
    #     searched_fid_list, self._key = feed_manager.paging_fid_list(fid_list=searched_fid_list,
    #                                                                 last_index=last_index,
    #                                                                 page_size=num_feed)
    #
    #     self._send_data = self._make_feed_data_n_interaction_data(feed_manager=feed_manager,fid_list=searched_fid_list)
    #
    #     return
    #
    # def try_search_feed_with_bid(self, feed_search_engine:FeedSearchEngine,
    #                              feed_manager:FeedManager, fclass="", target="", last_index=-1, num_feed=8):
    #     searched_fid_list = feed_search_engine.try_search_feed_new(target_type="bid", target=target, fclass=fclass)
    #     # 페이징
    #     searched_fid_list, self._key = feed_manager.paging_fid_list(fid_list=searched_fid_list,
    #                                                                 last_index=last_index,
    #                                                                 page_size=num_feed)
    #     self._send_data = self._make_feed_data_n_interaction_data(feed_manager=feed_manager, fid_list=searched_fid_list)
    #     return
    #
    # def try_search_feed_with_fid(self, feed_search_engine:FeedSearchEngine,
    #                              feed_manager:FeedManager, target="", last_index=-1, num_feed=8):
    #     searched_fid_list = feed_search_engine.try_search_feed_new(target_type="fid", target=target)
    #     # 페이징
    #     searched_fid_list, self._key = feed_manager.paging_fid_list(fid_list=searched_fid_list,
    #                                                                 last_index=last_index,
    #                                                                 page_size=num_feed)
    #     self._send_data = self._make_feed_data_n_interaction_data(feed_manager=feed_manager, fid_list=searched_fid_list)
    #     return

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

class FeedSearchModel(FeedModel):
    def __init__(self, database:Local_Database) -> None:
        super().__init__(database)
        self._hashtag_feed= []
        self._uname_feed= []
        self.__feed = []
        self.__history = []

    # 추천하는 단일 피드 제공
    def set_recommend_feed(self, feed_search_engine:FeedSearchEngine, fid:str, history:list, feed_manager):
        fid = feed_search_engine.try_recommend_feed(fid=fid, history=history, user=self._user)

        self.__history = history.append(fid)

        feed_data = self._database.get_data_with_id(target="fid", id=fid)

        feed = Feed()
        feed.make_with_dict(feed_data)

        feeds = self._set_feed_json_data(user=self._user, feeds=[feed])

        # 인터엑션 넣을 필요 있음
        self._send_data = self.__set_send_data(feeds=feeds)
        return

    # fid로 검색 (숏피드 들어갈때 사용했었음)
    def try_search_feed_with_fid(self, feed_search_engine:FeedSearchEngine, feed_manager, fid="" ):
        if fid == "":
            fid=feed_search_engine.try_get_random_feed()

        self.__history.append(str(fid))
        second_fid = feed_search_engine.try_recommend_feed(fid=str(fid),
                                                history=self.__history,
                                                user=self._user,
                                                )
        self.__history.append(second_fid)

        # pprint(self.__history)

        feed_datas = self._database.get_datas_with_ids(target_id="fid", ids=[str(fid), second_fid])
        for feed_data in feed_datas:
            feed = Feed()
            feed.make_with_dict(dict_data=feed_data)
            self.__feed.append(feed)

        # 인터엑션은 별도라 여기 포함 안됨
        self.__feed = self.__feed = self._set_feed_json_data(user=self._user, feeds=self.__feed)
        return

    # def try_search_feed(self, feed_search_engine:FeedSearchEngine, feed_manager,
    #                     target="", num_feed=1, index=-1, ):
    #
    #     hashtag_feed_fid, self._key = feed_search_engine.try_search_feed(
    #         target_type="hashtag", target=target, num_feed=num_feed, index=index)
    #
    #     user_feed_fid, self._key = feed_search_engine.try_search_feed(
    #         target_type="uname", target=target, num_feed=num_feed, index=index)
    #
    #     hashtag_feed_data = self._database.get_datas_with_ids(target_id="fid", ids=hashtag_feed_fid)
    #     user_feed_fid = self._database.get_datas_with_ids(target_id="fid", ids=user_feed_fid)
    #
    #     for feed_data1 in hashtag_feed_data:
    #         feed = Feed()
    #         feed.make_with_dict(feed_data1)
    #         self._hashtag_feed.append(feed)
    #
    #     for feed_data2 in user_feed_fid:
    #         feed = Feed()
    #         feed.make_with_dict(feed_data2)
    #         self._uname_feed.append(feed)
    #
    #     self._hashtag_feed = self._set_feed_json_data(user=self._user, feeds=self._hashtag_feed )
    #     self._uname_feed = self._set_feed_json_data(user=self._user, feeds=self._uname_feed)
    #
    #     return
    #
    # def try_search_feed_with_hashtag(self, feed_search_engine:FeedSearchEngine, feed_manager,
    #                                 target="", num_feed=1, index=-1):
    #
    #     hashtag_feed_fid, self._key = feed_search_engine.try_search_feed(
    #         target_type="hashtag", target=target, num_feed=num_feed, index=index)
    #
    #     hashtag_feed_data = self._database.get_datas_with_ids(target_id="fid", ids=hashtag_feed_fid)
    #
    #     feeds = []
    #
    #     for feed_data in hashtag_feed_data:
    #         feed = Feed()
    #         feed.make_with_dict(feed_data)
    #         feeds.append(feed)
    #
    #     feeds = self._set_feed_json_data(user=self._user, feeds=feeds)
    #
    #     # 인터엑션 필요
    #     self._send_data = self.__set_send_data(feeds=feeds)
    #     return
    #
    # def try_search_feed_with_keyword(self, feed_search_engine:FeedSearchEngine,
    #                                  feed_manager:FeedManager, target="", last_index=-1, num_feed=1):
    #     searched_fid_list = feed_search_engine.try_search_feed_new(target_type="keyword", target=target)
    #
    #     # 페이징
    #     searched_fid_list, self._key = feed_manager.paging_fid_list(fid_list=searched_fid_list,
    #                                                                 last_index=last_index,
    #                                                                 page_size=num_feed)
    #
    #     self._send_data = self._make_feed_data_n_interaction_data(feed_manager=feed_manager,
    #                                                               fid_list=searched_fid_list)
    #     return


    def get_response_form_data(self, head_parser):
        try:
            body = {
                'hashtag_feed' : self._make_dict_list_data(list_data=self._hashtag_feed),
                'uname_feed' : self._make_dict_list_data(list_data=self._uname_feed),
                'feed' : self._make_dict_list_data(list_data=self.__feed),
                'history' : self.__history,
                'key' : self._key,
                'comments' : self._make_dict_list_data(list_data=self._comments)
            }

            response = self._get_response_data(head_parser=head_parser, body=body)
            return response

        except Exception as e:
            raise CoreControllerLogicError("response making error | " + e)

class MyFeedsModel(FeedModel):
    def __init__(self, database:Local_Database) -> None:
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
            # 마이페이지에 인터엑션은 표시 없음
            feed.iid = ""

            # 삭제된거 지우고
            if feed.display < 3:
                continue

            # 롱폼은 바디 데이터를 받아야됨
            if feed.fclass != "short":
                feed.raw_body = ObjectStorageConnection().get_feed_body(fid = feed.fid)
                _, feed.image = ObjectStorageConnection().extract_body_n_image(raw_data=feed.raw_body)

            else:
                feed.raw_body = feed.body

            # comment 길이 & image 길이
            feed.num_comment = len(feed.comment)
            feed.num_image = len(feed.image)

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

    def get_my_long_feeds(self, feed_manager:FeedManager, last_index:int=-1):
        # 이게 가능한게, 리스트에서, 인덱스로만 사용해서 참조 하기 때문에 이거 써도 된다.
        self._feeds = feed_manager.get_my_long_feeds(user=self._user)
        self._feeds, self._key = feed_manager.paging_fid_list(fid_list=self._feeds, last_index=last_index, page_size=3)
        self._feeds = self.__set_send_data()
        return

    def get_my_short_feeds(self, feed_manager:FeedManager, last_index:int=-1):
        # 이게 가능한게, 리스트에서, 인덱스로만 사용해서 참조 하기 때문에 이거 써도 된다.
        self._feeds = feed_manager.get_my_short_feeds(user=self._user)
        self._feeds, self._key = feed_manager.paging_fid_list(fid_list=self._feeds, last_index=last_index, page_size=3)
        self._feeds = self.__set_send_data()

        return

    def get_liked_feeds(self, feed_manager:FeedManager, last_index:int=-1):
        self._feeds = feed_manager.get_liked_feeds(user=self._user)
        self._feeds, self._key = feed_manager.paging_fid_list(fid_list=self._feeds, last_index=last_index, page_size=3)
        self._feeds = self.__set_send_data()

        return

    def get_interacted_feeds(self, feed_manager:FeedManager, last_index:int=-1):
        self._feeds = feed_manager.get_interacted_feeds(user=self._user)
        self._feeds, self._key = feed_manager.paging_fid_list(fid_list=self._feeds, last_index=last_index, page_size=3)
        self._feeds = self.__set_send_data()

        return

class CommentSearchModel(FeedModel):
    def __init__(self, database:Local_Database) -> None:
        super().__init__(database)

    def try_search_comment_with_keyword(self, feed_manager:FeedManager,
                                        target:str, last_index=-1, num_comments=8):

        self._feeds = feed_manager.get_comments_with_type_and_keyword(
            user=self._user, type="search", keyword=target
        )
        self._feeds, self._key = feed_manager.paging_fid_list(fid_list=self._feeds, last_index=last_index, page_size=num_comments)
        # self._comments = feed_manager.get_comments_with_keyword(keyword=target)
        # self._comments, self._key = feed_manager.paging_fid_list(fid_list=self._comments, last_index=last_index, page_size=num_comments)

        return

    def get_response_form_data(self, head_parser):
        try:
            body = {
                'key' : self._key,
                'feeds' : self._make_dict_list_data(list_data=self._feeds)
            }

            response = self._get_response_data(head_parser=head_parser, body=body)
            return response

        except Exception as e:
            raise CoreControllerLogicError("response making error | " + e)

class FilteredFeedModel(FeedModel):
    def __init__(self, database:Local_Database):
        super().__init__(database)
        
    def is_bids_data_empty(self, data_payload):
        if not data_payload.bids:
            data_payload.bids = data_payload.cookie_bid_list
        return

    def try_filtered_feed_with_options(self,
                                       feed_search_engine:FeedSearchEngine,
                                       feed_manager:FeedManager,
                                       category:list,
                                       fclass:str="",
                                       last_index:int=-1,
                                       num_feed:int=4,
                                       ):

        
        # 필터링 전 Feeds 들을 가져옵니다.
        # 모든 Feed를 가져온 다음. 게시글을 하나하나씩 쳐내는 방식을 씁니다.
        fid_list = feed_manager.get_all_fids()

        # pprint(fclass)

        # 1차 필터링 : FClass를 통한 분류를 먼저 진행합니다.
        #   왜 FClass 부터 먼저 진행하나요? -> 간단한 것부터 먼저 분류합니다.
        #
        fid_list = feed_search_engine.try_filtered_feed_with_option(fid_list=fid_list, option="fclass", keys=[fclass])
        # pprint(len(fid_list))
        # 2차 필터링 : Category 별 분류를 진행합니다.
        # AD의 경우, 생각중
        fid_list = feed_search_engine.try_filtered_feed_with_option(fid_list=fid_list, option="category", keys=category)
        # pprint(len(fid_list))
        # 마지막, 분류가 끝이 났으면 페이징을 진행합니다.
        fid_list, self._key = feed_manager.paging_fid_list(fid_list=fid_list, last_index=last_index, page_size=num_feed)

        self._send_data = self._make_feed_data_n_interaction_data(feed_manager=feed_manager, fid_list=fid_list)

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
        self._send_data = self._make_feed_data_n_interaction_data(feed_manager=feed_manager, fid_list=fid_list)

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

class CommunityFeedModel(FeedModel):
    def __init__(self, database:Local_Database) -> None:
        super().__init__(database)
        self.__last_fid = ""

    # 단순히 bid만 요청했을 때
    def try_search_feed_with_bid(self, bid:str, last_fid:str,
                                 feed_search_engine:FeedSearchEngine,
                                 feed_manager:FeedManager
                                 ):

        # bias를 선택하지 않았을 때
        if bid == "":
            fid_list, self.__last_fid = feed_search_engine.try_feed_with_bid_n_filtering(
                target_bids=self._user.bids, page_size=5,
                last_fid=last_fid, search_type="default",
            )

        # bias를 선택했을 때
        else:
            fid_list, self.__last_fid = feed_search_engine.try_feed_with_bid_n_filtering(
                target_bids=[bid], page_size=5,
                last_fid=last_fid, search_type="just_bias",
            )

        # 보낼 데이터 만들어 주기
        self._send_data = self._make_feed_data_n_interaction_data(feed_manager=feed_manager, fid_list=fid_list)
        return

    # community와 board_type을 함께 요청했을 때

    def try_search_feed_with_bid_n_board_type(self, bid:str, last_fid:str,
                                             board_type:str,
                                             feed_search_engine:FeedSearchEngine,
                                             feed_manager:FeedManager,
                                             ):

        # bias를 선택하지 않았을 때
        if bid =="":
            fid_list, self.__last_fid = feed_search_engine.try_feed_with_bid_n_filtering(
                target_bids=self._user.bids, board_type=board_type,
                page_size=5, last_fid=last_fid, search_type="board_only",
            )

        # bias를 선택했을 때
        else:
            fid_list, self.__last_fid = feed_search_engine.try_feed_with_bid_n_filtering(
                target_bids=[bid], board_type=board_type,
                page_size=5, last_fid=last_fid, search_type="bias_and_board",
            )

        # 보낼 데이터 만들어 주기
        self._send_data = self._make_feed_data_n_interaction_data(feed_manager=feed_manager, fid_list=fid_list)
        return


    def try_filtering_feed_with_options(self, bid:str, board_type:str, last_fid:str, options:list,
                                        feed_search_engine:FeedSearchEngine, feed_manager:FeedManager):
        fid_list = []

        # 1차 필터링
        # Board_type이 필터링 옵션으로 들어갔기 때문에 커뮤니티 분리만 시킵니다, BID만 관여
        if board_type == "" :
            if bid == "":
                fid_list, _ = feed_search_engine.try_feed_with_bid_n_filter(
                    target_bids=self._user.bids, last_fid=last_fid, search_type="default"
                )
            else:
                fid_list, _ = feed_search_engine.try_feed_with_bid_n_filter(
                    target_bids=[bid], last_fid=last_fid, search_type="just_bias"
                )

        fid_list, self.__last_fid = feed_search_engine.try_filtering_feed_with_options(fid_list=fid_list,
                                                                                  options=options, page_size=5, last_fid=last_fid)

        self._send_data = self._make_feed_data_n_interaction_data(feed_manager=feed_manager, fid_list=fid_list)

        return

    def get_response_form_data(self, head_parser):
        try:
            body = {
                'send_data' : self._send_data,
                'last_fid' : self.__last_fid
            }

            response = self._get_response_data(head_parser=head_parser, body=body)
            return response

        except Exception as e:
            raise CoreControllerLogicError("response making error | " + e)

