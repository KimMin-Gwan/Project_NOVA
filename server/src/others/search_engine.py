from email.policy import default
from time import sleep
import time
import asyncio
import pandas as pd
from bintrees import AVLTree
from copy import copy
from others.data_domain import Feed, User, Bias
from datetime import  datetime, timedelta
from pprint import pprint

# 검색엔진이 해야하는일

# 1. 키워드를 통한 피드 검색
# 2. 특정 피드 다음으로 제시할 피드 검색
# 3. 피드 분석 및 최신화
# 4. 추천 피드 제공

# 아래는 검색 엔진
class FeedSearchEngine:
    def __init__(self, database):
        self.__feed_algorithm= FeedAlgorithm(database=database)
        self.__search_manager = SearchManager(database=database, feed_algorithm=self.__feed_algorithm)

        self.__recommand_manager = RecommandManager(database=database,feed_algorithm=self.__feed_algorithm)
        self.__database=database

    def try_test_graph_recommnad_system(self, fid):
        feed = self.__database.get_data_with_id(target="fid", id=fid)
        #result = self.__feed_algorithm.find_recommend_feed(start_fid=feed.fid)
        result = "2"

        return result

    # 피드 매니저가 관리중인 피드를 보기 위해 만든 함수
    def try_search_managed_feed(self, fid):
        return self.__search_manager.try_search_managed_feed(fid=fid)
    
    # 새로운  관리 피드를 추가하는 함수
    def try_make_new_managed_feed(self, feed):
        # 알고리즘에도 추가해야되ㅏㅁ
        self.__search_manager.try_make_new_managed_feed(feed)
        self.try_add_feed(feed=feed)

        return

    # 이 함수가 핵심 -> feed 데이터를 요청하면 주기 위한 함수
    # target_type -> feed 검색을 하기 위한 key값
    # 조건 명 : (hasthtag -> 해시태그로 검색, fid -> fid로 검색, uname -> 작성자, string -> 본문)

    # target -> 검색 하는 key 데이터

    # num_feed -> 검색 결과에서 요구하는 피드 갯수

    # index - > 사용자가 이전에 받았던 피드들 중, 마지막 피드 값
    # 조건 : index가 -2 이라면 이전에 피드를 받은 적이 없거나 이전에 받은 피드 값을 무시한다는 의미

    # 예외 사항 : fid로 검색의 결과값은 반드시 1개 또는 0개
    # 예외 사항 : 아직은 string으로 검색 하지 않음

    # 예시 ||  [버튜버] 라는 해시 태그로 4개의 피드를 최초 요청
    # result , index = try_serach_feed(target_type="hashtag", target = "버튜버", num_feed=4, index=-2):

    # 예시 ||  [바위게] 라는 이름을 가진 작성자로 10개의 피드를 요청하는데 이번이 두번 째 요청
    # result , index = try_serach_feed(target_type="uname", target = "바위게", num_feed=10, index=240):
    def try_search_feed(self, target_type="default", target = "", num_feed=1, index=-2):

        result_fid = []
        result_index = -2

        # 해시태그로 검색한 피드 요청
        if target_type == "hashtag":   
            # 아래의 코드는 샘플이며 원하는 상태에 따라 다시 작성
            result_fid, result_index = self.__search_manager.search_feed_with_hashtag(hashtag=target, num_feed=num_feed, index=index)

        # fid로 검색한 피드 (피드 아이디)
        elif target_type == "fid":
            # 아래의 코드는 샘플이며 원하는 상태에 따라 다시 작성
            result_fid, result_index = self.__search_manager.search_feed_with_fid(fid=target, num_feed=num_feed, index=index)
        
        # uname으로 검색한 피드 (유저 이름)
        elif target_type == "uname":
            # 아래의 코드는 샘플이며 원하는 상태에 따라 다시 작성
            result_fid, result_index = self.__search_manager.search_feed_with_uname(uname=target, num_feed=num_feed, index=index)

        #elif target_type == "string":
            #result, key = self.__search_manager.search_feed_with_string(string=target, key=key)
        else:
            print("default 가 입력됨")
            pass
            
        return result_fid, result_index

    # search_type -> 검색하는 조건
    # 조건명 : (recent -> 단순한 최신순, today -> 24시간 이내 좋아요 순, weekly -> 168시간 이내 좋아요 순, like-> 단순 좋아요 순)

    # 예시 ||  홈 화면의 전체 게시글 파트에 보여줄, 전체 피드 중 가장 최신 피드에서 6개 요청
    # result , index = try_get_feed_in_recent(search_type ="recent", num_feed= 6, index=-2):

    # 예시 || 홈 화면의 오늘의 인기 게시글 파트에 보여줄, 지금 기준 24 시간 이내에 작성된 피드 중 좋아요 30개를 넘은 피드
    # result , index = try_get_feed_in_recent(search_type ="today", num_feed= 6, index=-2):

    # 예시 || 주간 Top100 페이지에서 사용자가 스크롤을 내려 주간 탑 100의 두번째 요청을 넣음
    # result , index = try_get_feed_in_recent(search_type ="weekly", num_feed= 10, index=320):

    def try_get_feed_in_recent(self, search_type="recent", num_feed=1, index=-1):
        result_fid = []
        result_index = -2

        # 여기서 조건에 따른 검색을 해야함
        
        # 차라리 여기서 타임 스탬프를 받아가는건 어떨까?

        # 1. 단순히 최신순 검색 ( 모든 피드 보기 기능 )
        if search_type == "recent":
            # 아래의 코드는 샘플이며 원하는 상태에 따라 다시 작성
            result_fid, result_index = self.__search_manager.try_get_feed_with_target_hour(
                search_type="all", num_feed=num_feed, target_hour=-1, index=index)

        # 2. 24시간 이내에 좋아요가 30개 이상인 피드 ( 오늘의 인기 게시글 기능 )
        elif search_type == "today":
            # 아래의 코드는 샘플이며 원하는 상태에 따라 다시 작성
            result_fid, result_index = self.__search_manager.try_get_feed_with_target_hour(
                search_type="best", num_feed=num_feed, target_hour=24, index=index)

        # 3. 168시간 이내에 좋아요 순 ( 주간 Top 100 기능 )
        elif search_type == "weekly":
            # 아래의 코드는 샘플이며 원하는 상태에 따라 다시 작성
            result_fid, result_index = self.__search_manager.try_get_feed_with_target_hour(
                search_type="best", num_feed=num_feed, target_hour=168, index=index)

        # 4. 좋아요가 30개 이상인 피드들을 최신순으로 나열 ( 베스트 피드  기능)
        elif search_type == "like":
            # 아래의 코드는 샘플이며 원하는 상태에 따라 다시 작성
            result_fid, result_index = self.__search_manager.try_get_feed_with_target_hour(
                search_type="best", num_feed=num_feed, target_hour=-1, index=index)

        return result_fid, result_index

    # 여기도 아직 하지 말것 
    # 목적 : 숏피드에서 다음 피드 제공 받기
    def try_recommand_feed(self, fid:str, history:list):
        fid = self.__recommand_manager.get_recommand_feed(fid=fid, history=history)
        return fid
    # ------------------------------------------------------------------------------------
    def get_best_hashtag(self, num_hashtag=10):
        return self.__recommand_manager.get_best_hashtags(num_hashtag=num_hashtag)

    def get_recommnad_hashtag(self, bid:str):
        return self.__recommand_manager.get_user_recommand_hashtags(bid=bid)


    # ----------------------------------------------------------------------------------------------------------
    # feed algorithm 테스트용
    #

    # 1. 그래프 호출
    # 2. 노드 얻기
    # 3. 유저 노드 추가
    # 4. Feed 노드 추가 (Hash까지 추가)
    # 5. 유저 지우기
    # 6. Feed 지우기
    # 7. Feed 좋아요 누르기
    # 8. Feed 좋아요 헤제하기

    def try_graph_call(self):
        print(self.__feed_algorithm)

    def try_get_user_node_call(self):
        pprint(self.__feed_algorithm.get_user_nodes())

    def try_get_feed_node_call(self):
        pprint(self.__feed_algorithm.get_feed_nodes())

    def try_get_hash_node_call(self):
        pprint(self.__feed_algorithm.get_hash_nodes())

    def try_add_user(self, user:User):
        # 받은 유저 추가
        result = self.__feed_algorithm.add_user_node(user)

        if result:
            return True
        return False

    def try_remove_user(self, uid):
        result = self.__feed_algorithm.remove_user_node(uid)

        if result:
            return True
        return False

    def try_add_feed(self, feed:Feed):
        result = self.__feed_algorithm.add_feed_node(feed)

        return result

    def try_remove_feed(self, fid):
        result = self.__feed_algorithm.remove_feed_node(fid)
        return result

    def try_like_feed(self, fid, uid, like_time):
        result = self.__feed_algorithm.connect_feed_like_user(fid=fid, uid=uid, like_time=like_time)
        return result

    def try_dislike_feed(self, fid, uid):
        result = self.__feed_algorithm.disconnect_feed_like_user(fid=fid, uid=uid)
        return result

    def try_modify_hash(self, fid, new_hashtags):
        return
    # ------------------------------------------------------------------------------------------------------------


