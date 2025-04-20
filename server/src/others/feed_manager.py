import copy

from others.data_domain import Feed, User, Comment, ManagedUser, Interaction, FeedLink
from others.search_engine import FeedSearchEngine
from others.object_storage_connector import ObjectStorageConnection, HTMLEXtractor, ImageDescriper
#from model import Local_Database
from datetime import datetime, timedelta
import string
import random
import warnings
import re
from pprint import pprint


# Boto3의 경고 메시지 무시
warnings.filterwarnings("ignore", module='boto3.compat')

# Feed manager
class FeedManager:
    def __init__(self, database, feed_search_engine) -> None:
        #self._feedClassManagement = FeedClassManagement(fclasses=fclasses)
        #self._database:Local_Database= database
        self._database= database
        #self._managed_user_table = ManagedUserTable(database=database)
        self._feed_class_analist = FeedClassAnalist()
        self._feed_search_engine:FeedSearchEngine = feed_search_engine
        self._num_feed = 0
        self._managed_feed_list = []

    def __get_argo(self, user):
        return self._feed_class_analist.dice_argo(option=user.option)

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
    def __make_new_feed(self, user:User, fid, fclass, choice, body, hashtag,
                        board_type, images, link, bid, raw_body="", ai_manager=None, data_payload_body=None):
        # 검증을 위한 코드는 이곳에 작성하시오
        new_feed = self.__set_new_feed(user=user, fid=fid, fclass=fclass,
                                       choice=choice, body=body, hashtag=hashtag,
                                       board_type=board_type, image=images, link=link, bid=bid, raw_body=raw_body)


        if data_payload_body:
            # ai한테 넣어서 다시 만들기
            new_feed = ai_manager.treat_new_feed(feed=new_feed, data_payload_body=data_payload_body)
        else:
            new_feed = ai_manager.treat_new_feed(feed=new_feed)
            
        
        self._database.add_new_data(target_id="fid", new_data=new_feed.get_dict_form_data())

        self._feed_search_engine.try_make_new_managed_feed(feed=new_feed)
        self._feed_search_engine.try_add_feed(feed=new_feed)
        return

    # 링크 만들기
    def _make_new_link(self, fid, feed_links):
        result_feed_links = []

        lid_list = []

        # 여기서 실제 링크를 타고 들어가서 해당 사이트의 ㅡ내용을 긁어 올 필요가 있음
        # 크롤링이 안되는 사이트면 하는 수 없고
        for feed_link in feed_links:
            feed_link:FeedLink = feed_link
            # pprint(feed_link.get_dict_form_data())
            lid = self.__make_new_iid()
            feed_link.lid = lid
            feed_link.fid = fid
            feed_link.domain = HTMLEXtractor().extract_link_domain_string(url=feed_link.url)
            feed_link.title = HTMLEXtractor().extract_external_webpage_title_tag(url=feed_link.url)
            result_feed_links.append(feed_link.get_dict_form_data())
            lid_list.append(lid)

        # 데이터 저장
        self._database.add_new_datas(target_id="lid", new_datas=result_feed_links)

        return lid_list

    # 새로운 피드의 데이터를 추가하여 반환
    def __set_new_feed(self, user:User,fid, fclass, choice, body, hashtag,
                       board_type, image, link, bid, raw_body):
        # 인터액션이 있으면 작업할것
        if len(choice) > 1:
            iid, _ = self.try_make_new_interaction(fid=fid, choice=choice)
        else:
            iid = ""

        # link가 있다면 작업할 것
        if link:
            lids = self._make_new_link(fid=fid, feed_links=link)
        else:
            lids = []

        # 새로운 피드 만들어지는 곳
        new_feed = Feed()
        new_feed.fid = fid
        new_feed.uid = user.uid
        new_feed.nickname = user.uname
        new_feed.body = body
        new_feed.date = self.__set_datetime()
        new_feed.fclass = fclass
        new_feed.board_type = board_type
        new_feed.image= image
        new_feed.hashtag = hashtag
        new_feed.num_image = len(image)
        new_feed.iid = iid
        new_feed.lid = lids
        new_feed.bid = bid
        new_feed.raw_body = raw_body
        return new_feed

    # FEED 클래스를 반환하는 함수
    def __get_class_name(self, fclass):
        fname, result = self._feedClassManagement.get_class_name(fclass=fclass)
        return fname, result

    # FEED 작성
    def try_make_new_feed(self, user:User, data_payload, fid = "", ai_manager=None):
        # fid 만들기 feed 수정기능을 겸하고 있기 때문에, 다음을 추가한 것
        if fid == "":
            fid = self.__make_new_fid(user=user)

        if data_payload.fclass == "short":
            
            # 이미지를 업로드 할것
            # 근데 이미지가 없으면 디폴트 이미지로
            if len(data_payload.image_names) == 0:
                #image_result, flag = image_descriper.get_default_image_url()
                image_result = []
                flag = True
            else:
                image_result, flag = ImageDescriper().try_feed_image_upload(
                    fid=fid, image_names=data_payload.image_names,
                    images=data_payload.images)
            # 이미지 업로드 실패하면
            if not flag:
                return image_result, False

            # 여기서 댓글 허용 같은 부분도 처리해야될 것임
            self.__make_new_feed(user=user,
                                 fid=fid,
                                 fclass=data_payload.fclass,
                                 choice=data_payload.choice,
                                 body=data_payload.body,
                                 hashtag=data_payload.hashtag,
                                 board_type=data_payload.board_type,
                                 images=image_result,
                                 link=data_payload.link,
                                 bid=data_payload.bid,
                                 ai_manager=ai_manager
                                 )

        # 롱폼의 경우 작성된 html을 올리고 저장하면됨
        # 이때 body 데이터는 url로 되어야함
        # 대신 전송될 때는 body데이터가 html로 다시 복구되어 전송되어야함
        elif data_payload.fclass == "long":
            connector = ObjectStorageConnection()
            # 1. 전송된 body데이터를 확인
            if data_payload.body:
                data_payload_body = data_payload.body
                # 2. body데이터를 오브젝트 스토리지에 저장
                url = connector.make_new_feed_body_data(fid = fid, body=data_payload.body)
                body, _ = connector.extract_body_n_image(raw_data=data_payload.body)

            else:
                data_payload_body = " "
                body = " "
                url = connector.make_new_feed_body_data(fid=fid, body=body)

            # 3. url을 body로 지정

            # 여기서 댓글 허용 같은 부분도 처리해야될 것임
            self.__make_new_feed(user=user,
                                 fid=fid,
                                 fclass=data_payload.fclass,
                                 choice=data_payload.choice,
                                 body=body,
                                 hashtag=data_payload.hashtag,
                                 board_type=data_payload.board_type,
                                 images=[],
                                 link=data_payload.link,
                                 bid=data_payload.bid,
                                 raw_body = url, # 이거 url이라는 변수가 없어서
                                 ai_manager=ai_manager,
                                 data_payload_body = data_payload_body
                                 )

        #작성한 피드 목록에 넣어주고
        user.my_feed.append(fid)

        # 유저 데이터에 Feed 개수 늘리기. 생성 시 개수가 늘어남
        if data_payload.fclass == "short":
            user.num_short_feed+=1
        elif data_payload.fclass == "long":
            user.num_long_feed+=1

        self._database.modify_data_with_id(target_id="uid", target_data=user.get_dict_form_data())
        # 끝
        return "Upload Success", True

    # FEED 수정
    # 댓글하고 다르게 이미지도 수정이 가능하므로, 데이터를 삭제하고 다시 작성하는 방식을 취함.
    def try_modify_feed(self, user:User, data_payload):
        # FEED 데이터 불러옴
        feed_data=self._database.get_data_with_id(target="fid",id=data_payload.fid)
        feed = Feed()
        feed.make_with_dict(feed_data)

        # 내 글이 아니네!
        if feed.uid != user.uid:
            return "NOT_OWNER", False

        # 기존의 FEED를 삭제하고(?), 새롭게 데이터를 작성한다.
        self._database.delete_data_with_id(target="fid", id=feed.fid)
        result, flag = self.try_make_new_feed(user=user, data_payload=data_payload, fid=feed.fid)
        return result, flag

    def try_remove_feed_new(self, user:User, fid):
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

        # 댓글 삭제 시
        if feed.fclass == "short":
            user.num_short_feed-=1
        elif feed.fclass == "long":
            user.num_long_feed-=1

        #
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
    def get_my_long_feeds(self, user:User):
        feed_datas = self._database.get_datas_with_ids(target_id="fid", ids=user.my_feed)
        feeds = []

        for _, feed_data in enumerate(reversed(feed_datas)):
            feed = Feed()
            feed.make_with_dict(feed_data)
            if feed.fclass == "long":
                if feed.display == 0:
                    continue
                feeds.append(feed)

        return feeds

    # Moment(숏 피드)만 가져오는 거
    def get_my_short_feeds(self, user:User):
        feed_datas = self._database.get_datas_with_ids(target_id="fid", ids=user.my_feed)
        feeds = []

        for _, feed_data in enumerate(reversed(feed_datas)):
            feed = Feed()
            feed.make_with_dict(feed_data)
            if feed.fclass == "short":
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

    # 상호작용한 Feed만 가져오기
    def get_interacted_feed(self, user:User):
        feed_datas = self._database.get_datas_with_ids(target_id="fid", ids=user.active_feed)
        feeds = []

        for i, feed_data in enumerate(reversed(feed_datas)):
            feed = Feed()
            feed.make_with_dict(feed_data)
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
    def try_staring_feed(self, user:User, fid:str):
        feed = self.__try_staring_feed(user=user, fid=fid)
        return [feed]

    # feed 와 상호작용 -> 관심 표시
    def __try_staring_feed(self, user:User, fid):
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
            feed.star -= 1
        else:
            self._feed_search_engine.try_like_feed(fid=feed.fid, uid=user.uid, like_time=date)
            user.like.append(str_fid_n_date)
            feed.star += 1

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

    # 멘션한 유저를 찾아내자
    def _extract_mention_data(self, body):
        # 정규식으로 찾음, 이메일 형식도 가져올수 있는 문제가 있어 정규식을 더 정교하게 설정
        match = re.search(r'@(\w+)(?!\.\w+)', body)
        # 매칭 실패시
        if match:
            return match.group(1)
        return ""

    # 댓글, 대댓글 작성 함수
    def try_make_comment_on_feed(self, user:User, fid, target_cid, body, ai_manager):
        # FEED 데이터 불러오기
        feed_data = self._database.get_data_with_id(target="fid", id=fid)
        feed = Feed()
        feed.make_with_dict(feed_data)

        # CID 만들기, 중복이 있을 가능성 있음
        # 일단 __set_datetime()쓰면 cid 분리 시, -때문에 분리가 이상하게 됨. 그래서 FID 만들 때랑 동일한 시간제작방식 사용
        cid = fid+"-"+self.__set_fid_with_datatime()
        date = self.__get_today_date()
        mention = self._extract_mention_data(body)

        # 타겟 CID도 Comment 객체 멤버로 담아버림. CID 너무 길어지기도 하고, 프론트에서 작업을 안시키게 함.
        new_comment = Comment(
            cid=cid, fid=feed.fid, uid=user.uid, uname=user.uname, target_cid=target_cid,
            body=body, date=date, mention=mention
        )
        new_comment = ai_manager.treat_new_comment(comment=new_comment)
        
        feed.comment.append(cid)
        user.my_comment.append(cid)
        user.num_comment += 1

        self._database.add_new_data("cid", new_data=new_comment.get_dict_form_data())
        self._database.modify_data_with_id("fid", target_data=feed.get_dict_form_data())
        self._database.modify_data_with_id("uid", target_data=user.get_dict_form_data())
        return

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

    # 댓글 삭제
    def remove_comment_on_feed(self, user:User, fid, cid):
        comment_data = self._database.get_data_with_id(target="cid", id=cid)
        comment = Comment()
        comment.make_with_dict(comment_data)

        # 어 내 댓글 아니다.
        if user.uid != comment.uid:
            return

        # 디스플레이 옵션만 바꾸면 됨
        comment.display = 0

        # Feed 안에서는 댓글리스트에서 삭제합니다.
        # 근데 댓글 리스트에서
        # feed_data = self._database.get_data_with_id(target="fid", id=fid)
        # feed = Feed()
        # feed.make_with_dict(feed_data)
        # feed.comment.remove(cid)

        # 유저 데이터베이스에서 갯수를 줄임. 단, 실제 댓글은 데이터베이스에 남는다.
        user.my_comment.remove(cid)
        user.num_comment -= 1
        self._database.modify_data_with_id("cid", target_data=comment.get_dict_form_data())
        # self._database.modify_data_with_id("fid", target_data=feed.get_dict_form_data())
        self._database.modify_data_with_id("uid", target_data=user.get_dict_form_data())


        return

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

    # 댓글에 좋아요를 누르는 기능

    # 댓글 좋아요 표시
    def try_like_comment(self, user:User, fid, cid):
        feed_data = self._database.get_data_with_id(target="fid", id=fid)
        feed = Feed()
        feed.make_with_dict(dict_data=feed_data)

        comment_data = self._database.get_data_with_id(target="cid", id=cid)
        comment = Comment()
        comment.make_with_dict(comment_data)

        if user.uid in comment.like_user:
            comment.like_user.remove(user.uid)
            comment.like -= 1
        else:
            comment.like_user.append(user.uid)
            comment.like += 1

        self._database.modify_data_with_id("cid", target_data=comment.get_dict_form_data())

        return

        # 댓글 도메인 리스트에서 찾아야 할 댓글을 찾는 함수

    def __find_comment_in_comment_list(self, comments, cid):
        for comment in comments:
            if comment.cid == cid:
                return comment
        return None

    # 댓글 분류를 해주는 함수. 도저히 저 밑에서 하기힘들다고 생각했음. 그래서 따로 함수를 나눴어
    # taregted는 타케팅 당한 쪽아니라 하는쪽임 따라서 사실은 [targeting]임 -> 읽을 때 유의할것
    def __classify_reply_comment(self, comments):
        # 1. 대댓글인 애들이랑 아닌 애들을 분리
        # 2. 대댓글인 애들을 하나씩 뽑아서 목표 댓글 reply에 넣음
        # 2-1. (댓글을 하나씩 뽑아서 대댓글과 대조하는 것과 같은 시간 복잡도를 가짐)
        # 3. 만약 이미 들어간 댓글이면 continue해야됨
        # 4. reply에 넣을 땐, dict로 넣어야됨
        no_targeted_comments = []       # target_cid가 없는 놈
        exist_targeted_comments = []    # target_cid가 있는 놈

        for comment in comments:
            if comment.target_cid != '':
                exist_targeted_comments.append(comment)
            else:
                no_targeted_comments.append(comment)

        # 대댓글을 분류하는 작업.
        # 대댓글의 cid를 비교해서 댓글의 reply에 담는 작업을 합니다.
        for targeted_comment in exist_targeted_comments:
            comment = self.__find_comment_in_comment_list(no_targeted_comments, targeted_comment.target_cid)
            if comment is not None:
                for reply_comment in comment.reply:
                    if reply_comment["cid"] == targeted_comment.cid:
                        continue
                comment.reply.append(targeted_comment.get_dict_form_data())

            # 리스트에 없는 경우. 이 경우는 조금 위험하긴하지만, Database에서 찾아내서 붙인다.
            # 마이페이지의 내가 쓴 댓글 중, 다른 댓글의 대댓글을 단 경우에 해당된다.
            else:
                comment_data = self._database.get_data_with_id(target="cid", id=targeted_comment.target_cid)
                comment = Comment()
                comment.make_with_dict(comment_data)

                for reply_comment in comment.reply:
                    if reply_comment["cid"] == targeted_comment.cid:
                        continue
                comment.reply.append(targeted_comment.get_dict_form_data())
                # 이 댓글은 마이페이지에서 가져온 no_targeted_comments에는 없는 데이터이기 때문에
                # 만약 한 댓글에 2개 이상의 대댓글을 달았다면.. 딱 한번만 들어가게 된다.
                if comment not in no_targeted_comments:
                    no_targeted_comments.append(comment)

        return no_targeted_comments

    # Feed에 있는 모든 댓글들을 모두 가져와야 함
    # 피드 안에 있는 모든 Comment를 가져옴.
    def get_all_comment_on_feed(self, user, fid):
        feed_data = self._database.get_data_with_id(target="fid", id=fid)
        feed=Feed()
        feed.make_with_dict(dict_data=feed_data)

        comments = []
        comment_datas = self._database.get_datas_with_ids(target_id="cid", ids=feed.comment)

        for comment_data in comment_datas:
            new_comment = Comment()
            new_comment.make_with_dict(comment_data)

            # 기본적으로 owner는 False
            if new_comment.uid == user.uid:
                new_comment.owner= True
            
            if user.level < new_comment.level:
                # 리워크된 데이터로 변경
                new_comment.body = new_comment.reworked_body
                # 리워크 됨을 알려줄 것
                new_comment.is_reworked = True

            if new_comment.display == 0:
                new_comment.body = "  삭제된 댓글입니다."
                new_comment.uname = ""
                
            elif new_comment.display == 1 :
                new_comment.body="  차단된 댓글입니다."
                new_comment.uname = ""

            elif new_comment.display == 2:
                new_comment.body="  비공개된 댓글입니다."
                new_comment.uname = ""

            comments.append(new_comment)

        self.__get_comment_liked_info(user=user, comments=comments)

        classified_comments = self.__classify_reply_comment(comments=comments)
        return classified_comments

        # pprint(classified_comments)
        #
        # pprint("분류 후 댓글")
        # for comment in classified_comments:
        #     pprint(comment.get_dict_form_data())
        #     pprint(comment.reply)

        # pprint("분류전 댓글")
        # for comment in comments:
        #     pprint(comment.get_dict_form_data())
        # reply에 담는 작업
        # 왜 이렇게 하나면 마지막부터 시작하니까 저 위에서 처리하기엔 꼬이는 것 같음.

        # pprint("분류 후 댓글들")
        # for comment in comments:
        #     pprint(comment.get_dict_form_data())

        # 이거 바꿔야함.
        # return classified_comments

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



    #---------------------------------interaction 수행 관련------------------------------------------------------
    # IID를 만드는 곳
    def __make_new_iid(self):
        random_string = "default"

        # 사용할 문자 : FID와 비슷하게 대문자, 소문자, 숫자
        characters = string.ascii_letters + string.digits

        # 랜덤 문자열 7자리 생성 (단, 앞자리는 Interaction임을 알도록 붙여야함.)
        random_string = 'i'+''.join(random.choice(characters) for _ in range(6))

        # FID가 이미 고유번호라 중복이 되어도 따로 상관없겠지?
        # iid = iid고유
        iid = random_string

        return iid

    # 기본 뼈대 : FEED 만드는 함수 참고
    def _make_new_interaction(self, iid, fid, choice:list):
        user_attend_list = list([] for _ in choice)
        new_interaction = Interaction()

        iid_dict = dict()
        iid_dict['iid'] = iid
        iid_dict['fid'] = fid
        iid_dict['choice'] = copy.copy(choice)
        iid_dict['attend'] = copy.copy(user_attend_list)

        new_interaction.make_with_dict(iid_dict)

        return new_interaction

    # INTERACTION 만들기
    def try_make_new_interaction(self, fid, choice:list):
        # modify 의미가 없음
        #fid = self._database.modify_data_with_id("fid", target_data=fid)
        #feed = Feed()
        #feed.make_with_dict(fid)

        # 혹시 몰라서 예외처리 남김
        if len(choice) == 0:
            return "No Choice", False

            # iid 만들기
        new_iid = self.__make_new_iid()

        new_interaction = self._make_new_interaction(iid=new_iid, fid=fid, choice=choice)

        self._database.add_new_data(target_id="iid", new_data=new_interaction.get_dict_form_data())
        # 음.. 따로 더 저장할게 있나요? 검토좀

        return new_interaction.iid, True

    # INTERACTION 수정, 근데 이거 필요한지는 모르겠음.

    # Choice를 선택한 순간, USER 정보가 저장되는데, choice를 수정하면 그 선택지는 날려야할 것 같으니까.
    # 그리고 이거 움직일려면 Try_modify_Feed랑 같이 움직여야 하는데
    # 일단 잠시만 그 부분은 컨펌 이후에 진행하겠음
    def try_modify_interaction(self, fid, iid, new_choice:list):
        interaction_data = self._database.get_data_with_id(target="iid", id=iid)
        interaction = Interaction()
        interaction.make_with_dict(interaction_data)

        self._database.delete_datas_with_id(target="iid", id=iid)
        result, flag = self.try_make_new_interaction(fid=fid, choice=new_choice)

        return result, flag

    # 데이터베이스에서 삭제
    def try_remove_interaction(self, fid):
        feed_data = self._database.get_data_with_id(target="fid", id=fid)
        feed = Feed()
        feed.make_with_dict(feed_data)

        # 데이터베이스에서 삭제
        if not self._database.delete_datas_with_id(target="iid", id=feed.iid):
            return "DATABASE_ERROR", False

        # iid가 REMOVE되어서 FEED도 수정함.
        feed.iid = ""
        self._database.modify_data_with_id(target="fid", target_data=feed.get_dict_form_data())

        return "COMPLETE", True

    # FEED 상호 작용
    def try_interaction_feed(self, user:User, fid:str, action):
        feed = self.__try_interaction_with_feed(user=user, fid=fid, action=action)
        return [feed]

    # feed 와 상호작용 -> 선택지를 선택하는 경우
    # interaction 객체에 맞게 수정했음.
    def __try_interaction_with_feed(self, user:User, fid, action):
        fid_data = self._database.get_data_with_id(target="fid", id=fid)
        feed = Feed()
        feed.make_with_dict(fid_data)

        try:
            iid = feed.iid
            interaction_data = self._database.get_data_with_id(target="iid", id=iid)
            interaction = Interaction()
            interaction.make_with_dict(interaction_data)

            # 참여한 기록이 있는지 확인
            # 있으면 지우고, 결과값도 하나 줄여야됨

            target = -1
            for i, uids in enumerate(interaction.attend):
                for uid in uids:
                    if uid == user.uid:
                        uids.remove(uid)
                        target = i
                        break

            if target != -1:
                user.active_feed.remove(fid)
                interaction.result[target] -= 1

            # 이제 참여한 데이터를 세팅하고 저장하면됨
            if target != action:
                user.active_feed.append(fid)
                interaction.attend[action].append(user.uid)
                interaction.result[action] += 1

            else:
                #user.active_feed.remove(fid)  # 지울 필요가 없어보임 -> 주석 처리됨
                action = -1

            self._database.modify_data_with_id(target_id="iid", target_data=interaction.get_dict_form_data())
            self._database.modify_data_with_id(target_id="uid", target_data=user.get_dict_form_data())

        except Exception as e:
            print(e)
        finally:
            return feed

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

