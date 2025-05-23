from bintrees import AVLTree
from others.data_domain import Feed, User, Bias, Notice, Comment, Schedule, ScheduleBundle
from datetime import  datetime, timedelta
import pandas as pd
import random
from copy import copy

import logging

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
    def __init__(self, sid="", sname="", uname="", bid="", bname="", bias_gender="", bias_category=[],
                 date=None, start_date_time=None, end_date_time=None, time_section=[],  location=[],
                 code="", state:bool=True, bias_tags=[]):
        self.sid=sid
        self.sname=sname
        self.bid=bid
        self.bname=bname
        self.bias_gender=bias_gender
        self.bias_category=bias_category            # 바이어스 카테고리
        self.bias_tags=bias_tags                     # 바이어스 태그
        self.uname=uname
        self.date=date                              # update_datetime
        self.start_date_time=start_date_time        # start_date + start_time
        self.end_date_time=end_date_time            # end_date + end_time
        self.time_section=time_section              # 타임 섹션
        self.location=location
        self.code=code
        self.state=state


    # 무슨 데이터인지 출력해보기
    def __call__(self):
        print("sid: ", self.sid)
        print("sname: ", self.sname)
        print("bid: ", self.bid)
        print("bname: ", self.bname)
        print("bias_gender: ", self.bias_gender)
        print("bias_category: ", self.bias_category)
        print("bias_tags: ", self.bias_tags)
        print("uname: ", self.uname)
        print("date: ", self.date)
        print("start_date_time: ", self.start_date_time)
        print("end_date_time: ", self.end_date_time)
        print("time_section", self.time_section)
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
            "bias_gender": self.bias_gender,
            "bias_category": self.bias_category,
            "bias_tags": self.bias_tags,
            "uname": self.uname,
            "date": self.date,
            "start_date_time": self.start_date_time,
            "end_date_time": self.end_date_time,
            "time_section": self.time_section,
            "location": self.location,
            "code": self.code,
            "state": self.state
        }

class ManagedScheduleBundle:
    def __init__(self, sbid="", sbname="", bid="", bname="", bias_gender="", bias_category=[],
                 bias_tags=[], uname="", date=None, start_date=None, end_date=None, location=[], code="", sids=[]):
        self.sbid=sbid
        self.sbname=sbname
        self.bid=bid
        self.bname=bname
        self.bias_gender=bias_gender
        self.bias_category=bias_category
        self.bias_tags=bias_tags
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
        print("bias_gender: ", self.bias_gender)
        print("bias_category: ", self.bias_category)
        print("bias_tags: ", self.bias_tags)
        print("uname: ", self.uname)
        print("date: ", self.date)
        print("start_date: ", self.start_date)
        print("end_date: ", self.end_date)
        print("location: ", self.location)
        print("code: ", self.code)
        print("sids: ", self.sids)

    def to_dict(self):
        return {
            "sbid": self.sbid,
            "sbname": self.sbname,
            "bid": self.bid,
            "bname": self.bname,
            "bias_gender": self.bias_gender,
            "bias_category": self.bias_category,
            "bias_tags": self.bias_tags,
            "uname": self.uname,
            "date": self.date,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "location": self.location,
            "code": self.code,
            "sids": self.sids
        }



SKIP_TUPLE = ("", "전체", "all", "선택없음")

