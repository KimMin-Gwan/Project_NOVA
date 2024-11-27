from model.base_model import BaseModel
from model import Local_Database
#from others.data_domain import Alert
from others import CoreControllerLogicError,FeedManager, FeedSearchEngine
from others import Comment, Feed
from pprint import pprint


class FeedModel(BaseModel):
    def __init__(self, database:Local_Database) -> None:
        super().__init__(database)
        self._feeds = []
        self._key = -1
        self._comments = []

    def set_home_feed_data(self, feed_manager:FeedManager, key= -1):
        self._feeds, self._key = feed_manager.get_feed_in_home(user=self._user, key=key)
        return
    

    def set_feed_data(self, feed_search_engine:FeedSearchEngine,
                        target_type="default", target="", num_feed=1, index=-1):

        fid_list, self._key = feed_search_engine.try_search_feed(
            target_type=target_type, target=target, num_feed=num_feed, index=index)
        
        feed_datas = self._database.get_datas_with_ids(target_id="fid", ids=fid_list)

        for feed_data in feed_datas:
            feed = Feed()
            feed.make_with_dict(feed_data)
            self._feeds.append(feed)

        self._feeds = self._is_user_interacted(user=self._user, feeds=self._feeds)
        return

    def set_today_best_feed(self, feed_search_engine:FeedSearchEngine, index=-1, num_feed=4):
        fid_list, self._key = feed_search_engine.try_get_feed_in_recent(
            search_type="today", num_feed=num_feed, index=index)

        feed_datas = self._database.get_datas_with_ids(target_id="fid", ids=fid_list)

        for feed_data in feed_datas:
            feed = Feed()
            feed.make_with_dict(feed_data)
            self._feeds.append(feed)

        self._feeds = self.__is_user_interacted(user=self._user, feeds=self._feeds)
        return

    def set_weekly_best_feed(self, feed_search_engine:FeedSearchEngine, index=-1, num_feed=4):
        fid_list, self._key = feed_search_engine.try_get_feed_in_recent(
            search_type="weekly", num_feed=num_feed, index=index)
        
        feed_datas = self._database.get_datas_with_ids(target_id="fid", ids=fid_list)

        for feed_data in feed_datas:
            feed = Feed()
            feed.make_with_dict(feed_data)
            self._feeds.append(feed)

        self._feeds = self._is_user_interacted(user=self._user, feeds=self._feeds)
        return

    def set_all_feed(self, feed_search_engine:FeedSearchEngine, index=-1, num_feed=4):
        fid_list, self._key = feed_search_engine.try_get_feed_in_recent(
            search_type="recent", num_feed=num_feed, index=index)
        
        feed_datas = self._database.get_datas_with_ids(target_id="fid", ids=fid_list)

        for feed_data in feed_datas:
            feed = Feed()
            feed.make_with_dict(feed_data)
            self._feeds.append(feed)

        self._feeds = self._is_user_interacted(user=self._user, feeds=self._feeds)
        return
    



    def set_specific_feed_data(self, feed_manager:FeedManager, data_payload):
        self._feeds, self._key = feed_manager.get_feed_in_fclass(user=self._user,
                                                                  key=data_payload.key,
                                                                  fclass=data_payload.fclass)
        return
    
    def try_interact_feed(self, feed_manager:FeedManager, data_payload):
        self._feeds = feed_manager.try_interaction_feed(user=self._user,
                                                    fid=data_payload.fid,
                                                    action=data_payload.action)
        return

    def try_staring_feed(self, feed_manager:FeedManager, data_payload):
        self._feeds = feed_manager.try_staring_feed(user=self._user,
                                                    fid=data_payload.fid)
        return

    def try_make_new_comment(self, feed_manager:FeedManager, data_payload):
        self._feeds = feed_manager.make_new_comment_on_feed(user=self._user,
                                                    fid=data_payload.fid,
                                                    body=data_payload.body)
        self._comments = feed_manager.get_all_comment_on_feed( user=self._user,
                                                               fid=data_payload.fid)
        return

    def get_all_comment_on_feed(self, feed_manager:FeedManager, data_payload):
        self._comments = feed_manager.get_all_comment_on_feed( user=self._user,
                                                               fid=data_payload.fid)
        return

    def try_remove_comment(self, feed_manager:FeedManager, data_payload):
        self._feeds= feed_manager.remove_comment_on_feed( user=self._user,
                                                               fid=data_payload.fid,
                                                               cid=data_payload.cid)
        self._comments = feed_manager.get_all_comment_on_feed( user=self._user,
                                                               fid=data_payload.fid)
        return

    def try_like_comment(self, feed_manager:FeedManager, data_payload):
        self._feeds= feed_manager.try_like_comment( user=self._user,
                                                               fid=data_payload.fid,
                                                               cid=data_payload.cid)
        self._comments = feed_manager.get_all_comment_on_feed( user=self._user,
                                                               fid=data_payload.fid)
        return
    
    # 유저가 참여한 feed인지 확인할것
    # 사실상 User에게 전송하는 모든 feed는 이 함수를 통함
    def _is_user_interacted(self, user, feeds:list):
        result = []
        for feed in feeds:
            # 검열된 feed면 생략
            if feed.state != "y":
                continue

            # 피드에 참여한 내역이 있는지 확인
            attend = -1
            for i, choice in enumerate(feed.attend):
                for uid in choice:
                    if uid == user.uid:
                        attend = i

            comment = self.__get_feed_comment(user=user, feed=feed)
            feed.num_comment = len(feed.comment)
            feed.attend = attend
            feed.comment = comment
            # 기본적으로 star_flag는 False
            if feed.fid in user.like:
                feed.star_flag = True
            result.append(feed)
        return result

    def __get_feed_comment(self, user, feed:Feed):
        if len(feed.comment) == 0:
            comment = Comment(body="아직 작성된 댓글이 없어요")
            comment = comment.get_dict_form_data()
        else:
            #comment = Comment(body="아직 작성된 댓글이 없어요")
            #comment = comment.get_dict_form_data()
            cid = feed.comment[-1]
            comment = self._database.get_data_with_id(target="cid", id=cid)
            # 기본적으로 owner는 False로 고정
            if comment['uid'] == user.uid:
                comment['owner'] = True
        return comment
    

    def get_response_form_data(self, head_parser):
        try:
            body = {
                'feed' : self._make_dict_list_data(list_data=self._feeds),
                'key' : self._key,
                'comments' : self._make_dict_list_data(list_data=self._comments)
            }

            response = self._get_response_data(head_parser=head_parser, body=body)
            return response

        except Exception as e:
            raise CoreControllerLogicError("response making error | " + e)
        