# 이건 뭐냐하면
# fclass 간의 유사도를 판별하여
# 전송하는 데이터에 추가적인 변화를 주려고 만듬
# 그냥 일종의 알고리즘 저장소 같은 개념
class FeedClassAnalist:
    def __init__(self):
        pass

    def dice_argo(self, option):
        if not len(option):
            return "None"

        len_option = len(option)
        key =  random.randint(0, 1000)
        target = key % len_option
        result = option[target]
        return result


class FeedClass:
    def __init__(self, fclass, fname, specific, num_choice):
        self.fclass = fclass
        self.fname = fname
        self.specific = specific
        self.num_choice = num_choice

    def __call__(self):
        print("fclass : ", self.fclass )
        print("fname : ", self.fname)
        print("specific : ", self.specific)
        print("choice : ", self.num_choice)


class ManagedFeed:
    def __init__(self, key, fid ="", fclass="", category = [], star=0, hashtag =[]):
        self.key = key
        self.fid = fid
        self.fclass = fclass
        self.category  = category
        self.star = star
        self.hashtag = hashtag

    def __call__(self):
        print(f"key: {self.key} | fid: {self.fid} | fclass: {self.fclass} | category: {self.category} | star: {self.star}")


# 메모리에 올려서 관리할 유저
# 알고리즘에 따라 적절한 피드 제공에 목적을 둠
class ManagedUserTable:
    def __init__(self, database):
        self.__key = 0  # ttl 체크용 index key
        self._managed_user_list = []
        self._database= database
        self.__trash_table = TrashTable(database=database)

    # 리스트 보여주기
    def __call__(self):
        for user in self._managed_user_list:
            user()

    # 세션 테이블에서 유저 찾기
    def find_user(self, user) -> ManagedUser:
        for i, managed_user in enumerate(self._managed_user_list):
            if managed_user.uid == user.uid:
                self.__refresh_ttl(index=i)
                return self.get_user_data(index=i)
        index = self._add_user(user=user)
        return self.get_user_data(index)
    
    # 유저 데이터 반환
    def get_user_data(self, index):
        self.__set_trash_table(self._managed_user_list[index])
        return self._managed_user_list[index]

    # 테이블에 유저 추가하기
    def _add_user(self, user:User):
        managed_user_data = self._database.get_data_with_id(target="muid", id=user.uid)

        new_user = ManagedUser()
        new_user.make_with_dict(managed_user_data)
        new_user.ttl = self.__get_new_ttl()

        index = self.__check_ttl()
        if index != -1:
            temp = self._managed_user_list[index]
            self._database.modify_data_with_id(target_id="muid", target_data=temp.get_dict_form_data())
            self._managed_user_list[index] = new_user
        else:
            self._managed_user_list.append(new_user)
            index = len(self._managed_user_list) - 1
        return index

    # 만료되었으면 메모리에서 내릴꺼라서 체크해야됨
    def __check_ttl(self):
        index = -1
        if self.__key == len(self._managed_user_list):
            self.__key = 0

        for i in range(self.__key, len(self._managed_user_list)):
            if self._managed_user_list[i].ttl < datetime.now():
                self.__key = i
                index = i
                break
        return index
                
    # ttl 초기화
    def __refresh_ttl(self, index):
        self._managed_user_list[index].ttl = self.__get_new_ttl()
        return
    
    def __get_new_ttl(self):
        ttl = datetime.now() + timedelta(seconds=3600)
        return ttl
    
    # 유저를 찾을 때 마다 이짓을 반복해야됨
    # 그럼 효율이 좋을 것이라 판단
    def __set_trash_table(self, user:ManagedUser):
        if self.__trash_table.clean_up_managed_user_data(user=user):
            self._database.modify_data_with_id("muid", target_data=user.get_dict_form_data())
        return

    def add_trash_feed_fid(self, fid:str):
        self.__trash_table.add_trash_feed_fid(fid)
        return

    # 데이터가 삭제되면 추가됨 여긴 리스트로 받아야됨
    def add_trash_comment_cids(self, cids:list):
        self.__trash_table.add_trash_comment_cids(cids)
        return