class ManagedTable:
    def __init__(self, database):
        self._database = database
        # self._data_table = []
        # self._data_df = pd.DataFrame()

    # 오늘 날짜 반환
    def _get_datetime_now(self):
        now = datetime.now()
        return now

    # 오늘 날짜를 기준으로 금주의 월요일, 일요일을 반환합니다.
    def _get_monday_sunday_of_this_week(self):
        today_str = datetime.today().strftime("%Y/%m/%d")
        today = datetime.strptime(today_str, "%Y/%m/%d")

        # weekday() -> 월 : 0, 화 : 1 ...  일 : 6
        monday = today - timedelta(days=today.weekday())
        sunday = today + timedelta(days=(6 - today.weekday()))

        return monday, sunday

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

    # 타임 섹션을 얻는 함수
    # 24시간을 4등분 하고 각 구간을 0, 1, 2, 3으로 설정합니다.
    def _get_schedule_time_section(self, start_time:datetime, end_time:datetime):
        current_time = start_time
        first_section = True
        end_flag = False
        time_sections = set()       # 타임 섹션을 판별할 때, 0, 1, 2, 3의 값만 가지며, 이후의 날도 넘어간다면 그것도 포함시킨다.

        # 첫 타임 섹션 설정
        time_ranges = [(0, 6), (6, 12), (12, 18), (18, 24)]

        # end_time을 넘기전 까지 Time Section을 찾아낸다.
        while current_time < end_time:
            hour = current_time.hour

            # 탈출 구문
            if end_flag:
                break

            for i, (start_hour, end_hour) in enumerate(time_ranges):
                if start_hour <= hour < end_hour:
                    if not first_section and i == 0:
                        end_flag = True
                        break

                    # 구간이 끝는 시각이 24면 다음날 00시로 설정
                    if end_hour == 24:
                        current_range_end = current_time.replace(hour=0, minute=0, second=0) + timedelta(days=1)
                    else:
                        current_range_end = current_time.replace(hour=end_hour, minute=0, second=0)

                    # 구간 종료 시간이 스케줄 종료 시간보다 크면 종료시간으로 제한
                    actual_end = min(end_time, current_range_end)

                    # time_sections에 추가
                    time_sections.add(i)
                    current_time = actual_end       # 구간 재설정

                    first_section = False

                    break

        # 리스트로 반환합니다.
        return list(time_sections)



    # table list DataFrame화
    def _dataframing_table(self, data_table:list):
        # ManagedFeed들은 객체이므로, 딕셔너리화 시켜서 리스트로 만든다.
        managed_dict_list = [managed_data.to_dict() for managed_data in data_table]
        data_df = pd.DataFrame(managed_dict_list)
        # 데이터프레임을 정렬함
        data_df = data_df.sort_values(by='date', ascending=False).reset_index(drop=True)
        return data_df





    # 데이터 프레임 삽입 / 삭제 / 편집
    def _add_new_data_in_df(self, df:pd.DataFrame, new_dict_data:dict, **condition):
        # 딕셔너리를 통해 새로운 DF를 만들고 Transpose(전치)시키면 된다
        new_data = pd.DataFrame.from_dict(new_dict_data, orient="index").transpose()


        if not condition:
            logging.error("추가 행 지정 조건 필요")
            return df

        mask = pd.Series(True, index=df.index)      # 초기 마스크 생성 모두가 True.
        for key, val in condition.items():
            # 동작 조건은 키가 id만!
            if "id" not in key:
                logging.error("조건은 ID로만 가능합니다.")
                return df
            if key == '':
                logging.error('조건에 값이 입력되지 않음')

            mask &= (df[key] == val)            # df[id] = "아이디" 인 행만 True, 나머지 False인 마스크와 AND 연산으로 MASK 찾아냄

        if mask.sum() > 0 :
            logging.error("이미 추가되어 있는 ID!")
            return df

        # 최종 추가 과정
        df = pd.concat([df, new_data], ignore_index=True)
        return df

    # id_type : fid / sid 같은 경우를 말합니다.
    # condition으로 만들었지만 id로만 동작하도록 제작했습니다.
    # ID가 일치하는 경우는 단 한가지 이므로 가능한 일 .
    def _modify_data_in_df(self, df:pd.DataFrame, modify_dict_data:dict, **condition):
        # 모든 반환은 데이터프레임으로 고정합니다.
        # 따라서 에러가 나도 로깅 에러만 나고 수정되지 않은 데이터가 반환됩니다.
        if not condition:
            logging.error("수정 행 지정 조건이 필요")
            return df

        mask = pd.Series(True, index=df.index)      # 초기 마스크 생성 모두가 True.
        for key, val in condition.items():
            # 동작 조건은 키가 id만!
            if "id" not in key:
                logging.error("조건은 ID로만 가능")
                return df

            if key == '':
                logging.error("조건에 값이 입력되지 않음")
                return df

            mask &= (df[key] == val)            # df[id] = "아이디" 인 행만 True, 나머지 False인 마스크와 AND 연산으로 MASK 찾아냄

        # ID와 같은 고유번호로 찾아내는건데 2개 이상있으면 에러임
        if mask.sum() != 1:
            logging.error("조건에 맞는 행이 하나가 아님")
            return df

        # 최종 업데이트 과정
        update_index = df.index[mask][0]
        df.loc[update_index] = modify_dict_data
        return df

    # 삭제 로직
    # id_type의 설명 : 이상과 동일
    def _remove_data_in_df(self, df:pd.DataFrame, **condition):
        # 모든 반환은 데이터프레임으로 고정합니다.
        # 따라서 에러가 나도 로깅 에러만 나고 수정되지 않은 데이터가 반환됩니다.
        if not condition:
            logging.error("수정 행 지정 조건이 필요")
            return df

        mask = pd.Series(True, index=df.index)      # 초기 마스크 생성 모두가 True.
        for key, val in condition.items():
            # 동작 조건은 키가 id만!
            if "id" not in key:
                logging.error("조건은 ID로만 가능")
                return df
            if key == '':
                logging.error("조건에 값이 입력되지 않음")
                return df
            mask &= (df[key] == val)            # df[id] = "아이디" 인 행만 True, 나머지 False인 마스크와 AND 연산으로 MASK 찾아냄

        # ID와 같은 고유번호로 찾아내는건데 2개 이상있으면 에러임
        if mask.sum() != 1:
            logging.error("조건에 맞는 행이 하나가 아님")
            return df

        # 최종 업데이트 과정
        remove_index = df.index[mask][0]
        df = df.drop(index=remove_index).reset_index(drop=True)
        return df


    # 테이블에서 인덱스를 가져옴
    def _get_obj_index_in_table_with_id(self, table:list, **condition):
        if len(condition) > 1:
            logging.error("조건이 너무 많음. ID만 받음")
            return -1

        key, val = next(iter(condition.items()))
        if "id" not in key:
            logging.error("조건은 id여야함, (예시 : fid, sid, sbid 등)")
            return -1

        # id의 값은 고유값이므로 다음과 같이 해도 되긴 함.
        for item in table:
            # getattr를 사용함
            if getattr(item, key, "") == val:
                return table.index(item)

        # 못 찾은 거면 -1를 반환하고 그에따른 처리를 진행합니다.
        return -1




    # conditions를 이용해서 어떤 열이든, 리스트로 검색하든, 문자열로 검색하든, 날짜를 검색하든
    # 어떤 값이든 찾아드리려고 노력해봅니다.
    # key="..."를 입력한다면 특정 컬럼에 대해서 검색도 가능합니다.
    #  재밌는 로직이네요.
    def _search_data_with_key_str_n_columns(self, df:pd.DataFrame, columns:list=None, **conditions):
        searched_df = df.copy()

        def cell_match_exact(cell, search_value):
            try:
                search_date = pd.to_datetime(search_value)
            except:
                search_date = None

            if isinstance(cell, datetime):
                if search_date is not None:
                    return cell.date() == search_date.date()
                else:
                    return str(search_value) == cell.strftime("%Y/%m/%d-%H:%M:%S")

            if isinstance(cell, list):
                return any(str(search_value) == str(item) for item in cell)

            return str(search_value) == str(cell)


        # 데이터프레임 서치 조건 함수, 부분 일치에 대한 함수
        def cell_match_partial(cell, search_value):
            try:
                search_date = pd.to_datetime(search_value)
            except Exception:
                search_date = None

            if isinstance(cell, datetime):
                if search_date is not None:
                    return cell.date() == search_date.date()
                else:
                    return str(search_value) == cell.strftime("%Y/%m/%d-%H:%M:%S")

            if isinstance(cell, list):
                return any(str(search_value) == str(item) for item in cell)

            return str(search_value) in str(cell)

        # 값이 만약 공백이거나 전체, ALL이라는 글자가 들어올 시, 필터링을 진행하지 않습니다.
        def should_skip(val):
            if isinstance(val, str):
                return val.strip() in SKIP_TUPLE

            if isinstance(val, list):
                # 리스트가 공백인 경우에는 진짜 아무것도 서치하지 않겠다는 의미이므로..
                # 예외로 Skip하지 않겠습니다.
                if len(val) == 0:
                    return False
                return str(val[0]).strip() in SKIP_TUPLE

            return True



        # conditions 중, key라는 데이터 말고 다른 데이터들에 대해 각 컬럼에서 검색을 수행합니다.
        # 열 이름을 헷갈리면 안됩니다.
        for col, value in conditions.items():
            # key에 대한 검색은 후에 진행합니다.
            if col == "key":
                continue

            # 조건에 대한 검색어가 공백, 전체, 선택없음일 때는 스킵합니다.
            if should_skip(value):
                continue

            # 값이 리스트로 반환된다면, .
            if isinstance(value, list):
                if col in searched_df.columns.values.tolist():
                    searched_df = searched_df[searched_df[col].apply
                    (lambda cell: any(cell_match_exact(cell, v) for v in value))
                    ]
            # 아니면 문자열이므로 문자열 검색을 합니다.
            else:
                searched_df = searched_df[searched_df[col].apply(lambda cell: cell_match_exact(cell, value))]


        # key에 대한 검색을 진행합니다.
        if "key" in conditions:
            key_value = conditions["key"]
            if key_value != "":
                if columns is None:
                    columns = searched_df.columns.values.tolist()

                # columns에 값을 잘못넣으면 서치하지 않습니다.
                missing_cols = list(set(columns) - set(searched_df.columns.values.tolist()))
                if missing_cols:
                    logging.error("데이터프레임에 존재하지 않는 열은 검색할 수 없습니다.")
                    return df

                # 리스트 안에서도 검색할 수 있도록 합니다.
                mask = searched_df[columns].apply(
                    lambda row: any(cell_match_partial(cell, key_value) for cell in row), axis=1
                )
                searched_df = searched_df[mask]

        return searched_df

    # 날짜에 따라서 필터링 합니다. Update_time 필터링
    # 오늘로부터 하루동안, 일주일동안 등등 필터링
    def _filter_data_with_until_before_X_days(self, df:pd.DataFrame, date_column:str=None, target_time:str=""):
        if date_column is None:
            logging.error('date_column이 입력되지 않음')
            return df

        # Date_Column이 데이터프레임에 존재하지 않으면 펄티렁이 불가능하므로 다시 반환
        if date_column not in df.columns.values.tolist():
            logging.error("데이터프레임에 해당 컬럼이 존재하지 않음")
            return df

        if target_time == "":
            logging.error("target_time이 입력되지 않음")
            return df

        # target_time이 SKIP_TUPLE 안에 있는 값이라면 필터링을 하지 않습니다.
        if target_time.strip() in SKIP_TUPLE:
            return df

        target_hour:int = 0
        if target_time == "day":
            target_hour = 24
        elif target_time == "weekly":
            target_hour = 168

        if target_hour <= 0:
            logging.error("제대로 된 기간 필터링을 입력 바람. ('day','weekly','month','year'(month, year는 예정))")
            return df

        # 날짜 필터링
        mask = df[date_column].apply(lambda dt: self._get_time_diff(target_time=dt, target_hour=target_hour, reverse=True))
        filtered_df = df[mask]

        return filtered_df

    # 이거 수정해야함
    # 로직에 살짝 변경이 있을 예정
    # 오늘을 기준으로, 현재 진행 중인, 종료된, 예정인 데이터들을 필터링합니다.
    def _filter_data_with_date_in_progress(self, df:pd.DataFrame, date_columns:list=None, when:str=''):
        if date_columns is None:
            logging.error("date_columns가 입력되지 않음")
            return df

        missing_cols = list(set(date_columns) - set(df.columns.values.tolist()))
        if missing_cols:
            logging.error("존재하지 않는 열에 대해서는 검색이 불가능")
            return df

        if when not in ("ended", "in_progress", "not_start", "not_end"):
            logging.error("when은 다음 네 가지에 대해서만 대응됩니다. ('ended', 'in_progress', 'not_start', 'not_end')")
            return df

        now = datetime.now()

        # 리스트 분리 시, 조금의 꼼수를 사용합니다.
        # 리스트 길이가 가변일 수 있음. 길이가 1이거나 2일수있다.
        # 그래서 Padding을 하고 요소 2개만 가져와서 mapping합니다.


        start_column, end_column = date_columns[:2]
        mask = pd.Series(True, index=df.index)

        # 끝난 일정에 대한 필터링
        if when == "ended":
            mask &= (df[end_column] < now)

        # 끝나지 않은 일정에 대한 필터링 ( in_progress + not_start )
        elif when == "not_end":
            mask &= (df[end_column] >= now)

        # 진행 중인 일정에 대한 필터링
        elif when == "in_progress":
            mask &= (df[start_column] <= now < df[end_column])

        # 시작하지 않은 예정 일정에 대한 필터링
        elif when == "not_start":
            mask &= (df[start_column] > now)

        filtered_df = df[mask]

        return filtered_df

    # 일정에 맞는 데이터를 필터링합니다.
    # 이는 Update_time이 될수도 있고, Start_date, End_date가 될 수 있습니다.
    # date_option = day => 오늘을 기준으로 필터링 (오늘 하루동안 올라온/시작하는/끝나는 데이터를 분류)
    # date_option = week => 오늘을 포함하는 일주일 (월요일 ~ 금요일) 필터링
    def _filter_data_with_date_option(self, df:pd.DataFrame, date_option:str="", date_columns:list=None, **condition):
        if date_columns is None:
            logging.error("date_columns가 입력되지 않음")
            return df

        missing_cols = list(set(date_columns) - set(df.columns.values.tolist()))
        if missing_cols:
            logging.error("존재하지 않는 열에 대해서는 검색이 불가능")
            return df

        # 마스킹 데이터 만들기
        mask = pd.Series(True, index=df.index)
        if date_option in SKIP_TUPLE:
            pass

        elif date_option not in ("day", "weekly", "specific"):
            logging.error("date_option은 day, weekly, specific 에만 대응 됨")

        # 데이터가 당일에만 시작하는 / 끝나는 / 진행(시작-끝이 오늘) 인 데이터들만 필터링
        elif date_option == "day":
            today_str = datetime.now().strftime("%Y/%m/%d")
            today = datetime.strptime(today_str, "%Y/%m/%d")
            for date_column in date_columns:
                mask &= (df[date_column].dt.date == today)

        # 데이터가 이번 주에만 시작 / 끝/ 진행하는 데이터인지
        elif date_option == "weekly":
            # 월요일, 일요일 날짜 데이터, 마스킹 데이터 얻음
            monday, sunday = self._get_monday_sunday_of_this_week()
            for date_column in date_columns:
                mask &= ((monday <= df[date_column]) & (df[date_column] <= sunday))

        elif date_option == "specific":
            if "specific_date" in condition:
                # if specific_date == str, transform datetime object
                if type(condition["specific_date"]) == str and not condition["specific_date"] in SKIP_TUPLE:
                    specific_date = datetime.strptime(condition["specific_date"], "%Y/%m/%d").date()
                else:
                    specific_date = condition["specific_date"].date()      # datetime obj


                # if date_columns length is not 2, not filtering.
                if len(date_columns) < 2:
                    logging.error("시작 날짜, 종료 날짜가 제대로 설정되지 않아 필터링을 할 수 없습니다.")
                    mask = pd.Series(False, index=df.index)
                else:
                    # start_date_columns, end_date_columns가 서로 바뀌어도 날짜가 일찍이면 start, 늦으면 end로 판단함

                    start_date = df[[date_columns[0], date_columns[1]]].min(axis=1).dt.date
                    end_date = df[[date_columns[0], date_columns[1]]].max(axis=1).dt.date

                    # specific in start date ~ end_date
                    mask &= ((start_date <= specific_date) & (specific_date <= end_date))


        # 최종 필터링
        filtered_df = df[mask]
        return filtered_df