"""
case 1) 첫 page에서 HASH TAG로 좋아요 순으로 보여줘야함
    -get_all_feed() 모든 피드를 가져오고
    -
    -NUM_OF_FEED 갯수만큼 return 해야함
    -이때 날짜는 1주일 1달 3달 6달 1년 2년 .....첫날짜 까지 계속해서 늘려감
    -
"""



"""
상세
FeedSearchEngine은 인터페이스이다. 이제 인터페이스로 부터 연산을 수행할 로직이 필요하다
SearchManager는 그 연산을 수행하는 로직이다.

SearchManager는 조건에 맞는 피드를 검색할 수 있으면 된다.
예를 들어 FeedSearchEngine을 통해 이번 주 Top 100의 피드중 가장 첫번째를 요청하면
그 요청에 따라 피드 테이블에서 조건에 맞는 피드들 찾고
그 피드들과 마지막 피드의 index를 반환하면
모든 절차는 끝난다.

다시 수도 코드로 작성하자면

1. FeedSearchEngine으로 부터 요청이 들어옴
2. 요청에 따라 SearchManager의 적절한 함수가 실행됨
3. 클래스 내부 함수에서 연산을 통해 적절한 MaanagedFeed들을 list 형태로 추출함
4. 추출한 MangedFeed 리스트의 마지막 Feed의 인덱스를 테이블에서 추출함
5. 추출한 ManagedFeed리스트와 인덱스를 반환함
6. FeedSearchEngine은 반환받은 데이터를 확인하여 반환함
7. 모든 절차 완료

수도코드의 6번을 보면 FeedSearchEngind은 반환 받은 데이터를 확인하여 반환한다고 되어 있는데
이 확인 과정은 FeedSearchEngine에 있거나 FeedManager 안에 있거나 한번만 있으면 됨
그러나 좀더 클린한 코드 작성을 위해 FeedSearchEngine에 있는 것이 더욱 적절함

모든 코드는 마음대로 뜯고 고치고 해도 상관 없음
그러나 반드시 주의해야 할 것은 FeedSearchEngine에 있는 인터페이스로
인터페이스 함수들의 반환 값과 매게변수는 변해선 안된다.

즉, 인터페이스 함수들을 제외한 모든 코드는 변경  가능하다.
(본 파일이 커밋 되는 시점에서는 인터페이스 함수는 41번째 줄과 81번째 줄에 있는 함수를 의미한다.)

SearchManager를 설계할 때 추천하는 방법은
FeedSearchEngine의 인터페이스가 요구하는 요청 값의 공통점을 찾아 하나의 함수로 묶는 것이다.
이것은 클린 코드를 작성하는 기초적인 방법으로, 공통점을 가진 코드를 하나로 묶어 함수로 만드는 것이다.

요구하는 요청값은 인터페이스 함수(41번째줄과 81번째줄의 함수)주변에 주석으로 작성되어 있으며
이해가 되지 않는 부분은 주석으로 작성하지 말고 직접 연락하여 물어볼 것 (안되는걸 주석으로 적으면 코드를 이해하기 어려워짐)

"""

# 이건 아래에 피드 테이블에 들어가야되는 피드 자료형
# 데이터 베이스에서 피드 데이터 받아서 만들꺼임
# 필요한 데이터는 언제든 추가가능

# 이게 검색에 따른 피드를 제공하는 클래스
# 위에 FeedAlgorithm에서 작성한 내용을 가지고 와도됨

# 클래스 목적 : 피드를 검색하거나, 조건에 맞는 피드를 제공하기 위함

class ManagedFeed:
    def __init__(self, fid="", like=0, date=None, uname="", hashtag=[]):
        self.fid=fid
        self.like=like
        self.date=date
        self.uname = uname
        self.hashtag = hashtag

    # 무슨 데이터인지 출력해보기
    def __call__(self):
        print("fid : ", self.fid)
        print("like : ", self.like)
        print("date: ", self.date)
        print("uname: ", self.uname)
        print("hashtag: ", self.hashtag)

 
# LocalDatabase의 import 문제로 아래 코드는 정상동작 하지 않으니
# 코드를 작성하는 도중에는 주석을 해제하여 LocalDatabase 함수를 자동완성하고
# 실행할때는 다시 주석처리하여 사용할것
#from model import Local_Database

