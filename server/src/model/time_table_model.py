import re
from collections import Counter

from model.base_model import BaseModel
from model import Mongo_Database
from others.data_domain import Schedule, Bias, User
from others.time_table_engine import ScheduleSearchEngine as SSE
from others.object_storage_connector import ImageDescriper
import os

from pprint import pprint
from datetime import datetime,timedelta, time, date
import random
import string

#---------------------------------데이터 전송용 모델 (쁘띠 모델)----------------------------------------

# 얘들은 전부 쁘띠모델 입니다
# 스케쥴 트랜스포메이션 모델 (기본 변환 함수들만 담김)

# 근데 하다보니까 TransForm의 의미가 좀 더 확장되어
# Static Method를 통해 스케줄 만드는 함수를
class ScheduleTransformModel:
    def __init__(self):
        pass

    def _find_week_number(self, date_str):
        # 문자열을 datetime 객체로 변환
        date = datetime.strptime(date_str, "%Y/%m/%d")

        # 해당 달의 첫 번째 날
        first_day_of_month = datetime(date.year, date.month, 1)

        # 해당 날짜와 첫 번째 날의 주 번호 계산
        start_week = first_day_of_month.isocalendar()[1]  # 해당 달 첫 날의 주 번호
        current_week = date.isocalendar()[1]             # 해당 날짜의 주 번호

        # 현재 주가 3월 내의 몇 번째 주인지 계산
        week_in_month = current_week - start_week + 1

        return week_in_month

    def _calculate_day_hour_time(self, dtime:datetime):
        return dtime.strftime("%p %I:%M")

    def _transfer_date_str(self, dtime:datetime):
        return dtime.strftime("%m월 %d일")

        # formatted_date = f"{dtime.month}월 {dtime.day}일"
        # return formatted_date

    def _cal_update_time(self, update_time:datetime):
        today = datetime.today()

        diff = today - update_time
        seconds = diff.total_seconds()

        if seconds < 60:
            time_str = f"{int(seconds)} 초 전"
        elif seconds < 3600:
            minutes = seconds // 60
            time_str = f"{int(minutes)} 분 전"
        elif seconds < 3600 * 24:
            hours = seconds // 3600
            time_str = f"{int(hours)} 시간 전"
        elif seconds < 3600 * 24 * 30:
            days = seconds // (3600 * 24)
            time_str = f"{int(days)} 일 전"
        elif seconds < 3600 * 24 * 365:
            months = seconds // (3600 * 24 * 30)
            time_str = f"{int(months)} 달 전"
        else:
            years = seconds // (3600 * 24 * 365)
            time_str = f"{int(years)} 년 전"

        return time_str

    def _transfer_date_str_list(self, date_list):
        if len(date_list) == 0:
            return f"잘못된 데이터"

        if len(date_list) == 1:
            start_date = datetime.strptime(date_list[0],"%Y/%m/%d")
            start_date_str = start_date.strftime("%y년 %m월 %d일")
            return f"{start_date_str}"


        start_date = datetime.strptime(date_list[0],"%Y/%m/%d")
        start_date_str = start_date.strftime("%y년 %m월 %d일")
        end_date = datetime.strptime(date_list[1], "%Y/%m/%d")
        end_date_str = end_date.strftime("%y년 %m월 %d일")

        return f"{start_date_str}부터 {end_date_str}까지"

    def _linked_str(self,  str_list, sep=", "):
        return sep.join(str_list)

    # 전송용 폼을 만들기 위한 임시 데이터 작성 함수
    # 스태틱 메서드를 활용합니다.
    # 번들은 따로 만들지는 않음. (필요성은 있겠지만 나중에 요청받을 때 하겠습니다.)
    @staticmethod
    def make_temp_schedule(schedule:Schedule, bias:Bias, user:User):
        platform_list = re.split(r"\W+", schedule.platform)
        platform_list = [l for l in platform_list if l]

        schedule = Schedule(
            title=schedule.title,
            bid=bias.bid,
            bname=bias.bname,
            uid=user.uid,
            uname=user.uname,
            datetime=schedule.datetime,
            update_datetime=datetime.today().strftime("%Y/%m/%d-%H:%M:%S"),
            platform=platform_list,
            state=schedule.state
        )

        return schedule

# 일정 탭 전용 바이어스 데이터 폼 모델
class TimeBiasModel(ScheduleTransformModel):
    def __init__(self):
        super().__init__()
        self._biases = []

    # 일정, 시간표에서의 바이어스 데이터
    def _time_bias(self, bias:Bias):
        Sbias_data = {}

        Sbias_data["bid"] = bias.bid
        Sbias_data["bname"] = bias.bname
        Sbias_data["tags"] = self._linked_str(bias.tags)    # 연결해서 보냄
        Sbias_data["main_time"] = self._linked_str(bias.main_time) # 연결
        Sbias_data["is_ad"] = bias.is_ad
        if bias.platform:
            Sbias_data["category"] = bias.platform[0]       # 카테고리는 맨처음의 데이터만
        else:
            Sbias_data["category"] = "없음"

        return Sbias_data

    # 바이어스 데이터 폼 수정 리스트 반환
    def get_tbias_list(self, biases):
        for bias in biases:
            self._biases.append(self._time_bias(bias))
        return

    # 바이어스 데이터 반환
    def get_response_form_data(self):
        return self._biases

