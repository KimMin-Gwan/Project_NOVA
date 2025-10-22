# 검색엔진이 해야하는일

# 1. 키워드를 통한 피드 검색
# 2. 특정 피드 다음으로 제시할 피드 검색
# 3. 피드 분석 및 최신화
# 4. 추천 피드 제공

# LocalDatabase의 import 문제로 아래 코드는 정상동작 하지 않으니
# 코드를 작성하는 도중에는 주석을 해제하여 LocalDatabase 함수를 자동완성하고
# 실행할때는 다시 주석처리하여 사용할것
#from model import Mongo_Database

import time
import asyncio
from others.data_domain import Feed, User, Notice, Comment
from others.graph_domain import *
from others.managed_data_domain import ManagedFeedBiasTable,  ManagedBias
from pprint import pprint
from collections import Counter

# 아래는 검색 엔진
class FeedSearchEngine:
    def __init__(self, database):
        self.__feed_algorithm= FeedAlgorithm(database=database)
        self.__managed_feed_bias_table = ManagedFeedBiasTable(database=database, feed_algorithm=self.__feed_algorithm)
        self.__search_manager = SearchManager(database=database, feed_algorithm=self.__feed_algorithm,
                                              managed_feed_bias_table=self.__managed_feed_bias_table)
        self.__recommend_manager = RecommendManager(database=database,feed_algorithm=self.__feed_algorithm,
                                                    managed_feed_bias_table=self.__managed_feed_bias_table)
        self.__filter_manager = FilteringManager(database=database, feed_algorithm=self.__feed_algorithm,
                                                 managed_feed_bias_table=self.__managed_feed_bias_table)

        self.__database=database

    def make_task(self):
        return self.__recommend_manager.make_task()

    def try_test_graph_recommend_system(self, fid):
        feed = self.__database.get_data_with_id(target="fid", id=fid)
        #result = self.__feed_algorithm.find_recommend_feed(start_fid=feed.fid)
        result = "2"

        return result

    # 새롭게 최애를 지정했을 때 연결하는 시스템
    # 근데 이거 잘생각해보면 최애 지정하기 전에 쓴 글들은 해시태그에 반영되어야 하는가?
    def add_new_user_to_bias(self, bid:str, uid:str):
        self.__managed_feed_bias_table.add_new_user_to_bias(bid=bid, uid=uid)
        return
    
    def remove_user_to_bias(self, bid:str, uid:str):
        self.__managed_feed_bias_table.remove_user_to_bias(bid=bid, uid=uid)
        return

    def get_all_managed_bias(self):
        return self.__managed_feed_bias_table.get_all_managed_bias()

    # 피드 매니저가 관리중인 피드를 보기 위해 만든 함수
    def try_search_managed_feed(self, fid):
        return self.__search_manager.try_search_managed_feed(fid=fid)
    
    def try_search_managed_feeds(self, fids:list):
        return self.__search_manager.try_search_managed_feeds(fids=fids)
    
    # 새로운  관리 피드를 추가하는 함수
    def try_make_new_managed_feed(self, feed):
        # 알고리즘에도 추가해야되ㅏㅁ
        self.__search_manager.try_make_new_managed_feed(feed)
        self.try_add_feed(feed=feed)
        return
    
    def try_make_new_managed_bias(self, bias:Bias):
        self.__search_manager.try_make_new_managed_bias(bias)
        return

    def try_modify_managed_feed(self, feed):
        self.__search_manager.try_modify_managed_feed(feed)
        self.try_modify_feed(feed=feed)
        return

    def try_remove_managed_feed(self, feed):
        self.__search_manager.try_remove_managed_feed(feed)
        self.try_remove_feed(fid=feed.fid)
        return

    def try_get_random_feed(self) -> str:
        return self.__search_manager.try_get_random_feed()

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

    def try_search_feed_new(self, search_columns:list, target_time="", board_type="", target=""):
        fid_list = self.__search_manager.search_feeds_with_target_option(target = target,
                                                                         search_columns=search_columns,
                                                                         board_type = board_type,
                                                                         target_time=target_time
                                                                         )

        return fid_list

    def try_search_comment_new(self, target=""):
        result_cid = self.__search_manager.search_comments_with_keyword_new(keyword=target)
        return result_cid

    # search_type -> 검색하는 조건
    # 조건명 : (recent -> 단순한 최신순, today -> 24시간 이내 좋아요 순, weekly -> 168시간 이내 좋아요 순, like-> 단순 좋아요 순)

    # 예시 ||  홈 화면의 전체 게시글 파트에 보여줄, 전체 피드 중 가장 최신 피드에서 6개 요청
    # result , index = try_get_feed_in_recent(search_type ="recent", num_feed= 6, index=-2):

    # 예시 || 홈 화면의 오늘의 인기 게시글 파트에 보여줄, 지금 기준 24 시간 이내에 작성된 피드 중 좋아요 30개를 넘은 피드
    # result , index = try_get_feed_in_recent(search_type ="today", num_feed= 6, index=-2):

    # 예시 || 주간 Top100 페이지에서 사용자가 스크롤을 내려 주간 탑 100의 두번째 요청을 넣음
    # result , index = try_get_feed_in_recent(search_type ="weekly", num_feed= 10, index=320):

    def try_get_feed_in_recent(self, time_type, search_type):
        fid_list = self.__search_manager.try_get_feed_with_target_hour(search_type=search_type, time_type=time_type)

        return fid_list
    #
    # def try_get_feed_in_recent(self, search_type="recent", num_feed=1, index=-1):
    #     result_fid = []
    #     result_index = -2
    #
    #     # 여기서 조건에 따른 검색을 해야함
    #
    #     # 차라리 여기서 타임 스탬프를 받아가는건 어떨까?
    #
    #     # 1. 단순히 최신순 검색 ( 모든 피드 보기 기능 )
    #     if search_type == "recent":
    #         # 아래의 코드는 샘플이며 원하는 상태에 따라 다시 작성
    #         result_fid, result_index = self.__search_manager.try_get_feed_with_target_hour(
    #             search_type="all", num_feed=num_feed, target_hour=-1, index=index)
    #
    #     # 2. 24시간 이내에 좋아요가 30개 이상인 피드 ( 오늘의 인기 게시글 기능 )
    #     elif search_type == "today":
    #         # 아래의 코드는 샘플이며 원하는 상태에 따라 다시 작성
    #         result_fid, result_index = self.__search_manager.try_get_feed_with_target_hour(
    #             search_type="best", num_feed=num_feed, target_hour=24, index=index)
    #
    #     # 3. 168시간 이내에 좋아요 순 ( 주간 Top 100 기능 )
    #     elif search_type == "weekly":
    #         # 아래의 코드는 샘플이며 원하는 상태에 따라 다시 작성
    #         result_fid, result_index = self.__search_manager.try_get_feed_with_target_hour(
    #             search_type="best", num_feed=num_feed, target_hour=168, index=index)
    #
    #     # 4. 좋아요가 30개 이상인 피드들을 최신순으로 나열 ( 베스트 피드  기능)
    #     elif search_type == "like":
    #         # 아래의 코드는 샘플이며 원하는 상태에 따라 다시 작성
    #         result_fid, result_index = self.__search_manager.try_get_feed_with_target_hour(
    #             search_type="best", num_feed=num_feed, target_hour=-1, index=index)
    #
    #     return result_fid, result_index

    def try_filtered_feed_with_option(self, fid_list:list, option:str, keys:list):
        # 옵션과 키에 따라 필터링이 나뉘어진다.
        return self.__filter_manager.filtered_feed_option_and_key(fid_list=fid_list, option=option, keys=keys)

    # 최애 페이지에서 요청
    def try_feed_with_bid_n_filtering(self, target_bid:str = "", category=""):
        return self.__filter_manager.filtering_community(bid=target_bid, category=category)