class SearchManager:
    # LocalDatabase의 import 문제로 아래 코드는 정상동작 하지 않으니
    # 코드를 작성하는 도중에는 주석을 해제하여 LocalDatabase 함수를 자동완성하고
    # 실행할때는 다시 주석처리하여 사용할것
    #def __init__(self, database:Local_Database, feed_algorithm : FeedAlgorithm):
    def __init__(self, database, feed_algorithm=None):
        self.__database = database
        self.__feed_algorithm=feed_algorithm
    
        self.__feed_table = [] # 최신 기준으로 쌓이는 피드 스택 | 인덱스를 활용할 것
        self.__feed_avltree = AVLTree()

        # best_feed_table이 필요한가? 필요없는거 같은데?
        self.__best_feed_table = [] # 좋아요가 30개 이상인 피드 테이블 | 최신 기준 

        # 테이블 초기화
        self.__init_feed_table(database=database)
        self.__init_feed_avltree()

    def __init_feed_avltree(self):
        for feed in self.__feed_table:
            self.__feed_avltree.insert(feed.fid, feed)
        print(f'INFO<-[      NOVA FEED AVLTREE IN SEARCH ENGINE NOW READY.')

    # 테이블 초기화 함수
    def __init_feed_table(self, database):
        feeds = []
        # 먼저 피드 데이터를 DB에서 불러오고
        feed_datas = database.get_all_data(target="fid")

        # 불러온 피드들은 객체화 시켜준다음 잠시 보관
        for feed_data in feed_datas:
            feed = Feed()
            feed.make_with_dict(dict_data=feed_data)
            feeds.append(feed)

        # 잠시 보관한 피드 데이터에서 필요한 정보만 뽑아서 ManagedFeed 객체 생성
        for single_feed in feeds:
            managed_feed = ManagedFeed(fid=single_feed.fid,
                                        like=single_feed.star,
                                        date=self.__get_date_str_to_object(single_feed.date),
                                        hashtag=copy(single_feed.hashtag),
                                        uname=single_feed.nickname
                                        )
            # 보관
            self.__feed_table.append(managed_feed)

        # 리턴되면 위에서 잠시 보관한 피드 데이터는 사라지고 self.__feed_table에 ManagedFeed들만 남음

        self.__feed_table = sorted(self.__feed_table, key=lambda x:x.date, reverse=False)

        num_feed = str(len(self.__feed_table))
        print(f'INFO<-[      {num_feed} NOVA FEED IN SEARCH ENGINE NOW READY.')
        return 
    
    def try_make_new_managed_feed(self, feed:Feed):
        managed_feed = ManagedFeed(
            fid=feed.fid,
            like=feed.star,
            date=feed.date,
            uname=feed.nickname,
            hashtag=feed.hashtag)

        self.__feed_table.append(managed_feed)
        self.__feed_avltree.insert(managed_feed.fid, managed_feed)
        return

    # 피드 매니저에서 사용가능하게 만든 검색 기능
    def try_search_managed_feed(self, fid):
        target = self.__feed_avltree.get(key=fid)
        return target

    # 이런 함수를 미리 만들어서 쓰면 좋음
    # 아래는 예시 

    # 예시 1 | 특정 인덱스의 피드를 뽑아오기
    def __get_feed_data_in_index(self, index):
        return self.__feed_table[index]

    # 예시 2 | 특정 인덱스 아래의 피드를 모두 뽑아오기
    def __get_feed_from_index_to_everything(self, index):
        return self.__feed_table[:index]


    # 피드 테이블을 수정하는 함수
    def modify_feed_table(self, feed:Feed, ):
        # managed_feed를 찾아야됨
        managed_feed:ManagedFeed = self.__feed_avltree.get(feed.fid)

        # managed_feed가 가진 데이터로 원본 데이터를 변경
        managed_feed.date = feed.date
        managed_feed.hashtag = feed.hashtag
        managed_feed.like = feed.star
        managed_feed.uname = feed.nickname
        return
    
    # 삭제하는 함수. 피드가  삭제되면 None으로 바뀔것
    def remove_feed(self, feed:Feed):
        managed_feed = self.__feed_avltree.get(key=feed.fid)
        managed_feed = ManagedFeed()
        self.__feed_avltree.remove(key=feed.fid)
        return
    
    def __get_datetime_now(self):
        now = datetime.now()
        return now

    # string to datetime
    def __get_date_str_to_object(self, str_date):
        date_obj = datetime.strptime(str_date, "%Y/%m/%d-%H:%M:%S")
        return date_obj

    # datetime to string
    def __get_date_object_to_str(self, object:datetime):
        formatted_str = object.strftime("%Y/%m/%d-%H:%M:%S")
        return formatted_str

    # 시간 차이를 분석하는 함수
    # target_hour : 1, 24, 168
    def __get_time_diff(self, target_time, reference_time=datetime.now(),
                       target_hour=2) -> bool:
        time_diff = abs(target_time - reference_time)

        # 차이가 2시간 이상인지 확인
        return time_diff >= timedelta(hours=target_hour)

    # 시간 차이를 바탕으로 정해진 시간대 내의 피드 정보 구하기
    # target_hour : 1, 24, 168
    def __find_target_index(self, target_hour=1):
        target_index = len(self.__feed_table)


        for i, managed_feed in enumerate(self.__feed_table):
            # 삭제된 피드는 None으로 표시될것이라서
            if managed_feed.fid == "":
                continue

            if self.__get_time_diff(target_time=managed_feed.date, target_hour=target_hour):
                continue
            else:
                target_index = i
                break

        return target_index

    # 목표시간을 바탕으로 피드를 찾느 ㄴ함수
    # search_type == "all", "best"
    def try_get_feed_with_target_hour(self, search_type="all", num_feed=4, target_hour=1, index=-2):
        result_fid = []
        result_index = -3

        if index == -1 or index == -2:
            index = len(self.__feed_table)

        if target_hour > 0 :
            target_index = self.__find_target_index(target_hour=target_hour)
        else:
            target_index = 0

        search_range = self.__feed_table[target_index:index][::-1]

        if index < target_index  or index > len(self.__feed_table):
            return result_fid, -3


        count = 0

        if search_type == "all":
            for i, managed_feed in enumerate(search_range):
                if count == num_feed:
                    break
                
                # 삭제된 피드는 None으로 표시될것이라서
                if managed_feed.fid == "":
                    continue

                result_fid.append(managed_feed.fid)
                # result_index 업데이트
                result_index = index - 1 - i # 실제 self.__feed_table에서의 인덱스 계산
                count += 1


        elif search_type == "best":
            #print("monitor --------------------------------------------------------------")
            #for i, feed_data in enumerate(self.__feed_table):
                #print(f"index : {i}  | date : {feed_data.date} | hashtag : {feed_data.hashtag}")
            #print("monitor --------------------------------------------------------------")

            for i, managed_feed in enumerate(search_range):
                if count == num_feed:
                    break

                # 삭제된 피드는 None으로 표시될것이라서
                if managed_feed.fid == "":
                    continue
                
                if managed_feed.like < 30:
                    continue

                result_fid.append(managed_feed.fid)
                # result_index 업데이트
                result_index = index - 1 - i # 실제 self.__feed_table에서의 인덱스 계산
                count += 1

        return result_fid, result_index
    
    #type likes, time
    def search_feed_with_hashtag(self, hashtag, num_feed=10, index=-1) -> list:
        result_fid = []
        result_index = -3

        if index == -1:
            index = len(self.__feed_table)

        search_range = self.__feed_table[:index][::-1]

        if index < 0 or index > len(self.__feed_table):
            return result_fid, -3

        count = 0

        for i, managed_feed in enumerate(search_range):
            #ii = len(self.__feed_table) - 1 - i
            if count == num_feed:
                break

            # 삭제된 피드는 None으로 표시될것이라서
            if managed_feed.fid == "":
                continue

            if hashtag not in managed_feed.hashtag:
                continue

            result_fid.append(managed_feed.fid)

            # result_index 업데이트
            result_index = index - 1 - i  # 실제 self.__feed_table에서의 인덱스 계산
            count += 1

        return result_fid, result_index


    def search_feed_with_fid(self, fid, num_feed=1, index=-1) -> list:
        result_fid = []
        index = -1
        for i, managed_feed in enumerate(self.__feed_table):
            #index = len(self.__feed_table) - 1 - i
            if managed_feed.fid == fid:
                result_fid.append(managed_feed.fid)
                index = i
                break

        return  result_fid, index

    def search_feed_with_uname(self, uname, num_feed=1, index=-1) -> list:
        result_fid = []
        result_index = -3

        if index == -1:
            index = len(self.__feed_table)

        search_range = self.__feed_table[:index][::-1]

        if index < 0 or index > len(self.__feed_table):
            return result_fid, -3

        count = 0

        for i, managed_feed in enumerate(search_range):

            if count == num_feed:
                break

            # 삭제된 피드는 None으로 표시될것이라서
            if managed_feed.fid == "":
                continue

            if uname != managed_feed.uname:
                continue

            result_fid.append(managed_feed.fid)

            # result_index 업데이트
            result_index = index - 1 - i  # 실제 self.__feed_table에서의 인덱스 계산
            count += 1

        return result_fid, result_index

    #def search_feed_with_string(self, string, num_feed=10) -> list:   #본문 내용을 가지고 찾는거같음
        #return self.__feed_algorithm.get_feed_with_string(string,num_feed)
    