# 피드 삭제에 대응하기 위한 대책
# 기존에 삭제 방침은 데이터의 무결성을 유지하기 매우 어려움
# 특히 star를 표시한 피드와 active_feed, my_comment 등을 제제 하기 어려움
# 이에 TrashFeedTable과 TrashCommentTable을 만들어 체크하도록 하였음

class TrashTable:
    def __init__(self, database):
        self.__trash_feed_fids = []
        self.__trash_comment_cids = []
        self.__num_feed_trash = 0
        self.__num_comment_trash = 0
        self.__database = database
        self.__set_init_data(database=database)
        return

    def __set_init_data(self, database):
        self.__trash_feed_fids = database.get_trash_fids()
        self.__trash_comment_cids = database.get_trash_cids()
        self.__num_feed_trash = len(self.__trash_feed_fids)
        self.__num_comment_trash = len(self.__trash_comment_cids)
        return

    # 데이터가 삭제되면 추가됨
    def add_trash_feed_fid(self, fid:str):
        self.__trash_feed_fids.append(fid)
        self.__num_feed_trash += 1
        self.__database.set_trash_fids(self.__trash_feed_fids)
        return 

    # 데이터가 삭제되면 추가됨 여긴 리스트로 받아야됨
    def add_trash_comment_cids(self, cids:list):
        self.__trash_comment_cids.extend(cids)
        self.__num_comment_trash += 1
        self.__database.set_trash_cids(self.__trash_comment_cids)
        return

    def clean_up_managed_user_data(self, user:ManagedUser):
        if self.__num_feed_trash == user.feed_key and self.__num_comment_trash == user.comment_key:
            return False
        else:
            user.feed_key += self.__clean_up_feed_data_in_manage_user(user=user)
            user.comment_key += self.__clean_up_comment_data_in_manage_user(user=user)
            return True

    def __clean_up_feed_data_in_manage_user(self, user:ManagedUser):
        count = 0
        for i in range(user.feed_key, self.__num_feed_trash):
            if self.__trash_feed_fids[i] in user.star:
                user.star.remove(self.__trash_feed_fids[i])
            if self.__trash_feed_fids[i] in user.active_feed:
                user.active_feed.remove(self.__trash_feed_fids[i])
            if self.__trash_feed_fids[i] in user.history:
                user.history.remove(self.__trash_feed_fids[i])
            if self.__trash_feed_fids[i] in user.my_feed:
                user.my_feed.remove(self.__trash_feed_fids[i])
            count += 1
        return count
        
    def __clean_up_comment_data_in_manage_user(self, user:ManagedUser):
        count = 0
        for i in range(user.comment_key, self.__num_comment_trash):
            if self.__trash_comment_cids[i] in user.my_comment:
                user.my_comment.remove(self.__trash_feed_fids[i])
        return count
        

#-------------------------------------------------------------------------------------------------------------