# 검색엔진이 해야하는일

# 1. 키워드를 통한 피드 검색
# 2. 특정 피드 다음으로 제시할 피드 검색
# 3. 피드 분석 및 최신화
# 4. 추천 피드 제공

# LocalDatabase의 import 문제로 아래 코드는 정상동작 하지 않으니
# 코드를 작성하는 도중에는 주석을 해제하여 LocalDatabase 함수를 자동완성하고
# 실행할때는 다시 주석처리하여 사용할것
#from model import Local_Database

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
import random

from collections import Counter

#--------------------------------------------------------------------------------------------------

# 이건 아래에 피드 테이블에 들어가야되는 피드 자료형
# 데이터 베이스에서 피드 데이터 받아서 만들꺼임
# 필요한 데이터는 언제든 추가가능

# 이게 검색에 따른 피드를 제공하는 클래스
# 위에 FeedAlgorithm에서 작성한 내용을 가지고 와도됨

# 클래스 목적 : 피드를 검색하거나, 조건에 맞는 피드를 제공하기 위함
class ManagedFeed:
    def __init__(self, fid="", like=0, date=None, uname="", fclass="",
                 board_type="", hashtag=[], bid="", iid="", num_images=0):
        self.fid=fid
        self.fclass = fclass
        self.like=like
        self.date=date
        self.uname = uname
        self.hashtag = hashtag
        self.board_type = board_type
        self.bid = bid
        self.iid = iid
        self.num_images = num_images

    # 무슨 데이터인지 출력해보기
    def __call__(self):
        print("fid : ", self.fid)
        print("fclass: ", self.fclass)
        print("like : ", self.like)
        print("date: ", self.date)
        print("uname: ", self.uname)
        print("hashtag: ", self.hashtag)
        print("board_type: ", self.board_type)
        print("bid: ", self.bid)
        print("iid: ", self.iid)
        print("num_images: ", self.num_images)

    def to_dict(self):
        return {
            "fid": self.fid,
            "fclass": self.fclass,
            "like": self.like,
            "date": self.date,
            "uname": self.uname,
            "hashtag": self.hashtag,
            "board_type": self.board_type,
            "bid": self.bid,
            "iid": self.iid,
            "num_images": self.num_images
        }

# 이거는 Bias 테이블에 들어가게 되는 Bias 자료형
# 데이터베이스에 받아서 만들어진다.
class ManagedBias:
    def __init__(self, bid, user_nodes:list, board_types:list):
        self.bid = bid
        self.trend_hashtags = []
        self.user_nodes:list = user_nodes
        self.board_types:list = board_types

    def to_dict(self):
        return {
            "bid": self.bid,
            "trend_hashtags": self.trend_hashtags,
            "board_types": copy(self.board_types)
        }

