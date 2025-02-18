
from bintrees import AVLTree
from others.data_domain import Feed, User, Bias, Notice, Comment
from datetime import  datetime, timedelta
import pandas as pd
import random
from copy import copy
from pprint import pprint
#--------------------------------------------------------------------------------------------------

# 이건 아래에 피드 테이블에 들어가야되는 피드 자료형
# 데이터 베이스에서 피드 데이터 받아서 만들꺼임
# 필요한 데이터는 언제든 추가가능

# 이게 검색에 따른 피드를 제공하는 클래스
# 위에 FeedAlgorithm에서 작성한 내용을 가지고 와도됨

# 임시로 사용할 검색어 저장 및 활용 클래스입니다.
class Keyword:
    def __init__(self, keyword=""):
        self.keyword = keyword
        self.count = 0
        self.trend = {
            "now" : 0,
            "prev" : 0
        }

# 클래스 목적 : 피드를 검색하거나, 조건에 맞는 피드를 제공하기 위함
class ManagedFeed:
    def __init__(self, fid="", like=0, date=None, uname="", fclass="", display=4,
                 board_type="", hashtag=[], body="", bid="", iid="", num_images=0):
        self.fid=fid
        self.fclass = fclass
        self.display = display
        self.like=like
        self.date=date
        self.uname = uname
        self.hashtag = hashtag
        self.board_type = board_type
        self.body = body
        self.bid = bid
        self.iid = iid
        self.num_images = num_images

    # 무슨 데이터인지 출력해보기
    def __call__(self):
        print("fid : ", self.fid)
        print("fclass: ", self.fclass)
        print("display: ", self.display)
        print("like : ", self.like)
        print("date: ", self.date)
        print("uname: ", self.uname)
        print("hashtag: ", self.hashtag)
        print("board_type: ", self.board_type)
        print("body: ", self.body)
        print("bid: ", self.bid)
        print("iid: ", self.iid)
        print("num_images: ", self.num_images)

    def to_dict(self):
        return {
            "fid": self.fid,
            "fclass": self.fclass,
            "display": self.display,
            "like": self.like,
            "date": self.date,
            "uname": self.uname,
            "hashtag": self.hashtag,
            "board_type": self.board_type,
            "body": self.body,
            "bid": self.bid,
            "iid": self.iid,
            "num_images": self.num_images
        }