#-------------------------------------------------------------------------------------------------------------------------------------

# ManagedFeed 테이블 클래스.
# 기존의 SearchEngine 에서는 각 Manager마다 각기 정의된 ManagedTable을 가졌는데
# 너무 복잡해짐에 따라, 통합하기로 결정. 클래스화 시킵니다.
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
#         self.__init_feed_avltree()
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
#     def __get_time_diff(self, target_time, target_hour=0.5, reverse=False) -> bool:
#         reference_time=datetime.now()
#         time_diff = abs(target_time - reference_time)
#         # pprint("현재 시" + str(reference_time))
#         # pprint("시간 차 :" + str(time_diff))
#         # pprint("기준 시간 :" + str(timedelta(hours=target_hour)))
#
#         # 차이가 2시간 이상인지 확인
#         if reverse:
#             return time_diff < timedelta(hours=target_hour)
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
#             # 이제 관리될 바이어스를 만들고 연결한다음
#             managed_bias = ManagedBias(bid=single_bias.bid, bname=single_bias.bname, user_nodes=user_nodes, board_types=single_bias.board_types)
#             #pprint(managed_bias.to_dict())
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
#     def search_feed_with_time_or_like(self, search_type:str="", time_type:str=""):
#         searched_df = self.__feed_df
#         # pprint(searched_df)
#
#         if search_type == "best":
#             searched_df = searched_df[searched_df['like'] >= 30]
#
#         if time_type == "" or time_type == "all" or time_type == "전체":
#             pass
#         elif time_type == "day":
#             searched_df = searched_df[self.__get_time_diff(target_time=searched_df['date'],target_hour=24, reverse=True)]
#         elif time_type == "weekly":
#             searched_df = searched_df[self.__get_time_diff(target_time=searched_df['date'],target_hour=168, reverse=True)]
#
#         # pprint(searched_df[:10])
#         return searched_df['fid'].tolist()
#
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
#     # def search_feed_with_key_and_option(self, option:str, key:str="", num_feed=10, index=-1) -> tuple:
#     #     result_fid = []
#     #     result_index = -3
#     #
#     #     if index == -1:
#     #         index = self.len_feed_table()
#     #
#     #         # target_index default 값은 0
#     #     search_range = self.get_feeds_target_range(index=index)
#     #     # search_range = self.__feed_table[:index][::-1]
#     #
#     #     if index < 0 or index > self.len_feed_table():
#     #         return result_fid, -3
#     #
#     #     count = 0
#     #     for i, managed_feed in enumerate(search_range):
#     #         #i = len(self.__feed_table) - 1 - i
#     #         # count로 이미 다 살펴 봤다면
#     #         if count == num_feed:
#     #             break
#     #
#     #         # 삭제된 피드는 None으로 표시될것이라서
#     #         if managed_feed.fid == "":
#     #             continue
#     #
#     #         if option == "hashtag":
#     #             # 찾는 해시태그가 아님
#     #             if key not in managed_feed.hashtag:
#     #                 continue
#     #         elif option == "uname":
#     #             if key not in managed_feed.uname:
#     #                 continue
#     #         elif option == "bid":
#     #             if key != managed_feed.bid:
#     #                 continue
#     #
#     #         elif option == "fid":
#     #             if key == managed_feed.fid:
#     #                 result_fid.append(managed_feed)
#     #                 result_index = i
#     #                 break
#     #
#     #
#     #         result_fid.append(managed_feed.fid)
#     #
#     #         # result_index 업데이트
#     #         # 마지막 index 발견
#     #         result_index = index - 1 - i  # 실제 self.__feed_table에서의 인덱스 계산
#     #         count += 1
#     #
#     #     return result_fid, result_index
#
#     def search_feeds_with_key_n_option(self, key:str, fclass:str, board_type:str, target_time:str, option):
#         # Nan값의 경우, False 처리.
#         # 대소문자를 구분하지 않음
#         searched_df = self.__feed_df
#
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
#         # board_type 필터링
#         # board_type이 ""이거나 All이면 다 고름
#         # 아니라면 board_type 필터링을 진행함
#         if board_type == "" or board_type == "all" or board_type == "전체":
#             pass
#         else:
#             searched_df = searched_df[searched_df["board_type"] == board_type]
#
#         if fclass == "" or fclass == "all" or fclass == "전체":
#             pass
#         else:
#             # Fclass == long 인지 fclass == short인지 분류
#             searched_df = searched_df[searched_df["fclass"] == fclass]
#
#         # 시간에 따라 분류하는 함수 ( 일간 주간 )
#         if target_time=="" or target_time=="all" or target_time=="전체":
#             pass
#         elif target_time=="day":
#             searched_df = searched_df[self.__get_time_diff(target_time=searched_df['date'],target_hour=24, reverse=True)]
#         elif target_time=="weekly":
#             searched_df = searched_df[self.__get_time_diff(target_time=searched_df['date'],target_hour=168, reverse=True)]
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
#     #----------------------------------------------------------------------------------------------
#     def filtering_bias_community(self, bid:str, board_type:str):
#         filtered_feeds_df = self.__feed_df[self.__feed_df['bid']==bid]
#         if board_type == "" or board_type == "전체" or board_type == "all" or board_type == "선택없음":
#             pass
#         else:
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
#         if category != "" or category != "전체" or category != "all" or category != "선택없음" :
#             filtered_feeds_df = fid_list_df[(fid_list_df['board_type'] == category)]
#             # pprint(filtered_feeds_df)
#             return filtered_feeds_df['fid'].tolist()
#         return fid_list_df['fid'].tolist()
#
#     def filtering_categories_feed_new(self, fid_list:list, categories:list):
#         fid_list_df = self.__feed_df[(self.__feed_df['fid'].isin(fid_list))]
#         # Filtering 시, 다음의 값을 유의
#         # fclass == ""인 경우, 모든 경우를 가져옵니다. 어짜피 AD는 Notice의 경우로 들어가니까 상관없겠지요.
#         if categories[0] != "" or categories[0] != "전체" or categories[0] != "all" or categories[0] != "선택없음":
#             filtered_feeds_df = fid_list_df[(fid_list_df['board_type'].isin(categories))]
#             # pprint(filtered_feeds_df)
#             return filtered_feeds_df['fid'].tolist()
#         return fid_list_df['fid'].tolist()

