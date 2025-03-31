from bintrees import AVLTree
from others.data_domain import Feed, User, Bias, Notice, Comment, Schedule, ScheduleBundle
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

class ManagedSchedule:
    def __init__(self, sid="", sname="", uname="", bid="", bname="", date=None,
                 start_date_time=None, end_date_time=None, location=[],
                 code="", state:bool=True):
        self.sid=sid
        self.sname=sname
        self.bid=bid
        self.bname=bname
        self.uname=uname
        self.date=date                              # update_datetime
        self.start_date_time=start_date_time        # start_date + start_time
        self.end_date_time=end_date_time            # end_date + end_time
        self.location=location
        self.code=code
        self.state=state

    # 무슨 데이터인지 출력해보기
    def __call__(self):
        print("sid: ", self.sid)
        print("sname: ", self.sname)
        print("bid: ", self.bid)
        print("bname: ", self.bname)
        print("uname: ", self.uname)
        print("date: ", self.date)
        print("start_date_time: ", self.start_date_time)
        print("end_date_time: ", self.end_date_time)
        print("location: ", self.location)
        print("code: ", self.code)
        print("state: ", self.state)

    # 딕셔너리화
    def to_dict(self):
        return {
            "sid": self.sid,
            "sname": self.sname,
            "bid": self.bid,
            "bname": self.bname,
            "uname": self.uname,
            "date": self.date,
            "start_date_time": self.start_date_time,
            "end_date_time": self.end_date_time,
            "location": self.location,
            "code": self.code,
            "state": self.state
        }

class ManagedScheduleBundle:
    def __init__(self, sbid="", sbname="", bid="", bname="", uname="", date=None,
                  start_date=None, end_date=None, location=[], code="", sids=[]):
        self.sbid=sbid
        self.sbname=sbname
        self.bid=bid
        self.bname=bname
        self.uname=uname
        self.date=date                      # update_datetime
        self.start_date=start_date          # 스케쥴 번들 시작 날짜
        self.end_date=end_date              # 스케쥴 번들 끝 날짜
        self.location=location
        self.code=code
        self.sids=sids

    def __call__(self):
        print("sbid: ", self.sbid)
        print("sbname: ", self.sbname)
        print("bid: ", self.bid)
        print("bname: ", self.bname)
        print("uname: ", self.uname)
        print("date: ", self.date)
        print("start_date: ", self.start_date)
        print("end_date: ", self.end_date)
        print("location: ", self.location)
        print("code: ", self.code)
        print("sids: ", self.sids)

    def to_dict(self):
        return {
            "sid": self.sbid,
            "sname": self.sbname,
            "bid": self.bid,
            "bname": self.bname,
            "uname": self.uname,
            "date": self.date,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "location": self.location,
            "code": self.code,
            "sids": self.sids
        }