#-----------------------------------------------------------------------------------------------------------
    # 여기도 아직 하지 말것 
    # 목적 : 숏피드에서 다음 피드 제공 받기
    def try_recommend_feed(self, fid:str, history:list, user:User):
        # 유저 비로그인 시 데이터가 처리가 어떻게 되는지 알아야 할듯
        # 그래야 여기에 If문을 통한 로직을 추가하던가, 아니면 기존 로직에서 바꾸든가를 알 수 있을듯
        # 근데 이미 비로그인 유저에 대한 로직을 만들긴 했음

        fid = self.__recommend_manager.get_recommend_feed(fid=fid, history=history,user=user)

        # fid = self.__recommend_manager.get_recommend_feed_not_login(fid=fid, history=history)
        return fid

    # # 추천 키워드
    def try_get_recommend_keyword(self, num_keywords=10):
        # 저장된 키워드가 없는 현재는.. 추천 해시태그를 전해줄까.
        # 일단 로직만 넣었음. 이후에 검색어가 쌓여서 분석이 된다면 이제 넣을거야.
        keywords = []
        # keywords = self.__recommend_manager.get_recommend_keyword(num_keywords=num_keywords)
        keywords = self.__recommend_manager.get_spiked_hashtags_in_hours(
            num_hashtag=num_keywords, target_hours=720
        )
        return keywords

    # ------------------------------------------------------------------------------------
    def get_spiked_hashtags(self, target_type="today", num_hashtags=10) -> list:
        result_hashtags = []

        # 오늘의 급상승 해시태그
        if target_type == "today":
            result_hashtags = self.__recommend_manager.get_spiked_hashtags_in_hours(
                num_hashtag=num_hashtags,target_hours=24)
        # 이번 주의 급상승 해시태그
        elif target_type == "weekly":
            result_hashtags = self.__recommend_manager.get_spiked_hashtags_in_hours(
                num_hashtag=num_hashtags, target_hours=168)
        # 이번 달의 급상승 해시태그, 안쓸지도 모르지만 일단 만들어봤음.
        elif target_type == "monthly":
            result_hashtags = self.__recommend_manager.get_spiked_hashtags_in_hours(
                num_hashtag=num_hashtags, target_hours=720)

        return result_hashtags

    def get_best_hashtag(self, num_hashtag=10):
        return self.__recommend_manager.get_best_hashtags(num_hashtag=num_hashtag)

    def get_recommend_hashtag(self, bids):
        return self.__recommend_manager.get_user_recommend_hashtags(bids=bids)

    #------------------------------------------------------------------------------------------------
    def try_save_keyword_data(self, keyword:str):
        pass
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

    def try_modify_feed(self, feed:Feed):
        result = self.__feed_algorithm.modify_feed_node(feed=feed)
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

