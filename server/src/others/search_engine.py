# 검색엔진이 해야하는일

# 1. 키워드를 통한 피드 검색
# 2. 특정 피드 다음으로 제시할 피드 검색
# 3. 피드 분석 및 최신화
# 4. 추천 피드 제공

# LocalDatabase의 import 문제로 아래 코드는 정상동작 하지 않으니
# 코드를 작성하는 도중에는 주석을 해제하여 LocalDatabase 함수를 자동완성하고
# 실행할때는 다시 주석처리하여 사용할것
#from model import Local_Database

# from bintrees import AVLTree
# from datetime import  datetime, timedelta
# import random
# from copy import copy
from email.policy import default
from time import sleep
import pandas as pd
import time
import asyncio
from others.data_domain import Feed, User, Bias, Notice, Comment
from others.graph_domain import *
from others.managed_data_domain import ManagedFeedBiasTable, ManagedFeed, ManagedBias
from pprint import pprint
from collections import Counter, OrderedDict

# #--------------------------------------------------------------------------------------------------
#
# # 이건 아래에 피드 테이블에 들어가야되는 피드 자료형
# # 데이터 베이스에서 피드 데이터 받아서 만들꺼임
# # 필요한 데이터는 언제든 추가가능
#
# # 이게 검색에 따른 피드를 제공하는 클래스
# # 위에 FeedAlgorithm에서 작성한 내용을 가지고 와도됨
#
# # 임시로 사용할 검색어 저장 및 활용 클래스입니다.
# class Keyword:
#     def __init__(self, keyword=""):
#         self.keyword = keyword
#         self.count = 0
#         self.trend = {
#             "now" : 0,
#             "prev" : 0
#         }
#
# # 클래스 목적 : 피드를 검색하거나, 조건에 맞는 피드를 제공하기 위함
# class ManagedFeed:
#     def __init__(self, fid="", like=0, date=None, uname="", fclass="", display=4,
#                  board_type="", hashtag=[], body="", bid="", iid="", num_images=0):
#         self.fid=fid
#         self.fclass = fclass
#         self.display = display
#         self.like=like
#         self.date=date
#         self.uname = uname
#         self.hashtag = hashtag
#         self.board_type = board_type
#         self.body = body
#         self.bid = bid
#         self.iid = iid
#         self.num_images = num_images
#
#     # 무슨 데이터인지 출력해보기
#     def __call__(self):
#         print("fid : ", self.fid)
#         print("fclass: ", self.fclass)
#         print("display: ", self.display)
#         print("like : ", self.like)
#         print("date: ", self.date)
#         print("uname: ", self.uname)
#         print("hashtag: ", self.hashtag)
#         print("board_type: ", self.board_type)
#         print("body: ", self.body)
#         print("bid: ", self.bid)
#         print("iid: ", self.iid)
#         print("num_images: ", self.num_images)
#
#     def to_dict(self):
#         return {
#             "fid": self.fid,
#             "fclass": self.fclass,
#             "display": self.display,
#             "like": self.like,
#             "date": self.date,
#             "uname": self.uname,
#             "hashtag": self.hashtag,
#             "board_type": self.board_type,
#             "body": self.body,
#             "bid": self.bid,
#             "iid": self.iid,
#             "num_images": self.num_images
#         }
#
# # 이거는 Bias 테이블에 들어가게 되는 Bias 자료형
# # 데이터베이스에 받아서 만들어진다.
# class ManagedBias:
#     def __init__(self, bid, user_nodes:list, board_types:list):
#         self.bid = bid
#         self.trend_hashtags = []
#         self.user_nodes:list = user_nodes
#         self.board_types:list = board_types
#
#     def to_dict(self):
#         return {
#             "bid": self.bid,
#             "trend_hashtags": self.trend_hashtags,
#             "board_types": copy(self.board_types)
#         }
#
# # ManagedFeed 테이블 클래스.
# # 기존의 SearchEngine 에서는 각 Manager마다 각기 정의된 ManagedTable을 가졌는데
# # 너무 복잡해짐에 따라, 통합하기로 결정. 클래스화 시킵니다.
# class ManagedFeedBiasTable:
#     def __init__(self, database, feed_algorithm):
#         self.__database = database
#         self.__feed_algorithm = feed_algorithm
#         self.__feed_table =[]
#         self.__feed_df = pd.DataFrame()
#         self.__feed_avltree = AVLTree()
#         self.__bias_avltree = AVLTree()
#
#         self.__init_feed_table()
#         self.__init_bias_tree()
#
#     def __get_datetime_now(self):
#         now = datetime.now()
#         return now
#
#     # string to datetime
#     def __get_date_str_to_object(self, str_date):
#         date_obj = datetime.strptime(str_date, "%Y/%m/%d-%H:%M:%S")
#         return date_obj
#
#     # datetime to string
#     def __get_date_object_to_str(self, object:datetime):
#         formatted_str = object.strftime("%Y/%m/%d-%H:%M:%S")
#         return formatted_str
#
#     # 시간 차이를 분석하는 함수
#     # target_hour : 1, 24, 168
#     def __get_time_diff(self, target_time, reference_time=datetime.now(),
#                         target_hour=2) -> bool:
#         time_diff = abs(target_time - reference_time)
#
#         # 차이가 2시간 이상인지 확인
#         return time_diff >= timedelta(hours=target_hour)
#
#     # 시간 차이를 바탕으로 정해진 시간대 내의 피드 정보 구하기
#     # target_hour : 1, 24, 168
#     def __find_target_index(self, target_hour=1):
#         target_index = len(self.__feed_table)
#
#
#         for i, managed_feed in enumerate(self.__feed_table):
#             # 삭제된 피드는 None으로 표시될것이라서
#             if managed_feed.fid == "":
#                 continue
#
#             if self.__get_time_diff(target_time=managed_feed.date, target_hour=target_hour):
#                 continue
#             else:
#                 target_index = i
#                 break
#
#         return target_index
#
#     # Initialize 테이블
#     def __init_feed_table(self):
#         feeds = []
#         # 먼저 피드 데이터를 DB에서 불러오고
#         feed_datas = self.__database.get_all_data(target="fid")
#
#         # 불러온 피드들은 객체화 시켜준다음 잠시 보관
#         for feed_data in feed_datas:
#             feed = Feed()
#             feed.make_with_dict(dict_data=feed_data)
#             feeds.append(feed)
#
#         # 잠시 보관한 피드 데이터에서 필요한 정보만 뽑아서 ManagedFeed 객체 생성
#         for single_feed in feeds:
#             managed_feed = ManagedFeed(fid=single_feed.fid,
#                                        fclass=single_feed.fclass,
#                                        display=single_feed.display,
#                                        like=single_feed.star,
#                                        date=self.__get_date_str_to_object(single_feed.date),
#                                        hashtag=copy(single_feed.hashtag),
#                                        uname=single_feed.nickname,
#                                        board_type=single_feed.board_type,
#                                        body=single_feed.body,
#                                        bid=single_feed.bid,
#                                        iid=single_feed.iid,
#                                        num_images=len(single_feed.image)
#                                        )
#             # 보관
#             self.__feed_table.append(managed_feed)
#
#         # 리턴되면 위에서 잠시 보관한 피드 데이터는 사라지고 self.__feed_table에 ManagedFeed들만 남음
#         # 최신이 가장 밑으로 오지만, 데이터프레임만 최신 내림차순으로 정렬할 것
#         self.__feed_table = sorted(self.__feed_table, key=lambda x:x.date, reverse=False)
#         self.__feed_df = self.__dataframing_feed_list()
#
#         num_feed = str(len(self.__feed_table))
#         print(f'INFO<-[      {num_feed} NOVA FEED IN SEARCH ENGINE NOW READY.')
#         print(f'INFO<-[      {num_feed} NOVA FEED DATAFRAME IN SEARCH ENGINE NOW READY.')
#
#         return
#
#     # Feed_avltree 설정
#     def __init_feed_avltree(self):
#         for feed in self.__feed_table:
#             self.__feed_avltree.insert(feed.fid, feed)
#         print(f'INFO<-[      NOVA FEED AVLTREE IN SEARCH ENGINE NOW READY.')
#
#     # Bias Tree 설정
#     def __init_bias_tree(self):
#         biases = []
#         users = []
#         bias_datas = self.__database.get_all_data(target="bid")
#         user_datas = self.__database.get_all_data(target="uid")
#
#         for bias_data in bias_datas:
#             bias = Bias()
#             bias.make_with_dict(bias_data)
#             biases.append(bias)
#
#         for user_data in user_datas:
#             user = User()
#             user.make_with_dict(user_data)
#             users.append(user)
#
#         for single_bias in biases:
#             user_nodes = []
#             for single_user in users:
#                 single_user:User = single_user
#                 # bias를 팔로우하는 유저를 찾아서 노드 연결해야됨
#                 if single_bias.bid in single_user.bids:
#                     user_node = self.__feed_algorithm.get_user_node_with_uid(uid=single_user.uid)
#                     # 못찾 으면 예외 처리할 것
#                     if user_node:
#                         user_nodes.append(user_node)
#
#             # 이제 관리될 바이어스를 만들고 연결한다음
#             managed_bias = ManagedBias(bid=single_bias.bid, user_nodes=user_nodes, board_types=single_bias.board_types)
#             # avl트리에 넣어주면됨
#             self.__bias_avltree.insert(key=single_bias.bid, value=managed_bias)
#
#         return
#
#     # Feed list DataFrame화
#     def __dataframing_feed_list(self):
#         # ManagedFeed들은 객체이므로, 딕셔너리화 시켜서 리스트로 만든다.
#         managed_feed_dict_list = [managed_feed.to_dict() for managed_feed in self.__feed_table]
#         feed_df = pd.DataFrame(managed_feed_dict_list)
#         # 데이터프레임을 정렬함
#         feed_df = feed_df.sort_values(by='date', ascending=False).reset_index(drop=True)
#
#         return feed_df
#
#     def __add_new_data_in_df(self, managed_feed):
#         new_data = pd.DataFrame(managed_feed.to_dict())
#         self.__feed_df = pd.concat([self.__feed_df, new_data], ignore_index=True)
#         self.__feed_df = self.__feed_df.sort_values(by='date', ascending=False).reset_index(drop=True)
#         return
#
#     def __modify_data_in_df(self, new_managed_feed):
#         new_data = new_managed_feed.to_dict()
#         # fid는 고유값이므로, 하나밖에 안 나옴
#         update_index = self.__feed_df.index[self.__feed_df['fid'] == new_managed_feed.fid].tolist()[0]
#         self.__feed_df.loc[update_index] = new_data
#
#         return
#
#     def __remove_data_in_df(self, fid):
#         remove_index = self.__feed_df.index[self.__feed_df['fid'] == fid].tolist()[0]
#         self.__feed_df = self.__feed_df.drop(index=remove_index).reset_index(drop=True)
#         return
#
#     #---------------------------------------------------------------------------------------------
#     def get_managed_feed_test(self):
#         return self.__feed_table[2].to_dict()
#
#     def len_feed_table(self):
#         # Feed Table의 길이 구하기
#         return len(self.__feed_table)
#
#     # 새로운 ManagedFeed를 추가함
#     def make_new_managed_feed(self, feed:Feed):
#         managed_feed = ManagedFeed(
#             fid=feed.fid,
#             fclass=feed.fclass,
#             like=feed.star,
#             date=self.__get_date_str_to_object(feed.date),
#             uname=feed.nickname,
#             hashtag=feed.hashtag,
#             board_type=feed.board_type, # 이거 추가됨
#             body=feed.body,
#             bid=feed.bid,
#             iid=feed.iid,
#             num_images=feed.num_image
#         )
#
#         self.__feed_table.append(managed_feed)
#         self.__feed_avltree.insert(managed_feed.fid, managed_feed)
#         # 데이터 프레임 추가
#         self.__add_new_data_in_df(managed_feed)
#
#         return
#
#     # ManagedFeedTable을 수정, 새로운 Feed가 들어왔기 때문
#     def modify_feed_table(self, feed:Feed):
#         # 피드 테이블을 수정하는 함수
#         # managed_feed를 찾아야 됨
#         managed_feed:ManagedFeed = self.__feed_avltree.get(feed.fid)
#
#         # managed_feed가 가진 데이터로 원본 데이터를 변경
#         managed_feed.date = feed.date
#         managed_feed.hashtag = feed.hashtag
#         managed_feed.body = feed.body
#         managed_feed.like = feed.star
#         managed_feed.uname = feed.nickname
#
#         # dataframe도 업데이트
#         self.__modify_data_in_df(managed_feed)
#
#         return
#
#     # ManagedFeed가 삭제되었기 때문에, 테이블과 트리에서도 삭제시킴
#     def remove_feed(self, feed:Feed):
#         # 삭제하는 함수. 피드가  삭제되면 None으로 바뀔것
#         managed_feed = self.__feed_avltree.get(key=feed.fid)
#         managed_feed = ManagedFeed()
#         self.__feed_avltree.remove(key=feed.fid)
#         # dataframe 삭제
#         self.__remove_data_in_df(fid=feed.fid)
#         return
#
#     # 랜덤한 Feed 하나 추출
#     def get_random_feed(self):
#         random_index = random.randint(0, len(self.__feed_table)-1)
#         return self.__feed_table[random_index].fid
#
#     # 타겟범위내의 Feed를 반환
#     def get_feeds_target_range(self, index, target_index=0):
#         return self.__feed_table[target_index:index][::-1]
#
#     # 시간 차이를 바탕으로 정해진 시간대 내의 피드 정보 구하기
#     # target_hour : 1, 24, 168
#     def find_target_index(self, target_hour=1):
#         target_index = len(self.__feed_table)
#
#         for i, managed_feed in enumerate(self.__feed_table):
#             # 삭제된 피드는 None으로 표시될것이라서
#             if managed_feed.fid == "":
#                 continue
#
#             if self.__get_time_diff(target_time=managed_feed.date, target_hour=target_hour):
#                 continue
#             else:
#                 target_index = i
#                 break
#
#         return target_index
#
#     # Managed Feed 찾기
#     def search_managed_feed(self, fid):
#         return self.__feed_avltree.get(key=fid)
#
#     # 키, 옵션을 통해 Feed를 찾음
#     # 페이징기법을 적용했음. 역순페이징을 사용함.
#     def search_feed_with_key_and_option(self, option:str, key:str="", num_feed=10, index=-1) -> tuple:
#         result_fid = []
#         result_index = -3
#
#         if index == -1:
#             index = self.len_feed_table()
#
#             # target_index default 값은 0
#         search_range = self.get_feeds_target_range(index=index)
#         # search_range = self.__feed_table[:index][::-1]
#
#         if index < 0 or index > self.len_feed_table():
#             return result_fid, -3
#
#         count = 0
#         for i, managed_feed in enumerate(search_range):
#             #i = len(self.__feed_table) - 1 - i
#             # count로 이미 다 살펴 봤다면
#             if count == num_feed:
#                 break
#
#             # 삭제된 피드는 None으로 표시될것이라서
#             if managed_feed.fid == "":
#                 continue
#
#             if option == "hashtag":
#                 # 찾는 해시태그가 아님
#                 if key not in managed_feed.hashtag:
#                     continue
#             elif option == "uname":
#                 if key not in managed_feed.uname:
#                     continue
#             elif option == "bid":
#                 if key != managed_feed.bid:
#                     continue
#
#             elif option == "fid":
#                 if key == managed_feed.fid:
#                     result_fid.append(managed_feed)
#                     result_index = i
#                     break
#
#
#             result_fid.append(managed_feed.fid)
#
#             # result_index 업데이트
#             # 마지막 index 발견
#             result_index = index - 1 - i  # 실제 self.__feed_table에서의 인덱스 계산
#             count += 1
#
#         return result_fid, result_index
#
#     def search_feeds_with_key_n_option(self, key:str, option):
#         # Nan값의 경우, False 처리.
#         # 대소문자를 구분하지 않음
#         searched_df = self.__feed_df
#
#         if option == "keyword":
#             # 키워드를 통한 서치
#             searched_df = self.__feed_df[self.__feed_df["body"].str.contains(key, case=False, na=False)]
#         elif option == "hashtag":
#             # 해시태그 리스트 안에 들어있는 해시태그들 중 하나만 있어도 찾는다.
#             searched_df = self.__feed_df[self.__feed_df["hashtag"].apply(lambda hashtag: key in hashtag)]
#         elif option == "uname":
#             # 닉네임 서치
#             searched_df = self.__feed_df[self.__feed_df["uname"] == key]
#         elif option == "bid":
#             # bid 서치
#             searched_df = self.__feed_df[self.__feed_df["bid"] == key]
#         elif option == "fid":
#             # fid 서치
#             searched_df = self.__feed_df[self.__feed_df["fid"] == key]
#
#         return searched_df['fid'].tolist()
#     #---------------------------------------------------------------------------------------------
#
#     # 최애의 정보 하나 반환
#     def get_managed_bias(self, bid):
#         return self.__bias_avltree.get(key=bid, default=None)
#
#     def get_all_managed_bias(self):
#         return list(self.__bias_avltree.values())
#
#     def get_liked_biases(self, bids):
#         result = []
#         for bid in bids:
#             if bid in self.__bias_avltree:
#                 result.append(self.__bias_avltree.get(key=bid, default=None))
#
#         return result
#
#     # 새롭게 최애를 지정했을 때 연결하는 시스템
#     # 근데 이거 잘생각해보면 최애 지정하기 전에 쓴 글들은 해시태그에 반영되어야 하는가?
#     def add_new_user_to_bias(self, bid:str, uid:str):
#         managed_bias:ManagedBias = self.__bias_avltree.get(key=bid)
#         user_node = self.__feed_algorithm.get_user_node_with_uid(uid=uid)
#         managed_bias.user_nodes.append(user_node)
#         return
#
#     # 최애 연결 끊기
#     def remove_user_to_bias(self, bid:str, uid:str):
#         managed_bias:ManagedBias = self.__bias_avltree.get(key=bid)
#         user_node = self.__feed_algorithm.get_user_node_with_uid(uid=uid)
#         managed_bias.user_nodes.remove(user_node)
#         return
#
# #----------------------------------------------------------------------------------------------
#     def filtering_bias_community(self, bids:list, board_type:str):
#         filtered_feeds_df = self.__feed_df[self.__feed_df['bid'].isin(bids)]
#         if board_type != "":
#             filtered_feeds_df = filtered_feeds_df[filtered_feeds_df['board_type'] == board_type]
#         return filtered_feeds_df['fid'].tolist()
#
#     # 여기서는 추가적인 필터링을 위해 필터링된 FID리스트를 받고, 2차 필터링을 실시하는 곳입니다.
#     def filtering_fclass_feed(self, fid_list:list, fclass:str) -> list:
#         fid_list_df = self.__feed_df[(self.__feed_df['fid'].isin(fid_list))]
#         # Filtering 시, 다음의 값을 유의
#         # fclass == ""인 경우, 모든 경우를 가져옵니다. 어짜피 AD는 Notice의 경우로 들어가니까 상관없겠지요.
#         if fclass != "":
#             filtered_feeds_df = fid_list_df[(fid_list_df['fclass'] == fclass)]
#             return filtered_feeds_df['fid'].tolist()
#         return fid_list_df['fid'].tolist()
#
#     def filtering_category_feed(self, fid_list:list, category:str) -> list:
#         fid_list_df = self.__feed_df[(self.__feed_df['fid'].isin(fid_list))]
#         # Filtering 시, 다음의 값을 유의
#         # category == ""인 경우, 모든 경우를 가져옵니다. 똑같이 AD는 현재 아예 다른 모델을 사용하므로... 고려대상에서 제외합니다.
#         if category != "" :
#             filtered_feeds_df = fid_list_df[(fid_list_df['board_type'] == category)]
#             # pprint(filtered_feeds_df)
#             return filtered_feeds_df['fid'].tolist()
#         return fid_list_df['fid'].tolist()
#
#     def filtering_categories_feed_new(self, fid_list:list, categories:list):
#         fid_list_df = self.__feed_df[(self.__feed_df['fid'].isin(fid_list))]
#         # Filtering 시, 다음의 값을 유의
#         # fclass == ""인 경우, 모든 경우를 가져옵니다. 어짜피 AD는 Notice의 경우로 들어가니까 상관없겠지요.
#         if categories[0] != "":
#             filtered_feeds_df = fid_list_df[(fid_list_df['board_type'].isin(categories))]
#             # pprint(filtered_feeds_df)
#             return filtered_feeds_df['fid'].tolist()
#         return fid_list_df['fid'].tolist()

