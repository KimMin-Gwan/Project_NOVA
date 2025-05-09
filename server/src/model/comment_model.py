from model.base_model import BaseModel
from model import Local_Database
from others import Feed, Comment, User
from others import CoreControllerLogicError,FeedManager, FeedSearchEngine, ObjectStorageConnection, HTMLEXtractor
from datetime import datetime

class CommentModel(BaseModel):
    def __init__(self, database:Local_Database) -> None:
        super().__init__(database)
        self._comments = []


    def set_target_comment(self, fid:str, target_cid:str=""):
        feed_data = self._database.get_data_with_id(target="fid", id=fid)
        feed = Feed().make_with_dict(feed_data)
        
        if target_cid != "":
            index = feed.comment.index(target_cid)
            feed.comment = feed.comment[:index]
            
        
        cids = []
        
        for cid in reversed(feed.comment):
            if len(cids) > 10:
                break
            
            cids.append(cid)
            
        
        comment_datas = self._database.get_datas_with_ids(target_id="cid", ids=cids)
        for comment_data in comment_datas:
            comment = Feed().make_with_dict(comment_data)
            if comment.display == 2:
                comment.body = "차단된 댓글입니다."
            elif comment.display == 1:
                comment.body = "비공개 댓글입니다."
            elif comment.display == 0:
                comment.body = "삭제된 댓글입니다."
            
            if comment.uid == self._user.uid:
                comment.is_owner = True
                
            self._comments.append(comment)
        
        return

    def get_response_form_data(self, head_parser):
        try:
            body = {
                'comments' : self._make_dict_list_data(list_data=self._comments),
                'uid' : self._user.uid
            }

            response = self._get_response_data(head_parser=head_parser, body=body)
            return response

        except Exception as e:
            raise CoreControllerLogicError("response making error | " + e)

    def __get_datetime(self, date_str):
        return datetime.strptime(date_str, "%Y/%m/%d-%H:%M:%S")

    def __set_datetime(self):
        return datetime.now().strftime("%Y/%m/%d-%H:%M:%S")

    def __get_today_date(self):
        return datetime.now().strftime("%Y/%m/%d")
    
    def __set_fid_with_datatime(self):
        return datetime.now().strftime("%Y%m%d%H%M%S")

    async def make_new_comment(self, user:User, fid:str, cid:str, body:str, ai_manager):
        try:
            feed_data = self._database.get_data_with_id(target="fid", id=fid)
            feed = Feed()
            feed.make_with_dict(feed_data)

            # 이건 안해도됨
            ## CID 만들기, 중복이 있을 가능성 있음
            ## 일단 __set_datetime()쓰면 cid 분리 시, -때문에 분리가 이상하게 됨. 그래서 FID 만들 때랑 동일한 시간제작방식 사용
            ##cid = fid+"-"+self.__set_fid_with_datatime()
            #mention = self._extract_mention_data(body)
            
            date = self.__get_today_date()

            # 타겟 CID도 Comment 객체 멤버로 담아버림. CID 너무 길어지기도 하고, 프론트에서 작업을 안시키게 함.
            new_comment = Comment(
                cid=cid, fid=feed.fid, uid=user.uid, uname=user.uname,
                body=body, date=date, mention=""
            )
        
            # 이거 일단 대기
            #new_comment = ai_manager.treat_new_comment(comment=new_comment)
        
            feed.comment.append(cid)
            user.my_comment.append(cid)
            user.num_comment += 1

            self._database.add_new_data("cid", new_data=new_comment.get_dict_form_data())
            self._database.modify_data_with_id("fid", target_data=feed.get_dict_form_data())
            self._database.modify_data_with_id("uid", target_data=user.get_dict_form_data())
            
        except Exception as e:
            print(e)
            return False
        return True

    async def modify_comment(self, cid:str, body:str):
        try:
            comment_data = self._database.get_data_with_id(target="cid", id=cid)
            comment = Comment().make_with_dict(comment_data)
        
            comment.body = body
            self._database.add_new_data("cid", new_data=comment.get_dict_form_data())
        except Exception as e:
            print(e)
            return False

        return True
        
    async def delete_comment(self, cid:str):
        try:
            comment_data = self._database.get_data_with_id(target="cid", id=cid)
            comment = Comment().make_with_dict(comment_data)
            comment.display = 0
            
            self._database.add_new_data("cid", new_data=comment.get_dict_form_data())
        except Exception as e:
            print(e)
            return False
        return True
        
        
        
        