# --------------------------------------------------------------------------------------------

class ManagedBias:
    def __init__(self, bid, user_nodes):
        self.bid = bid
        self.trand_hashtags = []
        self.user_nodes = user_nodes


# 이건 사용자에게 맞는 데이터를 주려고 만든거

class RecommandManager:
    def __init__(self, database, feed_algorithm):
        self.__database = database
        self.__feed_algorithm:FeedAlgorithm = feed_algorithm
        self.__bias_avltree = AVLTree()
        self.__init__bias_avltree()
        self.hashtags = []
        self.loop =asyncio.get_event_loop()
        self.loop.create_task(self.__check_trend_hashtag())

    def __init__bias_avltree(self):
        biases = []
        users = []
        bias_datas = self.__database.get_all_data(target="bid")
        user_datas = self.__database.get_all_data(target="uid")

        for bias_data in bias_datas:
            bias = Bias()
            bias.make_with_dict(bias_data)
            biases.append(bias)

        for user_data in user_datas:
            user = User()
            user.make_with_dict(user_data)
            users.append(user)

        for single_bias in biases:
            user_nodes = []
            for single_user in users:
                single_user:User = single_user
                # bias를 팔로우하는 유저를 찾아서 노드 연결해야됨
                if single_user.solo_bid == single_bias.bid or single_user.group_bid == single_bias.bid:
                    user_node = self.__feed_algorithm.get_user_node_with_uid(uid=single_user.uid)
                    # 못찾으면 예외처리할것
                    if user_node:
                        user_nodes.append(user_node)

            # 이제 관리될 바이어스를 만들고 연결한다음
            managed_bias = ManagedBias(bid=single_bias.bid, user_nodes=user_nodes)
            # avl트리에 넣어주면됨
            self.__bias_avltree.insert(key=single_bias.bid, value=managed_bias)


    # 실시간 트랜드 해시태그 제공
    def get_best_hashtags(self, num_hashtag=10) -> list:
        return self.hashtags[0:num_hashtag]

    # 사용자에게 어울릴만한 해시태그 리스트 제공
    def get_user_recommand_hashtags(self, bid):
        result = []
        managed_bias:ManagedBias = self.__bias_avltree.get(key=bid)
        print(managed_bias)
        print(managed_bias.trand_hashtags)

        for hashtag in managed_bias.trend_hashtags:
            result.append(hashtag.hid)
        return result
    
    def get_recommand_feed(self, fid:str, history:list):
        fid = self.__feed_algorithm.recommend_next_feed(start_fid=fid, history=history)
        return  fid


    def __check_trend_hashtag_algo(self, weight=0, now_data=0, prev_data=0, num_feed=0):
        next_weight = weight + ((now_data - prev_data) / (num_feed ** 0.5)) * 0.9

        # 새로운 정규화: 상한선 기반 축소 (threshold=0.5, reduction factor=0.1)
        # signoid 함수
        threshold = 0.5
        if next_weight > threshold:
            next_weight = threshold + (next_weight - threshold) * 0.1

        return max(next_weight, 0)
    
    def __total_hashtag_setting(self):
        hashtag_rank = []
        hashtag_nodes = self.__feed_algorithm.get_hash_nodes()
        for hashtag_node in hashtag_nodes:
            hashtag_node: HashNode = hashtag_node

            new_weight = self.__check_trend_hashtag_algo(
                weight=hashtag_node.weight,
                now_data=hashtag_node.trend["now"],
                prev_data=hashtag_node.trend["prev"],
                num_feed=len(hashtag_node.edges["feed"]))

            # 안에 값을 최신화
            hashtag_node.weight = new_weight
            hashtag_node.trend["prev"] = hashtag_node.trend["now"]
            hashtag_node.trend["now"] = 0

            hashtag_rank.append(hashtag_node)

        count = 0
        hashtag_rank = sorted(hashtag_rank, key=lambda x:x.weight, reverse=False)

        for hash_node in hashtag_rank:
            if count == 10:
                break
            self.hashtags.append(hash_node.hid)
            count += 1

    def __bais_hashtag_setting(self):
        managed_bias_list = list(self.__bias_avltree.values())
        for managed_bias in managed_bias_list:
            hash_nodes = []

            managed_bias:ManagedBias = managed_bias

            # 대충 그래프 타고 들어가서 해시태그 전부다 찾아내는 함수
            for user_node in managed_bias.user_nodes:
                for user_edge in user_node.edges:
                    feed_node:FeedNode = user_edge.target_node
                    for feed_edge in feed_node.edges:
                        hash_node:HashNode = feed_edge.target_node
                        hash_nodes.append(hash_node)

            hash_nodes = sorted(hash_nodes, key=lambda x:x.weight, reverse=False)
            managed_bias.trand_hashtags = hash_node[:4]

    async def __check_trend_hashtag(self):
        while True:
            # time_diff 계산
            time_diff = 1

            # 만약 마지막으로 연산한지 1시간이 지났으며 다시 연산
            if time_diff > 1:
                self.__total_hashtag_setting()
                self.__bais_hashtag_setting()
                self.last_computed_time = current_time
            # 시간 간격이 1시간 미만인 경우
            else:
                await asyncio.sleep(10)  # 너무 자주 루프를 돌지 않도록 대기

            current_time = time.time()
            if hasattr(self, 'last_computed_time'):
                time_diff = (current_time - self.last_computed_time) / 3600  # 시간 단위로 계산
            else:
                self.last_computed_time = current_time
                time_diff = 0

                
# --------------------------------------------------------------------------------------------

# Edge 수도코드
# class Edge
#   __init__(target_node, gen_time:datetime):
#       self.target_node = target_node
#       self.get_time = gen_time        # 생성된 시간
#
#   equal(other) 오버로딩
#       조건: target_node와 Edge안에 있는 Target_node가 일치하는지 확인
#   sorted(other)
#       조건: generated time이 가장 최신순인 것이 먼저 오도록 하게 함
#           이 때, 값비교 시 timedelta값이 더 큰 쪽이 최신의 것이 됨.
#   weight():
#       시간차를 계산하는 함수
#   __calculate_timestamp():
#       current_time = datetime.now()
#       gen_time = datetime 객체로 만들어진 gen_time_str
#       return (current_time - gen_time).total_second()
#
#   get_target_node():
#       return target_node
#

# 노드 엣지 클래스
class Edge:
    def __init__(self, target_node, gen_time):
        self.target_node = target_node # 타겟 노드 저장
        self.gen_time:datetime = gen_time # 엣지의 생성 시간

        # 이 엣지는 Feed-User 의 경우, 좋아요(star)를 누른 시간, Feed를 작성한 시간을 가지게 됨
        # Feed-Hashtag 의 경우, Feed 생성 시간을 이어 받게됨.

    # 동일한 엣지인지 서로 비교 해야함.
    # 만약 향하는 노드가 같다면
    def __eq__(self, other):
        return self.target_node == other.target_node

    # 날짜가 더 최신의 edge 순으로 정렬
    def __lt__(self, other):
        return self.gen_time > other.gen_time

    # 출력 포맷
    def __str__(self):
        return 'Edge({}, {})'.format(self.target_node.get_id(), self.gen_time)

    # edge 리스트 출력 포맷
    def __repr__(self):
        return 'Edge({}, {})'.format(self.target_node.get_id(), self.gen_time)

    # 내부함수로 구현함. 초 단위로 계산함
    def weight(self):
        return self.__calculate_timestamp()

    # 향하고 있는 타겟 노드 얻기
    def get_target_node(self):
        return self.target_node

    # 내부 함수로 정의된 가중치 부여 함수 (매업데이트 되는것보다 제때 구하는 걸로)
    def __calculate_timestamp(self):
        # 왜인지는 모르겠지만, 현재 시간을 포맷에 맞게 변환하는데, datetime → str → datetime으로 변환해야 함.
        current_time_str = datetime.now().strftime("%Y/%m/%d-%H:%M:%S")
        current_time = datetime.strptime(current_time_str, "%Y/%m/%d-%H:%M:%S")

        # datetime 연산 시 timedelta값 반환
        time_difference = current_time - self.gen_time
        return time_difference.total_seconds() # timedelta 값을 초 단위로 변환하여 제공