class ManagedFeedBiasTable(ManagedTable):
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
        self.__feed_df = self._add_new_data_in_df(df=self.__feed_df,
                                                  new_dict_data=managed_feed.to_dict(),
                                                  fid=managed_feed.fid)
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
        self._modify_data_in_df(df=self.__feed_df,
                                modify_dict_data=managed_feed.to_dict(),
                                fid=managed_feed.fid)

        return

    # ManagedFeed가 삭제되었기 때문에, 테이블과 트리에서도 삭제시킴
    def remove_feed(self, feed:Feed):
        # 삭제하는 함수. 피드가  삭제되면 None으로 바뀔것
        managed_feed = self.__feed_avltree.get(key=feed.fid)
        managed_feed = ManagedFeed()
        table_index = self._get_obj_index_in_table_with_id(table=self.__feed_table, fid=feed.fid)

        if table_index != -1:
            self.__feed_table.pop(table_index)

        self.__feed_avltree.remove(key=feed.fid)
        # dataframe 삭제
        self.__feed_df = self._remove_data_in_df(df=self.__feed_df, fid=feed.fid)

        return



    # 시간 차이를 바탕으로 정해진 시간대 내의 피드 정보 구하기
    # target_hour : 1, 24, 168
    def search_feed_with_time_or_like(self, search_type:str="", time_type:str="", return_id:bool=True):
        searched_df = self.__feed_df
        if search_type == "best":
            searched_df = searched_df[searched_df['like'] >= 30]

        # 게시글 날짜 필터링
        searched_df = self._filter_data_with_until_before_X_days(df=searched_df, date_column="date", target_time=time_type)

        # 마지막, 삭제된 Feed는 반환하지 않는다.
        searched_df = searched_df[searched_df['display'] != 0]

        # pprint(searched_df[:10])
        if return_id:
            return searched_df['fid'].tolist()
        return searched_df.to_dict('records')

    # 키워드와 필터링을 통해 데이터프레임에서 Feed들을 찾아냅니다.
    # 다양한 옵션들을 제공하고.. 있긴 합니다.
    def search_feeds_with_key_n_option(self, key:str, fclass:str, board_type:str, target_time:str, option, return_id:bool=True):
        # # Nan값의 경우, False 처리.
        # # 대소문자를 구분하지 않음
        # 데이터 프레임 검색 옵션 : Option에 따라 리스트가 달라짐
        columns = [option]

        searched_df = self._search_data_with_key_str_n_columns(df=self.__feed_df, columns=columns,
                                                               key=key, board_type=board_type, fclass=fclass)

        # 시간에 따라 분류하는 함수 ( 일간, 주간 )
        searched_df = self._filter_data_with_until_before_X_days(df=searched_df, date_column="date", target_time=target_time)

        # 마지막, 삭제된 Feed는 반환하지 않는다.
        searched_df = searched_df[searched_df['display'] != 0]

        # ID를 반환할 지, 데이터를 반환할 지 결정합니다.
        if return_id:
            return searched_df['fid'].tolist()
        return searched_df.to_dict('records')



    # 바이어스 별 필터링을 진행합니다.
    def filtering_bias_community(self, bid:str, board_type:str, return_id:bool=True):
        filtered_feeds_df = self._search_data_with_key_str_n_columns(df=self.__feed_df, bid=bid, board_type=board_type)
        # 마지막, 삭제된 Feed는 반환하지 않는다.
        filtered_feeds_df = filtered_feeds_df[filtered_feeds_df['display'] != 0]
        if return_id:
            return filtered_feeds_df['fid'].tolist()
        return filtered_feeds_df.to_dict('records')

    # 여기서는 추가적인 필터링을 위해 필터링된 FID리스트를 받고, 2차 필터링을 실시하는 곳입니다.
    def filtering_fclass_feed(self, fid_list:list, fclass:str, return_id:bool=True):
        # Filtering 시, 다음의 값을 유의
        # fclass == ""인 경우, 모든 경우를 가져옵니다.
        filtered_feeds_df = self._search_data_with_key_str_n_columns(df=self.__feed_df, fid=fid_list, fclass=fclass)

        # 마지막, 삭제된 Feed는 반환하지 않는다.
        filtered_feeds_df = filtered_feeds_df[filtered_feeds_df['display'] != 0]
        if return_id:
            return filtered_feeds_df['fid'].tolist()
        return filtered_feeds_df.to_dict('records')

    # 카테고리별 피드를 나눕니다.
    def filtering_categories_feed(self, fid_list:list, categories:list, return_id:bool=True):
        # Filtering 시, 다음의 값을 유의
        # categories[0] == ""인 경우, 모든 경우를 가져옵니다.
        filtered_feeds_df = self._search_data_with_key_str_n_columns(df=self.__feed_df, fid=fid_list, board_type=categories)

        # 마지막, 삭제된 Feed는 반환하지 않는다.
        filtered_feeds_df = filtered_feeds_df[filtered_feeds_df['display'] != 0]
        if return_id:
            return filtered_feeds_df['fid'].tolist()
        return filtered_feeds_df.to_dict('records')

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
            bias_data = self._database.get_data_with_id(target="bid", id=single_schedule.bid)
            bias=Bias().make_with_dict(dict_data=bias_data)

            start_date_time = self._get_date_str_to_object(str_date=single_schedule.start_date+'-'+single_schedule.start_time+':00')
            end_date_time = self._get_date_str_to_object(str_date=single_schedule.end_date+'-'+single_schedule.end_time+':00')

            time_sections = self._get_schedule_time_section(start_time=start_date_time, end_time=end_date_time)

            managed_schedule = ManagedSchedule(sid=single_schedule.sid,
                                               sname=single_schedule.sname,
                                               bid=single_schedule.bid,
                                               bname=single_schedule.bname,
                                               bias_gender=bias.gender,
                                               bias_category=bias.category,
                                               bias_tags=bias.tags,
                                               uname=single_schedule.uname,
                                               date=self._get_date_str_to_object(str_date=single_schedule.update_datetime),
                                               start_date_time=start_date_time,
                                               end_date_time=end_date_time,
                                               time_section=time_sections,
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

        # pprint(self.__schedule_df[["sid", "sname", "bname", "date", "start_date_time", "end_date_time"]].head(10))
        pprint(f"init한 start_date_time : {self.__schedule_df['start_date_time'].dtype}")
        # datetime64[ns]로 출력됨. 정상적인 것

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
            bias_data = self._database.get_data_with_id(target="bid", id=bundle.bid)
            bias=Bias().make_with_dict(dict_data=bias_data)


            start_date = bundle.date[0]+"-00:00:00"
            end_date = bundle.date[1]+"-00:00:00"

            managed_bundle = ManagedScheduleBundle(sbid=bundle.sbid,
                                                   sbname=bundle.sbname,
                                                   bid=bundle.bid,
                                                   bname=bundle.bname,
                                                   bias_gender=bias.gender,
                                                   bias_category=bias.category,
                                                   bias_tags=bias.tags,
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
        start_date_time = self._get_date_str_to_object(schedule.start_date+'-'+schedule.start_time+':00')
        end_date_time = self._get_date_str_to_object(schedule.end_date+'-'+schedule.end_time+':00')

        # 타임 섹션 데이터 삽입
        time_section = self._get_schedule_time_section(start_time=start_date_time,
                                                       end_time=end_date_time)

        pprint("추가된 schedule")
        pprint(f"start_time : {start_date_time}")
        pprint(f"start_date_time.type : {type(start_date_time)}")
        pprint(f"end_time : {end_date_time}")
        pprint(f"end_date_time.type : {type(end_date_time)}")
        
        managed_schedule = ManagedSchedule(
            sid=schedule.sid,
            sname=schedule.sname,
            bid=schedule.bid,
            bname=schedule.bname,
            uname=schedule.uname,
            date=self._get_date_str_to_object(str_date=schedule.update_datetime),
            start_date_time=start_date_time,
            end_date_time=end_date_time,
            time_section=time_section,
            location=copy(schedule.location),
            code=schedule.code,
            state=schedule.state
        )

        managed_schedule()
        # 바이어스 데이터 삽입
        bias_data = self._database.get_data_with_id(target="bid", id=managed_schedule.bid)
        bias = Bias()
        bias.make_with_dict(dict_data=bias_data)

        managed_schedule.bias_gender = bias.gender
        managed_schedule.bias_tags = bias.tags
        managed_schedule.bias_category = bias.category

        self.__schedule_table.append(managed_schedule)
        self.__schedule_tree.insert(managed_schedule.sid, managed_schedule)

        self.__schedule_df = self._add_new_data_in_df(df=self.__schedule_df,
                                                      new_dict_data=managed_schedule.to_dict(),
                                                      sid=managed_schedule.sid)
        
        
        self.__schedule_df = self.__schedule_df.sort_values(by='date', ascending=False).reset_index(drop=True)

        pprint(self.__schedule_df[["sid","sname", "bname", "date", "start_date_time", "end_date_time"]].head(10))
        pprint(f"추가 된 후의 start_date_time : {self.__schedule_df['start_date_time'].dtype}")
        #

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

        self._modify_data_in_df(df=self.__schedule_df,
                                modify_dict_data=managed_schedule.to_dict(),
                                sid=managed_schedule.sid)

        return

    # 스케줄 삭제
    def remove_schedule_in_table(self, sid:str):
        managed_schedule = self.__schedule_tree.get(key=sid)
        managed_schedule = ManagedSchedule()
        table_index = self._get_obj_index_in_table_with_id(table=self.__schedule_table, sid=sid)

        if table_index != -1:
            self.__schedule_table.pop(table_index)

        self.__schedule_tree.remove(key=sid)
        self.__schedule_df = self._remove_data_in_df(df=self.__schedule_df, sid=sid)

        return

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


        # 바이어스 데이터
        bias_data = self._database.get_data_with_id(target="bid", id=managed_bundle.bid)
        bias = Bias()
        bias.make_with_dict(dict_data=bias_data)

        managed_bundle.bias_gender = bias.gender
        managed_bundle.bias_tags = bias.tags
        managed_bundle.bias_category = bias.category

        self.__schedule_bundle_table.append(managed_bundle)
        self.__bundle_tree.insert(managed_bundle.sbid, managed_bundle)

        self.__schedule_bundle_df = self._add_new_data_in_df(df=self.__schedule_bundle_df,
                                                             new_dict_data=managed_bundle.to_dict(),
                                                             sbid=managed_bundle.sbid)
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

        self._modify_data_in_df(df=self.__schedule_bundle_df,
                                modify_dict_data=managed_bundle.to_dict(),
                                sbid=managed_bundle.sbid)

        return

    # 번들 데이터 삭제
    def remove_bundle_in_table(self, sbid:str):
        managed_bundle = self.__bundle_tree.get(key=sbid)
        managed_bundle = ManagedScheduleBundle()
        table_index = self._get_obj_index_in_table_with_id(table=self.__schedule_bundle_table, sbid=sbid)

        # 못 찾은 경우에는 지우지 못한다
        if table_index != -1:
            self.__schedule_bundle_table.pop(table_index)       # 리스트에서 삭제

        self.__bundle_tree.remove(key=sbid)
        self.__schedule_bundle_df = self._remove_data_in_df(df=self.__schedule_bundle_df, sbid=sbid)

        return




    # 탐색 스케줄 얻음
    # 이거 기능을 분리하는게 나을지도 모르겠는데 생각 해볼려고 함
    def search_explore_schedule(self, time_section:int, style:str, gender:str, return_id:bool):
        searched_df = self._search_data_with_key_str_n_columns(df=self.__schedule_df, time_section=time_section,
                                                               bias_gender=gender, bias_tags=style)
        searched_df = self._filter_data_with_date_option(df=searched_df, date_option="weekly", date_columns=["start_date_time"])

        if return_id:
            return searched_df['sid'].to_list()
        return searched_df.to_dict('records')

    # 날짜와 bid를 통해 일정을 검색합니다.
    def search_schedule_with_date_n_bids(self, selected_sids:list, date:str, bid:str, return_id:bool):
        searched_df = self._search_data_with_key_str_n_columns(df=self.__schedule_df, sid=selected_sids, bid=bid, date=date)

        if return_id:
            return searched_df['sid'].to_list()
        return searched_df.to_dict('records')

    # 현재 시간에 맞춰서 스케줄 일정 필터링 (종료된 스케줄, 진행 중인 스케줄, 예정된 스케줄)
    def filtering_schedule_is_in_progress(self, selected_sids:list, when:str, return_id:bool):
        # 선택된 sid 필터링
        searched_df = self._search_data_with_key_str_n_columns(df=self.__schedule_df, sid=selected_sids)
        # 날짜 필터링
        searched_df = self._filter_data_with_date_in_progress(df=searched_df,
                                                              date_columns=["start_date_time", "end_date_time"],
                                                              when=when)
        if return_id:
            return searched_df['sid'].to_list()
        return searched_df.to_dict('records')

    # 오늘 날짜, 혹은 특정 날짜에 대한 일정들을 표시하는 기능.
    def filtering_schedule_in_specific_date(self, selected_sids:list, specific_date:str, return_id:bool):
        searched_df = self._search_data_with_key_str_n_columns(df=self.__schedule_df, sid=selected_sids)
        searched_df = self._filter_data_with_date_option(df=searched_df, date_option="specific",
                                                         date_columns=["start_date_time", "end_date_time"],
                                                         specific_date=specific_date)

        if return_id:
            return searched_df['sid'].to_list()
        return searched_df.to_dict('records')


    # 스케줄 번들 일정 필터링
    def filtering_bundle_is_in_progress(self, selected_sbids:list, when:str, return_id:bool):
        # 선택된 sbid 필터링
        searched_df = self._search_data_with_key_str_n_columns(df=self.__schedule_bundle_df, sbid=selected_sbids)
        # 날짜 필터링
        searched_df = self._filter_data_with_date_in_progress(df=searched_df,
                                                              date_columns=["start_date", "end_date"],
                                                              when=when)

        if return_id:
            return searched_df['sbid'].to_list()
        return searched_df.to_dict('records')

    # 금주의 일정 필터링
    def filtering_weekday_schedule(self, selected_sids:list, return_id:bool):
        # 선택된 sids 필터링
        searched_df = self._search_data_with_key_str_n_columns(df=self.__schedule_df, sid=selected_sids)
        # 금주의 일정 필터링
        searched_df = self._filter_data_with_date_option(df=searched_df, date_option="weekly", date_columns=["start_date_time", "end_date_time"])

        if return_id:
            return searched_df['sid'].to_list()
        return searched_df.to_dict('records')

    # 금주의 일정 번들 필터링
    def filtering_weekday_bundle(self, selected_sbids:list, return_id:bool):
        # 선택한 sbids 필터링
        searched_df = self._search_data_with_key_str_n_columns(df=self.__schedule_bundle_df, sid=selected_sbids)
        # 금주의 일정 필터링
        searched_df = self._filter_data_with_date_option(df=searched_df, date_option="weekly", date_columns=["start_date", "end_date"])

        if return_id:
            return searched_df['sid'].to_list()
        return searched_df.to_dict('records')



    # 키를 통해 스케줄을 검색합니다.
    def search_schedule_with_key(self, key:str, search_columns:list, return_id:bool):
        if len(search_columns) == 0 or search_columns[0]=="":
            columns =['sname', 'bname', 'uname', 'code']
        else:
            columns = search_columns
        searched_df = self._search_data_with_key_str_n_columns(df=self.__schedule_df, columns=columns, key=key)

        if return_id:
            return searched_df['sid'].to_list()
        return searched_df.to_dict('records')

    # 번들 서치 함수.
    def search_bundle_with_key(self, key:str, search_columns:list, return_id:bool):
        if len(search_columns) == 0 or search_columns[0]=="":
            columns =['sbname', 'bname', 'uname', 'code']
        else:
            columns = search_columns

        searched_df = self._search_data_with_key_str_n_columns(df=self.__schedule_bundle_df, columns=columns, key=key)

        if return_id:
            return searched_df['sbid'].to_list()
        return searched_df.to_dict('records')

    # sid를 넣으면 sid에 맞는 것들을 반환합니다.
    def search_schedule_with_sids(self, sids:list, return_id:bool):
        searched_df = self._search_data_with_key_str_n_columns(df=self.__schedule_df, sid=sids)

        if return_id:
            return searched_df['sid'].to_list()
        return searched_df.to_dict('records')

    # sbid를 넣으면 sbid에 맞는 Manged 객체들을 반환합니다.
    def search_bundle_with_sbids(self, sbids:list, return_id:bool):
        searched_df = self._search_data_with_key_str_n_columns(df=self.__schedule_bundle_df, sbid=sbids)

        if return_id:
            return searched_df['sbid'].to_list()
        return searched_df.to_dict('records')

    # 이거 위의 저 함수들을 쓰게되면 이걸 managed_table에서 해결하는게 아니라 Search_engine에서 2개의 함수를 운용하는게 나을지도 모르겠는데
    # 살짝만 더 고민하다가 바꾸겠음
    # 내가 선택한 일정들을 보는 함수
    def search_my_selected_schedules(self, bid:str, selected_sids:list, return_id:bool):
        searched_df = self._search_data_with_key_str_n_columns(df=self.__schedule_df, sid=selected_sids, bid=bid)

        if return_id:
            return searched_df['sbid'].to_list()
        return searched_df.to_dict('records')

    # 내가 선택한 일정 번들들을 보는 함수
    def search_my_selected_bundles(self, bid:str, selected_sbids:list, return_id:bool):
        searched_df = self._search_data_with_key_str_n_columns(df=self.__schedule_bundle_df, sbid=selected_sbids, bid=bid)

        if return_id:
            return searched_df['sbid'].to_list()
        return searched_df.to_dict('records')
