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

        for i, managed_feed in enumerate(reversed(self.__feed_table)):
            index = len(self.__feed_table) - 1 - i
            # 삭제된 피드는 None으로 표시될것이라서
            if managed_feed.fid == "":
                continue

            if self.__get_time_diff(target_time=managed_feed.date, target_hour=target_hour):
                continue
            else:
                target_index = index
                break

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




# 오류 에러 처리 클래스
class NodeNotExistError(Exception):
    pass
class NodeAlreadyExistError(Exception):
    pass
class EdgeAlreadyExistError(Exception):
    pass
class EdgeNotExistError(Exception):
    pass
class HashTableNodeAlreadyExistError(Exception):
    pass
class HashTableNodeNotExistError(Exception):
    pass
class NodetypeInputError(Exception):
    pass

# Edge 수도코드
# class Edge
#   __init__(target_node, gen_time_str):
#       self.target_node = target_node
#       self.get_time_str = gen_time_str        # 생성된 시간 string
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
        self.gen_time_str = gen_time # 엣지의 생성 시간

        # 이 엣지는 Feed-User 의  경우, 좋아요(star)를 누른 시간을 가지게 됨
        # Feed-Hashtag 의 경우, Feed 생성 시간을 이어 받게됨.

    # 동일한 엣지인지 서로 비교 해야함.
    # 만약 향하는 노드가 같다면
    def __eq__(self, other):
        return self.target_node == other.target_node

    # 날짜가 더 최신의 edge 순으로 정렬
    def __lt__(self, other):
        gen_time_self = datetime.strptime(self.gen_time_str, "%Y-%m-%d %H:%M:%S")
        gen_time_other = datetime.strptime(other.gen_time_str, "%Y-%m-%d %H:%M:%S")
        return gen_time_self > gen_time_other

    # 출력 포맷
    def __str__(self):
        return 'Edge({}, {})'.format(self.target_node.get_id(), self.gen_time_str)

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
        gen_time = datetime.strptime(self.gen_time_str,"%Y/%m/%d-%H:%M:%S")

        # datetime 연산 시 timedelta값 반환
        time_difference = current_time - gen_time
        return time_difference.total_seconds() # timedelta 값을 초 단위로 변환하여 제공

# BaseNode 수도코드
# class BaseNoe
#     initalize_varialbes
#           edges = {}      # 필요한 엣지를 담음
#           node_type 노드 타입 : 노드의 타입을 정의함. 엣지를 담을 때, 공통된 노드만을 담게하기 위해서 넣음
#
#   공통된 함수들 중, 추가, 삭제, 엣지 찾기를 내부함수로 구현
#   1. __add_edge(target_node, gen_time_str):
#         node_type = target_node.node_type
#         edge = Edge(target_node, gen_time_str)  # 엣지 생성
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
#     3. __find_edge(target_node):
#         #단순히 엣지를 찾는 함수임
#         node_type = target_node.node_type
#
#         for edge in self.edges[node_type]:
#             if target_node == edge.get_target_node():
#                 return edge
#         return None
#     4. get_weight(target_node):
#           타겟노드까지 향하는 엣지의 가중치를 얻음.
#         target_edge = self.__find_edge(target_node)
#         return target_edge.weight()
# Graph 베이스 노드 클래스
class BaseNode:
    def __init__(self, node_type):
        self.edges = {}     # 엣지 해시 테이블
        self.node_type = node_type  # 노드 타입  -> 중요함. 이게 엣지를 담는 위치를 정해준다

    #    # Iterator 정의
    #   def __iter__(self):
    #        return iter(self.edges)

    # Edge 추가 함수
    # node_type 필요 함.
    def __add_edge(self,  target_node, gen_time_str):
        node_type = target_node.node_type
        # 엣지를 담는 곳이 잘못 되었다면 False 를 반환
        # 상속받은 클래스에서 Edge 키를 정의 했기에 가능함
        if node_type not in self.edges:
            return False

        edge = Edge(target_node=target_node, gen_time=gen_time_str)            # 엣지 생성
        # 엣지가 존재하는 것만으로 판단하여 생성할 것인지 아닌지를 판단
        if edge not in self.edges[node_type]:
            self.edges[node_type].append(edge)                                 # 엣지 담기
            return True
        return False

    # Edge 제거 함수
    def __remove_edge(self,  target_node):
        # 리스트 컴프리헨션으로 작성하여, 조금 더 빠른 반복문 실행으로 만들었음
        # 실상 성능의 차이는 좀 적긴하다.
        node_type = target_node.node_type
        # 엣지를 담은 장소가 잘못되어있다면 바로 턴
        if node_type not in self.edges:
            return False

        # 엣지 찾기
        for edge in self.edges[node_type]:
            if target_node == edge.get_target_node():
                self.edges[node_type] = [edge_2 for edge_2 in self.edges[node_type] if edge_2.get_target_node() == target_node]
                return True
        return False

    # 이웃한 노드의 엣지 찾기
    def __find_edge(self, target_node):
        node_type = target_node.node_type
        # 엣지를 담은 곳이 잘못되어있음.
        if node_type not in self.edges:
            return None

        for edge in self.edges[node_type]:
            if target_node == edge.get_target_node():
                return edge
        return None

    # 오버 라이딩용
    def request_delete_all_edge_to_me(self):
        pass

    # 엣지 가중치 획득
    def get_weight(self, target_node):
        target_edge = self.__find_edge(target_node)
        if target_edge is None:
            return None
        return target_edge.weight()

    # 노드 삭제 시. edge까지 전부 삭제
    def __del__(self):
        self.edges.clear()