# BaseNode 수도코드
# class BaseNoe
#     initalize_varialbes
#           edges = {}      # 필요한 엣지를 담음
#           node_type 노드 타입 : 노드의 타입을 정의함. 엣지를 담을 때, 공통된 노드만을 담게하기 위해서 넣음
#
#   공통된 함수들 중, 추가, 삭제, 엣지 찾기를 내부함수로 구현
#     1. __add_edge(target_node, gen_time):
#         node_type = target_node.node_type
#         edge = Edge(target_node, gen_time)  # 엣지 생성
#         edges[node_type].append(edge)
#
#     2. __remove_edge(target_node):
#         node_type = target_node.node_type
#
#         # 엣지를 찾아냄
#         for edge in self.edges[node_type]:
#             if target_node == edge.get_target_node():
#                 self.edges[node_type] = self.edges[node_type](without this edge)
#                 return
#
#     3. get_edges():
#         edge_list = []
#         for node_type in edges.keys()
#             edge_list = edge_list + edges.edges[node_type]
#         return edge_list
#
# Graph 베이스 노드 클래스
class BaseNode:
    def __init__(self, node_type):
        self.edges = {}     # 엣지 해시 테이블
        self.node_type = node_type  # 노드 타입  -> 중요함. 이게 엣지를 담는 위치를 정해준다

    # Edge 추가 함수
    # node_type 필요 함. (protected)
    def _add_edge(self,  target_node, gen_time):
        node_type = target_node.node_type
        # 엣지를 담는 곳이 잘못 되었다면 False 를 반환
        # 상속받은 클래스에서 Edge 키를 정의 했기에 가능함
        if node_type not in self.edges:
            return False

        edge = Edge(target_node=target_node, gen_time=gen_time)            # 엣지 생성
        # 엣지가 존재하는 것만으로 판단하여 생성할 것인지 아닌지를 판단
        if edge not in self.edges[node_type]:
            self.edges[node_type].append(edge)                                 # 엣지 담기
            return True
        return False

    # Edge 제거 함수 (protected)
    def _remove_edge(self,  target_node):
        # 리스트 컴프리헨션으로 작성하여, 조금 더 빠른 반복문 실행으로 만들었음
        # 실상 성능의 차이는 좀 적긴하다.
        node_type = target_node.node_type
        # 엣지를 담은 장소가 잘못되어있다면 바로 턴
        if node_type not in self.edges:
            return False

        # 엣지 찾기
        for edge in self.edges[node_type]:
            if target_node == edge.get_target_node():
                self.edges[node_type].remove(edge)
                # self.edges[node_type] = [edge_2 for edge_2 in self.edges[node_type] if edge_2.get_target_node() == target_node]
                return True
        return False

    # 오버라이딩 용
    def get_id(self):
        pass

    def get_edges(self):
        edge_list = []
        for node_type in self.edges.keys():
            edge_list = edge_list + self.edges[node_type]
        return edge_list

    # # 이웃한 노드의 엣지 찾기
    # def __find_edge(self, target_node):
    #     node_type = target_node.node_type
    #     # 엣지를 담은 곳이 잘못되어있음.
    #     if node_type not in self.edges:
    #         return None
    #
    #     for edge in self.edges[node_type]:
    #         if target_node == edge.get_target_node():
    #             return edge
    #     return None
    #


    # 노드 삭제 시. edge까지 전부 삭제
    def __del__(self):
        self.edges.clear()

# class UserNode
#     1. initialize_variables(uid)
#         super().__init__()
#         uid = uid
#         edges["feed"] = []  # 노드 타입에 대한 엣지리스트를 정의
#
#     2. 아이디 얻기
#         # 다른 하위 클래스에서도 똑같은 함수를 만들어 둚.
#         return uid
#
#     3. 엣지 추가 add_edge (내부 함수로 동작)
#         return self.__add_edge(target_node, gen_time)
#
#     4. 엣지 삭제 remove_edge (내부 함수로 동작)
#         return self.__remove_edge(target_node)

# 유저 노드
class UserNode(BaseNode):
    def __init__(self, uid):
        super().__init__("user")
        self.uid = uid
        self.edges["feed"] = [] # 엣지 리스트를 따로 생성한다. 중요하다

    # 노드의 일치성 판단. 이는 기록된 id를 가지고 판단
    def __eq__(self, other):
        return self.uid == other.get_id()

    # 노드 출력 포맷
    def __str__(self):
        return 'Node({}, {})'.format(self.get_id(), self.node_type)

    # 리스트 전체 출력 포맷
    def __repr__(self):
        return 'Node({}, {})'.format(self.get_id(), self.node_type)

    # 유저 아이디 얻기
    def get_id(self):
        return self.uid

    # 엣지 추가
    def add_edge(self, target_node, gen_time:datetime):
        # 이 작업이 True, False를 반환 하기에 이렇게 함.
        return self._add_edge(target_node, gen_time)

    # 엣지 삭제, 이 작업은 나의 엣지만 없애는 작업. 상대노드꺼는 그래프에서 작업
    def remove_edge(self, target_node):
        # 노드 타입이 Feed 일 때만 수행
        return self._remove_edge(target_node)

# class HashNode
#     1. initialize_variables(hid)
#         super().__init__()
#         hid = hid
#         edges["feed"] = []  #  노드 타입에 대한 엣지리스트를 정의
#
#     2. 아이디 얻기
#         # 다른 하위 클래스에서도 똑같은 함수를 만들어 둚.
#         return hid
#
#     3. 엣지 추가 add_edge (내부 함수로 동작)
#         return self.__add_edge(target_node, gen_time)
#
#     4. 엣지 삭제 remove_edge (내부 함수로 동작)
#         return self.__remove_edge(target_node)

# 해시태그 노드
class HashNode(BaseNode):
    def __init__(self, hid):
        super().__init__("hashtag")
        self.hid = hid          # 해시태그 아이디, 문자열이 된다.
        self.edges["feed"] = []
        self.weight = 0
        self.trend= {
            "now":0,
            "prev":0
        }

    # 노드 일치성 판단. 기록된 id를 통해 판단
    def __eq__(self, other):
        return self.hid == other.get_id()

    # 노드 출력 포맷
    def __str__(self):
        return 'Node({}, {})'.format(self.get_id(), self.node_type)

    # 리스트 전체 출력 포맷
    def __repr__(self):
        return 'Node({}, {})'.format(self.get_id(), self.node_type)

    # 아이디 반환 함수
    def get_id(self):
        return self.hid

    # 엣지 추가
    def add_edge(self, target_node, gen_time:datetime):
        return self._add_edge(target_node, gen_time) # 엣지 추가

    # 엣지 삭제, 이 작업은 나의 엣지만 없애는 작업. 상대노드꺼는 그래프에서 작업
    def remove_edge(self, target_node):
        return self._remove_edge(target_node)