# ManagedFeed 테이블 클래스.
# 기존의 SearchEngine 에서는 각 Manager마다 각기 정의된 ManagedTable을 가졌는데
# 너무 복잡해짐에 따라, 통합하기로 결정. 클래스화 시킵니다.
class ManagedFeedBiasTable:
    def __init__(self, database, feed_algorithm):
        self.__database = database
        self.__feed_algorithm = feed_algorithm
        self.__feed_table =[]
        self.__feed_df = pd.DataFrame()
        self.__feed_avltree = AVLTree()
        self.__bias_avltree = AVLTree()

        self.__init_feed_table()
        self.__init_bias_tree()

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

    # Initialize 테이블
    def __init_feed_table(self):
        feeds = []
        # 먼저 피드 데이터를 DB에서 불러오고
        feed_datas = self.__database.get_all_data(target="fid")

        # 불러온 피드들은 객체화 시켜준다음 잠시 보관
        for feed_data in feed_datas:
            feed = Feed()
            feed.make_with_dict(dict_data=feed_data)
            feeds.append(feed)

        # 잠시 보관한 피드 데이터에서 필요한 정보만 뽑아서 ManagedFeed 객체 생성
        for single_feed in feeds:
            managed_feed = ManagedFeed(fid=single_feed.fid,
                                       fclass=single_feed.fclass,
                                       like=single_feed.star,
                                       date=self.__get_date_str_to_object(single_feed.date),
                                       hashtag=copy(single_feed.hashtag),
                                       uname=single_feed.nickname,
                                       board_type=single_feed.board_type,
                                       bid=single_feed.bid,
                                       iid=single_feed.iid,
                                       num_images=len(single_feed.image)
                                       )
            # 보관
            self.__feed_table.append(managed_feed)

        # 리턴되면 위에서 잠시 보관한 피드 데이터는 사라지고 self.__feed_table에 ManagedFeed들만 남음
        # 최신이 가장 밑으로 오지만, 데이터프레임만 최신 내림차순으로 정렬할 것
        self.__feed_table = sorted(self.__feed_table, key=lambda x:x.date, reverse=False)
        self.__feed_df = self.__dataframing_feed_list()

        num_feed = str(len(self.__feed_table))
        print(f'INFO<-[      {num_feed} NOVA FEED IN SEARCH ENGINE NOW READY.')
        print(f'INFO<-[      {num_feed} NOVA FEED DATAFRAME IN SEARCH ENGINE NOW READY.')

        return

    # Feed_avltree 설정
    def __init_feed_avltree(self):
        for feed in self.__feed_table:
            self.__feed_avltree.insert(feed.fid, feed)
        print(f'INFO<-[      NOVA FEED AVLTREE IN SEARCH ENGINE NOW READY.')

    # Bias Tree 설정
    def __init_bias_tree(self):
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
                if single_bias.bid in single_user.bids:
                    user_node = self.__feed_algorithm.get_user_node_with_uid(uid=single_user.uid)
                    # 못찾 으면 예외 처리할 것
                    if user_node:
                        user_nodes.append(user_node)

            # 이제 관리될 바이어스를 만들고 연결한다음
            managed_bias = ManagedBias(bid=single_bias.bid, user_nodes=user_nodes, board_types=single_bias.board_types)
            # avl트리에 넣어주면됨
            self.__bias_avltree.insert(key=single_bias.bid, value=managed_bias)

        return

    # Feed list DataFrame화
    def __dataframing_feed_list(self):
        # ManagedFeed들은 객체이므로, 딕셔너리화 시켜서 리스트로 만든다.
        managed_feed_dict_list = [managed_feed.to_dict() for managed_feed in self.__feed_table]
        feed_df = pd.DataFrame(managed_feed_dict_list)
        # 데이터프레임을 정렬함
        feed_df = feed_df.sort_values(by='date', ascending=False).reset_index(drop=True)

        return feed_df

    def __add_new_data_in_df(self, managed_feed):
        new_data = pd.DataFrame(managed_feed.to_dict())
        self.__feed_df = pd.concat([self.__feed_df, new_data], ignore_index=True)
        self.__feed_df = self.__feed_df.sort_values(by='date', ascending=False).reset_index(drop=True)
        return

    def __modify_data_in_df(self, new_managed_feed):
        new_data = new_managed_feed.to_dict()
        # fid는 고유값이므로, 하나밖에 안 나옴
        update_index = self.__feed_df.index[self.__feed_df['fid'] == new_managed_feed.fid].tolist()[0]
        self.__feed_df.loc[update_index] = new_data

        return

    def __remove_data_in_df(self, fid):
        remove_index = self.__feed_df.index[self.__feed_df['fid'] == fid].tolist()[0]
        self.__feed_df = self.__feed_df.drop(index=remove_index).reset_index(drop=True)
        return

    #---------------------------------------------------------------------------------------------
    def len_feed_table(self):
        # Feed Table의 길이 구하기
        return len(self.__feed_table)

    # 새로운 ManagedFeed를 추가함
    def make_new_managed_feed(self, feed:Feed):
        managed_feed = ManagedFeed(
            fid=feed.fid,
            fclass=feed.fclass,
            like=feed.star,
            date=self.__get_date_str_to_object(feed.date),
            uname=feed.nickname,
            hashtag=feed.hashtag,
            board_type=feed.board_type, # 이거 추가됨
            bid=feed.bid,
            iid=feed.iid,
            num_images=feed.num_image
        )

        self.__feed_table.append(managed_feed)
        self.__feed_avltree.insert(managed_feed.fid, managed_feed)
        # 데이터 프레임 추가
        self.__add_new_data_in_df(managed_feed)

        return

    # ManagedFeedTable을 수정, 새로운 Feed가 들어왔기 때문
    def modify_feed_table(self, feed:Feed):
        # 피드 테이블을 수정하는 함수
        # managed_feed를 찾아야 됨
        managed_feed:ManagedFeed = self.__feed_avltree.get(feed.fid)

        # managed_feed가 가진 데이터로 원본 데이터를 변경
        managed_feed.date = feed.date
        managed_feed.hashtag = feed.hashtag
        managed_feed.like = feed.star
        managed_feed.uname = feed.nickname

        # dataframe도 업데이트
        self.__modify_data_in_df(managed_feed)

        return

    # ManagedFeed가 삭제되었기 때문에, 테이블과 트리에서도 삭제시킴
    def remove_feed(self, feed:Feed):
        # 삭제하는 함수. 피드가  삭제되면 None으로 바뀔것
        managed_feed = self.__feed_avltree.get(key=feed.fid)
        managed_feed = ManagedFeed()
        self.__feed_avltree.remove(key=feed.fid)
        # dataframe 삭제
        self.__remove_data_in_df(fid=feed.fid)
        return

    # 랜덤한 Feed 하나 추출
    def get_random_feed(self):
        random_index = random.randint(0, len(self.__feed_table)-1)
        return self.__feed_table[random_index].fid

    # 타겟범위내의 Feed를 반환
    def get_feeds_target_range(self, index, target_index=0):
        return self.__feed_table[target_index:index][::-1]

    # 시간 차이를 바탕으로 정해진 시간대 내의 피드 정보 구하기
    # target_hour : 1, 24, 168
    def find_target_index(self, target_hour=1):
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

    # Managed Feed 찾기
    def search_managed_feed(self, fid):
        return self.__feed_avltree.get(key=fid)

    # 키, 옵션을 통해 Feed를 찾음
    # 페이징기법을 적용했음. 역순페이징을 사용함.
    def search_feed_with_key_and_option(self, option:str, key:str="", num_feed=10, index=-1) -> tuple:
        result_fid = []
        result_index = -3

        if index == -1:
            index = self.len_feed_table()

            # target_index default 값은 0
        search_range = self.get_feeds_target_range(index=index)
        # search_range = self.__feed_table[:index][::-1]

        if index < 0 or index > self.len_feed_table():
            return result_fid, -3

        count = 0
        for i, managed_feed in enumerate(search_range):
            #i = len(self.__feed_table) - 1 - i
            # count로 이미 다 살펴 봤다면
            if count == num_feed:
                break

            # 삭제된 피드는 None으로 표시될것이라서
            if managed_feed.fid == "":
                continue

            if option == "hashtag":
                # 찾는 해시태그가 아님
                if key not in managed_feed.hashtag:
                    continue
            elif option == "uname":
                if key not in managed_feed.uname:
                    continue
            elif option == "bid":
                if key != managed_feed.bid:
                    continue

            elif option == "fid":
                if key == managed_feed.fid:
                    result_fid.append(managed_feed)
                    result_index = i
                    break


            result_fid.append(managed_feed.fid)

            # result_index 업데이트
            # 마지막 index 발견
            result_index = index - 1 - i  # 실제 self.__feed_table에서의 인덱스 계산
            count += 1

        return result_fid, result_index

    #---------------------------------------------------------------------------------------------

    # 최애의 정보 하나 반환
    def get_managed_bias(self, bid):
        return self.__bias_avltree.get(key=bid, default=None)

    def get_all_managed_bias(self):
        return list(self.__bias_avltree.values())

    def get_liked_biases(self, bids):
        result = []
        for bid in bids:
            if bid in self.__bias_avltree:
                result.append(self.__bias_avltree.get(key=bid, default=None))

        return result

    # 새롭게 최애를 지정했을 때 연결하는 시스템
    # 근데 이거 잘생각해보면 최애 지정하기 전에 쓴 글들은 해시태그에 반영되어야 하는가?
    def add_new_user_to_bias(self, bid:str, uid:str):
        managed_bias:ManagedBias = self.__bias_avltree.get(key=bid)
        user_node = self.__feed_algorithm.get_user_node_with_uid(uid=uid)
        managed_bias.user_nodes.append(user_node)
        return

    # 최애 연결 끊기
    def remove_user_to_bias(self, bid:str, uid:str):
        managed_bias:ManagedBias = self.__bias_avltree.get(key=bid)
        user_node = self.__feed_algorithm.get_user_node_with_uid(uid=uid)
        managed_bias.user_nodes.remove(user_node)
        return

    #---------------------------------------------------------------------------------------------
    # 바이어스 커뮤니티에 따라 Feed를 분류함
    # 데이터프레임 활용
    def __paging_list_df(self, fid_list:list, fid, page_size):
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

        return paging_fid_list

    def filtering_bias_community(self, bids:list, last_fid, page_size:int):
        # Feed DF 중, bids안에 포함된 feed들만 반환함.
        filtered_feeds_df = self.__feed_df[self.__feed_df['bid'].isin(bids)]
        # 필터링된 Feed들의 리스트를 반환, 페이징기법을 적용한다
        return self.__paging_list_df(fid_list=filtered_feeds_df['fid'].tolist(),
                                     fid=last_fid, page_size=page_size)

    # Board만 선택
    def filtering_board_without_bid(self, last_fid:str, page_size:int, board_type:str):
        filtered_feeds_df = self.__feed_df[(self.__feed_df['board_type'] == board_type)]
        return self.__paging_list_df(fid_list=filtered_feeds_df['fid'].tolist(),
                                     fid=last_fid, page_size=page_size)

    def filtering_community_board(self, last_fid:str, page_size:int, bid:str, board_type:str):
        # 게시판 분리하여 필터링
        # 이 때, BID를 통한 필터링도 같이 선행되어야 함.
        filtered_feeds_df = self.__feed_df[(self.__feed_df['bid'] == bid) & (self.__feed_df['board_type'] == board_type)]
        return self.__paging_list_df(fid_list=filtered_feeds_df['fid'].tolist(),
                                     fid=last_fid, page_size=page_size)

    def filtering_choice_feed(self, bid:str, board_type:str, last_fid:str, page_size:int):
        # 투표 글만 필터링
        filtered_feeds_df = self.__feed_df[self.__feed_df['iid'] != ""]
        # 게시판 필터링
        filtered_feeds_df = filtered_feeds_df[(filtered_feeds_df['bid'] == bid) & (filtered_feeds_df['board_type'] == board_type)]
        return self.__paging_list_df(fid_list=filtered_feeds_df['fid'].tolist(),
                                     fid=last_fid, page_size=page_size)

    def filtering_image_in_feed(self, bid:str, board_type:str, last_fid:str, page_size:int):
        # 이미지 있는 Feed들만 골라서 뱉음
        filtered_feeds_df = self.__feed_df[self.__feed_df['num_images'] > 0]
        # 게시판 필터링
        filtered_feeds_df = filtered_feeds_df[(filtered_feeds_df['bid'] == bid) & (filtered_feeds_df['board_type'] == board_type)]
        return self.__paging_list_df(fid_list=filtered_feeds_df['fid'].tolist(),
                                     fid=last_fid, page_size=page_size)