# class UserNode
#
# 1. initialize_variables(uid)
# super().__init__()
# uid = uid
# edges["feed"] = []  #  노드 타입에 대한 엣지리스트를 정의
#
# 2. iterator 생성
# return iter(edges["feed"])
#
# 3. 노드 일치성 판단.
# 기록된 id가 완전히 동일한지 판단함.
# return self.uid == other.get_id()	# 다른 모든 노드들도 똑같이 get_id()라는 함수를 만듦.

# 4. 아이디 얻기
# 다른 하위 클래스에서도 똑같은 함수를 만들어 둚.
# return uid
#
# 5. 엣지 추가 add_edge (내부 함수로 동작)
# return self.__add_edge(target_node, gen_time_str)
#
# 6. 엣지 삭제 remove_edge (내부 함수로 동작)
# return self.__remove_edge(target_node)
#
# 7. 엣지 삭제 요청 request_delete_edge_to_me()
# 나로 향하는 엣지들을 타겟 노드에게 전부 삭제시켜 달라고 요청하는 함수
# for edge in edges["feed"]:
#     edge.get_target_node().remove_edge(self)

# 유저 노드
class UserNode(BaseNode):
    def __init__(self, uid):
        super().__init__("user")
        self.uid = uid
        self.edges["feed"] = [] # 엣지 리스트를 따로 생성한다. 중요하다

    # 엣지 리스트 반복자를 생성
    def __iter__(self):
        return iter(self.edges["feed"])

    # 노드의 일치성 판단. 이는 기록된 id를 가지고 판단
    def __eq__(self, other):
        return self.uid == other.get_id()

    # 노드 출력 포맷
    def __str__(self):
        return 'Node({}, {})'.format(self.get_id(), self.node_type)

    # 유저 아이디 얻기
    def get_id(self):
        return self.uid

    # 엣지 추가
    def add_edge(self, target_node, gen_time_str):
        # 이 작업이 True, False를 반환하기에 이렇게 함.
        return self.__add_edge(target_node, gen_time_str)

    # 엣지 삭제, 이 작업은 나의 엣지만 없애는 작업. 상대노드꺼는 그래프에서 작업
    def remove_edge(self, target_node):
        # 노드 타입이 Feed 일 때만 수행
        return self.__remove_edge(target_node)

    # 내게 연결된 모든 엣지를 없애달라고 요청하는 작업
    def request_delete_all_edge_to_me(self):
        for edge in self:
            edge.get_target_node().remove_edge(self)

# class HashNode
#
# 1. initialize_variables(hid)
# super().__init__()
# hid = hid
# edges["feed"] = []  #  노드 타입에 대한 엣지리스트를 정의
#
# 2. iterator 생성
# return iter(edges["feed"])
#
# 3. 노드 일치성 판단.
# 기록된 id가 완전히 동일한지 판단함.
# return self.hid == other.get_id()	# 다른 모든 노드들도 똑같이 get_id()라는 함수를 만듦.