# 이거는 Bias 테이블에 들어가게 되는 Bias 자료형
# 데이터베이스에 받아서 만들어진다.
class ManagedBias:
    def __init__(self, bid, bname:str, user_nodes:list, board_types:list):
        self.bid = bid
        self.bname = bname
        self.trend_hashtags = []
        self.user_nodes:list = user_nodes
        self.board_types:list = board_types

    def to_dict(self):
        return {
            "bid": self.bid,
            "bname": self.bname,
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
                                       display=single_feed.display,
                                       like=single_feed.star,
                                       date=self.__get_date_str_to_object(single_feed.date),
                                       hashtag=copy(single_feed.hashtag),
                                       uname=single_feed.nickname,
                                       board_type=single_feed.board_type,
                                       body=single_feed.body,
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
            managed_bias = ManagedBias(bid=single_bias.bid, bname=single_bias.bname, user_nodes=user_nodes, board_types=single_bias.board_types)
            #pprint(managed_bias.to_dict())
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
    def get_managed_feed_test(self):
        return self.__feed_table[2].to_dict()

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
            body=feed.body,
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
        managed_feed.body = feed.body
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
    # def search_feed_with_key_and_option(self, option:str, key:str="", num_feed=10, index=-1) -> tuple:
    #     result_fid = []
    #     result_index = -3
    #
    #     if index == -1:
    #         index = self.len_feed_table()
    #
    #         # target_index default 값은 0
    #     search_range = self.get_feeds_target_range(index=index)
    #     # search_range = self.__feed_table[:index][::-1]
    #
    #     if index < 0 or index > self.len_feed_table():
    #         return result_fid, -3
    #
    #     count = 0
    #     for i, managed_feed in enumerate(search_range):
    #         #i = len(self.__feed_table) - 1 - i
    #         # count로 이미 다 살펴 봤다면
    #         if count == num_feed:
    #             break
    #
    #         # 삭제된 피드는 None으로 표시될것이라서
    #         if managed_feed.fid == "":
    #             continue
    #
    #         if option == "hashtag":
    #             # 찾는 해시태그가 아님
    #             if key not in managed_feed.hashtag:
    #                 continue
    #         elif option == "uname":
    #             if key not in managed_feed.uname:
    #                 continue
    #         elif option == "bid":
    #             if key != managed_feed.bid:
    #                 continue
    #
    #         elif option == "fid":
    #             if key == managed_feed.fid:
    #                 result_fid.append(managed_feed)
    #                 result_index = i
    #                 break
    #
    #
    #         result_fid.append(managed_feed.fid)
    #
    #         # result_index 업데이트
    #         # 마지막 index 발견
    #         result_index = index - 1 - i  # 실제 self.__feed_table에서의 인덱스 계산
    #         count += 1
    #
    #     return result_fid, result_index

    def search_feeds_with_key_n_option(self, key:str, fclass:str, board_type:str, option):
        # Nan값의 경우, False 처리.
        # 대소문자를 구분하지 않음
        searched_df = self.__feed_df

        if option == "keyword":
            # 키워드를 통한 서치
            searched_df = self.__feed_df[self.__feed_df["body"].str.contains(key, case=False, na=False)]
        elif option == "hashtag":
            # 해시태그 리스트 안에 들어있는 해시태그들 중 하나만 있어도 찾는다.
            searched_df = self.__feed_df[self.__feed_df["hashtag"].apply(lambda hashtag: key in hashtag)]
        elif option == "uname":
            # 닉네임 서치
            searched_df = self.__feed_df[self.__feed_df["uname"] == key]
        elif option == "bid":
            # bid 서치
            searched_df = self.__feed_df[self.__feed_df["bid"] == key]
        elif option == "fid":
            # fid 서치
            searched_df = self.__feed_df[self.__feed_df["fid"] == key]

        # board_type 필터링
        # board_type이 ""이거나 All이면 다 고름
        # 아니라면 board_type 필터링을 진행함
        if board_type == "" or board_type == "all" or board_type == "전체":
            pass
        else:
            searched_df = searched_df[searched_df["board_type"] == board_type]

        if fclass == "" or fclass == "all" or fclass == "전체":
            pass
        else:
            # Fclass == long 인지 fclass == short인지 분류
            searched_df = searched_df[searched_df["fclass"] == fclass]

        # pprint(searched_df)

        return searched_df['fid'].tolist()
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

    #----------------------------------------------------------------------------------------------
    def filtering_bias_community(self, bids:list, board_type:str):
        filtered_feeds_df = self.__feed_df[self.__feed_df['bid'].isin(bids)]
        if board_type != "":
            filtered_feeds_df = filtered_feeds_df[filtered_feeds_df['board_type'] == board_type]
        return filtered_feeds_df['fid'].tolist()

    # 여기서는 추가적인 필터링을 위해 필터링된 FID리스트를 받고, 2차 필터링을 실시하는 곳입니다.
    def filtering_fclass_feed(self, fid_list:list, fclass:str) -> list:
        fid_list_df = self.__feed_df[(self.__feed_df['fid'].isin(fid_list))]
        # Filtering 시, 다음의 값을 유의
        # fclass == ""인 경우, 모든 경우를 가져옵니다. 어짜피 AD는 Notice의 경우로 들어가니까 상관없겠지요.
        if fclass != "":
            filtered_feeds_df = fid_list_df[(fid_list_df['fclass'] == fclass)]
            return filtered_feeds_df['fid'].tolist()
        return fid_list_df['fid'].tolist()

    def filtering_category_feed(self, fid_list:list, category:str) -> list:
        fid_list_df = self.__feed_df[(self.__feed_df['fid'].isin(fid_list))]
        # Filtering 시, 다음의 값을 유의
        # category == ""인 경우, 모든 경우를 가져옵니다. 똑같이 AD는 현재 아예 다른 모델을 사용하므로... 고려대상에서 제외합니다.
        if category != "" :
            filtered_feeds_df = fid_list_df[(fid_list_df['board_type'] == category)]
            # pprint(filtered_feeds_df)
            return filtered_feeds_df['fid'].tolist()
        return fid_list_df['fid'].tolist()

    def filtering_categories_feed_new(self, fid_list:list, categories:list):
        fid_list_df = self.__feed_df[(self.__feed_df['fid'].isin(fid_list))]
        # Filtering 시, 다음의 값을 유의
        # fclass == ""인 경우, 모든 경우를 가져옵니다. 어짜피 AD는 Notice의 경우로 들어가니까 상관없겠지요.
        if categories[0] != "":
            filtered_feeds_df = fid_list_df[(fid_list_df['board_type'].isin(categories))]
            # pprint(filtered_feeds_df)
            return filtered_feeds_df['fid'].tolist()
        return fid_list_df['fid'].tolist()

#---------------------------------------------------------------------------------------------------------------------------------------