#---------------------------------------------------------------------------------------------------------------------------------------
    # 여기서는 게시판 필터링을 거친 후, 추가적인 필터링을 위해 필터링된 FID리스트를 받고, 2차 필터링을 실시하는 곳입니다.
    def filtering_fclass_feed(self, fid_list:list, fclass:str, last_fid:str, page_size:int):
        # 2차 게시판 필터링. Long Form인지, Short Form인지, 그리고, Board_type도 관여하게 됨.
        fid_list_df = self.__feed_df[self.__feed_df['fid'].isin(fid_list)]
        # DF 내에서 다시 한번 더, 결과를 가져옴.
        filtered_feeds_df = fid_list_df[fid_list_df['fclass'] == fclass]
        return self.__paging_list_df(fid_list=filtered_feeds_df['fid'].tolist(),
                                     fid=last_fid, page_size=page_size)

        # filtered_feeds_df = self.__feed_df[(self.__feed_df['fclass'] == fclass) & (self.__feed_df['board_type'] == board_type)]
        # return self.__paging_list_df(fid_list=filtered_feeds_df['fid'].tolist(),
        #                              fid=last_fid, page_size=page_size)

    def filtering_staring_feed(self, fid_list:list, stars:int, last_fid:str, page_size:int):
        # 2차 게시판 필터링. 추천 수에 관여함.
        fid_list_df = self.__feed_df[self.__feed_df['fid'].isin(fid_list)]
        # 추천수가 일정 수 이상인 피드만 걸러줌
        filtered_feeds_df = fid_list_df[fid_list_df['stars'] > stars]

        return self.__paging_list_df(fid_list=filtered_feeds_df['fid'].tolist(),
                                     fid=last_fid, page_size=page_size)

    def filtering_nickname_feed(self, fid_list:list, nickname:str, last_fid:str, page_size:int):
        # 2차 게시판 필터링. 글쓴이 필터링에 관여합니다
        fid_list_df = self.__feed_df[self.__feed_df['fid'].isin(fid_list)]

        # 닉네임으로 Feed를 검색하는 기능
        filtered_feeds_df = fid_list_df[fid_list_df['nickname'] == nickname]
        return self.__paging_list_df(fid_list=filtered_feeds_df['fid'].tolist(),
                                     fid=last_fid, page_size=page_size)