# class FeedNode
#     1. initialize_variables(fid)
#         super().__init__()
#         fid = fid
#         edges["user"] = []  #  노드 타입에 대한 엣지리스트를 정의
#         edges["hashtag"] = []
#
#     2. 아이디 얻기
#         # 다른 하위 클래스에서도 똑같은 함수를 만들어 둚.
#         return fid
#
#     3. 엣지 추가 add_edge (내부 함수로 동작)
#         return self.__add_edge(target_node, gen_time_str)
#
#     4. 엣지 삭제 remove_edge (내부 함수로 동작)
#         return self.__remove_edge(target_node)

# 피드 노드
class FeedNode(BaseNode):
    def __init__(self, fid):
        super().__init__("feed") # 상속
        self.fid = fid          # Feed id
        self.edges["user"] = []
        self.edges["hashtag"] = []

    # 노드 일치 비교
    def __eq__(self, other):
        return self.fid == other.get_id()

    # 노드 출력 포맷
    def __str__(self):
        return 'Node({}, {})'.format(self.get_id(), self.node_type)

    # 리스트 전체 출력 포맷
    def __repr__(self):
        return 'Node({}, {})'.format(self.get_id(), self.node_type)

    # 노드 아이디 얻기
    def get_id(self):
        return self.fid

    # 엣지 추가
    def add_edge(self, target_node, gen_time:datetime):
        result = self._add_edge(target_node, gen_time)
        return result

    # 엣지 삭제
    def remove_edge(self, target_node):
        result = self._remove_edge(target_node)
        return result

# class FeedChaosGraph
#     1. initalize_variables
#
#     2. Call 함수 정의
#         all_node_feeds = self.num_feed_nodes + self.num_user_nodes + self.num_hash_nodes
#         pprint(f'INFO<-[    {all_node_feeds} NOVA Graph IN SEARCH ENGINE NOW READY')
#         pprint(f'           {self.num_feed_nodes} feed nodes,')
#         pprint(f'           {self.num_user_nodes} user nodes,')
#         pprint(f'           {self.num_hash_nodes} hash nodes,')
#
#     3. 노드 존재 여부 확인(node_id, tree)
#         return booltype if tree.get(id)
#
#     4. 엣지 찾기(source, target) (내부 함수)
#         edge_list = source.get_edges()
#         for edge in edge_list:
#             edge.target_node == target:
#                 return True
#         return False
#
#     5. add_edge(source, target, date) (내부 함수)
#         source.add_edge(target, date)
#         target.add_edge(source, date)
#
#     6. remove_edge(source, target) (내부 함수)
#         source.remove_edge(target)
#         target.remove_edge(source)
#
#     7. add_node(노드 타입, 노드 아이디, 트리)
#         if tree에 노드가 존재한다면:
#             이미 존재하는 노드 반환
#
#         아니면:
#         노드 생성
#         트리에 노드를 insert
#
#     8. remove_node(노드, 트리):
#        edge_list = 노드.get_edges()
#
#         for edge in edge_list:
#             opponent = edge.target_node()
#             self.__remove_edge(node, opponent)
#
#         node_type = node.node_type
#         node_id = node_id
#         del node
#
#         노드 숫자 줄이기
#         tree.remove(node_id)
#
#     9. connect_feed_with_hashs( 피드, 해시노드들, 생성 날짜)
#         모든 해시태그에 대해
#         엣지를 생성함
#
#     10. sync_feed_with_hashs (노드, 새로운 해시노드들):
#     해시노드 엣지 리스트를 들고옴 (옛날 해시 + 새로운 해시)
#
#         for edge in edge_list:
#             target_node = edge.target_node
#             if not target_node in new_hash_nodes:
#                 remove_edge(feed, target)
#
#     11. disconnect_feed_with_hash ( 피드, 해시노드 ):
#         __remove_edge(feed, hash)
#
#     12. connect_feed_with_user ( 피드, 유저노드):
#         엣지 생성
#
#     13. disconnect_feed_with_user(피드, 유저 노드):
#         엣지 삭제
#
#     14. feed_recommend_user(start_fid, max_user_find=10, max_feed_find=5):
#         1. 시작하는 노드를 찾아냄
#         2. 시작한 노드에서 뻗어나가는 엣지들을 찾아냄
#         3. 가장 최신의 엣지순서대로 정렬한 후, 상위 10개만 잡아냄
#         4. 그 엣지들을 잇는 User들에게 이어진 Feed 노드 엣지 집합 찾아냄
#         5. 그 Feed 엣지들도 다시 최신의 순서대로 정렬 후, 상위 5개 만 집어내서
#         5-1. 이 때, source노드에서 이어진 edge는 제외해야한다.
#         6. 결과 리스트에 담음. 이 때, fid만 담아내어, 나중에 언제든지 참조하기 편하게 한다.
#         return recommend_list
#
#     15. feed_recommend_hash(start_fid, max_hashtags=4, max_feed_find=10):
#         1. 시작노드 찾아냄
#         2. 시작노드에서 뻗어나간 해시태그 엣지들을 찾음
#         3. 기준은 해시태그에 연결되어 있는 Feed들이 많은 순으로 정렬해서 상위 4개 정도 뽑아 옴
#         4. 연결된 해시태그가 가장 최신으로 연결된 랜덤 Feed 10개 까지 뽑아온다.
#         똑같이, 자신에게 붙은 edge는 제외한다.
#         5. recommend_list에 담고, 반환
#         return recommend_list

