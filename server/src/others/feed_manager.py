from others.data_domain import Feed, User, Comment,  FeedLink
from others.search_engine import FeedSearchEngine
from others.object_storage_connector import ObjectStorageConnection, HTMLEXtractor, ImageDescriper
from datetime import datetime
import string
import random
import warnings
from pprint import pprint
import uuid

# Boto3의 경고 메시지 무시
warnings.filterwarnings("ignore", module='boto3.compat')

# Feed manager
class FeedManager:
    def __init__(self, database, feed_search_engine) -> None:
        self._database= database
        self._feed_search_engine:FeedSearchEngine = feed_search_engine
        self._num_feed = 0
        self._managed_feed_list = []

    def __get_datetime(self, date_str):
        return datetime.strptime(date_str, "%Y/%m/%d-%H:%M:%S")

    def __set_datetime(self):
        return datetime.now().strftime("%Y/%m/%d-%H:%M:%S")

    def __get_today_date(self):
        return datetime.now().strftime("%Y/%m/%d")

    def __set_fid_with_datatime(self):
        return datetime.now().strftime("%Y%m%d%H%M%S")

    #------------------------------Feed 작성, 삭제, 편집-------------------------------------------
    # 새로운 fid 만들기
    def __make_new_fid(self, user:User):
        random_string = "default"
        # 중북되지 않는 fid 만들기
        while True:
            # 사용할 문자들: 대문자, 소문자, 숫자
            characters = string.ascii_letters + string.digits

            # 8자리 랜덤 문자열 생성
            random_string = ''.join(random.choice(characters) for _ in range(6))

            fid = user.uid + "-" + random_string

            if self._feed_search_engine.try_search_managed_feed(fid=fid):
                continue
            else:
                break

        return fid

    # 새로운 피드 만들기
    # 실제로 피드를 만들고, 서치 엔진에 추가하는 부분이다.
    def __make_new_feed(self, user:User, fid, body, hashtag,
                        board_type, link, bid, raw_body=""):
        bname = ""
        bias_data = self._database.get_data_with_id(target="bid", id=bid)
        
        if bias_data:
            bname = bias_data.get("bname", "")
        
        # 검증을 위한 코드는 이곳에 작성하시오
        new_feed = self.__set_new_feed(user=user, fid=fid, body=body, hashtag=hashtag, board_type=board_type,
                                        link=link, bid=bid, raw_body=raw_body, bname=bname)

        
        self._database.add_new_data(target_id="fid", new_data=new_feed.get_dict_form_data())

        self._feed_search_engine.try_make_new_managed_feed(feed=new_feed)
        # self._feed_search_engine.try_add_feed(feed=new_feed)
        return
    
    def __modify_feed(self, user:User, fid, body, hashtag, board_type, date,
                    link, bid, raw_body=""):
        bname = ""
        bias_data = self._database.get_data_with_id(target="bid", id=bid)
        
        if bias_data:
            bname = bias_data.bname
            
        # 검증을 위한 코드는 이곳에 작성하시오
        feed = self.__set_new_feed(user=user, fid=fid, body=body, hashtag=hashtag, board_type=board_type,
                                 link=link, bid=bid, raw_body=raw_body, date=date, bname = bname)

        self._database.modify_data_with_id(target_id="fid", target_data=feed.get_dict_form_data())

        # 이곳에 add와 make가 아닌 modify 되는 함수가 필요함
        self._feed_search_engine.try_modify_managed_feed(feed=feed)
        self._feed_search_engine.try_make_new_managed_feed(feed=feed)
        return
    
    def _make_new_id(self):
        return id

    # 링크 만들기
    def _make_new_link(self, fid, feed_links):
        result_feed_links = []

        lid_list = []

        # 여기서 실제 링크를 타고 들어가서 해당 사이트의 ㅡ내용을 긁어 올 필요가 있음
        # 크롤링이 안되는 사이트면 하는 수 없고
        for feed_link in feed_links:
            feed_link:FeedLink = feed_link
            # pprint(feed_link.get_dict_form_data())
            lid = str(uuid.uuid4())
            feed_link.lid = lid
            feed_link.fid = fid
            result, feed_link.url, feed_link.title = HTMLEXtractor().extract_external_webpage_title_tag(url=feed_link.url)
            if not result:
                continue
            feed_link.domain = HTMLEXtractor().extract_link_domain_string(url=feed_link.url)
            result_feed_links.append(feed_link.get_dict_form_data())
            lid_list.append(lid)

        if lid_list:
            # 데이터 저장
            self._database.add_new_datas(target_id="lid", new_datas=result_feed_links)

        return lid_list

    # 새로운 피드의 데이터를 추가하여 반환
    def __set_new_feed(self, user:User,fid, body, hashtag, bname,
                       board_type, link, bid, raw_body, date=None):
        # link가 있다면 작업할 것
        # 수정 하기 기능헤서도 동일하게 링크를 새로 만들어서 배포함
        if link:
            lids = self._make_new_link(fid=fid, feed_links=link)
        else:
            lids = []
            
        if not date:
            date = self.__set_datetime()

        # 새로운 피드 만들어지는 곳
        new_feed = Feed()
        new_feed.fid = fid
        new_feed.uid = user.uid
        new_feed.nickname = user.uname
        new_feed.body = body
        new_feed.date = date
        new_feed.board_type = board_type
        new_feed.hashtag = hashtag
        new_feed.lid = lids
        new_feed.bid = bid
        new_feed.bname = bname
        new_feed.raw_body = raw_body
        return new_feed
    

    # FEED 작성
    def try_make_new_feed(self, user:User, data_payload, fid = ""):
        # fid 만들기 feed 수정기능을 겸하고 있기 때문에, 다음을 추가한 것
        if fid == "":
            fid = self.__make_new_fid(user=user)
            
        # 롱폼의 경우 작성된 html을 올리고 저장하면됨
        # 이때 body 데이터는 url로 되어야함
        # 대신 전송될 때는 body데이터가 html로 다시 복구되어 전송되어야함
        connector = ObjectStorageConnection()
        # 1. 전송된 body데이터를 확인
        if data_payload.body:
            # 2. body데이터를 오브젝트 스토리지에 저장
            url = connector.make_new_feed_body_data(fid = fid, body=data_payload.body)
            body, _ = connector.extract_body_n_image(raw_data=data_payload.body)
                
        else:
            body = " "
            url = connector.make_new_feed_body_data(fid=fid, body=body)

        # 3. url을 body로 지정

        # 여기서 댓글 허용 같은 부분도 처리해야될 것임
        self.__make_new_feed(user=user,
                                fid=fid,
                                body=body,
                                hashtag=data_payload.hashtag,
                                board_type=data_payload.board_type,
                                link=data_payload.link,
                                bid=data_payload.bid,
                                raw_body= url, # 이거 url이라는 변수가 없어서
                                )

        #작성한 피드 목록에 넣어주고
        user.my_feed.append(fid)
        user.num_feed+=1

        self._database.modify_data_with_id(target_id="uid", target_data=user.get_dict_form_data())
        # 끝
        return "Upload Success", True

    # FEED 수정
    # 댓글하고 다르게 이미지도 수정이 가능하므로, 데이터를 삭제하고 다시 작성하는 방식을 취함.
    def try_modify_feed(self, user:User, data_payload, fid):
        # FEED 데이터 불러옴
        feed_data=self._database.get_data_with_id(target="fid",id=data_payload.fid)
        feed = Feed()
        feed.make_with_dict(feed_data)

        # 내 글이 아니네!
        if feed.uid != user.uid:
            return "NOT_OWNER", False
        
        connector = ObjectStorageConnection()
        # 1. 전송된 body데이터를 확인
        if data_payload.body:
            data_payload_body = data_payload.body
            # 2. body데이터를 오브젝트 스토리지에 저장
            url = connector.make_new_feed_body_data(fid = fid, body=data_payload_body)
            body, _ = connector.extract_body_n_image(raw_data=data_payload_body)
                
        else:
            body = " "
            url = connector.make_new_feed_body_data(fid=fid, body=body)

        # 3. url을 body로 지정

        # 여기서 댓글 허용 같은 부분도 처리해야될 것임
        self.__modify_feed(user=user,
                                fid=fid,
                                body=body,
                                hashtag=data_payload.hashtag,
                                board_type=data_payload.board_type,
                                link=data_payload.link,
                                bid=data_payload.bid,
                                date=data_payload.date,
                                raw_body = url, # 이거 url이라는 변수가 없어서
                                )
        
        return "Upload Success", True

    def try_remove_feed(self, user:User, fid):
        feed_data=self._database.get_data_with_id(target="fid",id=fid)
        feed = Feed()
        feed.make_with_dict(feed_data)

        if feed.uid != user.uid:
            return "NOT_OWNER", False

        # 댓글도 남기고, Feed도 삭제하지 않는다. 다만, Display 옵션을 따로 두어
        # 삭제해도 데이터베이스 안에 남기도록 한다.

        # 디스플레이 옵션
        #   0 : 삭제
        #   1 : 비공개
        #   2 : 차단
        #   3 : 댓글 작성 비활성화
        #   4 : 전체 공개
        # 디스플레이 옵션을 수정한 후, Feed를 수정한다.
        feed.display = 0
        user.num_feed-=1

        self._database.modify_data_with_id(target_id="fid", target_data=feed.get_dict_form_data())
        # 유저 데이터 수정
        self._database.modify_data_with_id(target_id="uid", target_data=user.get_dict_form_data())

        return "COMPLETE", True

    def try_set_private_feed(self, user:User, fid):
        feed_data = self._database.get_data_with_id(target="fid",id=fid)
        feed = Feed()
        feed.make_with_dict(feed_data)

        if feed.uid != user.uid:
            return "NOT_OWNER", False

        # 디스플레이 옵션
        #   0 : 삭제
        #   1 : 비공개
        #   2 : 차단
        #   3 : 댓글 작성 비활성화
        #   4 : 전체 공개
        # 디스플레이 옵션을 수정한 후, Feed를 수정한다.
        feed.display = 1
        self._database.modify_data_with_id(target_id="fid", target_data=feed.get_dict_form_data())

        return "COMPLETE", True

    # 피드 차단을 설정함
    def try_set_blocked_feed(self, fid):
        feed_data = self._database.get_data_with_id(target="fid",id=fid)
        feed = Feed()
        feed.make_with_dict(feed_data)

        feed.display = 2
        self._database.modify_data_with_id(target_id="fid", target_data=feed.get_dict_form_data())

        return "COMPLETE", True

    # Post( 롱 피드)만 가져오는 거
    def get_my_feeds(self, user:User):
        feed_datas = self._database.get_datas_with_ids(target_id="fid", ids=user.my_feed)
        feeds = []

        for _, feed_data in enumerate(reversed(feed_datas)):
            feed = Feed()
            feed.make_with_dict(feed_data)
            if feed.display == 0:
                continue
            feeds.append(feed)

        return feeds


    # 내가 좋아요를 누른 Feed만 가져오는 거
    def get_liked_feeds(self, user:User):
        # "fid=시간" -> "fid"
        liked_fid_data = [liked_feed.split('=')[0] for liked_feed in user.like]

        feed_datas = self._database.get_datas_with_ids(target_id="fid", ids=liked_fid_data)
        feeds = []

        # 마지막이 좋아요 최신 순이라 리버스해야함.
        for _, feed_datas in enumerate(reversed(feed_datas)):
            feed = Feed()
            feed.make_with_dict(feed_datas)
            if feed.display == 0:
                continue
            feeds.append(feed)

        return feeds

    # 모든 Feed fid를 가져옵니다.
    def get_all_fids(self):
        feed_datas = self._database.get_all_data(target="fid")
        fid_list = []

        for feed_data in feed_datas:
            fid_list.append(feed_data["fid"])

        return fid_list

    #------------------------------Feed 좋아요 누르기----------------------------------------------
    # Feed에 좋아요를 눌렀을 때의 작용
    def try_like_feed(self, user:User, fid:str):
        feed = self.__try_like_feed(user=user, fid=fid)
        return [feed]

    # feed 와 상호작용 -> 관심 표시
    def __try_like_feed(self, user:User, fid):
        feed_data = self._database.get_data_with_id(target="fid", id=fid)
        feed = Feed()
        feed.make_with_dict(feed_data)

        flag = False
        # fidNdate = "fid=date"

        for fid_n_date in user.like:
            # 문자열 변환
            fid_n_date:str = fid_n_date
            # 현재 Feed를 얻음
            target_fid = fid_n_date.split('=')[0]
            # 왜이랬는지 생각해봤더니 지울때 또 반복문 돌리니까 이렇게 한 거네
            if target_fid == feed.fid:
                user.like.remove(fid_n_date)
                flag=True
                break

        date = datetime.now()
        str_fid_n_date = feed.fid + "=" + self.__set_datetime()

        if flag:
            self._feed_search_engine.try_dislike_feed(fid=feed.fid, uid=user.uid)
            #user.like.remove(str_fid_n_date)
            feed.like -= 1
        else:
            self._feed_search_engine.try_like_feed(fid=feed.fid, uid=user.uid, like_time=date)
            user.like.append(str_fid_n_date)
            feed.like += 1

        self._database.modify_data_with_id(target_id="fid",
                                           target_data=feed.get_dict_form_data())
        self._database.modify_data_with_id(target_id="uid",
                                           target_data=user.get_dict_form_data())

        return feed

    #-----------------------------------댓글 기능--------------------------------------------------
    # 댓글 좋아요를 누른 정보를 가져옴
    # 내가 좋아요를 누를 댓글인지 플래그를 올리는 함수
    def __get_comment_liked_info(self, user:User, comments):
        for comment in comments:
            # pprint(comment.get_dict_form_data())
            if user.uid in comment.like_user:
                comment.like_user = True
            else:
                comment.like_user = False
        return

    # 서치한 댓글이 어떤 피드에서 긁어오는지 확인하기위해 feed 패키징을 하는 작업을 거칩니다.
    def __get_feeds_on_searched_comments(self, comments):
        # Set 자료형을 통해 중복을 처리함
        comments_fids = set()
        for comment in comments:
            comments_fids.add(comment.fid)
        # 리스트 화
        comments_fids = list(comments_fids)

        feed_datas = self._database.get_datas_with_ids(target_id="fid", ids=comments_fids)
        feeds = []
        for feed_data in feed_datas:
            feed = Feed()
            feed.make_with_dict(feed_data)
            feeds.append(feed)

        # Feed 데이터에서 comments의 Cid들을 비교해서 매칭된 cid리스트를 정리한 다음 다시 Feed.comment에 담아버림

        for feed in feeds:
            # feed.comment에는 원래 cid가 담기는 것이지만,
            # 지금은 Comment()객체가 담기게 됨. 딕셔너리 데이터로 담기게 됩니다.
            matched_comments = []
            for comment in comments:
                if feed.fid == comment.fid:
                    matched_comments.append(comment.get_dict_form_data())

            feed.comment = matched_comments

        return feeds

    # 댓글 수정
    # Feed에 저장된 CID는 따로 수정 대상이 아니므로, 따로 fid를 파라미터로 가져오지 않는다.
    # 이 부분은 검토를 해줬으면 좋겠음.
    def try_modify_comment(self, user:User, cid, new_body):
        comment_data = self._database.get_data_with_id(target="cid", id=cid)
        comment = Comment()
        comment.make_with_dict(dict_data=comment_data)

        if comment.uid != user.uid:
            return "NOT_OWNER", False

        new_mention = self._extract_mention_data(new_body)
        comment.body = new_body
        comment.mention = new_mention

        self._database.modify_data_with_id("cid", target_data=comment.get_dict_form_data())
        return "Update Success",True

    # 댓글 비공개
    def set_private_comment(self, user:User, fid, cid):
        comment_data = self._database.get_data_with_id(target="cid", id=cid)
        comment = Comment()
        comment.make_with_dict(comment_data)

        # 어 내 댓글 아니다.
        if user.uid != comment.uid:
            return

        comment.display = 1
        self._database.modify_data_with_id("cid", target_data=comment.get_dict_form_data())

        return


    # 검색 시, 그리고 마이페이지에서 검색되는 댓글들을 반환하는 함수입니다.
    def get_comments_with_type_and_keyword(self, user, type:str, keyword:str=""):
        comment_datas = self._database.get_all_data(target="cid")
        comments = []

        for comment_data in comment_datas:
            if type == "search":
                if keyword in comment_data["body"]:
                    comment = Comment()
                    comment.make_with_dict(comment_data)
                    comments.append(comment)

            elif type == "mypage":
                if comment_data["cid"] in user.my_comment:
                    comment = Comment()
                    comment.make_with_dict(comment_data)
                    comments.append(comment)

        # pprint(comments)
        # pprint("댓글 들")
        # for comment in comments:
        #     pprint(comment.get_dict_form_data())

        feeds = self.__get_feeds_on_searched_comments(comments)

        return feeds

    def get_comments_with_keyword(self, keyword:str):
        comment_datas = self._database.get_all_data(target="cid")
        comments = []

        for comment_data in comment_datas:
            if keyword in comment_data["body"]:
                comment = Comment()
                comment.make_with_dict(comment_data)

                if comment.display == 0:
                    comment.body = "  삭제된 댓글입니다."
                    comment.uname = ""
                elif comment.display == 1 :
                    comment.body = "  차단된 댓글입니다."
                    comment.uname = ""
                elif comment.display == 2 :
                    comment.body = "  비공개된 댓글입니다."
                    comment.uname = ""

                comments.append(comment)

        classified_comments = self.__classify_reply_comment(comments=comments)

        return classified_comments

    # 내가 작성한 댓글 전부 불러오기
    # 페이징 기법은 새롭게 재편하기 떄문에 여기서 페이징을 하지않습니다.
    def get_my_comments(self, user):
        comment_datas = self._database.get_datas_with_ids(target_id="cid", ids=user.my_comment)
        comments = []

        for comment_data in comment_datas:
            comment = Comment()
            comment.make_with_dict(comment_data)
            if comment.display == 0:
                continue
            comments.append(comment)

        self.__get_comment_liked_info(user=user, comments=comments)
        classified_comments = self.__classify_reply_comment(comments=comments)

        return classified_comments


    #------------------------------------------------------------------------------------------------------------
    def paging_fid_list(self, fid_list:list, last_index:int, page_size=5):
        # 최신순으로 정렬된 상태로 Fid_list를 받아오기 때문에, 인덱스 번호가 빠를수록 최신의 것
        # 만약에 페이지 사이즈보다 더 짧은 경우도 있을 수 있기에 먼저 정해놓는다.
        # 이러면 페이징된 리스트의 길이에 상관없이, 인덱스를 알아낼 수 있을 것

        paging_list = fid_list[last_index + 1:]

        # 예외 처리
        last_index_next = -1
        if len(fid_list) != 0:
            last_index_next = fid_list.index(fid_list[-1])

        # 만약 페이지 사이즈를 넘었다면 표시할 개수만큼 짜르고, last_index를 재설정한다.
        if len(paging_list) > page_size:
            paging_list = paging_list[:page_size]
            # Paging 넘버
            last_index_next = fid_list.index(fid_list[last_index + page_size])

        return paging_list, last_index_next