# 일정 스케줄 전송 데이터 폼 모델
class TimeScheduleModel(ScheduleTransformModel):
    def __init__(self) -> None:
        super().__init__()
        self._schedules = []

    # 스케쥴 Send Data 만드는 함수
    def _time_schedule(self, schedule:Schedule ):
        time_schedule_data = {}

        time_schedule_data["sid"] = schedule.sid
        time_schedule_data["detail"] = schedule.sname
        time_schedule_data["bid"] = schedule.bid
        time_schedule_data["bname"] = schedule.bname
        time_schedule_data["uid"] = schedule.uid
        time_schedule_data["uname"] = schedule.uname
        time_schedule_data["start_time"] = self._calculate_day_hour_time(datetime.strptime(schedule.start_time,"%H:%M"))
        time_schedule_data["end_time"] = self._calculate_day_hour_time(datetime.strptime(schedule.end_time, "%H:%M"))
        time_schedule_data["start_date"] = self._transfer_date_str(datetime.strptime(schedule.start_date, "%Y/%m/%d"))
        time_schedule_data["end_date"] = self._transfer_date_str(datetime.strptime(schedule.start_date, "%Y/%m/%d"))
        time_schedule_data["update_datetime"] = self._cal_update_time(datetime.strptime(schedule.update_datetime, "%Y/%m/%d-%H:%M:%S"))
        time_schedule_data["platform"] = self._linked_str(schedule.platform)
        time_schedule_data["code"] = schedule.code
        time_schedule_data["color_code"] = schedule.color_code
        time_schedule_data["subscribe"] = schedule.subscribe
        time_schedule_data["is_owner"] = schedule.is_owner
        time_schedule_data["url"] = schedule.url

        return time_schedule_data

    # 스케쥴 리스트 만드는 함수
    def get_tschedule_list(self, schedules):
        for schedule in schedules:
            self._schedules.append(self._time_schedule(schedule=schedule))

        return

    def get_response_form_data(self):
        return self._schedules

