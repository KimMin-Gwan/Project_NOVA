from model.base_model import BaseModel
from model import Local_Database
#from others.data_domain import Alert
from others import CoreControllerLogicError,FeedManager, FeedSearchEngine, ObjectStorageConnection
from others import Comment, Feed, User, Interaction
from pprint import pprint


class FeedModel(BaseModel):
    def __init__(self, database:Local_Database) -> None:
        super().__init__(database)
        self._feeds = []
        self._key = -1
        self._comments = []
        self._interactions = []
        self._send_data = []
    
    # 단일 피드 데이터 전송
    def set_single_feed_data(self, fid:str, feed_manager:FeedManager):
        feed_data = self._database.get_data_with_id(target="fid", id=fid)

        feed = Feed()
        feed.make_with_dict(feed_data)
        self._feeds.append(feed)

        # 포인터로 동작함
        self._set_feed_json_data(user=self._user, feeds=self._feeds, feed_manager=feed_manager)
        return

    def set_feed_data(self, feed_search_engine:FeedSearchEngine, feed_manager,
                        target_type="default", target="", num_feed=1, index=-1):

        fid_list, self._key = feed_search_engine.try_search_feed(
            target_type=target_type, target=target, num_feed=num_feed, index=index)
        
        feed_datas = self._database.get_datas_with_ids(target_id="fid", ids=fid_list)

        feeds = []
        iids = []

        for feed_data in feed_datas:
            feed = Feed()
            feed.make_with_dict(feed_data)
            feeds.append(feed)
            if feed.iid != "":
                iids.append(feed.iid)

        self._set_feed_json_data(user=self._user, feeds=feeds, feed_manager=feed_manager)
        
        interaction_datas = self._database.get_datas_with_ids(target_id="iid", ids=iids)
        interactions = []
        
        for interaction_data in interaction_datas:
            interaction = Interaction()
            interaction.make_with_dict(interaction_data)
            interactions.append(interaction)
            
        # 인터엑션 넣을 필요 있음
        self._send_data = self.__set_send_data(feeds=feeds, interactions=interactions)
        return

    def set_today_best_feed(self, feed_search_engine:FeedSearchEngine, feed_manager,
                             index=-1, num_feed=4):
        fid_list, self._key = feed_search_engine.try_get_feed_in_recent(
            search_type="today", num_feed=num_feed, index=index)

        feed_datas = self._database.get_datas_with_ids(target_id="fid", ids=fid_list)

        feeds = []
        iids = []

        for feed_data in feed_datas:
            feed = Feed()
            feed.make_with_dict(feed_data)
            feeds.append(feed)
            if feed.iid != "":
                iids.append(feed.iid)

        self._set_feed_json_data(user=self._user, feeds=feeds, feed_manager=feed_manager)
        
        interaction_datas = self._database.get_datas_with_ids(target_id="iid", ids=iids)
        interactions = []
        
        for interaction_data in interaction_datas:
            interaction = Interaction()
            interaction.make_with_dict(interaction_data)
            interactions.append(interaction)
            
        # 인터엑션 넣을 필요 있음
        self._send_data = self.__set_send_data(feeds=feeds, interactions=interactions)
        return

    def set_weekly_best_feed(self, feed_search_engine:FeedSearchEngine, feed_manager,
                             index=-1, num_feed=4):
        fid_list, self._key = feed_search_engine.try_get_feed_in_recent(
            search_type="weekly", num_feed=num_feed, index=index)
        
        feed_datas = self._database.get_datas_with_ids(target_id="fid", ids=fid_list)

        feeds = []
        iids = []

        for feed_data in feed_datas:
            feed = Feed()
            feed.make_with_dict(feed_data)
            feeds.append(feed)
            if feed.iid != "":
                iids.append(feed.iid)

        self._set_feed_json_data(user=self._user, feeds=feeds, feed_manager=feed_manager)
        
        interaction_datas = self._database.get_datas_with_ids(target_id="iid", ids=iids)
        interactions = []
        
        for interaction_data in interaction_datas:
            interaction = Interaction()
            interaction.make_with_dict(interaction_data)
            interactions.append(interaction)
            
        # 인터엑션 넣을 필요 있음
        self._send_data = self.__set_send_data(feeds=feeds, interactions=interactions)
        return

    def set_all_feed(self, feed_search_engine:FeedSearchEngine, feed_manager,
                      index=-1, num_feed=4):
        fid_list, self._key = feed_search_engine.try_get_feed_in_recent(
            search_type="recent", num_feed=num_feed, index=index)
        
        feed_datas = self._database.get_datas_with_ids(target_id="fid", ids=fid_list)

        feeds = []
        iids = []

        for feed_data in feed_datas:
            feed = Feed()
            feed.make_with_dict(feed_data)
            feeds.append(feed)
            if feed.iid != "":
                iids.append(feed.iid)

        self._set_feed_json_data(user=self._user, feeds=feeds, feed_manager=feed_manager)
        
        print("1")
        
        interaction_datas = self._database.get_datas_with_ids(target_id="iid", ids=iids)
        print("2")
        interactions = []
        
        print("3")
        
        for interaction_data in interaction_datas:
            interaction = Interaction()
            interaction.make_with_dict(interaction_data)
            interactions.append(interaction)
            
        # 인터엑션 넣을 필요 있음
        self._send_data = self.__set_send_data(feeds=feeds, interactions=interactions)
        return
    

    # 상호작용하기
    # 만들어야됨 
    def try_interact_feed(self, feed_manager:FeedManager, data_payload):
        self._feeds = feed_manager.try_interaction_feed(user=self._user,
                                                    fid=data_payload.fid,
                                                    action=data_payload.action)
        self._set_feed_json_data(user=self._user, feeds=self._feeds, feed_manager=feed_manager)
        return

    # 좋아요 누르기
    # 완료
    def try_staring_feed(self, feed_manager:FeedManager, data_payload):
        self._feeds = feed_manager.try_staring_feed(user=self._user,
                                                fid=data_payload.fid)
        
        self._set_feed_json_data(user=self._user, feeds=self._feeds, feed_manager=feed_manager)
        return

    # 댓글 새로 달기
    # 1. 댓글 달기 -> 2. 댓글 달고나서 전체 댓글 데이터만 제공
    # 파라미터 수정 필요 
    def try_make_new_comment(self, feed_manager:FeedManager, data_payload):
        feed_manager.try_make_comment_on_feed(user=self._user,
                                            fid=data_payload.fid,
                                            target_cid=data_payload.target_cid,
                                            body=data_payload.body)
        self._comments = feed_manager.get_all_comment_on_feed( user=self._user,
                                                               fid=data_payload.fid)
        return

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
        detail, result = feed_manager.remove_comment_on_feed( user=self._user,
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
    def _set_feed_json_data(self, user, feeds:list, feed_manager:FeedManager):
        users = []
        uids=[]
        for single_feed in feeds:
            single_feed:Feed = single_feed
            uids.append(single_feed.uid)

        user_datas = self._database.get_datas_with_ids(target_id="uid", ids=uids)

        for user_data in user_datas:
            user = User()
            user.make_with_dict(user_data)
            users.append(user)

        print("1")
        
        for feed, wuser in zip(feeds, users):
            # 노출 현황 이 1 이하면 죽어야됨
            # 0: 삭제됨 1 : 비공개 2: 차단 3: 댓글 작성 X 4 : 정상(전체 공개)
            if feed.display < 3:
                continue
            print("2")
            
            # 롱폼은 바디 데이터를 받아야됨
            if feed.fclass != "short":
                feed.body = ObjectStorageConnection().get_feed_body(fid = feed.fid)

            
            # comment 길이 & image 길이
            feed.num_comment = len(feed.comment)
            feed.num_image = len(feed.image)

            print(3)
            # 좋아요를 누를 전적
            if feed.fid in user.like:
                feed.star_flag = True

            # 피드 작성자 이름
            # 나중에 nickname으로 바꿀것
            feed.nickname = wuser.uname
            
        return
    
    # 상호작용에서 내가 상호작용한 내용이 있는지 검토하는 부분
    def _set_feed_interactied(self, user, interaction):
        for i, uid in enumerate(interaction.attend):
            if uid == user.uid:
                interaction.my_attend = i
        return

    # 전송 데이터 만들기
    # feed 데이터와 interaction을 모두 줘야하는 경우에만 사용
    def __set_send_data(self, feeds:list, interactions:list=[]):
        send_data = []

        for feed in feeds:
            feed:Feed = feed

            # 0: 삭제됨 1 : 비공개 2: 차단 3: 댓글 작성 X 4 : 정상(전체 공개)
            if feed.display < 3:
                continue

            interaction = Interaction()
            for single_interaction in interactions:
                print(feed.iid)
                if single_interaction.iid == feed.iid:
                    interaction = single_interaction
                    print("?>??")
                    self._set_feed_interactied(self._user, interaction=single_interaction)
                    

            dict_data={}
            dict_data['feed'] = feed.get_dict_form_data()
            dict_data['interaction'] = interaction.get_dict_form_data()

            send_data.append(dict_data)
        return send_data

    ## 유저가 참여한 feed인지 확인할것
    ## 사실상 User에게 전송하는 모든 feed는 이 함수를 통함
    #def _is_user_interacted(self, user, feeds:list):
        #result = []
        #for feed in feeds:

            #feed:Feed =feed
            ## 검열된 feed면 생략
            #if feed.state != "y":
                #continue

            ## 피드에 참여한 내역이 있는지 확인
            #attend = -1
            #for i, choice in enumerate(feed.attend):
                #for uid in choice:
                    #if uid == user.uid:
                        #attend = i

            #comment = self.__get_feed_comment(user=user, feed=feed)

            #feed.num_comment = len(feed.comment)
            #feed.attend = attend
            #feed.comment = comment
            ## 기본적으로 star_flag는 False
            #if feed.fid in user.like:
                #feed.star_flag = True
            #result.append(feed)
        #return result

    #def __get_feed_comment(self, user, feed:Feed):
        #if len(feed.comment) == 0:
            #comment = Comment(body="아직 작성된 댓글이 없어요")
            #comment = comment.get_dict_form_data()
        #else:
            ##comment = Comment(body="아직 작성된 댓글이 없어요")
            ##comment = comment.get_dict_form_data()
            #cid = feed.comment[-1]
            #comment = self._database.get_data_with_id(target="cid", id=cid)
            ## 기본적으로 owner는 False로 고정
            #if comment['uid'] == user.uid:
                #comment['owner'] = True
        #return comment
    

    def get_response_form_data(self, head_parser):
        try:
            body = {
                'feed' : self._make_dict_list_data(list_data=self._feeds),
                'key' : self._key,
                'comments' : self._make_dict_list_data(list_data=self._comments),
                'send_data' : self._send_data
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

    def try_edit_feed(self, feed_manager:FeedManager, data_payload):
        # 만약 fid가 ""가 아니면 수정이나 삭제 요청일것임
        # 근데 삭제 요청은 여기서 처리 안하니까 반드시 수정일것
        if data_payload.fid != "":
            detail, flag = feed_manager.try_modify_feed(
                user=self._user,
                data_payload = data_payload)
        else:
            detail, flag = feed_manager.try_make_new_feed(
                user=self._user,
                data_payload = data_payload)

        self._result = flag
        self._detail = detail
        return

    def try_delete_feed(self, feed_manager:FeedManager, data_payload):
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
                "detail" : self._detail 
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

        self._set_feed_json_data(user=self._user, feeds=[feed], feed_manager=feed_manager)

        # 인터엑션 넣을 필요 있음
        self._send_data = self.__set_send_data(feeds=[feed])
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
        feed_datas = self._database.get_datas_with_ids(target_id="fid", ids=[str(fid), second_fid])
        for feed_data in feed_datas:
            feed = Feed()
            feed.make_with_dict(dict_data=feed_data)
            self.__feed.append(feed)

        # 인터엑션은 별도라 여기 포함 안됨
        self._set_feed_json_data(user=self._user, feeds=self.__feed, feed_manager=feed_manager)
        return

    def try_search_feed(self, feed_search_engine:FeedSearchEngine, feed_manager,
                        target="", num_feed=1, index=-1, ):

        hashtag_feed_fid, self._key = feed_search_engine.try_search_feed(
            target_type="hashtag", target=target, num_feed=num_feed, index=index)

        user_feed_fid, self._key = feed_search_engine.try_search_feed(
            target_type="uname", target=target, num_feed=num_feed, index=index)
        
        hashtag_feed_data = self._database.get_datas_with_ids(target_id="fid", ids=hashtag_feed_fid)
        user_feed_fid = self._database.get_datas_with_ids(target_id="fid", ids=user_feed_fid)

        for feed_data1 in hashtag_feed_data:
            feed = Feed()
            feed.make_with_dict(feed_data1)
            self._hashtag_feed.append(feed)

        for feed_data2 in user_feed_fid:
            feed = Feed()
            feed.make_with_dict(feed_data2)
            self._uname_feed.append(feed)



        self._set_feed_json_data(user=self._user, feeds=self._hashtag_feed, feed_manager=feed_manager)
        self._set_feed_json_data(user=self._user, feeds=self._uname_feed, feed_manager=feed_manager)

        return

    def try_search_feed_with_hashtag(self, feed_search_engine:FeedSearchEngine, feed_manager,
                                    target="", num_feed=1, index=-1):

        hashtag_feed_fid, self._key = feed_search_engine.try_search_feed(
            target_type="hashtag", target=target, num_feed=num_feed, index=index)

        hashtag_feed_data = self._database.get_datas_with_ids(target_id="fid", ids=hashtag_feed_fid)

        feeds = []

        for feed_data in hashtag_feed_data:
            feed = Feed()
            feed.make_with_dict(feed_data)
            feeds.append(feed)

        self._set_feed_json_data(user=self._user, feeds=feeds, feed_manager=feed_manager)

        # 인터엑션 필요
        self._send_data = self.__set_send_data(feeds=feeds)
        return

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
        