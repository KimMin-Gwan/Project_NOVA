from others.data_domain import Feed, User
from model import Local_Database
from datetime import datetime
import string
import random

# 피드를 관리하는 장본인

class FeedManager:
    def __init__(self, database) -> None:
        self._database:Local_Database = database
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
    
    def get_feed_in_home(self, user, key:int):
        target_feed = []
        # 초기에는 -1로 올테니까 가장 최신으로
        if key == -1:
            key = self._num_feed
        else:
            key = key

        target = -1
        # 지지자의 요청이라면 유사한 내용으로 알고리즘
        if user == None:
            for i, single_feed in enumerate(reversed(self._managed_feed_list)):
                single_feed:ManagedFeed = single_feed
                if single_feed.key == key:
                    target = i
                    break

            tareget_feed = reversed(self._managed_feed_list[target:])

        # 일반 유저의 요청이라면 그냥 순서대로
        else:
            for i, single_feed in enumerate(reversed(self._managed_feed_list)):
                single_feed:ManagedFeed = single_feed
                if single_feed.key == key:
                    target = i
                    break

            target_feed = reversed(self._managed_feed_list[target:])

        # 남은 데이터 길이 보고 3개 보낼지 그 이하로 보낼지 생각해야함
        if len(target_feed) > 2:
            target_feed= target_feed[:3]
        else:
            target_feed= target_feed[:len(target_feed)]

        target_fid = []
        for single_feed in target_feed:
            target_fid.append(single_feed.fid)

        feed_datas = self._database.get_datas_with_ids(target_id="fid", ids=target_fid)

        result = []
        for data in feed_datas:
            feed = Feed()
            feed.make_with_dict(data)
            result.append(feed)

        result = self.make_get_data(user, result)
        return result

    def get_feed_in_fclass(self, user, key:int):
        for i, single_feed in enumerate(reversed(self._managed_feed_list)):
            single_feed:ManagedFeed = single_feed
            if single_feed.key == key:
                target = i
                break

        result = reversed(self._managed_feed_list[target:])

        if len(result) > 2:
            result = result[:3]
        else:
            result = result[:len(result)]


    # 유저가 참여한 feed인지 확인할것
    def make_get_data(self, user:User, feeds:list):
        result = []
        for feed in feeds:
            feed:Feed = feed

            # 검열된 feed면 생략
            if feed.state != "y":
                continue

            # 피드에 참여한 내역이 있는지 확인
            attend = -1
            for i, choice in enumerate(feed.attend):
                for uid in choice:
                    if uid == user.uid:
                        attend = i

            if len(feed.comment) != 0:
                comment = "아직 작성된 댓글이 없어요"
            else:
                comment = feed.comment[-1]

            feed.attend = attend
            feed.comment = comment
            result.append(feed)
        return result




# 이건 뭐냐하면
# fclass 간의 유사도를 판별하여
# 전송하는 데이터에 추가적인 변화를 주려고 만듬
# 그냥 일종의 알고리즘 저장소 같은 개념
class FeedClassAnalist:
    def __init__(self):
        pass



class ManagedFeed:
    def __init__(self, key, fid ="", fclass="", category = []):
        self.key = key
        self.fid = fid
        self.fclass = fclass
        self.category  = []