#---------------------------------------------------------------------------------------------------------------------------------------

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

    # 피드 매니저가 관리중인 피드를 보기 위해 만든 함수
    def try_search_managed_feed(self, fid):
        return self.__search_manager.try_search_managed_feed(fid=fid)
    
    # 새로운  관리 피드를 추가하는 함수
    def try_make_new_managed_feed(self, feed):
        # 알고리즘에도 추가해야되ㅏㅁ
        self.__search_manager.try_make_new_managed_feed(feed)
        self.try_add_feed(feed=feed)
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

    def try_search_feed_new(self, target_type="default", target=""):
        fid_list = []

        if target_type == "hashtag":
            fid_list = self.__search_manager.search_feeds_with_hashtag_new(hashtag=target)
        elif target_type == "fid":
            fid_list = self.__search_manager.search_feeds_with_fid_new(fid=target)
        elif target_type == "uname":
            fid_list = self.__search_manager.search_feeds_with_uname_new(uname=target)
        elif target_type == "bid":
            fid_list = self.__search_manager.search_feeds_with_bid_new(bid=target)
        elif target_type == "keyword":
            fid_list = self.__search_manager.search_feeds_with_keyword_new(keyword=target)

        else:
            print("default 가 입력됨")
            pass

        return fid_list

    def try_search_comment_new(self, target=""):
        result_cid = self.__search_manager.search_comments_with_keyword_new(keyword=target)
        return result_cid

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

        # bid로 검색한 피드 (최애의 ID)
        elif target_type == "bid":
            result_fid, result_index = self.__search_manager.search_feed_with_bid(bid=target, num_feed=num_feed, index=index)

        elif target_type == "keyword":
            pass
        # elif target_type == "string":
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

    def try_filtered_feed_with_option(self, fid_list:list, option:str, keys:list):
        # 옵션과 키에 따라 필터링이 나뉘어진다.
        return self.__filter_manager.filtered_feed_option_and_key(fid_list=fid_list, option=option, keys=keys)

    # 최애 페이지에서 요청
    def try_feed_with_bid_n_filtering(self, target_bids:list[str]=[""], category=""):
        return self.__filter_manager.filtering_community(bids=target_bids, category=category)

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
    #def __init__(self, database:Local_Database, feed_algorithm : FeedAlgorithm):
    def __init__(self, database, feed_algorithm=None, managed_feed_bias_table:ManagedFeedBiasTable=None):
        self.__database = database
        self.__feed_algorithm=feed_algorithm
        self.__managed_feed_bias_table=managed_feed_bias_table
    

        # best_feed_table이 필요한가? 필요없는거 같은데?
        self.__best_feed_table = [] # 좋아요가 30개 이상인 피드 테이블 | 최신 기준 

        # self.__feed_table = [] # 최신 기준으로 쌓이는 피드 스택 | 인덱스를 활용할 것
        # self.__feed_avltree = AVLTree()

        # 테이블 초기화
        # self.__init_feed_table(database=database)
        # self.__init_feed_avltree()

    def try_get_random_feed(self):
        return self.__managed_feed_bias_table.get_random_feed()

    def try_make_new_managed_feed(self, feed:Feed):
        self.__managed_feed_bias_table.make_new_managed_feed(feed)
        return

    # 피드 매니저에서 사용가능하게 만든 검색 기능
    def try_search_managed_feed(self, fid):
        return self.__managed_feed_bias_table.search_managed_feed(fid)

    # 이런 함수를 미리 만들어서 쓰면 좋음
    # 아래는 예시

    # # 예시 1 | 특정 인덱스의 피드를 뽑아오기
    # def __get_feed_data_in_index(self, index):
    #     return self.__feed_table[index]
    #
    # # 예시 2 | 특정 인덱스 아래의 피드를 모두 뽑아오기
    # def __get_feed_from_index_to_everything(self, index):
    #     return self.__feed_table[:index]
    #

    # =========================================================================
    # # 피드 테이블을 수정하는 함수
    # def modify_feed_table(self, feed:Feed):
    #     # managed_feed를 찾아야됨
    #     managed_feed:ManagedFeed = self.__feed_avltree.get(feed.fid)
    #
    #     # managed_feed가 가진 데이터로 원본 데이터를 변경
    #     managed_feed.date = feed.date
    #     managed_feed.hashtag = feed.hashtag
    #     managed_feed.like = feed.star
    #     managed_feed.uname = feed.nickname
    #     return
    #
    # # 삭제하는 함수. 피드가  삭제되면 None으로 바뀔것
    # def remove_feed(self, feed:Feed):
    #     managed_feed = self.__feed_avltree.get(key=feed.fid)
    #     managed_feed = ManagedFeed()
    #     self.__feed_avltree.remove(key=feed.fid)
    #     return
    #
    # def __get_datetime_now(self):
    #     now = datetime.now()
    #     return now
    #
    # # string to datetime
    # def __get_date_str_to_object(self, str_date):
    #     date_obj = datetime.strptime(str_date, "%Y/%m/%d-%H:%M:%S")
    #     return date_obj
    #
    # # datetime to string
    # def __get_date_object_to_str(self, object:datetime):
    #     formatted_str = object.strftime("%Y/%m/%d-%H:%M:%S")
    #     return formatted_str
    #
    # # 시간 차이를 분석하는 함수
    # # target_hour : 1, 24, 168
    # def __get_time_diff(self, target_time, reference_time=datetime.now(),
    #                    target_hour=2) -> bool:
    #     time_diff = abs(target_time - reference_time)
    #
    #     # 차이가 2시간 이상인지 확인
    #     return time_diff >= timedelta(hours=target_hour)
    #
    # # 시간 차이를 바탕으로 정해진 시간대 내의 피드 정보 구하기
    # # target_hour : 1, 24, 168
    # def __find_target_index(self, target_hour=1):
    #     target_index = len(self.__feed_table)
    #
    #     for i, managed_feed in enumerate(self.__feed_table):
    #         # 삭제된 피드는 None으로 표시될것이라서
    #         if managed_feed.fid == "":
    #             continue
    #
    #         if self.__get_time_diff(target_time=managed_feed.date, target_hour=target_hour):
    #             continue
    #         else:
    #             target_index = i
    #             break
    #
    #     return target_index
    #
    # =========================================================================

    # 목표시간을 바탕으로 피드를 찾는 함수
    # search_type == "all", "best"
    def try_get_feed_with_target_hour(self, search_type="all", num_feed=4, target_hour=1, index=-2):
        result_fid = []
        result_index = -3
        feed_table_len = self.__managed_feed_bias_table.len_feed_table()

        if index == -1 or index == -2:
            index = feed_table_len

        if target_hour > 0 :
            target_index = self.__managed_feed_bias_table.find_target_index(target_hour=target_hour)
        else:
            target_index = 0

        # 이거는 페이징 기법이 적용되어있음.
        search_range = self.__managed_feed_bias_table.get_feeds_target_range(index=index, target_index=target_index)
        # search_range = self.__feed_table[target_index:index][::-1]

        if index < target_index  or index > feed_table_len:
            return result_fid, -3

        count = 0

        if search_type == "all":
            for i, managed_feed in enumerate(search_range):
                if count == num_feed:
                    break
                
                # 삭제된 피드는 None으로 표시될것이라서
                if managed_feed.display < 3:
                    continue
                # if managed_feed.fid == "":
                #     continue

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
    def search_feed_with_hashtag(self, hashtag, num_feed=10, index=-1) -> tuple:
        result_fid, result_index = self.__managed_feed_bias_table.search_feed_with_key_and_option(
            option="hashtag",
            key=hashtag,
            num_feed=num_feed,
            index=index
        )
        return result_fid, result_index

    def search_feed_with_fid(self, fid, num_feed=1, index=-1) -> tuple:
        result_fid, result_index = self.__managed_feed_bias_table.search_feed_with_key_and_option(
            option="fid",
            key=fid,
            num_feed=num_feed,
            index=index
        )
        return result_fid, result_index

    def search_feed_with_uname(self, uname, num_feed=1, index=-1) -> tuple:
        result_fid, result_index = self.__managed_feed_bias_table.search_feed_with_key_and_option(
            option="uname",
            key=uname,
            num_feed=num_feed,
            index=index
        )
        return result_fid, result_index

    def search_feed_with_bid(self, bid, num_feed=10, index=-1) -> tuple:
        result_fid, result_index = self.__managed_feed_bias_table.search_feed_with_key_and_option(
            option="bid",
            key=bid,
            num_feed=num_feed,
            index=index,
        )
        return result_fid, result_index

