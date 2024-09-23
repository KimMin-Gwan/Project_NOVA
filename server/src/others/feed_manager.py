from others.data_domain import Feed, User
from model import Local_Database
from datetime import datetime
import string
import random



# 피드를 관리하는 장본인


class FeedManager:
    def __init__(self, database, fclasses) -> None:
        self._feedClassManagement = FeedClassManagement(fclasses=fclasses)
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
    
    
    def __get_class_name(self, fclass):
        return self._feedClassManagement.__get_class_name(fclass=fclass)

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

    def get_feed_meta_data(self):
        return self._feedClassManagement.get_fclass_meta_data()

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
        # 제일 위에서 하나 뽑고, 다음꺼 하나 더뽑고
        # key에 맞는 feed 하나 더 뽑아서 넣어주기
        if user != "":
            result, result_key = self.short_feed_with_user(user=user,key=key, fclass=fclass)
        else:


        ##target_feed = self.__make_target_feed(user=user, key=key)
        ##target_feed = self.__set_target_feed_with_fclass(target_feed=target_feed, fclass=fclass)
        ##result, result_key = self.__set_send_feed(target_feed=target_feed)
        ##result = self.make_get_data(user, result)
        ## ------------- 신규 -------------------
        ## 유저가 로그인 했으면
        #if user.uid != "":
            #result_key = 
            #result=[]
            #index = 0
            #user = self._find_managed_user(self, user)
            #while len(result) > 2:
                #target_category = self.get_argo(user)
                #target, index = self.pick_single_feed_with_category(user=user, category=target_category, index=index)
                #result.append(target)
        ## 유저가 로그인 안했으면
        #else:
            #target_feed = self.__make_target_feed(user=user, key=key)
            #target_feed = self.__set_target_feed_with_fclass(target_feed=target_feed, fclass=fclass)
            #result, result_key = self.__set_send_feed(target_feed=target_feed)
            #result_key += 1

        #result = self.make_get_data(user, result)
        return result, result_key

    def short_feed(self, key, fclass):
        sample_feed = []
        # 제일 위에서 하나 뽑고, 다음꺼 하나 더뽑고
        # key에 맞는 feed 하나 더 뽑아서 넣어주기
        for i in range(2):
            present_feed= self.pick_single_feed_with_category(user=user, category=target_category)
            sample_feed.append(present_feed)

        if key != -1:
            prev_feed = self._get_single_feed(key=key)
            sample_feed.append(prev_feed)
        result_key = sample_feed[0].key
        result = self.__set_send_feed(target_feed=sample_feed)

        return result, result_key

    def short_feed_with_user(self, user, key, fclass):
        sample_feed = []
        # 제일 위에서 하나 뽑고, 다음꺼 하나 더뽑고
        # key에 맞는 feed 하나 더 뽑아서 넣어주기
        for i in range(2):
            target_category = self.get_argo(user)
            present_feed= self.pick_single_feed_with_category(user=user, category=target_category)
            sample_feed.append(present_feed)

        if key != -1:
            prev_feed = self._get_single_feed(key=key)
            sample_feed.append(prev_feed)
        result_key = sample_feed[0].key
        result = self.__set_send_feed(target_feed=sample_feed)

        return result, result_key


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


        target_feed=self._database.get_data_with_id(target="fid",id=fid)
        return target_feed

    def _get_single_feed(self, key = -1, fid = ""):
        target_feed = None
        if key != -1:
            for feed in self._managed_feed_list:
                if feed.key == key:
                    fid = feed.fid

        target_feed=self._database.get_data_with_id(target="fid",id=fid)
        return target_feed


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
    
    # 단일 피드 뽑기
    # 만약 추천순 같이 정렬이 바뀔 일이 있으면
    # 여기다가 매게변수로 정렬된 리스트를 주면됨
    #  아니면 걍 내부에서 소팅 돌링 별도의 리스트를 가지고 검색할것
    def pick_single_feed(self, user):
        target = None
        for managed_feed in self._managed_feed_list:
            managed_feed:ManagedFeed=managed_feed
            if managed_feed.fid in user.history:
                continue

    # 이건 카테고리에 있는 단일 피드 뽑는 함수
    # 뒤집기 어려워서 in range 이터레이터로 동작하고 - 붙혀서 뒤집음
    # 인덱스를 반환해서 검색하도록 구성함
    def pick_single_feed_with_category(self, user, category):
        target = None
        while True:
            for managed_feed in self._managed_feed_list:
                if managed_feed.fid in user.history:
                    continue
                target = managed_feed
            if category in target.category:
                break
        if target:
            user.history.append(target.fid)
        return target



# 이건 뭐냐하면
# fclass 간의 유사도를 판별하여
# 전송하는 데이터에 추가적인 변화를 주려고 만듬
# 그냥 일종의 알고리즘 저장소 같은 개념
class FeedClassAnalist:
    def __init__(self):
        pass

    def dice_argo(self, option):
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

    def __get_class_name(self, fclass):
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


class ManagedFeed:
    def __init__(self, key, fid ="", fclass="", category = []):
        self.key = key
        self.fid = fid
        self.fclass = fclass
        self.category  = []

    def __call__(self):
        print(f"key: {self.key} | fid: {self.fid} | fclass: {self.fclass} | category: {self.category}")


# 메모리에 올려서 관리할 유저
# 알고리즘에 따라 적절한 피드 제공에 목적을 둠
class ManagedUserTable:
    def __init__(self):
        self.__key = 0
        self._managed_user_list = []

    # 리스트 보여주기
    def __call__(self):
        for user in self._managed_user_list:
            user()

    # 세션 테이블에서 유저 찾기
    def find_user(self, user):
        for i, managed_user in enumerate(self._managed_user_list):
            if managed_user.uid == user.uid:
                return i
        return -1
    
    # 유저 데이터 반환
    def get_user_data(self, index):
        return self._managed_user_list[index]

    # 테이블에 유저 추가하기
    def add_user(self, user:User):
        new_user = ManagedUser(
            uid = user.uid
        )
        

# 유저 특화 시스템 구성을 위한 관리 유저
class ManagedUser:
    def __init__(self, uid):
        self.uid = uid
        self.option = []
        self.history = []
        self.TTL = 0

    def __call__(self):
        print(f"uid : {self.uid}")
        print(f"category : {self.category}")
        print(f"history : {self.history}")
        print(f"TTL : {self.TTL}")