class ManagedTable:
    def __init__(self, database):
        self._database = database
        # self._data_table = []
        # self._data_df = pd.DataFrame()

    # 오늘 날짜 반환
    def _get_datetime_now(self):
        now = datetime.now()
        return now

    # string to datetime
    def _get_date_str_to_object(self, str_date):
        date_obj = datetime.strptime(str_date, "%Y/%m/%d-%H:%M:%S")
        return date_obj

    # datetime to string
    def _get_date_object_to_str(self, object:datetime):
        formatted_str = object.strftime("%Y/%m/%d-%H:%M:%S")
        return formatted_str

    # 시간 차이를 분석하는 함수
    # target_hour : 1, 24, 168
    def _get_time_diff(self, target_time, target_hour=0.5, reverse=False) -> bool:
        reference_time=datetime.now()
        time_diff = abs(target_time - reference_time)
        # 차이가 2시간 이상인지 확인
        if reverse:
            return time_diff < timedelta(hours=target_hour)
        return time_diff >= timedelta(hours=target_hour)

    # table list DataFrame화
    def _dataframing_table(self, data_table:list):
        # ManagedFeed들은 객체이므로, 딕셔너리화 시켜서 리스트로 만든다.
        managed_dict_list = [managed_data.to_dict() for managed_data in data_table]
        data_df = pd.DataFrame(managed_dict_list)
        # 데이터프레임을 정렬함
        # self._data_df = feed_df.sort_values(by='date', ascending=False).reset_index(drop=True)
        #
        return data_df

    # 데이터 프레임 삽입 / 삭제 / 편집
    def _add_new_data_in_df(self, df:pd.DataFrame, new_dict_data:dict):
        new_data = pd.DataFrame(new_dict_data)
        df = pd.concat([df, new_data], ignore_index=True)
        return df

    # id_type : fid / sid 같은 경우를 말합니다.
    # ID가 일치하는 경우는 단 한가지 이므로 가능한 일 .
    def _modify_data_in_df(self, df:pd.DataFrame, modify_dict_data:dict, id_type:str):
        update_index = df.index[df[id_type] == modify_dict_data[id_type].tolist()][0]
        df.loc[update_index] = modify_dict_data
        return

    # 삭제 로직
    # id_type의 설명 : 이상과 동일
    def _remove_data_in_df(self, df:pd.DataFrame, remove_id:str, id_type:str):
        remove_index = df.index[df[id_type] == remove_id].tolist()[0]
        df = df.drop(index=remove_index).reset_index(drop=True)
        return df

    # 검색 로직
    # GPT 도움
    def _search_data_with_key_str_n_columns(self, df:pd.DataFrame, key:str, columns:list=[]):
        # 안쪽 함수
        def cell_contains(cell):
            # datetime객체는 검색에서 제외
            if isinstance(cell, datetime):
                return False
            # List라면 들어있는 리스트를 검색함
            if isinstance(cell, list):
                return any(key in str(item) for item in cell)
            return key in str(cell)

        # key == "": 검색어가 없다면
        # 전체 df를 반환
        if key == "":
            return df

        # columns 지정 안되어 있으면 모든 열에 대해 검사합니다.
        if not columns:
            columns = df.columns

        # 데이터프레임 마스킹 데이터 만들기
        mask = df[columns].apply(lambda row: any(cell_contains(cell) for cell in row), axis=1)

        # df에 맞는 데이터프레임 행 반환
        return df[mask]

    # def get_managed_table_value_test(self):
    #     return self._data_table[2].to_dict()

    # def len_data_table(self):
    #     # Feed Table의 길이 구하기
    #     return len(self._data_table)