#--------------------------------------------------------------------------------------------------------------------

    def search_feeds_with_hashtag_new(self, hashtag:str):
        fid_list = self.__managed_feed_bias_table.search_feeds_with_key_n_option(key=hashtag, option="hashtag")
        return fid_list

    def search_feeds_with_keyword_new(self, keyword: str):
        fid_list = self.__managed_feed_bias_table.search_feeds_with_key_n_option(key=keyword, option="keyword")
        return fid_list

    def search_feeds_with_uname_new(self, uname: str):
        fid_list = self.__managed_feed_bias_table.search_feeds_with_key_n_option(key=uname, option="keyword")
        return fid_list

    def search_feeds_with_bid_new(self, bid: str):
        fid_list = self.__managed_feed_bias_table.search_feeds_with_key_n_option(key=bid, option="keyword")
        return fid_list

    def search_feeds_with_fid_new(self, fid: str):
        fid_list = self.__managed_feed_bias_table.search_feeds_with_key_n_option(key=fid, option="keyword")
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
            print(e)

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
            print(e)

    def __total_keyword_setting(self):
        pass

    # 매 시간마다 갱신되는 비동기성 함수
    async def check_trend_hashtag(self):
        try:
            time_diff = 1
            current_time = time.time()
            while True:
                # time_diff 계산

                # 만약 마지막으로 연산한지 1시간이 지났으며 다시 연산
                if time_diff >= 1:
                    self.__total_hashtag_setting()
                    self.__bias_hashtag_setting()
                    # 이거 오류안남? current_time 생성위치가 밑에 있는데 없는 변수 만드는 거 아니냐.
                    # 그러네 이거 왜 오류 안났냐 왜 서버에서는 정상동작 하는건데...

                    self.last_computed_time = current_time
                    # 시간 간격이 1시간 미만인 경우
                else:
                    await asyncio.sleep(60)  # 너무 자주 루프를 돌지 않도록 대기

                current_time = time.time()
                if hasattr(self, 'last_computed_time'):
                    time_diff = (current_time - self.last_computed_time) / 3600  # 시간 단위로 계산
                else:
                    self.last_computed_time = current_time
                time_diff = 0

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
        index = self.__managed_feed_bias_table.len_feed_table()

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


    # # 비로그인 유저를 위한 로직
    # def get_recommend_feed_not_login(self, fid:str, history:list):
    #     hashtag_ranking_list = self.get_best_hashtags() # 해시태그 랭킹 리스트
    #     # 비로그인을 위한 로직
    #     fid = self.__feed_algorithm.recommend_next_feed_not_login(
    #         start_fid=fid,
    #         history=history,
    #         hashtag_ranking=hashtag_ranking_list
    #     )
    #     return fid

