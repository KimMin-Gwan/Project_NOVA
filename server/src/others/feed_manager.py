from others.data_domain import Feed, User
#from model import Local_Database
from datetime import datetime
import string
import random

# 피드를 관리하는 장본인


class FeedManager:
    def __init__(self, database) -> None:
        self._database = database
        self._num_feed = 0
        self._managed_feed_list = []
        pass
    
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
        sorted_data = sorted(feed_list,key=lambda x:x.date, reverse=True)

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
    
    def __get_class_name(self, fclass):
        name_data = {
            "multiple" : "넷 중 하나",
            "station" : "정거장",
            "balance" : "둘 중 하나",
            "card" : "자랑"
        }
        return name_data[fclass]

    # 새로운 fid 만들기
    def __make_new_fid(self):
        random_string = "default"

        # 중북되지 않는 fid 만들기
        while True:
            flag = True 
            # 사용할 문자들: 대문자, 소문자, 숫자
            characters = string.ascii_letters + string.digits

            # 8자리 랜덤 문자열 생성
            random_string = ''.join(random.choice(characters) for _ in range(8))

            for feed in self._managed_feed_list:
                if feed.fid == random_string:
                    flag = False
                    break

            if flag:
                break

        return random_string


    # 새로운 피드 만들기
    def make_new_feed(self, user:User, fclass, choice, title, body):
        # 검증을 위한 코드는 이곳에 작성하시오

        new_feed = self.__set_new_feed(user, fclass=fclass,
                                        choice=choice, title=title, body=body)
        self._database.add_new_data(target_id="fid", new_data=new_feed.get_dict_form_data())
        mangaed_feed = ManagedFeed()
        mangaed_feed.fid = new_feed.fid
        mangaed_feed.fclass = new_feed.fclass
        mangaed_feed.category = new_feed.category
        mangaed_feed.key = self._num_feed
        self._managed_feed_list.append(mangaed_feed)
        self._num_feed += 1

    # 새로운 피드의 데이터를 추가하여 반환
    def __set_new_feed(self, user:User, fclass, choice, title, body):
        new_feed = Feed()
        new_feed.fid = self.__make_new_fid()
        new_feed.uid = user.uid
        new_feed.nickname = user.uname
        new_feed.title = title
        new_feed.body = body
        new_feed.date = self.__set_datetime()
        new_feed.fclass = fclass
        new_feed.class_name = self.__get_class_name(fclass=fclass)
        new_feed.choice = choice
        new_feed.result = []
        new_feed.state = "y"
        new_feed.category = []
        return new_feed
    
    def __make_target_feed(self, user:User, key:int):
        target_feed = []
        # 초기에는 -1로 올테니까 가장 최신으로
        if key == -1:
            key = self._num_feed - 1
        else:
            key = key

        # 출력
        #for f in self._managed_feed_list:
            #f()

        target = -1
        # 지지자의 요청이라면 유사한 내용으로 알고리즘
        if user.uid != "":
            for i, single_feed in enumerate(reversed(self._managed_feed_list)):
                single_feed:ManagedFeed = single_feed
                if single_feed.key == key:
                    target = i
                    break

        # 일반 유저의 요청이라면 그냥 순서대로
        else:
            for i, single_feed in enumerate(reversed(self._managed_feed_list)):
                single_feed:ManagedFeed = single_feed
                if single_feed.key == key:
                    target = i
                    break
                
        #self._managed_feed_list[target]() 출력

        # 메모리상에 올라와있는 목록에서 보내야하는 타겟을 기준으로 아래를 모두 추출
        if target != 0:
            for data in self._managed_feed_list[:-target]:
                #data()
                target_feed.append(data)
        else:
            for data in self._managed_feed_list:
                #data()
                target_feed.append(data)

        return target_feed

    def __set_send_feed(self, target_feed):
        result_key = -1
        # 남은 데이터 길이 보고 3개 보낼지 그 이하로 보낼지 생각해야함
        if len(target_feed) > 2:
            target_feed= target_feed[-3:]
            result_key = target_feed[0].key
        else:
            target_feed= target_feed[:len(target_feed)]
            result_key = target_feed[len(target_feed)-1].key

        target_fid = []
        for single_feed in target_feed:
            target_fid.append(single_feed.fid)
        feed_datas = self._database.get_datas_with_ids(target_id="fid", ids=target_fid)

        result = []
        for data in reversed(feed_datas):
            feed = Feed()
            feed.make_with_dict(data)
            result.append(feed)

        result_key = result_key - 1
        return result, result_key
    
    # 홈 화면에서 feed를 요청하는 상황
    def get_feed_in_home(self, user:User, key:int):
        target_feed = self.__make_target_feed(user=user, key=key)
        result, result_key = self.__set_send_feed(target_feed=target_feed)
        result = self.make_get_data(user, result)
        return result, result_key
    
    def __set_target_feed_with_fclass(self, target_feed:list, fclass:str):
        target = []

        for single_feed in target_feed:
            if single_feed.fclass == fclass:
                target.append(single_feed)
        return target

    # 위성 탐색에서 feed데이터를 요청하는 상황
    def get_feed_in_fclass(self, user:User, key:int, fclass:str):
        target_feed = self.__make_target_feed(user=user, key=key)
        target_feed = self.__set_target_feed_with_fclass(target_feed=target_feed, fclass=fclass)
        result, result_key = self.__set_send_feed(target_feed=target_feed)
        result = self.make_get_data(user, result)
        return result, result_key

    # get 요청에 대한 반환값 조사
    # 유저가 참여한 feed인지 확인할것
    def make_get_data(self, user:User, feeds:list):
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
            comment = self.__get_feed_comment(feed=feed)

            feed.attend = attend
            feed.comment = comment
            result.append(feed)
        return result
    
    def __get_feed_comment(self, feed:Feed):
        if len(feed.comment) == 0:
            comment = "아직 작성된 댓글이 없어요"
        else:
            comment = feed.comment[-1]
        return comment


    # feed 와 상호작용 -> 선택지를 선택하는 경우
    def get_feed_result(self, user:User, fid, action) -> Feed:
        fid_data = self._database.get_data_with_id(target="fid", id=fid)
        feed = Feed()
        feed.make_with_dict(fid_data)

        # 참여한 기록이 있는지 확인
        # 있으면 지우고, 결과값도 하나 줄여야됨
        target = -1
        for i, uids in enumerate(feed.attend):
            for uid in uids:
                if uid == user.uid:
                    uids.remove(uid)
                    target = i
                    break
        if target != -1:
            feed.result[target] -= 1

        # 이제 참여한 데이터를 세팅하고 저장하면됨
        feed.attend[action].append(user.uid)
        feed.result[action] += 1

        self._database.modify_data_with_id(target_id="fid",
                                            target_data=feed.get_dict_form_data())
        feed.attend = action
        feed.comment = self.__get_feed_comment(feed=feed)
        return feed


# 이건 뭐냐하면
# fclass 간의 유사도를 판별하여
# 전송하는 데이터에 추가적인 변화를 주려고 만듬
# 그냥 일종의 알고리즘 저장소 같은 개념
class FeedClassAnalist:
    def __init__(self):
        pass

class FeedClassManagement:
    def __init__(self):
        self.feedClass

        self._name_data = {
            "multiple" : "넷 중 하나",
            "station" : "정거장",
            "balance" : "둘 중 하나",
            "card" : "자랑"
        }
        
        self._


    def __get_class_name(self, fclass):
        return self._name_data[fclass]
    

class FeedClass:
    def __init__(self, fname, specific, ):
        self.name = fname
        self.specific = specific


class ManagedFeed:
    def __init__(self, key, fid ="", fclass="", category = []):
        self.key = key
        self.fid = fid
        self.fclass = fclass
        self.category  = []

    def __call__(self):
        print(f"key: {self.key} | fid: {self.fid} | fclass: {self.fclass} | category: {self.category}")