# ------------------------------------ 기본 타임 테이블 모델 ------------------------------------------
class TimeTableModel(BaseModel):
    def __init__(self, database:Mongo_Database) -> None:
        super().__init__(database)
        self._tuser = None
        self._key = -1
        
        self.__num_bias = 0
        self.__num_schedule = 0
        self.__target_month= f'00년 0월'
        self.__target_week= f'0주차'
        
        self._result = True
        self._detail = ""
        
    def _check_valid_access_schedule(self, bid, sid):
        # 일단 작성자인지 확인해야됨
        if sid not in self._user.my_sids:
            # 작성자가 아니면 스트리머가 직접 수정중인지 확인해야됨
            if self._user.verified_bias != bid:
                self._result = False
                self._detail = "잘못된 접근입니다."
                return False
            
        return True

    # string_date를 넣어서 몇주차인지 알아내는 함수임
    # date_str = "2025/03/06"
    def _find_week_number(self, date_str):
        # 문자열을 datetime 객체로 변환
        date = datetime.strptime(date_str, "%Y/%m/%d")

        # 해당 달의 첫 번째 날
        first_day_of_month = datetime(date.year, date.month, 1)

        # 해당 날짜와 첫 번째 날의 주 번호 계산
        start_week = first_day_of_month.isocalendar()[1]  # 해당 달 첫 날의 주 번호
        current_week = date.isocalendar()[1]             # 해당 날짜의 주 번호

        # 현재 주가 3월 내의 몇 번째 주인지 계산
        week_in_month = current_week - start_week + 1
        
        return week_in_month

    def _find_week_monday_N_sunday(self):
        today_str = datetime.today().strftime("%Y/%m/%d")
        today = datetime.strptime(today_str, "%Y/%m/%d")

        # weekday() -> 월 : 0, 화 : 1 ...  일 : 6
        monday = today - timedelta(days=today.weekday())
        sunday = today + timedelta(days=(6 - today.weekday()))

        return monday, sunday

    def _calculate_day_hour_time(self, dtime:datetime):
        hour = dtime.hour
        minute = dtime.minute

        if hour < 12:
            period = "오전"
            display_hour = hour if hour != 0 else 12

        else:
            period = "오후"
            display_hour = hour - 12 if hour > 12 else 12

        result = f"{period} {display_hour:02d}:{minute:02d}"
        return result

    def _transfer_date_str(self, dtime:datetime):
        formatted_date = f"{dtime.month}월 {dtime.day}일"
        return formatted_date

    def _cal_update_time(self, update_time:datetime):
        today = datetime.today()

        diff = today - update_time
        seconds = diff.total_seconds()

        if seconds < 60:
            time_str = f"{int(seconds)} 초 전"
        elif seconds < 3600:
            minutes = seconds // 60
            time_str = f"{int(minutes)} 분 전"
        elif seconds < 3600 * 24:
            hours = seconds // 3600
            time_str = f"{int(hours)} 시간 전"
        elif seconds < 3600 * 24 * 30:
            days = seconds // (3600 * 24)
            time_str = f"{int(days)} 일 전"
        elif seconds < 3600 * 24 * 365:
            months = seconds // (3600 * 24 * 30)
            time_str = f"{int(months)} 달 전"
        else:
            years = seconds // (3600 * 24 * 365)
            time_str = f"{int(years)} 년 전"

        return time_str

    # 쨍하고 밝은 색깔 코드 생성기
    def _make_color_code(self):
        # 더 쨍하고 밝은 색상을 위해 범위 설정
        r = random.randint(170, 255)  # 밝은 색상 범위
        g = random.randint(170, 255)
        b = random.randint(170, 255)

        # 흰색과의 혼합을 줄여 더 선명한 색상 유지
        r = (r * 3 + 255) // 4
        g = (g * 3 + 255) // 4
        b = (b * 3 + 255) // 4

        return f'#{r:02x}{g:02x}{b:02x}'

    # bias 세팅
    def set_num_bias(self):
        self.__num_bias= len(self._user.bids)
        return
        
    def set_num_schedule(self, schedule_search_engine:SSE):
        
        today = datetime.today()
        # 이번 주 월요일 계산
        monday = today - timedelta(days=today.weekday())
         # 이번 주 일요일 계산
        sunday = monday + timedelta(days=6)
        
        sid_list = []
        
         # 월요일부터 일요일까지 날짜 생성
        current_day = monday
        while current_day <= sunday:
            sids = schedule_search_engine.try_get_schedules_in_specific_date(sids=["all"], specific_date=current_day, return_id=True)
            sid_list.extend(sids)
            current_day += timedelta(days=1)  # 하루씩 증가
        
        for sid in sid_list:
            if sid in self._user.subscribed_sids:
                self.__num_schedule += 1
        
        return
    
    def __calc_date(self, today:datetime):
        first_day_of_month = datetime(today.year, today.month, 1)
        #print(first_day_of_month)

        # 월요일이 가장 빠른 날을 찾기 위해 이번 달 첫째 날부터 시작해서 월요일을 찾습니다.
        current_date = first_day_of_month
        while current_date.weekday() != 0:  # 0은 월요일을 나타냅니다.
            current_date += timedelta(days=1)

        # 해당 주가 1주차인지 계산합니다.
        start_week = current_date.isocalendar()[1]  # 해당 달 첫 번째 월요일이 속한 주 번호
        current_week = today.isocalendar()[1]       # 오늘 날짜의 주 번호
        
        return start_week, current_week
    
    def set_target_date(self, date=datetime.today().strftime("%Y/%m/%d")):
        today = datetime.strptime(date, "%Y/%m/%d")
        start_week, current_week = self.__calc_date(today)
    
        if start_week > current_week:
            # 이번 주의 월요일이 today임
            today = today = today - timedelta(days=today.weekday())
            start_week, current_week = self.__calc_date(today)
        
        # 현재 주가 이번 달 내 몇 번째 주인지 계산합니다.
        week_in_month = current_week - start_week + 1
        
        shorted_year = today.year % 100
        
        # 만약 미래에 있는 사람이 2100에 산다면 이 곳의 코드를 고치면 됩니다
        self.__target_month = f'{shorted_year}년 {today.month}월'
        self.__target_week = f'{week_in_month}주차'
        return
    
    # 컨트롤러에서 유저가 있는지 확인이 가능하게 하는 부분
    def is_tuser_alive(self):
        if self._tuser.tuid == "":
            return False
        else:
            return True

    # 현재 시간이 end_date/ end_time을 넘기면 True, 아니면 False다.
    def __check_schedule_time(self, date:str, when:str, time:str=""):
        # # 날짜 데이터

        date_obj = datetime.strptime(date, "%Y/%m/%d")

        # 시간 데이터가 존재한다면 시간도 같이 붙여야 함
        if time != "":
            time_obj = datetime.strptime(time, "%H:%M")
            date_obj = datetime.combine(date=date_obj.date(), time=time_obj.time())

        if when == "end":
            return date_obj < datetime.now()
        elif when == "start":
            return date_obj > datetime.now()


    # 페이징 기법 함수
    def paging_id_list(self, id_list:list, last_index:int, page_size=8):
        # 최신순으로 정렬된 상태로 id_list를 받아오기 때문에, 인덱스 번호가 빠를수록 최신의 것
        # 만약에 페이지 사이즈보다 더 짧은 경우도 있을 수 있기에 먼저 정해놓는다.
        # 이러면 페이징된 리스트의 길이에 상관없이, 인덱스를 알아낼 수 있을 것

        # 아이디 리스트 중 last_index 부터 시작해서 나머지 모든 데이터를 꺼냄
        paging_list = id_list[last_index + 1:]
        last_index_next = -1
        if len(id_list) != 0:
            last_index_next = id_list.index(id_list[-1]) # 다음 라스트 인덱스를 설정

        # 페이지 사이즈가 -1 (전체)인 경우, 그대로 전체를 반환하고 라스트 인덱스도 갱신반환한다.
        if page_size == -1:
            return paging_list, last_index_next


        # 만약 페이지 사이즈를 넘었다면 표시할 개수만큼 짜르고, last_index를 재설정한다.
        if len(paging_list) > page_size:
            paging_list = paging_list[:page_size]
            # Paging 넘버
            last_index_next = id_list.index(id_list[last_index + page_size])

        return paging_list, last_index_next

    def get_response_form_data(self, head_parser):
        body = {
            #"tuser" : self._tuser,
            "num_bias" : self.__num_bias,
            "num_schedules" : self.__num_schedule,
            "target_month" : self.__target_month,
            "target_week" : self.__target_week
            }

        response = self._get_response_data(head_parser=head_parser, body=body)
        return response


# ------------------------------------- 스케쥴 모델 ------------------------------------------------
# 단일 스케줄을 반환할 때 사용하는 모델
# 사용할 일이 있을지는 모르는데, 아마 수정 같은 상황에 사용될것
class SingleScheduleModel(TimeTableModel):
    def __init__(self, database:Mongo_Database) -> None:
        super().__init__(database)
        self.__schedule = Schedule()

    def get_response_form_data(self, head_parser):
        body = {
            "schedule" : self.__schedule.get_dict_form_data(),
            "key" : self._key
            }

        response = self._get_response_data(head_parser=head_parser, body=body)
        return response

