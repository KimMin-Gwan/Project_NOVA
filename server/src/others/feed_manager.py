from others.data_domain import Feed, User, Comment, ManagedUser
#from model import Local_Database
from datetime import datetime, timedelta
import string
import random
import boto3
import cv2
import glob
import os
import time
import numpy as np
import warnings
from io import BytesIO
from PIL import Image

# Boto3의 경고 메시지 무시
warnings.filterwarnings("ignore", module='boto3.compat')

# 피드를 관리하는 장본인


class FeedManager:
    def __init__(self, database, fclasses) -> None:
        self._feedClassManagement = FeedClassManagement(fclasses=fclasses)
        self._database= database
        self._managed_user_table = ManagedUserTable(database=database)
        self._feed_class_analist = FeedClassAnalist()
        self._num_feed = 0
        self._managed_feed_list = []
        pass

    def __get_argo(self, user):
        return self._feed_class_analist.dice_argo(option=user.option)
    
    # 서버 시작 초기에 관리용 피드를 메모리에 올리는 작업
    def init_feed_data(self):
        feed_list = []
        # 데이터 베이스에서 feed 데이터 전부다 가지고 오기
        raw_feed_data = self._database.get_all_data(target="fid")
        for data in raw_feed_data:
            feed = Feed()
            feed.make_with_dict(dict_data=data)
            feed.date = self.__get_datetime(date_str=feed.date) # 데이트 타임
            feed_list.append(feed)
        
        # 데이터를 날짜에 맞춰 정렬
        sorted_data = sorted(feed_list,key=lambda x:x.date, reverse=False)

        # 정렬된 데이터를 managed_feed로 만들어 메모리에 보관
        for data in sorted_data:
            managed_feed = ManagedFeed( key= self._num_feed,
                                        fid=data.fid,
                                        fclass=data.fclass,
                                        category=data.category)
            self._num_feed += 1
            self._managed_feed_list.append(managed_feed)
        print(f'INFO<-[      {self._num_feed} NOVA FEED NOW READY.')
        
    def __get_datetime(self, date_str):
        return datetime.strptime(date_str, "%Y/%m/%d-%H:%M:%S")

    def __set_datetime(self):
        return datetime.now().strftime("%Y/%m/%d-%H:%M:%S")

    def __set_fid_with_datatime(self):
        return datetime.now().strftime("%Y%m%d%H%M%S")

    def __get_today_date(self):
        return datetime.now().strftime("%Y/%m/%d")
    
    def __get_class_name(self, fclass):
        return self._feedClassManagement.get_class_name(fclass=fclass)

    # 새로운 fid 만들기
    def __make_new_fid(self, user):
        random_string = "default"
        # 중북되지 않는 fid 만들기
        while True:
            flag = True 
            # 사용할 문자들: 대문자, 소문자, 숫자
            characters = string.ascii_letters + string.digits

            # 8자리 랜덤 문자열 생성
            random_string = ''.join(random.choice(characters) for _ in range(6))

            fid = user.uid + random_string

            for feed in self._managed_feed_list:
                if feed.fid == fid:
                    flag = False
                    break

            if flag:
                break

        return fid

    def get_feed_meta_data(self):
        return self._feedClassManagement.get_fclass_meta_data()
    
    def try_modify_feed(self, user, data_payload):
        print("공사중")
        pass

    
    # 피드 새로 만들기
    def try_make_new_feed(self, user:User, data_payload):
        managed_user = self._managed_user_table.find_user(user=user)

        # fid 만들기
        fid = self.__make_new_fid(user=managed_user)

        # 이미지를 업로드 할것
        image_descriper = ImageDescriper()
        # 근데 이미지가 없으면 디폴트 이미지로 
        if data_payload.image_name == "image_not_exist?":
            image_result, flag = image_descriper.get_default_image_url()
        else:
            image_result, flag = image_descriper.try_feed_image_upload(
                fid=fid, image_name=data_payload.image_name,
                image=data_payload.image)

        # 이미지 업로드 실패하면
        if not flag:
            return image_result, False
        # 여기서 댓글 허용 같은 부분도 처리해야될것임
        self.__make_new_feed(user=user,
                            fid=fid,
                            fclass=data_payload.fclass,
                            choice=data_payload.choice,
                            body=data_payload.body,
                            image=image_result)
        
        #작성한 피드 목록에 넣어주고
        managed_user.my_feed.append(fid)

        # 끝
        return "Upload Success", True
    
    # 새로운 피드 만들기
    def __make_new_feed(self, user:User, fid, fclass, choice, body, image):

        # 검증을 위한 코드는 이곳에 작성하시오
        new_feed = self.__set_new_feed(user=user, fid=fid, fclass=fclass,
                                        choice=choice, body=body,
                                        image=image
                                        )
        self._database.add_new_data(target_id="fid", new_data=new_feed.get_dict_form_data())
        mangaed_feed = ManagedFeed(key=self._num_feed)
        mangaed_feed.fid = new_feed.fid
        mangaed_feed.fclass = new_feed.fclass
        mangaed_feed.category = new_feed.category
        self._managed_feed_list.append(mangaed_feed)
        self._num_feed += 1
        return

    # 새로운 피드의 데이터를 추가하여 반환
    def __set_new_feed(self, user:User,fid, fclass, choice, body, image):
        new_feed = Feed()
        new_feed.fid = fid
        new_feed.uid = user.uid
        new_feed.nickname = user.uname
        new_feed.body = body
        new_feed.date = self.__set_datetime()
        new_feed.fclass = fclass
        new_feed.class_name = self.__get_class_name(fclass=fclass)
        new_feed.choice = choice
        new_feed.state = "y"
        new_feed.category = [] # 여기서 카테고리 추가
        new_feed.image= image
        return new_feed
    

    def __set_send_feed(self, target_feed):
        result_key = 0
        target_fid = []
        for single_feed in target_feed:
            target_fid.append(single_feed.fid)
        feed_datas = self._database.get_datas_with_ids(target_id="fid", ids=target_fid)

        result = []
        for data in feed_datas:
            feed = Feed()
            feed.make_with_dict(data)
            result.append(feed)

        return result, result_key
    
    # 홈 화면에서 feed를 요청하는 상황
    def get_feed_in_home(self, user:User, key:int = -4):

        if user.uid != "":
            managed_user = self._managed_user_table.find_user(user=user)
            result, result_key = self._get_home_feed_with_user(user=managed_user, key=key)
            result = self.is_user_interacted(managed_user, result)
        else:
            result, result_key = self._get_home_feed(key=key)
            managed_user = ManagedUser()
            result = self.is_user_interacted(managed_user, result)

        return result, result_key
    
    def _get_home_feed_with_user(self, user, key):
        sample_feeds = []
        count = 0
        while True:
            if count > 100:
                break
            target_category =self.__get_argo(user)
            #present_feed = self.pick_single_feed_with_category(user=user, category=target_category)
            single_feed = self.pick_single_feed_with_category(user=user, category=target_category)
            if single_feed.key == -1:
                count += 1
                continue
            sample_feeds.append(single_feed)
            result_key = single_feed.key

            if len(sample_feeds) == 3:
                break

        result, _ = self.__set_send_feed(target_feed=sample_feeds)
        return result, result_key
    
    def _get_home_feed(self, key=-4):
        sample_feeds = []
        if key == -4:
            key = self._num_feed -1
            single_feed = self._get_single_managed_feed(key=key)
            sample_feeds.append(single_feed)
            result_key = single_feed.key
        count = 0
        while True:
            if count > 8:
                break
            single_feed = self.pick_single_feed_with_key(key=key)
            if single_feed.key == -1:
                count += 1
                continue
            sample_feeds.append(single_feed)
            result_key = single_feed.key
            key = result_key

            if len(sample_feeds) == 3:
                break

        result, _ = self.__set_send_feed(target_feed=sample_feeds)
        return result, result_key
    
    # 위성 탐색에서 feed데이터를 요청하는 상황
    def get_feed_in_fclass(self, user:User, key:int, fclass:str):
        # 제일 위에서 하나 뽑고, 다음꺼 하나 더뽑고
        # key에 맞는 feed 하나 더 뽑아서 넣어주기
        #for feed in self._managed_feed_list:
            #feed()
        if user.uid != "":
            managed_user = self._managed_user_table.find_user(user=user)
            result, result_key = self._get_short_feed_with_user(user=managed_user,key=key, fclass=fclass)
            result = self.is_user_interacted(managed_user, result)
        else:
            result, result_key = self._get_short_feed(key=key, fclass=fclass)
            managed_user = ManagedUser()
            result = self.is_user_interacted(managed_user, result)
        return result, result_key

    def _get_short_feed(self, key, fclass = "None"):
        sample_feeds = []
        # 제일 위에서 하나 뽑고, 다음꺼 하나 더뽑고
        # key에 맞는 feed 하나 더 뽑아서 넣어주기
        if key == -4:
            key = self._num_feed - 1
            while True:
                single_feed = self._get_single_managed_feed(key=key)
                if fclass != "None":
                    if single_feed.fclass != fclass:
                        key -= 1
                        continue
                sample_feeds.append(single_feed)
                result_key = single_feed.key
                break
            #self.__swap_list(sample_feeds)

        single_feed = self.pick_single_feed_with_key(key=key, fclass=fclass)
        sample_feeds.append(single_feed)
        result_key = single_feed.key

        result, _ = self.__set_send_feed(target_feed=sample_feeds)
        return result, result_key

    # 숏폼 피드에서 유저데이터가 있을때 데이터를 받아감
    # result = [지금 볼꺼, 다음볼꺼, 방금 본거]
    # result_key = 지금 볼꺼.key
    def _get_short_feed_with_user(self, user, key, fclass):
        sample_feeds = []
        # 제일 위에서 하나 뽑고, 다음꺼 하나 더뽑고
        # key에 맞는 feed 하나 더 뽑아서 넣어주기
        count = 0
        while True:
            if count > 100:
                break
            target_category =self.__get_argo(user)
            present_feed= self.pick_single_feed_with_category(user=user, category=target_category, fclass=fclass)
            if present_feed.key == -1:
                count += 1
                continue
            sample_feeds.append(present_feed)
            result_key = present_feed.key
            break

        if key == -4:
            count = 0
            while True:
                if count > 100:
                    break
                target_category =self.__get_argo(user)
                next_feed = self.pick_single_feed_with_category(user=user, category=target_category, fclass=fclass)
                if next_feed.key == -1:
                    count += 1
                    continue
                sample_feeds.append(next_feed)
                result_key = next_feed.key
                break
            #self.__swap_list(sample_feeds)

        result, _ = self.__set_send_feed(target_feed=sample_feeds)
        return result, result_key
    
    # 두개일때 뒤집기 해주는건데 이건 이제 안씀
    def __swap_list(self, list_data):
        temp = list_data[0]
        list_data[0] = list_data[1]
        list_data[1] = temp
        return 

    # fid나 key로 단일 feed 하나만 호출할 때
    def _get_single_feed(self, key = -1, fid = ""):
        target_feed = None
        if key != -1:
            for feed in self._managed_feed_list:
                if feed.key == key:
                    target_feed=feed
        else:
            for feed in self._managed_feed_list:
                if feed.fid== fid:
                    target_feed=feed

        if not target_feed:
            target_feed = Feed()
        else:
            feed_data=self._database.get_data_with_id(target="fid",id=feed.fid)
            target_feed = Feed()
            target_feed.make_with_dict(feed_data)
        return target_feed

    # fid나 key로 단일 feed 하나만 호출할 때
    def _get_single_managed_feed(self, key = -1, fid = ""):
        target_feed = None
        if key != -1:
            for feed in self._managed_feed_list:
                if feed.key == key:
                    target_feed=feed
        else:
            for feed in self._managed_feed_list:
                if feed.fid== fid:
                    target_feed=feed

        if not target_feed:
            target_feed = ManagedFeed(key=-1)
        return target_feed

    # 유저가 참여한 feed인지 확인할것
    # 사실상 User에게 전송하는 모든 feed는 이 함수를 통함
    def is_user_interacted(self, user, feeds:list):
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
            if feed.fid in user.star:
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

    def make_new_comment_on_feed(self, user:User, fid, body):
        managedUser:ManagedUser = self._managed_user_table.find_user(user=user)
        feed_data = self._database.get_data_with_id(target="fid", id=fid)
        feed = Feed()
        feed.make_with_dict(dict_data=feed_data)

        cid = fid+"-"+self.__set_fid_with_datatime()
        date = self.__get_today_date()
        new_comment = Comment(
            cid=cid, fid=feed.fid, uid=user.uid, 
            uname=user.uname, body=body, date=date)
        feed.comment.append(cid)

        managedUser.my_comment.append(cid)

        self._database.add_new_data("cid", new_data=new_comment.get_dict_form_data())
        self._database.modify_data_with_id("fid", target_data=feed.get_dict_form_data())

        result = self.is_user_interacted(user=managedUser, feeds=[feed])
        return result

    def remove_comment_on_feed(self, user:User, fid, cid):
        managedUser:ManagedUser = self._managed_user_table.find_user(user=user)

        feed_data = self._database.get_data_with_id(target="fid", id=fid)
        feed = Feed()
        feed.make_with_dict(dict_data=feed_data)

        comment_data = self._database.get_data_with_id(target="cid", id=cid)
        comment = Comment()
        comment.make_with_dict(comment_data)

        # 이거 지우는거 뭔가 대책이 필요함
        managedUser.my_comment.remove(cid)

        if user.uid == comment.uid:
            feed.comment.remove(cid)
            self._database.delete_data_With_id(target="cid", id=cid)
            self._database.modify_data_with_id("fid", target_data=feed.get_dict_form_data())

        result = self.is_user_interacted(user=managedUser, feeds=[feed])
        return result

    def get_all_comment_on_feed(self, user, fid):
        feed_data = self._database.get_data_with_id(target="fid", id=fid)
        feed=Feed()
        feed.make_with_dict(dict_data=feed_data)

        comments = []
        comment_datas = self._database.get_datas_with_ids(target_id="cid", ids=feed.comment)

        for comment_data in reversed(comment_datas):
            new_comment = Comment()
            new_comment.make_with_dict(comment_data)
            # 기본적으로 owner는 False
            if new_comment.uid == user.uid:
                new_comment.owner= True
            comments.append(new_comment)

        self.__get_comment_liked_info(user=user, comments=comments)
        return comments

    def __get_comment_liked_info(self, user:User, comments):
        for comment in comments:
            if user.uid in comment.like_user:
                comment.like_user = True
            else:
                comment.like_user = False
        return

    def try_like_comment(self, user:User, fid, cid):

        managedUser = self._managed_user_table.find_user(user=user)

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

        result = self.is_user_interacted(user=managedUser, feeds=[feed])
        return result

    def try_interaction_feed(self, user:User, fid:str, action):
        managed_user:ManagedUser = self._managed_user_table.find_user(user=user)

        if fid in managed_user.history:
            managed_user.history.remove(fid)
        feed = self.__try_interaction_with_feed(user=managed_user, fid=fid, action=action)

        return [feed]
        
    # feed 와 상호작용 -> 선택지를 선택하는 경우
    def __try_interaction_with_feed(self, user:ManagedUser, fid, action):
        fid_data = self._database.get_data_with_id(target="fid", id=fid)
        feed = Feed()
        feed.make_with_dict(fid_data)

        # 참여한 기록이 있는지 확인
        # 있으면 지우고, 결과값도 하나 줄여야됨
        target = -1
        print(feed.attend)

        for i, uids in enumerate(feed.attend):
            for uid in uids:
                if uid == user.uid:
                    uids.remove(uid)
                    print(i)
                    print(uids)
                    target = i
                    break

        if target != -1:
            user.active_feed.remove(fid)
            feed.result[target] -= 1

        # 이제 참여한 데이터를 세팅하고 저장하면됨
        print(target)
        print(action)

        if target != action:
            user.active_feed.append(fid)
            feed.attend[action].append(user.uid)
            feed.result[action] += 1
        else:
            #user.active_feed.remove(fid)  # 지울 필요가 없어보임 -> 주석 처리됨
            action = -1

        self._database.modify_data_with_id(target_id="fid",
                                            target_data=feed.get_dict_form_data())
        
        print(action)

        feed.attend = action
        feed.comment = self.__get_feed_comment(user=user, feed=feed)
        return feed

    def try_staring_feed(self, user:User, fid:str):
        managed_user:ManagedUser = self._managed_user_table.find_user(user=user)
        if fid in managed_user.history:
            managed_user.history.remove(fid)

        feed = self.__try_staring_feed(user=managed_user, fid=fid)
        feed = self.is_user_interacted(managed_user, feeds=[feed])
        return feed

    # feed 와 상호작용 -> 관심 표시
    def __try_staring_feed(self, user, fid):
        fid_data = self._database.get_data_with_id(target="fid", id=fid)
        feed = Feed()
        feed.make_with_dict(fid_data)

        if feed.fid in user.star:
            user.star.remove(feed.fid)
            feed.star -= 1
        else:
            user.star.append(feed.fid)
            feed.star += 1

        self._database.modify_data_with_id(target_id="fid",
                                            target_data=feed.get_dict_form_data())

        return feed
    
    # 단일 피드 뽑기
    # 만약 추천순 같이 정렬이 바뀔 일이 있으면
    # 여기다가 매게변수로 정렬된 리스트를 주면됨
    #  아니면 걍 내부에서 소팅 돌링 별도의 리스트를 가지고 검색할것
    def pick_single_feed_with_key(self, key, fclass = "None"):
        target = None
        flag = False
        for managed_feed in reversed(self._managed_feed_list):
            if managed_feed.key == key:
                flag = True
                continue
            if flag:
                if fclass == "None":
                    target = managed_feed
                    break

                if managed_feed.fclass == fclass:
                    target = managed_feed
                    break
        return target

    # 이건 카테고리에 있는 단일 피드 뽑는 함수
    def pick_single_feed_with_category(self, user, category, fclass="None"):
        target = None
        for managed_feed in reversed(self._managed_feed_list):
            if fclass != "None":
                if managed_feed.fclass != fclass:
                    continue
            
            if managed_feed.fid in user.history:
                continue
            target = managed_feed

            # 옵션이 하나도 없는 사람은 category를 검사할 수 없음
            if category == "None":
                break
            
            # 옵션 이 있는 사람은 카테고리 검사 하삼
            if category in target.category:
                break

        if target:
            user.history.append(target.fid)
        else:
            # 만약에 category로 찍은 데이터가 없음?
            target = ManagedFeed(key=-1)
        return target

    # 내가 작성한 피드 전체 불러오기
    def get_my_feeds(self, user, fid):
        managed_user:ManagedUser= self._managed_user_table.find_user(user=user)
        feed_datas = self._database.get_datas_with_ids(target_id="fid", ids=managed_user.my_feed)

        target = -1
        feeds = []
        for i, feed_data in enumerate(reversed(feed_datas)):
            feed = Feed()
            feed.make_with_dict(feed_data)
            feeds.append(feed)
            if feed.fid == fid:
                target = i


        if target != -1:
            feeds = feeds[target+1:]

        if len(feeds) > 5:
            feeds = feeds[:5]

        feeds = self.is_user_interacted(user=managed_user, feeds=feeds)

        return feeds

    # 내가 댓글을 작성한 피드 전부 불러오기
    #def get_commented_feed(self, user, fid):
        #managed_user:ManagedUser= self._managed_user_table.find_user(user=user)
        #print(managed_user.ttl)
        #comment_datas = self._database.get_datas_with_ids(target_id="cid", ids=managed_user.my_comment)
        #print(comment_datas)
        #fid_list = []
        #for comment_data in comment_datas:
            #comment = Comment()
            #comment.make_with_dict(comment_data)
            #fid_list.append(comment.fid)

        #feed_datas = self._database.get_datas_with_ids(target_id="fid", ids=fid_list)

        #feeds = []
        #target = -1
        #for i, feed_data in enumerate(reversed(feed_datas)):
            #feed = Feed()
            #feed.make_with_dict(feed_data)
            #feeds.append(feed)
            #if feed.fid == fid:
                #target = i

        #if target != -1:
            #feeds = feeds[target:]

        #if len(feeds) > 5:
            #feeds[:5]
        #return feeds

    # 내가 작성한 댓글 전부 불러오기
    def get_my_comments(self, user, cid):
        managed_user:ManagedUser= self._managed_user_table.find_user(user=user)
        comment_datas = self._database.get_datas_with_ids(target_id="cid", ids=managed_user.my_comment)

        comments = []
        target = -1
        for i, comment_data in enumerate(reversed(comment_datas)):
            comment = Comment()
            comment.make_with_dict(comment_data)
            comments.append(comment)
            if comment.cid == cid:
                target = i

        if target != -1:
            comments = comments[target+1:]

        if len(comments) > 5:
            comments = comments[:5]

        return comments 

    # 관심 표시한 피드 전부 불러오기
    def get_stared_feed(self, user, fid):
        managed_user:ManagedUser= self._managed_user_table.find_user(user=user)
        feed_datas = self._database.get_datas_with_ids(target_id="fid", ids=managed_user.star)

        feeds = []
        target = -1
        for i, feed_data in enumerate(reversed(feed_datas)):
            feed = Feed()
            feed.make_with_dict(feed_data)
            feeds.append(feed)
            if feed.fid == fid:
                target = i

        if target != -1:
            feeds = feeds[target+1:]

        if len(feeds) > 5:
            feeds = feeds[:5]

        feeds = self.is_user_interacted(user=managed_user, feeds=feeds)

        return feeds

    # 상호작용한 피드 전부 불러오기
    def get_interactied_feed(self, user, fid):
        managed_user:ManagedUser= self._managed_user_table.find_user(user=user)
        feed_datas = self._database.get_datas_with_ids(target_id="fid", ids=managed_user.active_feed)

        feeds = []
        target = -1
        for i, feed_data in enumerate(reversed(feed_datas)):
            feed = Feed()
            feed.make_with_dict(feed_data)
            feeds.append(feed)
            if feed.fid == fid:
                target = i

        if target != -1:
            feeds = feeds[target + 1:]

        if len(feeds) > 5:
            feeds = feeds[:5]
        feeds = self.is_user_interacted(user=managed_user, feeds=feeds)

        return feeds

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