# 피드-유저-해시태그 통합 그래프
class FeedChaosGraph:
    def __init__(self):
        self.num_feed_nodes = 0
        self.num_user_nodes = 0
        self.num_hash_nodes = 0

    def __call__(self):
        all_node_feeds = self.num_feed_nodes + self.num_user_nodes + self.num_hash_nodes
        pprint(f'INFO<-[    {all_node_feeds} NOVA Graph IN SEARCH ENGINE NOW READY')
        pprint(f'           {self.num_feed_nodes} feed nodes,')
        pprint(f'           {self.num_user_nodes} user nodes,')
        pprint(f'           {self.num_hash_nodes} hash nodes,')

    # 노드 존재 여부 확인
    # noinspection PyMethodMayBeStatic
    def __is_node_exist(self, node_id, tree) -> bool:
        if tree.get(node_id):
            return True
        return False

    # edge 찾기
    # noinspection PyMethodMayBeStatic
    def __find_edge(self, source_node, target_node):
        edge_list = source_node.get_edges()

        for edge in edge_list:
            if edge.get_target_node() == target_node:
                print("found")
                return True
        return False

    # 엣지 추가
    # noinspection PyMethodMayBeStatic
    def __add_edge(self, source_node, target_node, gen_time):
        source_node.add_edge(target_node, gen_time)
        target_node.add_edge(source_node, gen_time)

    # 엣지 삭제
    # noinspection PyMethodMayBeStatic
    def __remove_edge(self, source_node, target_node):
        source_node.remove_edge(target_node)
        target_node.remove_edge(source_node)

    # 노드 추가
    def add_node(self, node_type, node_id, tree:AVLTree):
        node = None

        # 만약 노드가 이미 트리에 있다면, 이미 만들어진 노드를 반환
        if self.__is_node_exist(node_id=node_id, tree=tree):
            return tree.get(node_id)

        # 노드 생성
        if node_type == "user":
            node = UserNode(node_id)
            self.num_user_nodes += 1
        elif node_type == "hashtag":
            node = HashNode(node_id)
            self.num_hash_nodes += 1
        elif node_type == "feed":
            node = FeedNode(node_id)
            self.num_feed_nodes += 1

        # 노드 추가
        tree.insert(key=node_id, value=node)
        return node

    # 노드 삭제
    def remove_node(self, node, tree:AVLTree):
        edge_list = node.get_edges()

        for edge in edge_list:
            opponent_node = edge.get_target_node()
            self.__remove_edge(node, opponent_node)

        # 자신이 제거되면서 자신에게서 출발하는 모든 엣지가 가비지 컬렉팅으로 사라짐
        node_type = node.node_type
        node_id = node.get_id()
        del node

        if node_type == "user":
            self.num_user_nodes -= 1
        if node_type == "hashtag":
            self.num_hash_nodes -= 1
        if node_type == "feed":
            self.num_feed_nodes -= 1

        tree.remove(key=node_id)
        return True

    # Feed-Hash 간 엣지 연결 함수 # 수정 필요. 이미 엣지가 연결되어 있는지 확인이 필요함
    def connect_feed_with_hashs(self, feed_node, hash_nodes, date):
        for hash_node in hash_nodes:
            if not self.__find_edge(feed_node, hash_node):
                self.__add_edge(feed_node, hash_node, date)

        return

    # Feed-new hashtags 엣지 수정, 기존의 엣지 중, 없어진 해시태그는 삭제된다.
    def sync_feed_with_hashs(self, feed_node, new_hash_nodes):
        edge_list = feed_node.edges["hashtag"]

        # 이 때, 기존의 해시태그와 새로운 해시태그 모두 연결되어 있음
        for edge in edge_list:
            # 리스트 안에 있는 에지들을 모두 비교
            target_node = edge.get_target_node()
            # 연결된 노드가 새로운 해시 조합에 해당되지 않는다면 엣지 삭제
            if not target_node in new_hash_nodes:
                self.__remove_edge(feed_node, target_node)

        return

    # Feed-Hash 간의 연결을 끊음
    def disconnect_feed_with_hash(self, feed_node, hash_node):
        if self.__find_edge(feed_node, hash_node):
            self.__remove_edge(feed_node, hash_node)
            return True
        return False

    # 유저 노드와 Feed 노드의 연결
    def connect_feed_with_user(self, feed_node, user_node, date):
        if not self.__find_edge(feed_node, user_node):
            self.__add_edge(feed_node, user_node, date)
        return

    # 유저 노드와 Feed 노드 간 연결을 끊음
    def disconnect_feed_with_user(self, feed_node, user_node):
        if self.__find_edge(feed_node, user_node):
            self.__remove_edge(feed_node, user_node)
            return True
        return False

    # 피드-유저 사이에서 찾아내는 유사한 피드 (수정필)
    def feed_recommend_by_user(self, start_node, max_user_find=10, max_feed_find=5):
        # 가장 먼저, Feed를 확인
        recommend_list = []
        user_queue = []

        # 각 연결된 유저 edge를 찾음
        sorted_edges_latest_related = sorted(start_node.edges["user"])[:max_user_find]

        # 그 중, 가장 최근에 Feed에 관심을 가진(좋아요를 누른) 유저들 10명을 추려냄
        for edge in sorted_edges_latest_related:
            user_queue.append(edge.target_node)

        # 이제, 그 유저들과 연결된 Feed를 담아내는 과정
        for user_node in user_queue:
            # 최신 순으로 정렬된 엣지 중에서, 최대 5개의 feed들을 가져올 것
            sorted_edges_latest_relate_feed = sorted(user_node.edges["feed"])[:max_feed_find]
            for edge in sorted_edges_latest_relate_feed:
                # 가져온 Edge에서 Feed id를 추출하여 recommend_list에 담음
                related_feed_id = edge.get_target_node().get_id()
                recommend_list.append(related_feed_id)

        return recommend_list

    # 피드-해시태그 사이에서 찾아내는 유사한 피드 (수정필)
    def feed_recommend_by_hashtag(self, start_node, max_hash=4, max_feed_find=10):
        recommend_list = []
        hash_queue = []

        # 각 연결된 hash노드 엣지를 찾아냄
        sorted_edges_latest_related_hash = sorted(start_node.edges["hashtag"])[:max_hash]
        # 여기서 이제 해시태그 노드들을 얻어냄
        for edge in sorted_edges_latest_related_hash:
            hash_queue.append(edge.target_node)

        # 다시, 해시노드와 연관된 Feed와 연결된 엣지를 찾아냄
        for hash_node in hash_queue:
            # 최신 순으로 정렬된 edge들을 가져옴
            sorted_edges_latest_related_feed = sorted(hash_node.edges["feed"])[:max_feed_find]
            for edge in sorted_edges_latest_related_feed:
                # 가져온 Feed Edge에서 feed id를 추출해 recommend_list를 다음
                related_feed_id = edge.get_target_node().get_id()
                recommend_list.append(related_feed_id)

        return recommend_list