#--------------------------------------------------------------------------------------------------

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
    
       
    # 최애 페이지에서 요청
    def try_feed_with_bid_n_filtering(self, target_bids:list[str]=[""], board_type="default",
                                      page_size=-1, last_fid="", search_type="default"
                                      ):
        result = []
        
        # 선택 없음 상태에서 요청
        if search_type == "default":
            result = self.__filter_manager.filtering_community(page_size=page_size, last_fid=last_fid, bids=target_bids)
        
        # bias만 선택했을 때 요청
        elif search_type == "just_bias":
            result = self.__filter_manager.filtering_community(page_size=page_size, last_fid=last_fid, bids=target_bids)

        # 야 이건 Bias 선택안하면 Board는 전체로만 나와야하는거 아니냐
        # Bias마다 Board가 다 달라지는거라고 생각했는ㄷ

        # bias를 선택하지 않고 board만 선택했을 때 요청
        # 이것만 추가되면됨 -> bid 말고 bids (list) 로 변경
        elif search_type == "board_only":
            result = self.__filter_manager.filtering_board_no_bid(board_type=board_type,
                                                                     last_fid=last_fid, page_size=page_size)
            
        # bias와 board를 모두 선택했들 때 요청
        elif search_type == "bias_and_board":
            result = self.__filter_manager.filtering_board_community(bid=target_bids[0], board_type=board_type,
                                                                     last_fid=last_fid, page_size=page_size)
        
        
        # 마지막 feed의 fid 반환
        if result:
            last_fid = result[-1]
            
        return result, last_fid

    def try_feed_filtering_with_class(self, fid_list:list, fclass="all", page_size=-1, last_fid=""):

        result = []
        result_last_fid = ""

        # 기능 통합 가능성이 있음.
        if fclass == "long" or fclass == "short":
            result, result_last_fid = self.__filter_manager.filtering_feed_type_in_result_feeds(fid_list=fid_list, fclass=fclass,
                                                                                                last_fid=last_fid, page_size=page_size)
        return result, result_last_fid

    # 여기도 아직 하지 말것 
    # 목적 : 숏피드에서 다음 피드 제공 받기
    def try_recommend_feed(self, fid:str, history:list, user:User):
        # 유저 비로그인 시 데이터가 처리가 어떻게 되는지 알아야 할듯
        # 그래야 여기에 If문을 통한 로직을 추가하던가, 아니면 기존 로직에서 바꾸든가를 알 수 있을듯
        # 근데 이미 비로그인 유저에 대한 로직을 만들긴 했음

        fid = self.__recommend_manager.get_recommend_feed(fid=fid,
                                                          history=history,
                                                          user=user
                                                          )

        # fid = self.__recommend_manager.get_recommend_feed_not_login(fid=fid, history=history)
        return fid

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

    # def search_feed_with_string(self, string, num_feed=10) -> list: #본문 내용을 가지고 찾는거같음
        #return self.__feed_algorithm.get_feed_with_string(string,num_feed)