# 이건 피드 메타 정보를 가지고 있는 친구
# configure.txt 에서 설정 가능함
class FeedClassManagement:
    def __init__(self, fclasses):
        self._fclasses = self.__set_fclasses(fclasses=fclasses)

    # 초기 class들 세팅
    def __set_fclasses(self, fclasses):
        result = []
        for fclass_data in fclasses:
            fclass = FeedClass(fclass_data[0], fclass_data[1], fclass_data[2])
            result.append(fclass)
        return result

    def get_class_name(self, fclass):
        for instance in self._fclasses:
            if instance.fclass == fclass:
                return instance.fname
            
    def get_fclass_meta_data(self):
        return self._fclasses


class FeedClass:
    def __init__(self, fclass, fname, specific):
        self.fclass = fclass
        self.fname = fname
        self.specific = specific

    def __call__(self):
        print("fclass : ", self.fclass )
        print("fname : ", self.fname)
        print("specific : ", self.specific)


class ManagedFeed:
    def __init__(self, key, fid ="", fclass="", category = [], star=0):
        self.key = key
        self.fid = fid
        self.fclass = fclass
        self.category  = category
        self.star = star

    def __call__(self):
        print(f"key: {self.key} | fid: {self.fid} | fclass: {self.fclass} | category: {self.category} | star: {self.star}")