# 필터링 매니저
class FilteringManager:
    def __init__(self, database, feed_algorithm=None, managed_feed_bias_table:ManagedFeedBiasTable=None):
        self.__database = database
        self.__feed_algorithm:FeedAlgorithm = feed_algorithm
        self.__managed_feed_bias_table=managed_feed_bias_table

#--------------------실제로 사용하게 될 구간입니다. 필터링 옵션이 확정났기 때문에 이렇게 새로만듭니다----------------------------------------------

    def __paging_list(self, fid_list:list, fid, page_size):
        # 이미 Date 최신순으로 정렬되어서 맨처음이 젤 최신의 글임
        start_index = 0

        # 페이징을 하지 않음
        if page_size == -1:
            return fid_list

        if fid != "":
            start_index = fid_list.index(fid)  # 타겟으로 잡은 구간부터, 불러오기

        paging_fid_list = fid_list[start_index:]        # 페이징으로 짜르기
        # 만약 자른 리스트가 페이지를 넘어간다면 짤라야한다
        if len(paging_fid_list) > page_size:
            paging_fid_list = paging_fid_list[:page_size]

        # Paging Fid List, Last_fid
        return paging_fid_list, paging_fid_list[-1]

    def _filtering_notices_list(self):
        notice_datas = self.__database.get_all_data(target="notice")
        notices = []

        for notice_data in notice_datas:
            notice = Notice()
            notice.make_with_dict(notice_data)
            notices.append(notice)

        return notices

    def filtered_feed_option_and_key(self, fid_list:list, option:str, keys:list):
        if option == "fclass":
            # 키가 하나밖에 없기 때문에.. keys[0]만으로 판별해야한다.
            # Fclass == ""인 경우, Managed_Feed_table에서 처리하도록 하였음
            return self.__managed_feed_bias_table.filtering_fclass_feed(fid_list=fid_list, fclass=keys[0])

        elif option == "category":
            # 구분하기 쉽도록 하였음. 또한, category가 []인 상태라면 뒤에 나올 반복문 자체가 동작하지 않는다.
            # category = []인 경우. 1차 필터링을 거친 것을 그대로 반환

            filtered_fid_list = []
            # 조건문을 추가했음
            if len(keys) <= 0 or keys[0] == "":
                filtered_fid_list = fid_list

            # if "공지사항" in keys:
            #     notice_list = self._filtering_notices_list()
            #     filtered_fid_list.extend(notice_list)
            #     keys.remove("공지사항")
            else:
                temp_list = self.__managed_feed_bias_table.filtering_categories_feed_new(fid_list=fid_list, categories=keys)

                filtered_fid_list.extend(temp_list)
            return filtered_fid_list

    # BID로 필터링 하는 작업 수행, 카테고리별 필터링도 진행 됨
    def filtering_community(self, bids:list, category:str):
        return self.__managed_feed_bias_table.filtering_bias_community(bids=bids, board_type=category)