# 이건 사용자에게 맞는 데이터를 주려고 만든거
class RecommendManager:
    def __init__(self, database, feed_algorithm=None, managed_feed_bias_table:ManagedFeedBiasTable=None):
        self.__database = database
        self.__feed_algorithm:FeedAlgorithm = feed_algorithm
        self.__managed_feed_bias_table=managed_feed_bias_table

        self.hashtags = []
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
            for hashtags in managed_feed.hashtags:
                # 해시태그 리스트를 가져오므로, 빈 리스트에 Extend로 이어 붙임.
                list_of_hashtags_in_hours.extend(hashtags)

        # 카운팅 후, 내림차순 정렬되서, 해시태그만 뽑아옴
        counting_hashtags = Counter(list_of_hashtags_in_hours)
        sorted_list_of_hashtag_count = [hashtag for hashtag, count in counting_hashtags.most_common()]

        return sorted_list_of_hashtag_count[0:num_hashtag]

    # 실시간 트랜드 해시태그 제공
    def get_best_hashtags(self, num_hashtag=10) -> list:
        return self.hashtags[0:num_hashtag]

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

#------------------------------------------------------------------------------------
    # BID로 필터링 하는 작업 수행
    def filtering_community(self, page_size, bids:list, last_fid=""):
        # Search Engine에 들어가기 전에 BID 리스트를 검사할거임
        # BID 리스트 요소는 1개가 될 수 있고, 아니면 선택을 하지 않아서 여러 개가 될 수 있음.
        return self.__managed_feed_bias_table.filtering_bias_community(bids=bids, last_fid=last_fid, page_size=page_size)

    def filtering_board_no_bid(self, board_type:str, page_size:int, last_fid=""):
        return self.__managed_feed_bias_table.filtering_board_without_bid(board_type=board_type, page_size=page_size, last_fid=last_fid)

    def filtering_board_community(self, bid:str, board_type:str, page_size:int, last_fid:str=""):
        # 게시판 타입마다 필터링하는 함수.
        return self.__managed_feed_bias_table.filtering_community_board(bid=bid, board_type=board_type, last_fid=last_fid, page_size=page_size)

    def filtering_choice_feed(self, bid:str, board_type:str, page_size:int, last_fid:str=""):
        # 게시판 중, 투표가 있는 Feed만 필터링
        return self.__managed_feed_bias_table.filtering_choice_feed(bid=bid, board_type=board_type, last_fid=last_fid, page_size=page_size)

    def filtering_image_in_feed(self, bid:str, board_type:str, page_size:int, last_fid:str=""):
        # 게시판 글 중, 이미지만 있는 글들만 필터링
        return self.__managed_feed_bias_table.filtering_image_in_feed(bid=bid, board_type=board_type, last_fid=last_fid, page_size=page_size)

    def filtering_feed_type_in_result_feeds(self, fid_list:list, fclass:str, page_size:int, last_fid:str=""):
        return self.__managed_feed_bias_table.filtering_fclass_feed(fid_list=fid_list, fclass=fclass, last_fid=last_fid, page_size=page_size)


    # # 이거 아직 안 됨
    # # 전체 게시글 중 필터링
    # def _filter_single_option_feed(self, feed_list, option):
    #     result = []
    #     for feed in feed_list:
    #         # 롱폼 / 숏폼
    #         if option == "long":
    #             if feed.fclass == "long":
    #                 result.append(feed)
    #         if option == "short":
    #             if feed.fclass == "short":
    #                 result.append(feed)
    #         if option == "choice":
    #             if feed.iid != "":
    #                 result.append(feed)
    #         if option == "quiz":
    #             if feed.iid != "":
    #                 continue
    #         if option == "funding":
    #             continue
    #         if option == "picture":
    #             if len(feed.image) != 0:
    #                 result.append(feed)
    #
    #     return result
    #
    # # 필터링된 Feed중 Fid만 추출하는 부분
    # def _extract_fid_in_feed_list(self, feed_list):
    #     result = []
    #
    #     for feed in feed_list:
    #         result.append(feed.fid)
    #
    #     return result
    #
    # # 피드를 필터링하는 함수
    # def filter_options_feeds(self, options:list):
    #     result = copy(self.__feed_table)
    #
    #     for option in options:
    #         result = self._filter_single_option_feed(result, option)
    #
    #     result = self._extract_fid_in_feed_list(result)
    #
    #     return result

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

        # 추가된 해시태그의 사용량 체크
        self.weight = 0         # Ranking에 사용되는 값인데 계산하는 함수가 따로 있음
        self.trend= {
            "now":0,            # 기준시간 ~ 1시간까지의 사용량 체크
            "prev":0            # 1시간 후 ~ 2시간 후 사용량 체크. 이전의 사용량 체크
        }

    # 노드 일치성 판단. 기록된 id를 통해 판단
    def __eq__(self, other):
        return self.hid == other.get_id()

    # 노드 출력 포맷
    def __str__(self):
        return 'Node({}, {}, {})'.format(self.get_id(), self.node_type, self.weight)

    # 리스트 전체 출력 포맷
    def __repr__(self):
        return 'Node({}, {}, {})'.format(self.get_id(), self.node_type, self.weight)

    # 아이디 반환 함수
    def get_id(self):
        return self.hid

    # Weight를 업 시킴
    # 글을 작성하는 시점 = Weight 중, now가 증가하는 시점
    # Feed를 수정하여, 새로운 해시태그가 생성될 때에도 이 함수가 적용
    def weight_up(self):
        self.trend["now"] += 1

    # Weight의 상태가 업데이트.
    # Weight는 recommend Manager에서 업데이트됨
    def weight_update(self, new_weight):
        self.weight = new_weight
        self.trend["prev"] = self.trend["now"]
        self.trend["now"] = 0

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
#         # 긴급 추가 (write_uid 정보를 feed 그래프 내에서 찾아오는 방법이 없어서 feed node 추가 시, 이것도 같이 들고옴.
#         write_uid = write_uid
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
    def __init__(self, fid, write_uid):
        super().__init__("feed") # 상속
        self.fid = fid          # Feed id
        self.write_uid = write_uid      # 작성한 User id
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
    def add_node(self, node_type, node_id, tree:AVLTree, write_uid:str=""):
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
            # feed 노드만의 특징, 작성한 유저의 아이디를 또하나의 값으로 가진다, 기본값은 ""로 한다.
            node = FeedNode(node_id, write_uid)
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

    # 피드-유저 사이에서 찾아내는 유사한 피드

    # 1단계 : 유저 상위 10명 집계
    # 2단계 : 유저 담기. 방문한 Feed_id 집계 : list()
    #	가장 중요한 건, 글쓴이에 대해서는 집계하지 않는다.
    #
    # 3단계 : 첫번째 줄에서 유저에 대한 feed 집계. 중복을 고려해 10개로 늘리고.
    # 	set()을 최대한 활용해 중복을 지워나가는 방향으로 잡는다
    #	방문했던 feed임이 확인되면, 가차없이 지워야함. 왜냐하면 똑같은 노드가 발생할 수 있기 때문.
    #	따라서, Set()을 사용한다.
    #
    # for user_node in user_queue:
    #	sorted_edges = sorted(user_node.edges["feed"])[:max_feed]
    #	for edge in sorted_edges:
    #		# 어짜피 set()을 사용하기 때문에, 중복은 알아서 없어짐
    #		related_fid = edge.target.id()
    #		if not in visited_feed:
    #			recommend_list.append(related_fid)
    #
    # noinspection PyMethodMayBeStatic
    def feed_recommend_by_like_user(self, start_node:FeedNode, max_user_find=10, max_feed_find=8):
        # 가장 먼저, Feed를 확인
        recommend_list = set()
        user_queue = []


        # 각 연결된 유저 edge를 찾음
        sorted_edges_latest_related = sorted(start_node.edges["user"])[:max_user_find]
        # 그 중, 가장 최근에 Feed에 관심을 가진(좋아요를 누른) 유저들 10명을 추려냄
        for edge in sorted_edges_latest_related:
            # 진짜 만약에 연결된 edge중에서 작성자와 연결된 edge들이 있을 경우, 그 노드만을 제외하고 추가한다.
            # 즉, 하나의 유저만 걸러지는 방법.
            if edge.target_node.get_id() != start_node.write_uid:
                user_queue.append(edge.target_node)

        # 이제, 그 유저들과 연결된 Feed를 담아내는 과정
        for user_node in user_queue:
            # 최신 순으로 정렬된 엣지 중에서, 최대 5개의 feed들을 가져올 것
            sorted_edges_latest_relate_feed = sorted(user_node.edges["feed"])[:max_feed_find]
            for edge in sorted_edges_latest_relate_feed:
                # 가져온 Edge에서 Feed id를 추출하여 recommend_list에 담음
                related_feed_id = edge.get_target_node().get_id()
                recommend_list.add(related_feed_id)


        # 시작Feed가 다시 추천리스트에 들어가는 것을 방지하기 위해 recommend_list에서 삭제 진행
        recommend_list.discard(start_node.fid)   # discard 쓰는 이유 (set()에 있을수도 있고, 없을 수도 있음. GPT 피셜임)

        return list(recommend_list)

    # 피드-해시태그 사이에서 찾아내는 유사한 피드

    # 1단계 : 시작한 Feed에 대한 해시태그 최대 4개에 대해 Edge 수집
    # 2단계 : Hash태그 담기. 방문한 Feed는 집계해야됨.
    # 3단계 : 해시태그에 대해 Feed를 집계함. 가장 최신의 글을 먼저 집계한다.
    #	여기서도 방문했던 Feed는 가차없이 지워야한다. (물론 이는 History에서 관리된다.)
    #	set()을 이용해 중복된 Feed는 지워내면서 추가하면 된다.
    #
    # for hash_node in hash_queue:
    #	sorted_edges = sorted(hash_node.edges["feed"])[:max_feed]
    #	for edge in sorted_edges:
    #		related_fid = edge.target.id()
    #		recommend_list.add(related_fid)
    #
    # 4단계 : 내가 본 Feed는 전부 쳐내야함.

    # noinspection PyMethodMayBeStatic
    def feed_recommend_by_hashtag(self, start_node:FeedNode, max_hash=4, max_feed_find=5):
        recommend_list = set()
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
                recommend_list.add(related_feed_id)

        # 시작Feed가 다시 추천리스트에 들어가는 것을 방지하기 위해 recommend_list에서 삭제 진행
        recommend_list.discard(start_node.fid)   # discard 쓰는 이유 (set()에 있을수도 있고, 없을 수도 있음. GPT 피셜임)

        return list(recommend_list)

    # User의 좋아요에 따라 Feed를 추천하는 시스템

    # 1단계: 로그인한 유저에게로부터 좋아요로 태깅된 Edge들을 통해 좋아요를 누른 Feed들을 모음
    # 2단계: 그렇게 모은 Feed들은 이미 본 Feed들이기 때문에 추천 feed에는 집계하지 않지만, 이 Feed들에 좋아요를 남긴 유저들을 찾는데 쓰임
    #   따라서, Feed에 좋아요를 남긴 유저들을 모음.
    # 3단계 : 이렇게 해서 모인 유저들에 따라, 좋아요한 Feed를 담음. 이 때, 내가 좋아요를 남겨서 찾아온 Feed에 대해서는 담지않음

    # noinspection PyMethodMayBeStatic
    def feed_recommend_by_me(self, watch_me:UserNode, max_like=10, max_related_user=4, max_feed_find=5):
        # 비로그인 유저는 빈 리스트를 반환
        if watch_me.get_id() == "":
            return []


        # 중복된 Feed를 방지하기 위해서
        recommend_list = set()
        visited_like_feeds = []
        # 내가 좋아한 Feed들에 대해 같은 유저가 다른 2개의 Feed들도 동시에 좋아할 수 있음
        # visited like_user_queue는 user가 변할수 있는 노드이기 떄문에 set() 사용x
        # 오류가 발생한 부분, unhashable Error
        # 잘못된 Set()의 사용이 불러온 오류임.
        like_user_queue = [watch_me]

        # 최대 10개 의 좋아요한 Feed나, 작성한 feed에 대한 리스트를 불러옴
        sorted_edges_latest_like_feed = sorted(watch_me.edges["feed"])[:max_like]

        # visited_like_feed를 분리해놓는 이유
        # 구분하기 편하라고요
        for edge in sorted_edges_latest_like_feed:
            visited_like_feeds.append(edge.target_node)

        # 유저들을 골라내는 과정
        for visited_feed in visited_like_feeds:
            sorted_edge_feed_like_user = sorted(visited_feed.edges["user"])[:max_related_user]
            for edge in sorted_edge_feed_like_user:
                # 시작된 본인만 아니라면 모두 OK
                # 리스트에 이미 UserNode가 담겨있는 상태라면, 담지 않아도 된다.
                if edge.target_node.get_id() != watch_me.get_id() and edge.target_node not in like_user_queue:
                    like_user_queue.append(edge.target_node)


        # 골라낸 유저 중
        for like_user_node in like_user_queue:
            sorted_edge_like_feed = sorted(like_user_node.edges["feed"])[:max_feed_find]

            for edge in sorted_edge_like_feed:
                if edge.target_node not in visited_like_feeds:
                    related_fid = edge.target_node.get_id()
                    recommend_list.add(related_fid)

        return list(recommend_list)

    # HashTag 랭킹에 관해 Feed를 추출하는 시스템
    # Feed 해시태그 랭킹에 집계된 Hash태그들과 연결된 Feed들을 무작위로 추첨
    # noinspection PyMethodMayBeStatic
    def feed_recommend_by_ranking(self, hash_tree:AVLTree, hashtag_rank:list, top_n_hashtags=5, max_feed_find=6):
        hashtag_top_n = hashtag_rank[:top_n_hashtags]
        recommend_list = set()

        for hashtag in hashtag_top_n:
            hash_node = hash_tree.get(key=hashtag)
            sorted_edge = sorted(hash_node.edges["feed"])[:max_feed_find]
            for edge in sorted_edge:
                recommend_list.add(edge.target_node.get_id())

        return list(recommend_list)

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
        return (f"INFO<-[    {all_node_feeds} nodes in NOVA Graph IN SEARCH ENGINE NOW READY\n")
                #f"             {list(self.__feed_node_avltree.values())} feed node in Graph.\n" +
                #f"             {list(self.__user_node_avltree.values())} user node in Graph.\n" +
                #f"             {list(self.__hash_node_avltree.values())} hash node in Graph.\n" )

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

        # 빈 유저를 생성 후, 추가하는 과정
        null_user = User()
        self.add_user_node(null_user)

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

        #$print(f"             {list(self.__feed_node_avltree.values())} feed node in Graph.")
        #$print(f"             {list(self.__user_node_avltree.values())} user node in Graph.")
        #$print(f"             {list(self.__hash_node_avltree.values())} hash node in Graph.")

        return

    # 해시 노드들 추가 # 트리 안에 있는 해시태그를 발견하면 기존의 노드를 반환하도록 한다. 수정필요
    def __add_hash_nodes(self, hashtags:list):
        hash_nodes = []
        for hashtag in hashtags:
            # 해시 태그 마다 노드를 생성
            # 중요한 점 : 노드가 이미 생성되어있으면, 기존의 노드를 반환 받음
            hash_node = self.__feed_chaos_graph.add_node(node_type="hashtag", node_id=hashtag, tree=self.__hash_node_avltree)

            # hashtag의 사용량을 갱신
            hash_node.weight_up()

            # 반환할 노드
            hash_nodes.append(hash_node)

        return hash_nodes

    # Feed 중 랜덤하게 샘플을 골라서
    def __random_feed_sample(self, samples_feed_n=15):
        feeds_value = list(self.__feed_node_avltree.values())
        if len(feeds_value) <= samples_feed_n:
            return feeds_value
        return random.sample(feeds_value, samples_feed_n)

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


        write_uid = feed.uid
        hashtags = feed.hashtag     # feed에 담긴 해시태그
        gen_time = datetime.strptime(feed.date, '%Y/%m/%d-%H:%M:%S')

        # 피드 노드 생성
        # FeedNode는 다른 노드들과 달리 특수한 id값인 작성자id를 가지게 된다.

        feed_node = self.__feed_chaos_graph.add_node(node_type="feed", node_id=feed.fid, write_uid=write_uid, tree=self.__feed_node_avltree)
        # 해시 노드 생성 (해시 노드들은 생성이 될 때, 이미 존재하는 노드들이라면 그 노드를 반환함
        hash_nodes = self.__add_hash_nodes(hashtags=hashtags)

        # Feed - 해시노드 간 edge 생성
        self.__feed_chaos_graph.connect_feed_with_hashs(feed_node=feed_node, hash_nodes=hash_nodes, date=gen_time)

        # 글을 쓸 때, 작성자가 트리안에 있어야만 가능.
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

        # 이미 수정된 Feed를 가지고 진행, 즉, Feed 수정 버튼을 누른 직후에 일어나는 일
        feed_node = self.__feed_node_avltree.get(key=feed.fid)

        # 새롭게 작성된 해시태그들
        new_hashtags = feed.hashtag
        feed_date = datetime.strptime(feed.date, '%Y/%m/%d-%H:%M:%S')

        # 새로운 해시태그들에 대한 노드들과 edge가 생성
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
    def recommend_next_feed(self, start_fid:str, mine_uid:str, hashtag_ranking:list, history:list):

        # 추천 Feed를 찾을 때, 다음의 경우를 고려했어야 했음.
        # 문제점 : 노드에 연결된 엣지가 부득이하게 하나만 존재하는 경우

        # 1. Feed에 좋아요가 있고, 해시태그들이 다양함.
        # 2. Feed에 좋아요가 없지만, 해시태그들이 다양함.
        # 3. Feed에 좋아요는 있지만, 해시태그가 하나만 붙음. (타고온 노드만)
        # 4. Feed에 좋아요도 없고, 해시태그도 진짜 희귀한 경우 (진짜 알고리즘을 타고와서 겨우발견할 법한 글)

        # 1의 경우. 이미 다양한 경우에 대해, Feed를 추천 받고 있음.
        # 2의 경우, 해시태그들의 경우에서 Feed를 받을 수 있음.
        # 3의 경우, 좋아요에 관해서 Feed 추천을 받을 수 있음.
        # 4의 경우, DB안에 있는 무작위의 Feed를 골라내야함

        # 만약에 두 상황에서 모두 뽑지 않았다. 이제 유저 본인에 대한 좋아요를 눌렀던 Feed내에서 찾기 시작해야함.


        # 그래야 더 다양한 주제에 대한 Feed를 추천 받을 수 있다.
        # 즉, Feed->User가 아닌 User->Feed 시스템이라는 점

        # 5. 로그인된 유저 본인에게 좋아요를 누른 Feed들을 기점으로 움직이는 Feed 추천
        #  이 때, 본인에게서 시작되는 것은 자신이 작성한 글또한 모두 포함시켜서 Search를 하는데 그 대신, 최종 추천 Feed에는 추가되지 않도록 헤야함.

        # 6. HashTag 랭킹에 의해 집계되어 추천되는 Feed
        #   진짜 초기에 가입되서 아무것도 없는 경우, 혹은 저 위에서 HashTag 주제 전환을 위해서 Rank에 집계된 HashTag를 이용해 feed를 추천해준다.

        # 7. 무작위의 feed를 추천. 이는 랜덤한 feed 중 20개를 추첨해 리스트에 담는다.
        # 진짜 무작위로 뽑아야됨.

        # Start 노드에 대한 Feed를 찾아냄.
        start_feed_node = self.__feed_node_avltree.get(key=start_fid)

        # 1, 2, 3, 4에 대한 경우
        # 매개의 중심은 내가 보고있는 Feed라는 점

        # User-Feed 간의 관계를 이용해 찾음
        # Hash-Feed 간의 관계를 이용해 찾음
        user_feed_recommend_list = self.__feed_chaos_graph.feed_recommend_by_like_user(start_node=start_feed_node)
        hash_feed_recommend_list = self.__feed_chaos_graph.feed_recommend_by_hashtag(start_node=start_feed_node)

        # 5에 대한 경우.
        # User가 Like했던 Feed들을 중심으로 찾음
        # 매가의 중심은 현재 Feed를 보고 있는 "나"라는 점.

        my_user_node = self.__user_node_avltree.get(mine_uid)
        me_feed_recommend_list = self.__feed_chaos_graph.feed_recommend_by_me(watch_me=my_user_node)

        # 6. 해시태그 랭킹에 대한 추천
        ranking_feed_recommend_list = self.__feed_chaos_graph.feed_recommend_by_ranking(
            hash_tree=self.__hash_node_avltree,
            hashtag_rank=hashtag_ranking
        )


        # 7. 완전 무작위 Feed List 추출.
        # 15개 정도의 무작위 Feed를 추출해내서 추천 Feed 리스트에 담음
        # AVLTree에서 뽑아서 씀

        random_feed_samples = self.__random_feed_sample()

        # Feed를 찾은 리스트들을 모두 합함.
        result_fid_list = user_feed_recommend_list + hash_feed_recommend_list + me_feed_recommend_list + ranking_feed_recommend_list + random_feed_samples

        # 히스토리에 존재하는 피드, 즉, 이전, 현재까지 본 모든 Feed들을 제외해야함
        for fid in result_fid_list:
            if fid not in history:
                return fid

        return None