#
# class FeedAlgorithm:
#     Feed 추천을 위해 만들어진 알고리즘을 담는 곳
#     여기서는 그래프와 데이터들을 담고 있음
#     __init__(database):
#           feed_chaos_graph = FeedChaosGraph()
#           feed_avltree = AVLTree()
#           user_avltree = AVLTree()
#           hash_avltree = AVLTree()
#           __initialize_graph()
#
#     __str__():
#         출력 포맷 설정
#
#     get_nodes_list():
#         노드에 대한 정보 공개
#
#     1. initialize_all_feeds(database):
#         1) 데이터들을 모두 객체화함
#         2) 데이터들을 모두 테이블에 담는다.
#         3) 데이터에 담긴 해시들을 꺼내서 set()에 담는다.
#
#     2. initialize_user_table(database):
#         1) 유저 데이터들을 모두 불러와서 객체화
#         2) 유저 테이블에 담는다.
#
#     3. initialize_graph(self):
#         graph_initialize화를 함.
#
#     4. graph_nodes_print():
#         print(self.__feed_chaos_graph.nodes)
#
#     5. graph_add_feed_node(feed):
#         1) 피드테이블에 새롭게 생긴 피드를 추가
#         2) 피드 노드를 생성하고, 그래프에 추가한다.
#         3) 피드에 저장된 해시태그마다 테이블에 담고, 해시태그 노드를 만들어낸다.
#         4) 글을 작성한 유저 노드를 찾아서 엣지를 연결한다. (이 때, 유저 노드가 없으면 실패)
#
#     6. graph_add_user_node(user):
#         1) 유저테이블에 있는지 확인
#         2) 없으면 노드를 만들어 붙임
#
#
#     7. Graph_remove_node(node_id):
#         1) 먼저 id를 통해 일치하는 노드들을 찾는다.
#         2) 노드를 삭제한다.
#         3) 노드타입에 따라 테이블도 삭제
#
#     8. Graph_remove_edge(source_id, target_id):
#         1) 노드 찾기 (소스노드, 타겟노드)
#         2) 엣지 삭제
#
#     9. find_recommend_feed(start_fid):
#         1) 유저-feed 관계를 바탕으로 한 리스트 추출
#         2) 해시태그-feed 관계를 바탕으로 한 리스트 추출
class FeedAlgorithm:
    def __init__(self, database):
        self.__feed_chaos_graph = FeedChaosGraph()
        self.__feed_node_avltree = AVLTree()
        self.__user_node_avltree = AVLTree()
        self.__hash_node_avltree = AVLTree()
        self.__initialize_graph(database=database)

    def __str__(self):
        all_node_feeds = len(self.__feed_node_avltree) + len(self.__user_node_avltree) + len(self.__hash_node_avltree)
        return (f"INFO<-[    {all_node_feeds} nodes in NOVA Graph IN SEARCH ENGINE NOW READY\n" +
                f"             {list(self.__feed_node_avltree.values())} feed node in Graph.\n" +
                f"             {list(self.__user_node_avltree.values())} user node in Graph.\n" +
                f"             {list(self.__hash_node_avltree.values())} hash node in Graph.\n" )

    # uid로 유저 노드 찾기
    def get_user_node_with_uid(self, uid:str):
        return self.__user_node_avltree.get(key=uid)

    def get_user_nodes(self):
        return list(self.__user_node_avltree.values())

    def get_feed_nodes(self):
        return list(self.__feed_node_avltree.values())

    def get_hash_nodes(self):
        return list(self.__hash_node_avltree.values())

    def __initialize_graph(self, database):
        user_datas = database.get_all_data(target="uid")
        feed_datas = database.get_all_data(target="fid")
        user_list = []
        feed_list = []

        # 유저 데이터 문자열 딕셔너리 -> User() 변환
        for user_data in user_datas:
            single_user = User()
            single_user.make_with_dict(dict_data=user_data)
            user_list.append(single_user)

        # 유저 데이터를 먼저 Graph와 트리에 추가
        for user in user_list:
            self.add_user_node(user)

        # 피드 데이터를 객체화
        for feed_data in feed_datas:
            single_feed = Feed()
            single_feed.make_with_dict(dict_data=feed_data)
            feed_list.append(single_feed)

        # Feed 데이터 노드를 추가
        for feed in feed_list:
            self.add_feed_node(feed)

        all_node_feeds = len(self.__feed_node_avltree) + len(self.__user_node_avltree) + len(self.__hash_node_avltree)
        print(f'INFO<-[      {all_node_feeds} nodes in NOVA Graph IN SEARCH ENGINE NOW READY')

        print(f"             {list(self.__feed_node_avltree.values())} feed node in Graph.")
        print(f"             {list(self.__user_node_avltree.values())} user node in Graph.")
        print(f"             {list(self.__hash_node_avltree.values())} hash node in Graph.")

        return

    # 해시 노드들 추가 # 트리 안에 있는 해시태그를 발견하면 기존의 노드를 반환하도록 한다. 수정필요
    def __add_hash_nodes(self, hashtags:list):
        hash_nodes = []
        for hashtag in hashtags:
            # 해시 태그 마다 노드를 생성
            hash_node = self.__feed_chaos_graph.add_node(node_type="hashtag", node_id=hashtag, tree=self.__hash_node_avltree)
            # 반환할 노드
            hash_nodes.append(hash_node)
        return hash_nodes

    # 유저 노드 추가 (테스트 O)
    def add_user_node(self, user:User):
        if self.__user_node_avltree.get(key=user.uid):
            return False

        # 이미 노드가 트리에 존재 함 -> 노드 객체가 전부 포인터로 이루어져 있어서 트리, 그래프 모두 있음
        user_node = self.__feed_chaos_graph.add_node(node_type="user", node_id=user.uid, tree=self.__user_node_avltree)
        return user_node

    # Feed 노드 추가
    def add_feed_node(self, feed:Feed):
        if self.__feed_node_avltree.get(key=feed.fid):
            return "case1"

        hashtags = feed.hashtag     # feed에 담긴 해시태그
        gen_time = datetime.strptime(feed.date, '%Y/%m/%d-%H:%M:%S')

        # 피드 노드 생성
        feed_node = self.__feed_chaos_graph.add_node(node_type="feed", node_id=feed.fid, tree=self.__feed_node_avltree)
        # 해시 노드 생성 (해시 노드들은 생성이 될 때, 이미 존재하는 노드들이라면 그 노드를 반환함
        hash_nodes = self.__add_hash_nodes(hashtags=hashtags)

        # Feed - 해시노드 간 edge 생성
        self.__feed_chaos_graph.connect_feed_with_hashs(feed_node=feed_node, hash_nodes=hash_nodes, date=gen_time)


        if feed.uid not in self.__user_node_avltree:
            return "case2"
        user_node = self.__user_node_avltree.get(feed.uid)

        # 작성한 글쓴이와 Feed 연결
        self.__feed_chaos_graph.connect_feed_with_user(feed_node=feed_node, user_node=user_node, date=gen_time)

        return "case success"

    # Feed 노드 삭제
    def remove_feed_node(self, fid):
        # 해당하는 Feed가 존재히지 않는 경우, False를 반환
        feed_node = self.__feed_node_avltree.get(key=fid)
        if not feed_node:
            return False
        return self.__feed_chaos_graph.remove_node(node=feed_node, tree=self.__feed_node_avltree)

    # 유저 노드 삭제
    def remove_user_node(self, uid):
        # 만약 uid에 해당하는 노드가 존재하지 않는다면 삭제할 수 없으니 False를 반한
        user_node = self.__user_node_avltree.get(key=uid)
        if not user_node:
            return False
        return self.__feed_chaos_graph.remove_node(node=user_node, tree=self.__user_node_avltree)

    # feed_node 해시 태그 수정
    def modify_feed_node(self, feed:Feed):
        if feed.id not in self.__feed_node_avltree:
            return False

        feed_node = self.__feed_node_avltree.get(key=feed.fid)
        new_hashtags = feed.hashtag
        feed_date = datetime.strptime(feed.date, '%Y/%m/%d-%H:%M:%S')

        new_hash_nodes = self.__add_hash_nodes(hashtags=new_hashtags)
        self.__feed_chaos_graph.connect_feed_with_hashs(feed_node=feed_node, hash_nodes=new_hash_nodes, date=feed_date)

        # 새롭게 연결된 새로운 해시노드들과 비교하여 옛날의 해시태그의 엣지들을 끊어내는 작업
        self.__feed_chaos_graph.sync_feed_with_hashs(feed_node=feed_node, new_hash_nodes=new_hash_nodes)

        return True

    # 좋아요를 누른 게시글과 유저 잇기
    def connect_feed_like_user(self, uid, fid, like_time):
        if uid not in self.__user_node_avltree or fid not in self.__feed_node_avltree:
            return False
        user_node = self.__user_node_avltree.get(key=uid)
        feed_node = self.__feed_node_avltree.get(key=fid)

        self.__feed_chaos_graph.connect_feed_with_user(feed_node=feed_node, user_node=user_node, date=like_time)
        return True

    # 좋아요를 해제한 게시글과 유저 엣지 제거
    def disconnect_feed_like_user(self, uid, fid):
        user_node = self.__user_node_avltree.get(key=uid)
        feed_node = self.__feed_node_avltree.get(key=fid)

        return self.__feed_chaos_graph.disconnect_feed_with_user(feed_node=feed_node, user_node=user_node)

    # 추천 feed를 찾아줌
    def recommend_next_feed(self, start_fid:str, history:list):
        start_feed_node = self.__feed_node_avltree.get(key=start_fid)
        user_feed_recommend_list = self.__feed_chaos_graph.feed_recommend_by_user(start_node=start_feed_node)
        hash_feed_recommend_list = self.__feed_chaos_graph.feed_recommend_by_hashtag(start_node=start_fid)

        result_fid_list = user_feed_recommend_list + hash_feed_recommend_list

        for fid in result_fid_list:
            if fid not in history:
                return fid

        return None