# 메모리에 올려서 관리할 유저
# 알고리즘에 따라 적절한 피드 제공에 목적을 둠
class ManagedUserTable:
    def __init__(self, database):
        self.__key = 0  # ttl 체크용 index key
        self._managed_user_list = []
        self._database= database

    # 리스트 보여주기
    def __call__(self):
        for user in self._managed_user_list:
            user()

    # 세션 테이블에서 유저 찾기
    def find_user(self, user):
        for i, managed_user in enumerate(self._managed_user_list):
            if managed_user.uid == user.uid:
                self.__refresh_ttl(index=i)
                return self.get_user_data(index=i)
        index = self._add_user(user=user)
        return self.get_user_data(index)
    
    # 유저 데이터 반환
    def get_user_data(self, index):
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

class ImageDescriper():
    def __init__(self):
        self.__path = './model/local_database/feed_temp_image'
        self.__service_name = 's3'
        self.__endpoint_url = 'https://kr.object.ncloudstorage.com'
        self.__region_name = 'kr-standard'
        self.__access_key = 'eeJ2HV8gE5XTjmrBCi48'
        self.__secret_key = 'zAGUlUjXMup1aSpG6SudbNDzPEXHITNkEUDcOGnv'
        self.__s3 = boto3.client(self.__service_name,
                           endpoint_url=self.__endpoint_url,
                           aws_access_key_id=self.__access_key,
                      aws_secret_access_key=self.__secret_key)
        self.__bucket_name = "nova-feed-images"
        self.__default_image = "https://kr.object.ncloudstorage.com/nova-feed-images/nova-platform.PNG"

    def _check_image_size(self, img):
        width, height = img.size
        if width / height > 3 or height / width > 3:
            return False
        else:
            return True
    
    def __set_image_to_byte(self, image):
        return Image.open(BytesIO(image))
    
    def __set_image_to_cv2(self, image):
        return cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    
    def get_default_image_url(self):
        return [self.__default_image], True


    # 이미지 업로드
    def try_feed_image_upload(self, fid:str, image_name:str, image):
        try:
            byte_img = self.__set_image_to_byte(image=image)

            if not self._check_image_size(img=byte_img):
                return "image size does not fit in", False

            cv_image = self.__set_image_to_cv2(image=byte_img)

            #image_name = f'/{fid}-{image_name}'
            cv2.imwrite(self.__path+f'/{fid}_{image_name}',cv_image)

            self.__s3.upload_file(self.__path+f'/{fid}_{image_name}',
                                    self.__bucket_name ,
                                    f'{fid}_{image_name}',
                                    ExtraArgs={'ACL':'public-read'})
            

            self.delete_temp_image()
            url = self.__endpoint_url +"/"+ self.__bucket_name + "/" + fid + "_" + image_name

            return [url], True
        except Exception as e:
            print(e)
            return "Something Goes Bad", False

    # 임시 이미지 파일 지우기
    def delete_temp_image(self):
        # 파일이 작성되기 까지 대기 시간
        time.sleep(0.1)

        # 디렉토리 내의 모든 파일을 찾음
        files = glob.glob(os.path.join(self.__path, '*'))
        for file in files:
            # 파일인지 확인 후 삭제
            if os.path.isfile(file):
                os.remove(file)
        return