# --------------------------------------------------------------------------------------------

# 서치 매니저
class SearchManager:
    # LocalDatabase의 import 문제로 아래 코드는 정상동작 하지 않으니
    # 코드를 작성하는 도중에는 주석을 해제하여 LocalDatabase 함수를 자동완성하고
    # 실행할때는 다시 주석처리하여 사용할것
    #def __init__(self, database:Mongo_Database, feed_algorithm : FeedAlgorithm):
    def __init__(self, database, feed_algorithm=None, managed_feed_bias_table:ManagedFeedBiasTable=None):
        self.__database = database
        self.__feed_algorithm=feed_algorithm
        self.__managed_feed_bias_table=managed_feed_bias_table

        # best_feed_table이 필요한가? 필요없는거 같은데?
        self.__best_feed_table = [] # 좋아요가 30개 이상인 피드 테이블 | 최신 기준 

    def try_get_random_feed(self):
        return self.__managed_feed_bias_table.get_random_feed()

    def try_make_new_managed_feed(self, feed:Feed):
        self.__managed_feed_bias_table.make_new_managed_feed(feed)
        return

    def try_modify_managed_feed(self, feed:Feed):
        self.__managed_feed_bias_table.modify_feed_table(feed)
        return

    def try_remove_managed_feed(self, feed:Feed):
        self.__managed_feed_bias_table.remove_feed(feed)
        return

    # 피드 매니저에서 사용가능하게 만든 검색 기능
    def try_get_all_managed_feeds(self):
        return self.__managed_feed_bias_table.get_managed_df()

    def try_search_managed_feed(self, fid):
        return self.__managed_feed_bias_table.search_managed_feed(fid)
    
    def try_search_managed_feeds(self, fids:list):
        return self.__managed_feed_bias_table.search_managed_feeds(fids=fids)
    
    def try_make_new_managed_bias(self, bias:Bias):
        self.__managed_feed_bias_table.make_new_bias(bias)
        return

    # 목표시간을 바탕으로 피드를 찾는 함수
    # search_type == "all", "best"
    def try_get_feed_with_target_hour(self, time_type, search_type):
        fid_list = self.__managed_feed_bias_table.search_feed_with_time_or_like(search_type=search_type, time_type=time_type)

        return fid_list

    def search_feeds_with_target_option(self, target:str, search_columns:list, board_type="", target_time=""):
        fid_list = self.__managed_feed_bias_table.search_feeds_with_key_n_option(key=target,
                                                                                  board_type=board_type,
                                                                                  search_columns=search_columns,
                                                                                  target_time=target_time)
        return fid_list

    # 댓글 검색
    def search_comments_with_keyword_new(self, keyword: str):
        comment_datas = self.__database.get_all_data(target="comment")
        result_cids = []

        for comment_data in comment_datas:
            comment=Comment()
            comment.make_with_dict(comment_data)
            if keyword in comment.body:
                result_cids.append(comment.cid)

        return result_cids


    # 바이어스 검색 로직 
    def search_biases_with_keyword(self, target:str):
        bid_list = self.__managed_feed_bias_table.search_bias_with_keyword(key=target)
    # def search_feed_with_string(self, string, num_feed=10) -> list: #본문 내용을 가지고 찾는거같음
    #return self.__feed_algorithm.get_feed_with_string(string,num_feed)