# 복수 스케줄을 반환할 때 사용하는 모델 NEW ( Search Engine 사용 )
# 아마 대부분이 여러개를 반환해야하니 이거 쓰면 될듯
class MultiScheduleModel(TimeTableModel):
    def __init__(self, database:Mongo_Database) -> None:
        super().__init__(database)
        self.__schedules:list = []
        self.__bias:Bias= Bias()
    
    def set_bias_data(self, bid:str):
        bias = self._get_bias_data(bid=bid)
        if bias:
            self.__bias = bias
            return True
        self._detail = "존재하지 않는 스트리머입니다."
        self._result = False
        return False
        

    def set_schedules_with_sids(self, data_payload):
        self._make_send_data_with_ids(id_list=data_payload.sids)
        return

    # id_list는 서치한 데이터들의 고유 아이디
    # 전송용 데이터를 만드는 함수
    def _make_send_data_with_ids(self, id_list:list):
        schedule_datas = self._database.get_datas_with_ids(target_id="sid", ids=id_list)

        for data in schedule_datas:
            schedule = Schedule()
            schedule.make_with_dict(data)
            self.__schedules.append(schedule)

        # 데이터들을 전부 변환
        self._make_send_data_with_datas()

        return

    # 이미 데이터를 받아온 경우에 씀
    def _make_send_data_with_datas(self):

        # 이미 등록 했는지 확인하는 함수
        for schedule in self.__schedules:
            schedule:Schedule = schedule
            if schedule.sid in self._user.subscribed_sids:
                schedule.subscribe = True

            if schedule.sid in self._user.my_sids:
                schedule.is_owner = True
                
            if schedule.bid == self._user.verified_bias:
                schedule.is_owner = True

        return


    def set_schedule_by_this_week(self):
        schedule_datas = self._database.get_datas_with_ids(target_id="sid", ids=self._tuser.this_week_sids)

        # 오늘 날잡아야됨
        today = datetime.today()
        today_week_number = today.isocalendar()[1]

        # 저장해야하는지 체크하는 플래그
        flag = False

        for schedule_data in schedule_datas:
            schedule = Schedule()
            schedule.make_with_dict(dict_data=schedule_data)

            # 이거 이번주 맞는지 체크해야되서 일단 날짜를 객체로 만들어줌
            target_date = datetime.strptime(schedule.date, "%Y/%m/%d")
            target_week_number = target_date.isocalendar()[1]

            # 년도가 같으면?
            if today.year == target_week_number:
                # 이번주랑 주차가 다르면 싹다 비워버리면됨
                if today_week_number != target_week_number:
                    self._tuser.this_week_sids.remove(schedule.sid)
                    flag = True
                    continue

            # 년도 다르면 걍 비우면됨
            else:
                self._tuser.this_week_sids.remove(schedule.sid)
                flag = True
                continue

            # 리스트에 넣으면됨
            self.__schedules.append(schedule)

        # 업데이트 했으면 데베에 저장할것
        if flag:
            self._database.modify_data_with_id(target_id="tuid", target_data=self._tuser.get_dict_form_data())

        # 스케줄 데이터 폼 수정
        self._make_send_data_with_datas()
        return

    # by_this_week이랑 by_week들을 데이터프레임으로 쇼부보고 싶은데 아직 마땅히 좋은게 떠오르지 않음.
    # 내가 타임테이블에 노출시키려고 했던 schedule을 보여줌
    # tuser의 this_week_sids를 기반으로 함

    # 주차에 따른 내가 추가한 스케줄을 보여줌
    def set_schedule_by_week(self, year="", week=0):
        # 데이터 불러오고
        schedule_datas = self._database.get_datas_with_ids(target_id="sid", ids=self._tuser.sids)

        # 필터링 해야되는데 날짜 기준이 필요함
        # year 가 없으면 그냥 이번주임

        # 아래가 이번주 체크하는거고
        if year =="":
            today = datetime.today()
            target_week_number = today.isocalendar()[1]
            year = today.year
        # 아래는 목표 주를 기준으로 체크
        else:
            target_week_number = week

        for schedule_data in schedule_datas:
            schedule = Schedule()
            schedule.make_with_dict(dict_data=schedule_data)
            # 날짜를 뽑아서 객체화 시키고
            date = datetime.strptime(schedule.date, "%Y/%m/%d")
            # 년도와 몇주차 비교해서 맞으면 넣어주면됨
            if year == date.year and target_week_number == date.isocalendar()[1]:
                self.__schedules.append(schedule)

        # 스케줄 데이터 폼 수정
        self._make_send_data_with_datas()

        return

    # 키워드를 통해 검색합니다.
    def search_schedule_with_keyword(self, schedule_search_engine:SSE, keyword:str, search_columns:str,
                                      when:str, num_schedules:int, last_index:int=-1):
        searched_list = []

        if search_columns == "":
            search_columns_list= []
        else:
            search_columns_list = [i.strip() for i in search_columns.split(",")]

        searched_list = schedule_search_engine.try_search_schedule_w_keyword(target_keyword=keyword, search_columns=search_columns_list)
        
        if when != "": # 진행중인 애만 찾고싶으면
            searched_list = schedule_search_engine.try_filtering_schedule_in_progress(sids=searched_list, when=when)

        searched_list, self._key = self.paging_id_list(id_list=searched_list, last_index=last_index, page_size=num_schedules)
        self._make_send_data_with_ids(id_list=searched_list)
        return

    # 내가 선택한 스케줄들을 반환
    def get_my_selected_schedules(self, schedule_search_engine:SSE, bid:str, num_schedules:int, last_index:int=-1):
        searched_list = schedule_search_engine.try_search_selected_schedules(sids=self._tuser.sids, bid=bid)
        searched_list, self._key = self.paging_id_list(id_list=searched_list, last_index=last_index, page_size=num_schedules)
        self._make_send_data_with_ids(id_list=searched_list)

        return

    # 이번 주 일정을 들고 옮
    def get_weekday_schedules(self, schedule_search_engine:SSE):
        searched_list = schedule_search_engine.try_get_weekday_schedule_list(sids=self._tuser.sids)
        self._make_send_data_with_ids(id_list=searched_list)

        return

    # 내가 설정한 모든 스케쥴 불러오기
    def search_my_all_schedule(self, schedule_search_engine:SSE):
        # 데이터 불러오고
        searched_list = schedule_search_engine.try_search_selected_schedules(sids=self._tuser.sids)
        self._make_send_data_with_ids(id_list=searched_list)

        return

    # 탐색용 스케줄 불러오기
    def get_explore_schedule_with_category(self, schedule_search_engine:SSE, time_section:int, category:str,
                                           style:str, gender:str, num_schedules:int, last_index:int=-1):
        searched_list = schedule_search_engine.try_get_explore_schedule_list(time_section=time_section, style=style, gender=gender, category=category)
        searched_list, self._key = self.paging_id_list(id_list=searched_list, last_index=last_index, page_size=num_schedules)
        self._make_send_data_with_ids(id_list=searched_list)

        return


    # 내가 작성한 스케쥴 가져오기 (수정을 위해서)
    def get_written_schedule(self, sid:str):
        schedule_data = self._database.get_data_with_id(target="sid",id=sid)
        if schedule_data:
            schedule=Schedule().make_with_dict(schedule_data)
        else:
            return

        if schedule.sid in self._user.my_sids:
            schedule.is_owner = True
            
        if schedule.bid == self._user.verified_bias:
            schedule.is_owner = True

        self.__schedules.append(schedule)
        return
    
    # 특정 월에 포함된 일정들 bias에 맞춰서 가져오기
    def set_schedule_in_monthly(self, schedule_search_engine:SSE, date:datetime):
        searched_list = schedule_search_engine.try_get_monthly_schedule_list(sids=self.__bias.sids, date=date)
        if searched_list:
            schedule_datas = self._database.get_datas_with_ids(target_id="sid", ids=searched_list)
            for data in schedule_datas:
                schedule = Schedule().make_with_dict(dict_data=data)
                if schedule.sid in self._user.subscribed_sids:
                    schedule.subscribe = True

                if schedule.sid in self._user.my_sids:
                    schedule.is_owner = True
                    
                if schedule.bid == self._user.verified_bias:
                    schedule.is_owner = True
                    

                self.__schedules.append(schedule)
        return

    # 전송용 폼데이터를 만드는 함수
    def get_print_forms_schedule(self, schedules:list, bid:str):
        bias_data = self._database.get_data_with_id(target="bid", id=bid)
        bias = Bias()
        bias.make_with_dict(bias_data)

        for make_schedule in schedules:
            schedule = ScheduleTransformModel.make_temp_schedule(schedule=make_schedule,bias=bias,user=self._user)
            self.__schedules.append(schedule)

        self._make_send_data_with_datas()

        return


    # 전송 데이터 만들기
    def get_response_form_data(self, head_parser):
        body = {
            "schedules" : self._make_dict_list_data(self.__schedules),
            "key" : self._key,
            "result" : self._result,
            "detail" : self._detail
        }
        
        if body["schedules"]:
            for schedule in body["schedules"]:
                datetime_obj:datetime = schedule["datetime"]
                schedule["datetime"] = datetime_obj.isoformat()
            
        response = self._get_response_data(head_parser=head_parser, body=body, serializable=False)
        return response


