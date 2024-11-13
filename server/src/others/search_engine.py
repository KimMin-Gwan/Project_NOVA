import pandas as pd
from bintrees import AVLTree
from copy import copy
from others.data_domain import Feed
from datetime import  datetime, timedelta


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
        self.db=database

    # 피드 매니저가 관리중인 피드를 보기 위해 만든 함수
    def try_search_managed_feed(self, fid):
        return self.__search_manager.try_search_managed_feed(fid=fid)
    
    # 새로운  관리 피드를 추가하는 함수
    def try_make_new_managed_feed(self, feed):
        # 알고리즘에도 추가해야되ㅏㅁ
        self.__search_manager.try_make_new_managed_feed(feed)

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

    # ------------------------------------------------------------------------------------------------------------
    # 여기는 아직 하지 말것
    # 목적 : 추천하는 해시태그 제공, 실시간 트랜드 해시태그 제공
    def try_get_hashtags(self, num_hashtag,target_type="default", user=None, bias=None):
        result = []

        if target_type == "default":
            result = self.__recommand_manager.get_best_hashtags(num_hashtag=num_hashtag)
        elif target_type == "all":
            result = self.__recommand_manager.get_recommand_hashtags(user, bias, num_hashtag)

        return result

    # 여기도 아직 하지 말것 
    # 목적 : 숏피드에서 다음 피드 제공 받기
    def try_recommand_feed(self, num_hashtag,target_type="default", feed=None, user=None, bias=None):
        result = []

        if target_type == "short":
            
            result = self.__recommand_manager.get_next_feeds(feed, user, num_hashtag)
        elif target_type == "best":
            result = self.__recommand_manager.get_recommand_hashtags(user, bias, num_hashtag)

        return result 
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

        self.__feed_table = sorted(self.__feed_table, key=lambda x:x.date, reverse=True)

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
        target_index = -1

        print(5)
        for i, managed_feed in enumerate(reversed(self.__feed_table)):
            index = len(self.__feed_table) - 1 - i
            # 삭제된 피드는 None으로 표시될것이라서
            if managed_feed.fid == "":
                continue

            object_date = self.__get_date_str_to_object(str_date=managed_feed.date)

            if self.__get_time_diff(target_time=object_date, target_hour=target_hour):
                continue
            else:
                target_index = index
                break
        print(6)

        return target_index

    # 목표시간을 바탕으로 피드를 찾느 ㄴ함수
    # search_type == "all", "best"
    def try_get_feed_with_target_hour(self, search_type="all", num_feed=4, target_hour=1, index=-2):
        result_fid = []
        result_index = -3


        if index == -1:
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
            for i, managed_feed in enumerate(reversed(search_range)):
                ii = len(self.__feed_table) - 1 - i
                if count == num_feed:
                    break
                
                # 삭제된 피드는 None으로 표시될것이라서
                if managed_feed.fid == "":
                    continue

                result_fid.append(managed_feed.fid)
                # result_index 업데이트
                result_index = index - 1 - ii # 실제 self.__feed_table에서의 인덱스 계산
                count += 1


        elif search_type == "best":
            for i, managed_feed in enumerate(search_range):
                ii = len(self.__feed_table) - 1 - i
                if count == num_feed:
                    break

                # 삭제된 피드는 None으로 표시될것이라서
                if managed_feed.fid == "":
                    continue
                
                if managed_feed.like < 30:
                    continue

                result_fid.append(managed_feed.fid)
                # result_index 업데이트
                result_index = index - 1 - ii # 실제 self.__feed_table에서의 인덱스 계산
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

        for i, managed_feed in enumerate(reversed(search_range)):
            ii = len(self.__feed_table) - 1 - i
            if count == num_feed:
                break

            # 삭제된 피드는 None으로 표시될것이라서
            if managed_feed.fid == "":
                continue

            if hashtag not in managed_feed.hashtag:
                continue

            result_fid.append(managed_feed.fid)

            # result_index 업데이트
            result_index = index - 1 - ii  # 실제 self.__feed_table에서의 인덱스 계산
            count += 1

        return result_fid, result_index


    def search_feed_with_fid(self, fid, num_feed=1, index=-1) -> list:
        result_fid = []
        for i, managed_feed in enumerate(reversed(self.__feed_table)):
            index = len(self.__feed_table) - 1 - i
            if managed_feed.fid == fid:
                result_fid.append(managed_feed.fid)
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

        for i, managed_feed in enumerate(reversed(search_range)):
            ii = len(self.__feed_table) - 1 - i

            if count == num_feed:
                break

            # 삭제된 피드는 None으로 표시될것이라서
            if managed_feed.fid == "":
                continue

            if uname != managed_feed.uname:
                continue

            result_fid.append(managed_feed.fid)

            # result_index 업데이트
            result_index = index - 1 - ii  # 실제 self.__feed_table에서의 인덱스 계산
            count += 1

        return result_fid, result_index

    #def search_feed_with_string(self, string, num_feed=10) -> list:   #본문 내용을 가지고 찾는거같음
        #return self.__feed_algorithm.get_feed_with_string(string,num_feed)
    
# --------------------------------------------------------------------------------------------

# 이건 아직 만지지 말것 ------------------------------------------------------------------------


# 이건 사용자에게 맞는 데이터를 주려고 만든거

class RecommandManager:
    def __init__(self, database,feed_algorithm):
        self.__database = database
        self.__feed_algorithm = feed_algorithm

    # 사용자에게 어울릴만한 해시태그 리스트 제공
    def get_best_hashtags(self, num_hashtag=10) -> list:
        return 

    # 숏피드에서 다음 피드 요청
    def get_next_feeds(self, feed, user, num_feed=1) -> list:
        return 

    # 실시간 트랜드 해시태그 제공
    def get_recommand_hashtags(self, user, bias, num_hashtag=4) -> list:
        return 


# --------------------------------------------------------------------------------------------





# 여기는 신대홍이 만드는 피드 알고리즘 부분

class FeedAlgorithm:
    def __init__(self, database):
        self.__now_all_feed=[]
        self.__database=database 