#-------------------------------------------------------------------------------------------------------------------------------------

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
        self.__init_feed_avltree()

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
    def __get_time_diff(self, target_time, target_hour=0.5, reverse=False) -> bool:
        reference_time=datetime.now()
        time_diff = abs(target_time - reference_time)
        # pprint("현재 시" + str(reference_time))
        # pprint("시간 차 :" + str(time_diff))
        # pprint("기준 시간 :" + str(timedelta(hours=target_hour)))

        # 차이가 2시간 이상인지 확인
        if reverse:
            return time_diff < timedelta(hours=target_hour)
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
    def search_feed_with_time_or_like(self, search_type:str="", time_type:str=""):
        searched_df = self.__feed_df
        # pprint(searched_df)

        if search_type == "best":
            searched_df = searched_df[searched_df['like'] >= 30]

        if time_type == "" or time_type == "all" or time_type == "전체":
            pass
        elif time_type == "day":
            searched_df = searched_df[self.__get_time_diff(target_time=searched_df['date'],target_hour=24, reverse=True)]
        elif time_type == "weekly":
            searched_df = searched_df[self.__get_time_diff(target_time=searched_df['date'],target_hour=168, reverse=True)]

        # pprint(searched_df[:10])
        return searched_df['fid'].tolist()

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

    def search_feeds_with_key_n_option(self, key:str, fclass:str, board_type:str, target_time:str, option):
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

        # 시간에 따라 분류하는 함수 ( 일간 주간 )
        if target_time=="" or target_time=="all" or target_time=="전체":
            pass
        elif target_time=="day":
            searched_df = searched_df[self.__get_time_diff(target_time=searched_df['date'],target_hour=24, reverse=True)]
        elif target_time=="weekly":
            searched_df = searched_df[self.__get_time_diff(target_time=searched_df['date'],target_hour=168, reverse=True)]

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
    def filtering_bias_community(self, bid:str, board_type:str):
        filtered_feeds_df = self.__feed_df[self.__feed_df['bid']==bid]
        if board_type == "" or board_type == "전체" or board_type == "all" or board_type == "선택없음":
            pass
        else:
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
        if category != "" or category != "전체" or category != "all" or category != "선택없음" :
            filtered_feeds_df = fid_list_df[(fid_list_df['board_type'] == category)]
            # pprint(filtered_feeds_df)
            return filtered_feeds_df['fid'].tolist()
        return fid_list_df['fid'].tolist()

    def filtering_categories_feed_new(self, fid_list:list, categories:list):
        fid_list_df = self.__feed_df[(self.__feed_df['fid'].isin(fid_list))]
        # Filtering 시, 다음의 값을 유의
        # fclass == ""인 경우, 모든 경우를 가져옵니다. 어짜피 AD는 Notice의 경우로 들어가니까 상관없겠지요.
        if categories[0] != "" or categories[0] != "전체" or categories[0] != "all" or categories[0] != "선택없음":
            filtered_feeds_df = fid_list_df[(fid_list_df['board_type'].isin(categories))]
            # pprint(filtered_feeds_df)
            return filtered_feeds_df['fid'].tolist()
        return fid_list_df['fid'].tolist()