# 스케줄 추가 모델 New (Search_Engine) 사용
class AddScheduleModel(TimeTableModel):
    def __init__(self, database:Mongo_Database):
        super().__init__(database=database)
        self._result = False

    # sid 만들기
    def __make_new_sid(self):
        sid = self._make_new_id()
        return sid

    def __make_schedule_code(self):
        # 영어 대문자와 숫자로 이루어진 6자리 코드 생성
        characters = string.ascii_uppercase + string.digits
        code = ''.join(random.choices(characters, k=6))
        return code

    
    # 스케줄 구독하기
    def handle_subscribe_schedule(self, sid):
        if sid in self._user.subscribed_sids:
            self._user.subscribed_sids.remove(sid)
        else:
            self._user.subscribed_sids = list(set(self._user.subscribed_sids + [sid]))
            
        self._database.modify_data_with_id(target_id='uid', target_data=self._user.get_dict_form_data())
        self._result = True
        return

    # 내 스케줄 목록에서 지워버리는 곳 (이번주 목록이면 여기서 함)
    def reject_from_my_week_schedule(self, sid):
        # 저장해야하는지 체크하는 플래장
        flag= False

        if sid in self._user.subscribed_sids:
            self._user.subscribed_sids.remove(sid)
            flag = True

        if flag:
            self._database.modify_data_with_id(target_id="uid", target_data=self._user.get_dict_form_data())
            self._result = True
        return


    # 단일 스케줄 만들기
    def make_new_single_schedule(self, request_schedule):
        dt:datetime = request_schedule.datetime

        # 1️⃣ tz-aware -> tz-naive 변환
        if dt.tzinfo is not None:
            dt = dt.replace(tzinfo=None)

        # 2️⃣ datetime 객체 확인 (혹시 str로 들어오는 경우 처리)
        if not isinstance(dt, datetime):
            import pandas as pd
            dt = pd.to_datetime(dt, errors='coerce')  # 변환 불가 시 NaT

        # 3️⃣ Schedule 객체 생성
        schedule = Schedule(
            bid=request_schedule.bid,
            title=request_schedule.title,
            datetime=dt,
            duration=request_schedule.duration,
            tags=request_schedule.tags
        )

        bias_data = self._database.get_data_with_id(target="bid", id=schedule.bid)
        
        if bias_data:
            bias = self._bias = Bias().make_with_dict(bias_data)
        else:
            self._detail = "존재하지 않는 스트리머 입니다."
            return None
        
        schedule.sid = self.__make_new_sid()
        schedule.bname = bias.bname
        schedule.url = bias.platform_url
        schedule.uid = self._user.uid
        schedule.uname = self._user.uname
        schedule.code = self.__make_schedule_code()
        schedule.update_datetime = datetime.today().strftime("%Y/%m/%d-%H:%M:%S")
        schedule.platform = bias.platform 

        return schedule
    
    # 해당 날짜에 이미 스케줄이 있는지 체크
    def check_schedule_not_in_time(self, schedule_search_engine:SSE, schedule:Schedule):
        result = schedule_search_engine.try_find_schedules_in_all_schedules_with_specific_date(specific_date=schedule.datetime)
        if result:
            self._result = False
            self._detail = "선택한 날짜에 이미 스케줄이 존재합니다."
            return False
        else:
            return True
    
    
     # 복수 개의 (단일 포함) 스테줄 저장
    def save_new_schedule(self, schedule_search_engine:SSE, schedule:Schedule):
        schedule_search_engine.try_add_new_managed_schedule(new_schedule=schedule, category=self._bias.category)    # 서치 엔진에다가 저장합니다.
        self._database.add_new_data(target_id="sid", new_data=schedule.get_dict_form_data())                  # 데이터베이스에 먼저 저장

        self._user.my_sids.append(schedule.sid)  # 내가 만든 스케줄이기에 내 스케줄에도 추가
        self._user.subscribed_sids.append(schedule.sid)  # 내가 만든 스케줄이기에 구독한 스케줄에도 추가
        self._bias.sids.append(schedule.sid)  # 바이어스에도 추가

        self._database.modify_data_with_id(target_id="uid", target_data=self._user.get_dict_form_data())
        self._database.modify_data_with_id(target_id="bid", target_data=self._bias.get_dict_form_data())
        
        self.__auto_subscribe(sid=schedule.sid, bid=schedule.bid)
        
        self._result = True
        self._detail = "스케줄이 성공적으로 저장되었습니다."
        return
    
    # 자동으로 전부다 스케줄 넣어주는 마법의 함수
    def __auto_subscribe(self, sid:str, bid:str):
        uid_list = self._database.get_followers_with_bid(bid=bid)
        
        user_datas = self._database.get_datas_with_ids(target_id="uid", ids=uid_list)
        
        user_dict_list = []
        for user_data in user_datas:
            user = User().make_with_dict(user_data)
            temp_list = list(set(user.subscribed_sids + [sid]))
            user.subscribed_sids = temp_list
            user_dict_list.append(user.get_dict_form_data())
        
        self._database.modify_datas_with_ids(target_id="uid", ids=uid_list, target_datas=user_dict_list)
        return
    
    
    # 검증 해야됨
    def verifiy_modifying_schedule(self, modified_schedule:Schedule, sid):
        schedule_data = self._database.get_data_with_id(target="sid", id=sid)
        
        if schedule_data:
            schedule = Schedule().make_with_dict(schedule_data)
        else:
            return schedule, False
        
        
        if not self._check_valid_access_schedule(bid=schedule.bid, sid=schedule.sid):
            return schedule, False
        
        modified_schedule.sid = sid
        return modified_schedule, True
    
      # 복수 개의 (단일 포함) 스테줄 저장
    def update_modify_schedule(self, schedule_search_engine:SSE, schedule:Schedule):
        schedule_search_engine.try_modify_schedule(modify_schedule=schedule)
        self._database.modify_data_with_id(target_id="sid", target_data=schedule.get_dict_form_data())                  # 데이터베이스에 먼저 저장
        self._result = True
        self._detail = "스케줄이 성공적으로 저장되었습니다."
        return   


    # 스케줄 삭제
    def delete_schedule(self, schedule_search_engine:SSE, sid:str):
        schedule_data = self._database.get_data_with_id(target="sid", id=sid)
        if not schedule_data:
            self._detail = "존재하지 않는 스케줄입니다."
            return
        schedule = Schedule().make_with_dict(schedule_data)
        
        schedule.display = 0 # 삭제 표시

        self._database.modify_data_with_id(target_id="sid", target_data=schedule.get_dict_form_data())
        #self._database.delete_data_with_id(target="sid", id=sid)

        # 서치 엔진에서 편집합니다.
        schedule_search_engine.try_remove_schedule(sid=sid)
        self._result = True
        return
    
    
    # 이미지 업로드 준비
    def prepare_schedule_image(self, image_name, sid, bid):
        extension = ""
        
        if not self._database.get_data_with_id(target="sid", id=sid):
            self._result = False
            self._detail = "목표 일정을 찾을 수 없어요"
            return extension, False
        
        if not self._check_valid_access_schedule(bid=bid, sid=sid):
            return extension, False
        
        _, ext = os.path.splitext(image_name)
        extension = ext[1:].lower()
        
        return extension, True
        
    # 이미지 업로드 시도
    def upload_schedule_image(self, extenstion, image, sid):
        url, result = ImageDescriper().try_schedule_image_upload(sid=sid, extension=extenstion, image=image)
        
        if result:
            self._result = True
            self._detail = "업로드가 성공적으로 완료되었습니다."
        else :
            self._result = False
            self._detail = "이미지 업로드가 실패했습니다."
        
        return

    def get_response_form_data(self, head_parser):
        body = {
            "result" : self._result,
            "detail" : self._detail
        }

        response = self._get_response_data(head_parser=head_parser, body=body)
        return response


    