# 이건 사용자에게 맞는 데이터를 주려고 만든거
class RecommendManager:
    def __init__(self, database, feed_algorithm=None, managed_feed_bias_table:ManagedFeedBiasTable=None):
        self.__database = database
        self.__feed_algorithm:FeedAlgorithm = feed_algorithm
        self.__managed_feed_bias_table=managed_feed_bias_table

        self.hashtags = []

        # 이거 나중에 쓸거긴 함. 키워드 쌓이면 활성화 시키자
        self.keywords = []
        #asyncio.get_event_loop()
        #self.loop.create_task(self.check_trend_hashtag())

    # 해시태그 랭킹을 위해 사용하는 랭킹 스코어링 알고리즘
    # 시그모이드를 기반으로 함.
    def __check_trend_hashtag_algo(self, weight=0, now_data=0, prev_data=0, num_feed=1):
        if now_data == 0 and prev_data == 0 and weight == 0:
            now_data = num_feed

        next_weight = weight + ((now_data - prev_data) / (num_feed ** 0.5)) * 0.9
        # 새로운 정규화: 상한선 기반 축소 (threshold=0.5, reduction factor=0.1)
        # signoid 함수
        threshold = 0.5
        if next_weight > threshold:
            next_weight = threshold + (next_weight - threshold) * 0.1

        return max(next_weight, 0)

    def __total_hashtag_setting(self):
        try:
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
                hashtag_node.weight_update(new_weight=new_weight)

                # hashtag_node.weight = new_weight
                # hashtag_node.trend["prev"] = hashtag_node.trend["now"]
                # hashtag_node.trend["now"] = 0

                hashtag_rank.append(hashtag_node)

            count = 0
            hashtag_rank = sorted(hashtag_rank, key=lambda x:x.weight, reverse=True)

            for hash_node in hashtag_rank:
                if count == 10:
                    break
                self.hashtags.append(hash_node.hid)
                count += 1
        except Exception as e:
            print(f"total hashtag setting error : {e}")

    def __bias_hashtag_setting(self):
        try:
            managed_bias_list = self.__managed_feed_bias_table.get_all_managed_bias()
            for managed_bias in managed_bias_list:
                hash_nodes = []

                managed_bias:ManagedBias = managed_bias

                # 대충 그래프 타고 들어가서 해시태그 전부다 찾아내는 함수
                for user_node in managed_bias.user_nodes:
                    for user_edge in user_node.edges['feed']:
                        feed_node:FeedNode = user_edge.target_node
                        for feed_edge in feed_node.edges['hashtag']:
                            hash_node:HashNode = feed_edge.target_node
                            hash_nodes.append(hash_node)

                hash_nodes = sorted(hash_nodes, key=lambda x:x.weight, reverse=True)
                managed_bias.trend_hashtags = hash_nodes[:4]
        except Exception as e:
            print(f"bias_hashtag_setting error : {e}")

    def __total_keyword_setting(self):
        pass

    # 매 시간마다 갱신되는 비동기성 함수
    async def check_trend_hashtag(self):
        try:
            last_computed_time = time.time()  # 초기값 설정
            
            while True:
                # 현재 시간 계산
                current_time = time.time()
                time_diff = (current_time - last_computed_time) / 3600  # 시간 단위로 계산

                # 마지막 계산 시간이 1시간 이상일 경우 갱신
                if time_diff >= 1:
                    self.__total_hashtag_setting()
                    self.__bias_hashtag_setting()
                    self.last_computed_time = current_time  # 갱신 완료 시점 기록

                # 60초 대기
                await asyncio.sleep(60)

        except KeyboardInterrupt:
            print("Shutting down due to KeyboardInterrupt.")

    # 키워드 실시간 트렌드 계산 비동기함수
    # 아직 키워드 관련해서 생성된 게 없어서 일단 냅둡니다.
    # 활성화시키지 마세요
    async def check_trend_keyword(self):
        try:
            time_diff = 1
            current_time = time.time()
            while True:
                # time_diff 계산
                if time_diff >= 1:
                    # self.__total_keyword_setting()

                    self.last_computed_time = current_time
                else:
                    await asyncio.sleep(60)

                current_time = time.time()
                if hasattr(self, 'last_computed_time'):
                    time_diff = (current_time - self.last_computed_time) / 3600 # 시간 단위로 계산
                else:
                    self.last_computed_time = current_time
                time_diff = 0
        except KeyboardInterrupt:
            print("Shutting down due to KeyboardInterrupt.")

    def make_task(self):
        return self.check_trend_hashtag

    # 실시간 트랜드 해시태그 제공
    # 급상승 해시태그 정의 : 단기간에 해시태그가 엄청 올라옴
    # 기준 시간) 1시간내에 올라온 글 중 해시태그가 가장 많이 달린 해시태그를 얻어야함
    # 그러면 기준시간은 어떻게 지정하나? -> 알아서 지정되겠지만, 정각을 기준으로 실행되겠지
    # 그러하면 한시간 내에 올라온 Feed들을 모두 모집하고, 데이터프레임화 시켜서 살펴보면 빠를지도

        # 근데, 내가할 건 주간, 일간 게시글이다. 시간 당 베스트는 지금 표본의 개수가 절대적으로 부족하기 때문에
        # 아직은 시행이 불가능하다.
    def get_spiked_hashtags_in_hours(self, num_hashtag=10, target_hours=1) -> list:
        # 시간 내에 올라온 모든 글을 긁어온다.
        index = self.__managed_feed_bias_table.get_len_feed_table()

        if target_hours > 0 :
            target_index = self.__managed_feed_bias_table.find_target_index(target_hour=target_hours)
        else:
            target_index = 0

        # managed_feeds_in_hours = self.__feed_table[target_index
        managed_feeds_in_hours = self.__managed_feed_bias_table.get_feeds_target_range(index=index, target_index=target_index)
        list_of_hashtags_in_hours = []

        for managed_feed in managed_feeds_in_hours:
            for hashtag in managed_feed.hashtag:
                # 해시태그 리스트를 가져오므로, 빈 리스트에 Extend로 이어 붙임.
                list_of_hashtags_in_hours.append(hashtag)

        # pprint(self.__managed_feed_bias_table.get_managed_feed_test())

        # 카운팅 후, 내림차순 정렬되서, 해시태그만 뽑아옴
        counting_hashtags = Counter(list_of_hashtags_in_hours)
        sorted_list_of_hashtag_count = [hashtag for hashtag, count in counting_hashtags.most_common()]

        # pprint("출력 테스트 : " + str(target_hours))
        # pprint(sorted_list_of_hashtag_count)

        return sorted_list_of_hashtag_count[0:num_hashtag]

    # 실시간 트랜드 해시태그 제공
    def get_best_hashtags(self, num_hashtag=10) -> list:
        if len(self.hashtags) < num_hashtag:
            return self.hashtags
        return self.hashtags[0:num_hashtag]

    # 실시간 추천 검색어 제공
    def get_trend_keywords(self, num_keywords=10) -> list:
        if  len(self.keywords) < num_keywords:
            return self.keywords
        return self.keywords[0:num_keywords]

    # 사용자에게 어울릴만한 해시태그 리스트 제공
    def get_user_recommend_hashtags(self, bids):
        result = []

        like_bias_list = self.__managed_feed_bias_table.get_liked_biases(bids)

        for managed_bias in like_bias_list:
            for hashtag in managed_bias.trend_hashtags:
                result.append(hashtag)

        result_set = set(result)

        return list(result_set)
    
    def get_recommend_feed(self, fid:str, history:list, user:User):
        hashtag_ranking_list = self.get_best_hashtags() # 해시태그 랭킹 리스트
        logined_user_uid = user.uid # 현재 로그인된 유저의 uid
        # 로그인이 되지 않은 유저는 uid를 ""를 반환함

        fid = self.__feed_algorithm.recommend_next_feed(
            start_fid=fid,
            history=history,
            mine_uid=logined_user_uid,
            hashtag_ranking=hashtag_ranking_list
            )
        return fid

    def get_recommend_keyword(self, num_keywords:int):
        trend_keyword_list = self.get_trend_keywords()
        return trend_keyword_list