# 4. 아이디 얻기
# 다른 하위 클래스에서도 똑같은 함수를 만들어 둚.
# return hid
#
# 5. 엣지 추가 add_edge (내부 함수로 동작)
# return self.__add_edge(target_node, gen_time_str)
#
# 6. 엣지 삭제 remove_edge (내부 함수로 동작)
# return self.__remove_edge(target_node)
#
# 7. 엣지 삭제 요청 request_delete_edge_to_me()
# 나로 향하는 엣지들을 타겟 노드에게 전부 삭제시켜 달라고 요청하는 함수
# for edge in edges["feed"]:
#     edge.get_target_node().remove_edge(self)

# 해시태그 노드
class HashNode(BaseNode):
    def __init__(self, hid):
        super().__init__("hashtag")
        self.hid = hid          # 해시태그 아이디, 문자열이 된다.
        self.edges["feed"] = []

    # 엣지 리스트 순회 반복자
    def __iter__(self):
        return iter(self.edges["feed"])

    # 노드 일치성 판단. 기록된 id를 통해 판단
    def __eq__(self, other):
        return self.hid == other.get_id()

    # 노드 출력 포맷
    def __str__(self):
        return 'Node({}, {})'.format(self.get_id(), self.node_type)

    # 아이디 반환 함수
    def get_id(self):
        return self.hid

    # 엣지 추가
    def add_edge(self, target_node, gen_time_str):
        return self.__add_edge(target_node, gen_time_str) # 엣지 추가

    # 엣지 삭제, 이 작업은 나의 엣지만 없애는 작업. 상대노드꺼는 그래프에서 작업
    def remove_edge(self, target_node):
        return self.__remove_edge(target_node)

    # 내게 연결된 모든 엣지를 없애달라고 요청하는 작업
    def request_delete_all_edge_to_me(self):
        for edge in self:
            edge.get_target_node().remove_edge(self) # 자신의 노드를 보낸다.

# class FeedNode
#
# 1. initialize_variables(fid)
#     super().__init__()
#     fid = fid
#     edges["user"] = []  #  노드 타입에 대한 엣지리스트를 정의
#     edges["hashtag"] = []
#
# 2. iterator 생성
#     2-1. 유저 엣지에 대한 iterator
#       return iter(edges["user"])
#     2-2. 해시태그 엣지에 대한 iterator
#       return iter(edges["hashtag"]
#
# 3. 노드 일치성 판단.
#       기록된 id가 완전히 동일한지 판단함.
#     return self.hid == other.get_id()	# 다른 모든 노드들도 똑같이 get_id()라는 함수를 만듦.
#
# 4. 아이디 얻기
# 다른 하위 클래스에서도 똑같은 함수를 만들어 둚.
#     return fid
#
# 5. 엣지 추가 add_edge (내부 함수로 동작)
#    return self.__add_edge(target_node, gen_time_str)
#
# 6. 엣지 삭제 remove_edge (내부 함수로 동작)
#     return self.__remove_edge(target_node)
#
# 7. 엣지 삭제 요청 request_delete_edge_to_me()
#       나로 향하는 엣지들을 타겟 노드에게 전부 삭제시켜 달라고 요청하는 함수
#     for edge in edges["user"]:
#         edge.get_target_node().remove_edge(self)
#     for edge in edges["hashtag"]:
#         edge.get_target_node().remove_edge(self)

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

    # 각각의 엣지 리스트 반복자를 정의
    def iter_user(self):
        return iter(self.edges["user"])
    def iter_hashtag(self):
        return iter(self.edges["hashtag"])

    # 노드 아이디 얻기
    def get_id(self):
        return self.fid

    # 엣지 추가
    def add_edge(self, target_node, gen_time_str):
        return self.__add_edge(target_node,gen_time_str)

    # 엣지 삭제
    def remove_edge(self, target_node):
        return self.__remove_edge(target_node)

    # 내게 연결된 모든 엣지를 없애달라고 요청하는 작업
    def request_delete_all_edge_to_me(self):
        for edge in self.iter_user():
            edge.get_target_node().remove_edge(self)
        for edge in self.iter_hashtag():
            edge.get_target_node().remove_edge(self)