class ManagedFeedBiasTableNew(ManagedTable):
    def __init__(self, database, feed_algorithm):
        super().__init__(database)
        self.__feed_table = []
        self.__feed_df = pd.DataFrame()
        self.__feed_algorithm = feed_algorithm
        self.__feed_avltree = AVLTree()
        self.__bias_avltree = AVLTree()


        self.__init_feed_table()
        self.__init_bias_tree()

    # Initialize feed 테이블
    def __init_feed_table(self):
        feeds = []
        # 먼저 피드 데이터를 DB에서 불러오고
        feed_datas = self._database.get_all_data(target="fid")

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
                                       date=self._get_date_str_to_object(single_feed.date),
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
            self.__feed_avltree.insert(managed_feed.fid, managed_feed)

        # 리턴되면 위에서 잠시 보관한 피드 데이터는 사라지고 self.__feed_table에 ManagedFeed들만 남음
        # 최신이 가장 밑으로 오지만, 데이터프레임만 최신 내림차순으로 정렬할 것
        self.__feed_table = sorted(self.__feed_table, key=lambda x:x.date, reverse=False)

        # 데이터 프레임화
        self.__feed_df = self._dataframing_table(data_table=self.__feed_table)
        self.__feed_df = self.__feed_df.sort_values(by='date', ascending=False).reset_index(drop=True)


        num_feed = str(len(self.__feed_table))

        print(f'INFO<-[      {num_feed} NOVA FEED IN SEARCH ENGINE NOW READY.')
        print(f'INFO<-[      {num_feed} NOVA FEED DATAFRAME IN SEARCH ENGINE NOW READY.')

        return

    # Bias Tree 설정
    def __init_bias_tree(self):
        biases = []
        users = []
        bias_datas = self._database.get_all_data(target="bid")
        user_datas = self._database.get_all_data(target="uid")


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



    # 랜덤한 Feed 하나 추출
    def get_random_feed(self):
        random_index = random.randint(0, len(self.__feed_table)-1)
        return self.__feed_table[random_index].fid

    # 타겟범위내의 Feed를 반환
    def get_feeds_target_range(self, index, target_index=0):
        return self.__feed_table[target_index:index][::-1]

    # Managed Feed 찾기
    def search_managed_feed(self, fid):
        return self.__feed_avltree.get(key=fid)

    # 시간에 따라서 찾는 함수. Feed 전용
    def find_target_index(self, target_hour=1):
        target_index = len(self.__feed_table)

        for i, managed_feed in enumerate(self.__feed_table):
            # 삭제된 피드는 None으로 표시될것이라서
            if managed_feed.fid == "":
                continue

            if self._get_time_diff(target_time=managed_feed.date, target_hour=target_hour):
                continue
            else:
                target_index = i
                break

        return target_index




    # 새로운 ManagedFeed를 추가함
    def make_new_managed_feed(self, feed:Feed):
        managed_feed = ManagedFeed(
            fid=feed.fid,
            fclass=feed.fclass,
            like=feed.star,
            date=self._get_date_str_to_object(feed.date),
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
        self.__feed_df = self._add_new_data_in_df(df=self.__feed_df, new_dict_data=managed_feed.to_dict())
        self.__feed_df = self.__feed_df.sort_values(by='date', ascending=False).reset_index(drop=True)

        return

    # ManagedFeedTable을 수정, (Feed가 REMOVE 된다면 DISPLAY 옵션이 0로 바뀌게 됩니다.
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
        self._modify_data_in_df(df=self.__feed_df, modify_dict_data=managed_feed.to_dict(), id_type='fid')

        return

    # ManagedFeed가 삭제되었기 때문에, 테이블과 트리에서도 삭제시킴
    def remove_feed(self, feed:Feed):
        # 삭제하는 함수. 피드가  삭제되면 None으로 바뀔것
        managed_feed = self.__feed_avltree.get(key=feed.fid)
        managed_feed = ManagedFeed()

        self.__feed_avltree.remove(key=feed.fid)
        # dataframe 삭제
        self.__feed_df = self._remove_data_in_df(df=self.__feed_df,remove_id=feed.fid, id_type='fid')

        return



    # 시간 차이를 바탕으로 정해진 시간대 내의 피드 정보 구하기
    # target_hour : 1, 24, 168
    def search_feed_with_time_or_like(self, search_type:str="", time_type:str=""):
        searched_df = self.__feed_df
        if search_type == "best":
            searched_df = searched_df[searched_df['like'] >= 30]

        if time_type == "" or time_type == "all" or time_type == "전체":
            pass
        elif time_type == "day":
            searched_df = searched_df[self._get_time_diff(target_time=searched_df['date'],target_hour=24, reverse=True)]
        elif time_type == "weekly":
            searched_df = searched_df[self._get_time_diff(target_time=searched_df['date'],target_hour=168, reverse=True)]

        # 마지막, 삭제된 Feed는 반환하지 않는다.
        searched_df = searched_df[searched_df['display'] != 0]

        # pprint(searched_df[:10])
        return searched_df['fid'].tolist()

    # 키워드와 필터링을 통해 데이터프레임에서 Feed들을 찾아냅니다.
    # 다양한 옵션들을 제공하고.. 있긴 합니다.
    def search_feeds_with_key_n_option(self, key:str, fclass:str, board_type:str, target_time:str, option):
        # # Nan값의 경우, False 처리.
        # # 대소문자를 구분하지 않음
        #
        # searched_df = self.__feed_df
        #
        # if option == "keyword":
        #     # 키워드를 통한 서치
        #     searched_df = self.__feed_df[self.__feed_df["body"].str.contains(key, case=False, na=False)]
        # elif option == "hashtag":
        #     # 해시태그 리스트 안에 들어있는 해시태그들 중 하나만 있어도 찾는다.
        #     searched_df = self.__feed_df[self.__feed_df[option].apply(lambda hashtag: key in hashtag)]
        # elif option == "uname" or option == "bid" or option=="fid":
        #     # 닉네임 / BID / FID 서치
        #     searched_df = self.__feed_df[self.__feed_df[option] == key]

        # 데이터 프레임 검색 옵션 : Option에 따라 리스트가 달라짐
        columns = [option]

        searched_df = self._search_data_with_key_str_n_columns(df=self.__feed_df, key=key, columns=columns)

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

        # 시간에 따라 분류하는 함수 ( 일간 주간 )
        if target_time=="" or target_time=="all" or target_time=="전체":
            pass
        elif target_time=="day":
            searched_df = searched_df[self._get_time_diff(target_time=searched_df['date'],target_hour=24, reverse=True)]
        elif target_time=="weekly":
            searched_df = searched_df[self._get_time_diff(target_time=searched_df['date'],target_hour=168, reverse=True)]

        # 마지막, 삭제된 Feed는 반환하지 않는다.
        searched_df = searched_df[searched_df['display'] != 0]

        return searched_df['fid'].tolist()



    # 바이어스 별 필터링을 진행합니다.
    def filtering_bias_community(self, bid:str, board_type:str):
        filtered_feeds_df = self.__feed_df[self.__feed_df['bid']==bid]
        if board_type == "" or board_type == "전체" or board_type == "all" or board_type == "선택없음":
            pass
        else:
            filtered_feeds_df = filtered_feeds_df[filtered_feeds_df['board_type'] == board_type]
        # 마지막, 삭제된 Feed는 반환하지 않는다.
        filtered_feeds_df = filtered_feeds_df[filtered_feeds_df['display'] != 0]
        return filtered_feeds_df['fid'].tolist()

    # 여기서는 추가적인 필터링을 위해 필터링된 FID리스트를 받고, 2차 필터링을 실시하는 곳입니다.
    def filtering_fclass_feed(self, fid_list:list, fclass:str) -> list:
        fid_list_df = self.__feed_df[(self.__feed_table['fid'].isin(fid_list))]
        # Filtering 시, 다음의 값을 유의
        # fclass == ""인 경우, 모든 경우를 가져옵니다.
        if fclass != "":
            filtered_feeds_df = fid_list_df[(fid_list_df['fclass'] == fclass)]
            # 마지막, 삭제된 Feed는 반환하지 않는다.
            filtered_feeds_df = filtered_feeds_df[filtered_feeds_df['display'] != 0]
            return filtered_feeds_df['fid'].tolist()
        # 마지막, 삭제된 Feed는 반환하지 않는다.
        fid_list_df = fid_list_df[fid_list_df['display'] != 0]
        return fid_list_df['fid'].tolist()

    # 카테고리별 피드를 나눕니다.
    def filtering_categories_feed_new(self, fid_list:list, categories:list):
        fid_list_df = self.__feed_df[(self.__feed_df['fid'].isin(fid_list))]
        # Filtering 시, 다음의 값을 유의
        # categories[0] == ""인 경우, 모든 경우를 가져옵니다.
        if categories[0] != "" or categories[0] != "전체" or categories[0] != "all" or categories[0] != "선택없음":
            filtered_feeds_df = fid_list_df[(fid_list_df['board_type'].isin(categories))]
            # 마지막, 삭제된 Feed는 반환하지 않는다.
            filtered_feeds_df = filtered_feeds_df[filtered_feeds_df['display'] != 0]
            return filtered_feeds_df['fid'].tolist()
        # 마지막, 삭제된 Feed는 반환하지 않는다.
        fid_list_df = fid_list_df[fid_list_df['display'] != 0]
        return fid_list_df['fid'].tolist()

    #---------------------------------------------------------------------------------------------------------
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

#---------------------------------------------------------------------------------------------------------------------------------------

# Managed Time Table 데이터프레임 클래스
class ManagedScheduleTable(ManagedTable):
    def __init__(self, database):
        super().__init__(database)
        self.__schedule_table = []
        self.__schedule_df = pd.DataFrame()
        self.__schedule_bundle_table = []
        self.__schedule_bundle_df = pd.DataFrame()

        self.__schedule_tree = AVLTree()
        self.__bundle_tree = AVLTree()

        self.__init_schedule_table()
        self.__init_schedule_bundle_table()

    # 최초 스케줄 데이터프레임 초기화 함수
    def __init_schedule_table(self):
        schedules = []

        schedule_datas = self._database.get_all_data(target="sid")

        for schedule_data in schedule_datas:
            schedule = Schedule()
            schedule.make_with_dict(dict_data=schedule_data)
            schedules.append(schedule)

        for single_schedule in schedules:
            start_date_time = single_schedule.start_date+'-'+single_schedule.start_time+':00'
            end_date_time = single_schedule.end_date+'-'+single_schedule.end_time+':00'

            managed_schedule = ManagedSchedule(sid=single_schedule.sid,
                                               sname=single_schedule.sname,
                                               bid=single_schedule.bid,
                                               bname=single_schedule.bname,
                                               uname=single_schedule.uname,
                                               date=self._get_date_str_to_object(str_date=single_schedule.update_datetime),
                                               start_date_time=self._get_date_str_to_object(str_date=start_date_time),
                                               end_date_time=self._get_date_str_to_object(str_date=end_date_time),
                                               location=copy(single_schedule.location),
                                               code=single_schedule.code,
                                               state=single_schedule.state
                                               )

            self.__schedule_table.append(managed_schedule)
            self.__schedule_tree.insert(managed_schedule.sid, managed_schedule)


        # 리턴되면 위에서 잠시 보관한 피드 데이터는 사라지고 self.__feed_table에 ManagedFeed들만 남음
        # 최신이 가장 밑으로 오지만, 데이터프레임만 최신 내림차순으로 정렬할 것
        self.__schedule_table = sorted(self.__schedule_table, key=lambda x:x.date, reverse=False)
        self.__schedule_df = self._dataframing_table(data_table=self.__schedule_table)

        num_schedules = str(len(self.__schedule_table))

        print(f'INFO<-[      {num_schedules} NOVA SCHEDULES IN SEARCH ENGINE NOW READY.')
        print(f'INFO<-[      {num_schedules} NOVA SCHEDULES DATAFRAME IN SEARCH ENGINE NOW READY.')

        return

    # 최초 스케줄 번들 데이터프레임 초기화 함수
    def __init_schedule_bundle_table(self):
        schedule_bundles = []

        schedule_bundle_datas = self._database.get_all_data(target="sbid")

        for schedule_bundle_data in schedule_bundle_datas:
            schedule_bundle = ScheduleBundle()
            schedule_bundle.make_with_dict(dict_data=schedule_bundle_data)
            schedule_bundles.append(schedule_bundle)

        for bundle in schedule_bundles:
            start_date = bundle.date[0]+"-00:00:00"
            end_date = bundle.date[1]+"-00:00:00"

            managed_bundle = ManagedScheduleBundle(sbid=bundle.sbid,
                                                   sbname=bundle.sbname,
                                                   bid=bundle.bid,
                                                   bname=bundle.bname,
                                                   uname=bundle.uname,
                                                   date=self._get_date_str_to_object(str_date=bundle.update_datetime),
                                                   start_date=self._get_date_str_to_object(str_date=start_date),
                                                   end_date=self._get_date_str_to_object(str_date=end_date),
                                                   location=copy(bundle.location),
                                                   code=bundle.code,
                                                   sids=copy(bundle.sids)
                                               )

            self.__schedule_bundle_table.append(managed_bundle)
            self.__bundle_tree.insert(managed_bundle.sbid, managed_bundle)

        # 리턴되면 위에서 잠시 보관한 피드 데이터는 사라지고 self.__feed_table에 ManagedFeed들만 남음
        # 최신이 가장 밑으로 오지만, 데이터프레임만 최신 내림차순으로 정렬할 것
        self.__schedule_bundle_table = sorted(self.__schedule_bundle_table, key=lambda x:x.date, reverse=False)
        self.__schedule_bundle_df = self._dataframing_table(data_table=self.__schedule_bundle_table)

        num_schedule_bundles = str(len(self.__schedule_bundle_table))

        print(f'INFO<-[      {num_schedule_bundles} NOVA SCHEDULE BUNDLES IN SEARCH ENGINE NOW READY.')
        print(f'INFO<-[      {num_schedule_bundles} NOVA SCHEDULE BUNDLES DATAFRAME IN SEARCH ENGINE NOW READY.')

        return

    # 랜덤하게 하나 스케줄 나옴
    def get_random_schedule(self):
        random_index = random.randint(0, len(self.__schedule_table)-1)
        return self.__schedule_table[random_index].sid


    # 새로운 스케줄을 추가하는 함수
    def make_new_managed_schedule(self, schedule:Schedule):
        start_date_time = schedule.start_date+'-'+schedule.start_time+':00'
        end_date_time = schedule.end_date+'-'+schedule.end_time+':00'

        managed_schedule = ManagedSchedule(
            sid=schedule.sid,
            sname=schedule.sname,
            bid=schedule.bid,
            bname=schedule.bname,
            uname=schedule.uname,
            date=self._get_date_str_to_object(str_date=schedule.update_datetime),
            start_date_time=self._get_date_str_to_object(str_date=start_date_time),
            end_date_time=self._get_date_str_to_object(str_date=end_date_time),
            location=copy(schedule.location),
            code=schedule.code,
            state=schedule.state
        )

        self.__schedule_table.append(managed_schedule)
        self.__schedule_tree.insert(managed_schedule.sid, managed_schedule)

        self.__schedule_df = self._add_new_data_in_df(df=self.__schedule_df, new_dict_data=managed_schedule.to_dict())
        self.__schedule_df = self.__schedule_df.sort_values(by='date', ascending=False).reset_index(drop=True)

        return

    # 스케줄 내용이 변경되었을 때
    def modify_schedule_table(self, modify_schedule:Schedule):
        managed_schedule:ManagedSchedule = self.__schedule_tree.get(modify_schedule.sid)

        mo_start_date_time = modify_schedule.start_date+'-'+modify_schedule.start_time+':00'
        mo_end_date_time = modify_schedule.end_date+'-'+modify_schedule.end_time+':00'

        # 스케줄 데이터를 변경합니다.
        managed_schedule.sname = modify_schedule.sname
        managed_schedule.date = self._get_date_str_to_object(str_date=modify_schedule.update_datetime)
        managed_schedule.start_date_time = self._get_date_str_to_object(str_date=mo_start_date_time)
        managed_schedule.end_date_time = self._get_date_str_to_object(str_date=mo_end_date_time)
        managed_schedule.location = copy(modify_schedule.location)
        managed_schedule.state = modify_schedule.state

        self._modify_data_in_df(df=self.__schedule_df, modify_dict_data=managed_schedule.to_dict(), id_type='sid')

        return

    # 스케줄 삭제
    def remove_schedule_df(self, schedule:Schedule):
        managed_schedule = self.__schedule_tree.get(key=schedule.sid)
        managed_schedule = ManagedSchedule()

        self.__schedule_tree.remove(key=schedule.sid)
        # 데이터프레임 삭제
        self.__schedule_df = self._remove_data_in_df(df=self.__schedule_df, remove_id=schedule.sid, id_type='sid')

    # 새로운 스케줄 번들 추가 함수
    def make_new_managed_bundle(self, bundle:ScheduleBundle):
        start_date = bundle.date[0]+"-00:00:00"
        end_date = bundle.date[1]+"-00:00:00"

        managed_bundle = ManagedScheduleBundle(
            sbid=bundle.sbid,
            sbname=bundle.sbname,
            bid=bundle.bid,
            bname=bundle.bname,
            uname=bundle.uname,
            date=self._get_date_str_to_object(str_date=bundle.update_datetime),
            start_date=self._get_date_str_to_object(str_date=start_date),
            end_date=self._get_date_str_to_object(str_date=end_date),
            location=copy(bundle.location),
            code=bundle.code,
            sids=copy(bundle.sids)
        )

        self.__schedule_bundle_table.append(managed_bundle)
        self.__bundle_tree.insert(managed_bundle.sbid, managed_bundle)

        self.__schedule_bundle_df = self._add_new_data_in_df(df=self.__schedule_bundle_df,
                                                             new_dict_data=managed_bundle.to_dict())
        self.__schedule_bundle_df = self.__schedule_bundle_df.sort_values(by='date', ascending=False).reset_index(drop=True)

        return

    # 번들 데이터 수정
    def modify_bundle_table(self, modify_bundle:ScheduleBundle):
        managed_bundle:ManagedScheduleBundle = self.__bundle_tree.get(modify_bundle.sbid)

        mo_start_date = modify_bundle.date[0]+"-00:00:00"
        mo_end_date = modify_bundle.date[1]+"-00:00:00"

        managed_bundle.sbname = modify_bundle.sbname
        managed_bundle.date = self._get_date_str_to_object(str_date=modify_bundle.update_datetime)
        managed_bundle.start_date = self._get_date_str_to_object(str_date=mo_start_date)
        managed_bundle.end_date = self._get_date_str_to_object(str_date=mo_end_date)
        managed_bundle.location = copy(modify_bundle.location)
        managed_bundle.sids = copy(modify_bundle.sids)

        self._modify_data_in_df(df=self.__schedule_bundle_df, modify_dict_data=managed_bundle.to_dict(), id_type='sbid')

        return

    # 번들 데이터 삭제
    def remove_bundle_df(self, bundle:ScheduleBundle):
        managed_bundle = self.__bundle_tree.get(key=bundle.sbid)
        managed_bundle = ManagedScheduleBundle()

        self.__bundle_tree.remove(key=bundle.sbid)
        self.__schedule_bundle_df = self._remove_data_in_df(df=self.__schedule_bundle_df, remove_id=bundle.sbid, id_type='sbid')



    # 키를 통해 스케줄을 검색합니다.
    def search_schedule_with_key(self, key:str, return_id:bool=True):
        columns = ['sname', 'bname', 'uname', 'code']
        searched_df = self._search_data_with_key_str_n_columns(df=self.__schedule_df, key=key, columns=columns)
        if return_id:
            return  searched_df['sid'].to_list()
        return searched_df.to_dict('records')

    # 번들 서치 함수.
    def search_bundle_with_key(self, key:str, return_id:bool=True):
        columns = ['sbname', 'bname', 'uname', 'code']
        searched_df = self._search_data_with_key_str_n_columns(df=self.__schedule_bundle_df, key=key, columns=columns)
        if return_id:
            return searched_df['sbid'].to_list()
        return searched_df.to_dict('records')

    # 내가 선택한 일정들을 보는 함수
    def search_my_selected_schedules(self, bid:str, selected_sids:list, return_id:bool=True):
        searched_df = self.__schedule_df[self.__schedule_df['sid'].isin(selected_sids)]
        searched_df = self._search_data_with_key_str_n_columns(df=searched_df, key=bid, columns=['bid'])
        if return_id:
            return searched_df['sbid'].to_list()
        return searched_df.to_dict('records')

    # 내가 선택한 일정 번들들을 보는 함수
    def search_my_selected_bundles(self, bid:str, selected_sbids:list, return_id:bool=True):
        searched_df = self.__schedule_bundle_df[self.__schedule_bundle_df['sbid'].isin(selected_sbids)]
        searched_df = self._search_data_with_key_str_n_columns(df=searched_df, key=bid, columns=['bid'])
        if return_id:
            return searched_df['sbid'].to_list()
        return searched_df.to_dict('records')