# 필터링 매니저
class FilteringManager:
    def __init__(self, database, feed_algorithm=None, managed_feed_bias_table:ManagedFeedBiasTable=None):
        self.__database = database
        self.__feed_algorithm:FeedAlgorithm = feed_algorithm
        self.__managed_feed_bias_table=managed_feed_bias_table

#--------------------실제로 사용하게 될 구간입니다. 필터링 옵션이 확정났기 때문에 이렇게 새로만듭니다----------------------------------------------

    # def __paging_list(self, fid_list:list, fid, page_size):
    #     # 이미 Date 최신순으로 정렬되어서 맨처음이 젤 최신의 글임
    #     start_index = 0
    #
    #     # 페이징을 하지 않음
    #     if page_size == -1:
    #         return fid_list
    #
    #     if fid != "":
    #         start_index = fid_list.index(fid)  # 타겟으로 잡은 구간부터, 불러오기
    #
    #     paging_fid_list = fid_list[start_index:]        # 페이징으로 짜르기
    #     # 만약 자른 리스트가 페이지를 넘어간다면 짤라야한다
    #     if len(paging_fid_list) > page_size:
    #         paging_fid_list = paging_fid_list[:page_size]
    #
    #     # Paging Fid List, Last_fid
    #     return paging_fid_list, paging_fid_list[-1]

    def _filtering_notices_list(self):
        notice_datas = self.__database.get_all_data(target="notice")
        notices = []

        for notice_data in notice_datas:
            notice = Notice()
            notice.make_with_dict(notice_data)
            notices.append(notice)

        return notices

    def filtered_feed_option_and_key(self, fid_list:list, option:str, keys:list):
        if option == "feed":
            # 키가 하나밖에 없기 때문에.. keys[0]만으로 판별해야한다.
            # Fclass == ""인 경우, Managed_Feed_table에서 처리하도록 하였음
            return self.__managed_feed_bias_table.filtering_fclass_feed(fid_list=fid_list)

        elif option == "category":
            # 구분하기 쉽도록 하였음. 또한, category가 []인 상태라면 뒤에 나올 반복문 자체가 동작하지 않는다.
            # category = []인 경우. 1차 필터링을 거친 것을 그대로 반환

            filtered_fid_list = []
            # 조건문을 추가했음
            if len(keys) <= 0 or keys[0] == "":
                filtered_fid_list = fid_list

            else:
                temp_list = self.__managed_feed_bias_table.filtering_categories_feed(fid_list=fid_list, categories=keys)

                filtered_fid_list.extend(temp_list)
            return filtered_fid_list

    # BID로 필터링 하는 작업 수행, 카테고리별 필터링도 진행 됨
    def filtering_community(self, bid:str, category:str):
        return self.__managed_feed_bias_table.filtering_bias_community(bid=bid, board_type=category)