# class FeedChaosGraph
#     1. initalize_variables
#         self.nodes = {}
#         self.nodes["user"] = []
#         self.nodes["hashtag"] = []
#         self.nodes["feed"] = []
#
#     2. iterator 정의
#         return iter(self.nodes[nodetype])
#
#     3. 생성된 노드 찾기 (node_id 필요)
#         for node in self.nodes[node_type]:
#             if node.get_id() == node_id
#                 return node
#
#     4. 노드 추가하기
#         1. 노드타입 제대로 들어왔는지 확인
#             if node_type not in self.nodes:
#                 raise error
#         2. 노드가 이미 존재하는 지
#             if find_node is not None:
#                 raise error
#     3. 노드 생성
#         노드타입에 맞게 대응되는 노드를 생성
#
#         self.nodes[node_type].append(node)
#         return node
#     5. 노드 삭제하기
#         1. 노드가 들어있는지 확인
#         2. 노드와 연결 되어있는 edge들을 전부 끊어내기
#             node.request_delete_all_edge_to_me()
#         3. 마지막으로 자신을 삭제함. 이 때 엣지들은 전부 가비지 컬렉팅 됨
#
#     6. 엣지 추가하기 (source_node, target_node)
#         1. 노드들이 존재하는지 확인
#         2. 노드들에 대해 엣지 추가를 함
#         source -> target
#         target -> source
#
#     7. 엣지 삭제하기 (개별 삭제)
#         1. 노드 존재 확인
#         2. 소스 <-> 타겟 엣지 삭제
#         source -> target
#         target -> source
#
#
#     8. Initalize_node(feed_table, user_table):
#         for user in user_table:
#             user_node 생성
#
#         for feed in feed_table:
#             각 feed의 id, feed 생성시간, hashtag 리스트들을 얻음
#             fid를 이용해서 feed node 생성
#
#             해시태그 노드 추가 및 Edge 생성
#             for hashtag in hashtags:
#                 hash_node 생성
#                 edge (feed -> hashnode) 생성
#                 edge (hash -> feed) 생성
#             작성자 유저 노드와 feed 노드 간 엣지 형성
#             edge(user -> feed)
#             edge(feed -> user)
#
#     9. feed_recommend_user(start_fid, max_user_find=10, max_feed_find=5):
#         1. 시작하는 노드를 찾아냄
#         2. 시작한 노드에서 뻗어나가는 엣지들을 찾아냄
#         3. 가장 최신의 엣지순서대로 정렬한 후, 상위 10개만 잡아냄
#         4. 그 엣지들을 잇는 User들에게 이어진 Feed 노드 엣지 집합 찾아냄
#         5. 그 Feed 엣지들도 다시 최신의 순서대로 정렬 후, 상위 5개 만 집어내서
#         5-1. 이 때, source노드에서 이어진 edge는 제외해야한다.
#         6. 결과 리스트에 담음. 이 때, fid만 담아내어, 나중에 언제든지 참조하기 편하게 한다.
#         return recommend_list
#
#     10. feed_recommend_hash(start_fid, max_hashtags=4, max_feed_find=10):
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
        self.nodes = {}
        self.nodes["user"] = []
        self.nodes["hashtag"] = []
        self.nodes["feed"] = []

    def iter_nodes(self, node_type):
        return iter(self.nodes[node_type])

    # 생성 되어있는 노드 찾기
    def find_node(self, node_type, node_id):
        for already_node in self.iter_nodes(node_type):
            if already_node.get_id() == node_id:
                return already_node
        return None

    # 노드 추가
    def add_node(self, node_type, node_id):
        try :
            # 노드의 타입이 제대로 입력이 되어있는지 확인
            if node_type not in self.nodes:
                raise NodetypeInputError("Node type is not valid")

            # 노드의 존재 여부 확인
            if self.find_node(node_type, node_id) is not None:
                raise NodeAlreadyExistError("Node is already exists")

            node = None
            # 노드 생성
            if node_type == "user":
                node = UserNode(node_id)
            elif node_type == "hashtag":
                node = HashNode(node_id)
            elif node_type == "feed":
                node = FeedNode(node_id)

            # 노드 추가
            if node is not None:
                self.nodes[node_type].append(node)

            return node

        except NodeAlreadyExistError as e:
            print(e)
            return None
        except NodetypeInputError as e:
            print(e)
            return None

    # 노드 삭제
    def remove_node(self, node_type, node_id):
        try:
            for node in self.iter_nodes(node_type):
                # 해당하는 노드를 발견했다면
                if node.get_id() == node_id:
                    # 자신에게 존재하는 인접노드에게 연결된 엣지들을 삭제요청
                    node.request_delete_all_edge_to_me()
                    # 자신이 제거되면서 자신에게서 출발하는 모든 엣지가 가비지 컬렉팅으로 사라짐
                    self.nodes[node_type].remove(node)
                    print("Remove Complete")
            raise NodeNotExistError("Node is not exist")

        except NodeNotExistError as e:
            print(e)

    # 엣지 추가
    def add_edge(self, source_node, target_node, gen_time_str):
        try:
            source_type = source_node.node_type
            target_type = target_node.node_type

            if source_node not in self.nodes[source_type]:
                raise NodeNotExistError("Source node is not exist")
            if target_node not in self.nodes[target_type]:
                raise NodeNotExistError("Target node is not exist")

            source_success = source_node.add_edge(target_node, gen_time_str)
            target_success = target_node.add_edge(source_node, gen_time_str)

            if source_success and target_success:
                print("Success Add Edge.")

        except NodeNotExistError as e:
            print(e)

    # 엣지 삭제
    def remove_edge(self, source_node, target_node):
        try:
            source_type = source_node.node_type
            target_type = target_node.node_type

            if source_node not in self.nodes[source_type]:
                raise NodeNotExistError("Source node is not exist")
            if target_node not in self.nodes[target_type]:
                raise NodeNotExistError("Target node is not exist")

            source_success = source_node.remove_edge(target_node)
            target_success = target_node.remove_edge(source_node)

            if source_success and target_success:
                print("Success Remove Edge.")

        except NodeNotExistError as e:
            print(e)

    def initialize_graph_nodes(self,feed_table, user_table):
        for user in user_table:
            uid = user.uid
            self.add_node("user", uid)

        for feed in feed_table:
            fid = feed.fid
            hashtags = feed.hashtag

            feed_node = self.add_node("feed", fid)
            for hashtag in hashtags:
                hash_node = self.add_node("hashtag", hashtag)
                self.add_edge(feed_node, hash_node, feed.gen_time_str)
                self.add_edge(hash_node, feed_node, feed.gen_time_str)

            user_node = self.find_node("user", feed.uid)
            self.add_edge(user_node, feed_node, feed.gen_time_str)
            self.add_edge(feed_node, user_node, feed.gen_time_str)

    # 피드-유저 사이에서 찾아내는 유사한 피드 (수정필)
    def feed_recommend_by_user(self, start_fid, max_user_find=10, max_feed_find=5):
        # 가장 먼저, Feed를 확인
        recommend_list = []
        user_queue = []

        # feed 노드 확인
        feed_node = self.find_node("feed", start_fid)
        # 각 연결된 유저 edge를 찾음
        sorted_edges_latest_related = sorted(feed_node.edges["user"])[:max_user_find]
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
    def feed_recommend_by_hashtag(self, start_fid, max_hash=4, max_feed_find=10):
        recommend_list = []
        hash_queue = []

        # Feed node 확인
        feed_node = self.find_node("feed", start_fid)
        # 각 연결된 hash노드 엣지를 찾아냄
        sorted_edges_latest_related_hash = sorted(feed_node.edges["hashtag"])[:max_hash]
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

class FeedAlgorithm:
    def __init__(self, database):
        self.__now_all_feed=[]
        self.__database=database
        self.feed_chaos_graph = FeedChaosGraph()
        self.__feed_table = []
        self.__user_table = []
        self.__hashtag_table = []

    def __initialize_feed_table(self, database):
        # 먼저 피드 데이터를 DB에서 불러오고
        feed_datas = database.get_all_data(target="fid")

        # 불러온 피드들은 객체화 시켜준다음 잠시 보관
        for feed_data in feed_datas:
            feed = Feed()
            feed.make_with_dict(dict_data=feed_data)
            self.__feed_table.append(feed)


    def __initialize_user_table(self, database):
        # 유저 데이터를 불러온 후
        user_datas = database.get_all_data(target="uid")

        # 불러온 유저데이터 객체화
        for user_data in user_datas:
            user = User()
            user.make_with_dict(dict_data=user_data)
            self.__user_table.append(user)

    def initialize_graph(self):
        self.feed_chaos_graph.initialize_graph_nodes(feed_table=self.__feed_table, user_table=self.__user_table)

    def print_graph_all_nodes(self):
        print(self.feed_chaos_graph.nodes)