# feed 의 메타 정보를 보내주는 모델
class FeedMetaModel(BaseModel):
    def __init__(self, database:Local_Database) -> None:
        super().__init__(database)
        self._feed_meta_data = []

    def set_feed_meta_data(self, feed_manager:FeedManager):
        self._feeds = feed_manager.get_feed_meta_data()
        return
    
    def __make_send_data(self):
        result = []
        for fclass in self._feeds:
            single_data = {
                "fname" : fclass.fname,
                "fclass" : fclass.fclass,
                "specific" : fclass.specific
            }
            result.append(single_data)
        return result

    def get_response_form_data(self, head_parser):
        try:
            body = {
                'feed_meta_data' : self.__make_send_data(),
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

    def set_recommand_feed(self, feed_search_engine:FeedSearchEngine, fid:str, history:list):
        fid = feed_search_engine.try_recommand_feed(fid=fid, history=history, user=self._user)
        history.append(fid)
        self.__history = history
        
        feed_data = self._database.get_data_with_id(target="fid", id=fid)

        feed = Feed()
        feed.make_with_dict(feed_data)
        self.__feed.append(feed)
        self.__feed = self._is_user_interacted(user=self._user, feeds=self.__feed)
        return

    def try_search_feed_with_fid(self, feed_search_engine:FeedSearchEngine, fid=""):
        if fid == "":
            fid=feed_search_engine.try_get_random_feed()

        self.__history.append(str(fid))
        second_fid = feed_search_engine.try_recommand_feed(fid=str(fid),
                                                history=self.__history,
                                                user=self._user
                                                )
        self.__history.append(second_fid)
        feed_datas = self._database.get_datas_with_ids(target_id="fid", ids=[str(fid), second_fid])
        for feed_data in feed_datas:
            feed = Feed()
            feed.make_with_dict(dict_data=feed_data)
            self.__feed.append(feed)

        self.__feed = self._is_user_interacted(user=self._user, feeds=self.__feed)

        return

    def try_search_feed(self, feed_search_engine:FeedSearchEngine,
                        target="", num_feed=1, index=-1):

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

        self._hashtag_feed = self._is_user_interacted(user=self._user, feeds=self._hashtag_feed)
        self._uname_feed = self._is_user_interacted(user=self._user, feeds=self._uname_feed)

        return

    def try_search_feed_with_hashtag(self, feed_search_engine:FeedSearchEngine,
                                    target="", num_feed=1, index=-1):

        hashtag_feed_fid, self._key = feed_search_engine.try_search_feed(
            target_type="hashtag", target=target, num_feed=num_feed, index=index)

        hashtag_feed_data = self._database.get_datas_with_ids(target_id="fid", ids=hashtag_feed_fid)

        for feed_data in hashtag_feed_data:
            feed = Feed()
            feed.make_with_dict(feed_data)
            self._hashtag_feed.append(feed)

        self._hashtag_feed = self._is_user_interacted(user=self._user, feeds=self._hashtag_feed)
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