# temp_schedule_data = [
#   { tag : "노래/음악"},
#   { section : "새벽", schedules : [
#       ]
#   },
#   { section : "오전", schedules : [
#       { time: "AM 11:00", type: "recommened", schedule_id: "0", schedule_title: "아침 노래뱅", schedule_bias: "주제이름1", schedule_bid:"1" },
#       { time: "AM 11:00", type: "recommened", schedule_id: "1", schedule_title: "한식 맛집 아테의 노래뱅", schedule_bias: "주제이름2" , schedule_bid:"2"},
#       ]
#   },
#   { section : "오후", schedules : [
#       { time: "PM 01:00", type: "added", schedule_id: "2", schedule_title: "마지막 노래 방송", schedule_bias: "주제이름3", schedule_bid:"3"},
#       ]
#   },
#   { section : "저녁", schedules : [
#       { time: "PM 07:00", type: "recommened", schedule_id: "3", schedule_title: "잔잔노래짧뱅", schedule_bias: "주제이름4", schedule_bid:"4" },
#       { time: "PM 08:00", type: "recommened", schedule_id: "4", schedule_title: "이쁜이들이랑 싱크룸", schedule_bias: "주제이름5", schedule_bid:"5"},
#       ]
#   }
# ]
        
class ScheduleTimeLayerModel(TimeTableModel):
    def __init__(self, database:Mongo_Database) -> None:
        super().__init__(database)
        self.__schedules = []
        self.__layer_data = [
            {"tag" : ""},
            {"section":"새벽", "schedules":[]},
            {"section":"오전", "schedules":[]},
            {"section":"오후", "schedules":[]},
            {"section":"저녁", "schedules":[]}
        ]
        self.__my_layer_data = [
            {"tag" : ""},
            {"section":"새벽", "schedules":[]},
            {"section":"오전", "schedules":[]},
            {"section":"오후", "schedules":[]},
            {"section":"저녁", "schedules":[]}
        ]
        self.__recommand_layer_data = [
            {"tag" : ""},
            {"section":"새벽", "schedules":[]},
            {"section":"오전", "schedules":[]},
            {"section":"오후", "schedules":[]},
            {"section":"저녁", "schedules":[]}
        ]   
        self.__my_target_sids = []
        self.__recommend_target_sids = []
        
    # 단일 스케줄의 데이터 폼을 받아내는 객체
    def __make_single_schedule_data_form(self, type, schedule:Schedule):
        schedule_form = {}
        
        schedule_form["time"] = schedule.datetime.isoformat()
        schedule_form["type"] = type
        schedule_form["schedule_id"] = schedule.sid
        schedule_form["schedule_title"] = schedule.title
        schedule_form["schedule_bias"] = schedule.bname
        schedule_form["schedule_bid"] = schedule.bid
        return schedule_form
    
    # 태그 데이터 넣어줘야됨
    def set_tag_data(self):
        target_sids = []
        count = 0
        
        # 분석할 정보가 부족하면 tuser의 bias 카테고리 기반으로 세팅하면됨
        if len(self._tuser.sids) < 10:
            index = random.randint(0, len(self._tuser.category)-1)
            self.__layer_data[0]["tag"] = self._tuser.category[index]
            return
        
        
        for sid in reversed(self._tuser.sids):
            if count > 10:
                break
            
            target_sids.append(sid)
            count+=1

        schedule_datas = self._database.get_datas_with_ids(target_id="sid", ids=target_sids)
        
        tags = []
        unigue_tag = set()
        
        for schedule_data in schedule_datas:
            schedule = Schedule().make_with_dict(schedule_data)
            for tag in schedule.tags:
                tags.append(tag)
                unigue_tag.add(tag)
        
        # 각 태그의 개수를 세기
        tag_counts = Counter(tags)

        # 가장 많이 나온 태그와 그 개수 찾기
        most_common_tag, count = tag_counts.most_common(1)[0]  # [(tag, count)] 형태 반환
        
        self.__layer_data[0]["tag"]=most_common_tag
        return
    
    
    # 날짜에 맞는 스케줄 데이터 불러오기
    def make_my_schedule_data(self, target_date, schedule_search_engine:SSE):
        # 여기서 schedule_search_engine으로 검색해야됨
        # sids 전체애 대한 검색은 무조건 ["all"]로 해주시길 바람
        # specific_date의 자료형은 str 그대로 써도됩니다. managed_table에서 Datetime 객체로 변환시키도록 만들었음.
        # return_id = True -> sid list 반환, False -> managed_Schedule list 반환

        sids = schedule_search_engine.try_get_schedules_in_specific_date(sids=["all"], specific_date=target_date, return_id=True)

        # 여기서 managed_schedule은 dict 형태임
        for sid in sids:
            if sid in self._user.subscribed_sids:
                self.__my_target_sids.append(sid)
            else:
                self.__recommend_target_sids.append(sid)
                
        schedule_datas = self._database.get_datas_with_ids(target_id="sid", ids= self.__my_target_sids)
        
        # 다 만들면 보관
        for schedule_data in schedule_datas:
            schedule = Schedule().make_with_dict(dict_data=schedule_data)
            self.__schedules.append(schedule)
        return
    
    # 레이어 만들기
    def set_my_schedule_layer(self):
        # 핵심 시간 섹션
        
        # 섹션마다 분류
        for single_schedule in self.__schedules:
            
            single_schedule:Schedule = single_schedule
            time_obj = single_schedule.datetime
            
            options = [
                {
                    "start": datetime.combine(time_obj, datetime.min.time()),
                    "end": datetime.combine(time_obj, datetime.min.time()).replace(hour=6, minute=0),
                },
                {
                    "start": datetime.combine(time_obj, datetime.min.time()).replace(hour=6, minute=0),
                    "end": datetime.combine(time_obj, datetime.min.time()).replace(hour=12, minute=0),
                },
                {
                    "start": datetime.combine(time_obj, datetime.min.time()).replace(hour=12, minute=0),
                    "end": datetime.combine(time_obj, datetime.min.time()).replace(hour=18, minute=0),
                },
                {
                    "start": datetime.combine(time_obj, datetime.min.time()).replace(hour=18, minute=0),
                    "end": datetime.combine(time_obj, datetime.min.time()).replace(hour=23, minute=59),
                },
            ]
            
        
            if options[0]["start"] <= time_obj < options[0]["end"]:
                self.__my_layer_data[1]["schedules"].append(single_schedule)
            elif options[1]["start"] <= time_obj < options[1]["end"]:
                self.__my_layer_data[2]["schedules"].append(single_schedule)
            elif options[2]["start"] <= time_obj < options[2]["end"]:
                self.__my_layer_data[3]["schedules"].append(single_schedule)
            elif options[3]["start"] <= time_obj <= options[3]["end"]:  # 하루 끝 비교는 <= 사용
                self.__my_layer_data[4]["schedules"].append(single_schedule)
            else:
                continue
            
            
    # 날짜에 맞는 스케줄 데이터 불러오기
    def make_recommand_schedule_data(self):
        # 0개에서 3개 랜덤 선택
        sample_size = random.randint(0, 3)  # 0부터 3까지의 개수 선택
        
        # recommend_target_sids는 이미 추천 대상 스케줄 ID로 채워져 있어야 함 (위에서 채워옴)
        result = random.sample(self.__recommend_target_sids, k=min(sample_size, len(self.__recommend_target_sids)))  # 데이터 크기를 초과하지 않도록 처리
                
        # 0개면 걍 끝
        if  len(result) == 0:
            return False
        
        schedule_datas = self._database.get_datas_with_ids(target_id="sid", ids= result)
        
        self.__schedules.clear()
        
        # 다 만들면 보관
        for schedule_data in schedule_datas:
            schedule = Schedule().make_with_dict(dict_data=schedule_data)
            self.__schedules.append(schedule)
        
        return True
    
    
    def set_recommand_schedule_layer(self):
        # 핵심 시간 섹션
        # 섹션마다 분류
        for single_schedule in self.__schedules:
            
            single_schedule:Schedule = single_schedule
            time_obj = single_schedule.datetime
            #time_obj = datetime.strptime(single_schedule.start_time, "%H:%M")
            
            options = [
                {
                    "start": datetime.combine(time_obj, datetime.min.time()),
                    "end": datetime.combine(time_obj, datetime.min.time()).replace(hour=6, minute=0),
                },
                {
                    "start": datetime.combine(time_obj, datetime.min.time()).replace(hour=6, minute=0),
                    "end": datetime.combine(time_obj, datetime.min.time()).replace(hour=12, minute=0),
                },
                {
                    "start": datetime.combine(time_obj, datetime.min.time()).replace(hour=12, minute=0),
                    "end": datetime.combine(time_obj, datetime.min.time()).replace(hour=18, minute=0),
                },
                {
                    "start": datetime.combine(time_obj, datetime.min.time()).replace(hour=18, minute=0),
                    "end": datetime.combine(time_obj, datetime.min.time()).replace(hour=23, minute=59),
                },
            ]
            
        
            if options[0]["start"] <= time_obj < options[0]["end"]:
                self.__recommand_layer_data[1]["schedules"].append(single_schedule)
            elif options[1]["start"] <= time_obj < options[1]["end"]:
                self.__recommand_layer_data[2]["schedules"].append(single_schedule)
            elif options[2]["start"] <= time_obj < options[2]["end"]:
                self.__recommand_layer_data[3]["schedules"].append(single_schedule)
            elif options[3]["start"] <= time_obj <= options[3]["end"]:  # 하루 끝 비교는 <= 사용
                self.__recommand_layer_data[4]["schedules"].append(single_schedule)
            else:
                continue

        
    # 전송용 폼으로 교체
    def change_layer_form(self):
        for my_single_time_section, recommand_single_time_section, layer_data in zip(self.__my_layer_data[1:5], self.__recommand_layer_data[1:5], self.__layer_data[1:5]):
            temp_list = []
            for my_single_schedule in my_single_time_section['schedules']:
                temp_list.append(self.__make_single_schedule_data_form(type="구독", schedule=my_single_schedule))
            for recommand_single_schedule in recommand_single_time_section['schedules']:
                temp_list.append(self.__make_single_schedule_data_form(type="추천", schedule=recommand_single_schedule))
            layer_data['schedules'].extend(temp_list)
        return
    
    
    def get_response_form_data(self, head_parser):
        body = {
            "schedule_layer" : self.__layer_data
            }

        response = self._get_response_data(head_parser=head_parser, body=body)
        return response
