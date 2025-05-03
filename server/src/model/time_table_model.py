import re

from model.base_model import BaseModel
from model import Local_Database
from others.data_domain import TimeTableUser as TUser
from others.data_domain import Schedule, ScheduleBundle, ScheduleEvent, Bias, User

from others.time_table_engine import ScheduleSearchEngine as SSE

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
        location_list = re.split(r"\W+", schedule.location)
        location_list = [l for l in location_list if l]

        schedule = Schedule(
            sname=schedule.sname,
            bid=bias.bid,
            bname=bias.bname,
            uid=user.uid,
            uname=user.uname,
            start_date=schedule.start_date,
            start_time=schedule.start_time,
            end_date=schedule.end_date,
            end_time=schedule.end_time,
            update_datetime=datetime.today().strftime("%Y/%m/%d-%H:%M:%S"),
            location=location_list,
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
        Sbias_data["category"] = bias.category[0]       # 카테고리는 맨처음의 데이터만
        Sbias_data["tags"] = self._linked_str(bias.tags)    # 연결해서 보냄
        Sbias_data["main_time"] = self._linked_str(bias.main_time) # 연결
        Sbias_data["is_ad"] = bias.is_ad

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
        time_schedule_data["location"] = self._linked_str(schedule.location)
        time_schedule_data["code"] = schedule.code
        time_schedule_data["color_code"] = schedule.color_code
        time_schedule_data["is_already_have"] = schedule.is_already_have
        time_schedule_data["is_owner"] = schedule.is_owner

        return time_schedule_data

    # 스케쥴 리스트 만드는 함수
    def get_tschedule_list(self, schedules):
        for schedule in schedules:
            self._schedules.append(self._time_schedule(schedule=schedule))

        return

    def get_response_form_data(self):
        return self._schedules

# 일정 스케줄 이벤트 데이터 폼 모델
class TimeEventModel(ScheduleTransformModel):
    def __init__(self) -> None:
        super().__init__()
        self._events = []

    # Event 보낼 거 만드는 함수
    def _tevent_data(self, event:ScheduleEvent):
        time_event_data = {}

        time_event_data["seid"] = event.seid
        time_event_data["sename"] = event.sename
        time_event_data["bid"] = event.bid
        time_event_data["bname"] = event.bname
        time_event_data["uid"] = event.uid
        time_event_data["uname"] = event.uname
        time_event_data["date"] = self._transfer_date_str(datetime.strptime(event.date,"%Y/%m/%d"))
        time_event_data["start"] = self._calculate_day_hour_time(datetime.strptime(event.start_time, "%H:%M"))
        time_event_data["end"] = self._calculate_day_hour_time(datetime.strptime(event.end_time, "%H:%M"))
        time_event_data["sids"] = event.sids
        time_event_data["location"] = self._linked_str(event.location)

        return time_event_data

    # 이벤트 딕셔너리 데이터 리스트를 만드는 곳
    def get_tevent_list(self, events):
        for event in events:
            self._events.append(self._tevent_data(event))

        return

    def get_response_form_data(self):
        return self._events

# 일정 스케줄 번들 전송 데이터 폼 모델
class TimeScheduleBundleModel(ScheduleTransformModel):
    def __init__(self) -> None:
        super().__init__()
        self._schedule_bundles = []

    def _time_schedule_bundle(self, schedule_bundle:ScheduleBundle):
        time_schedule_bundle_data = {}

        time_schedule_bundle_data["sbid"] = schedule_bundle.sbid
        time_schedule_bundle_data["sbname"] = schedule_bundle.sbname
        time_schedule_bundle_data["bid"] = schedule_bundle.bid
        time_schedule_bundle_data["bname"] = schedule_bundle.bname
        time_schedule_bundle_data["uid"] = schedule_bundle.uid
        time_schedule_bundle_data["uname"] = schedule_bundle.uname
        time_schedule_bundle_data["sids"] = schedule_bundle.sids
        time_schedule_bundle_data["date"] = self._transfer_date_str_list(schedule_bundle.date)
        time_schedule_bundle_data["location"] = self._linked_str(schedule_bundle.location)

        return time_schedule_bundle_data

    def get_tschedule_bundle_list(self, schedule_bundles):
        for schedule_bundle in schedule_bundles:
            self._schedule_bundles.append(self._time_schedule_bundle(schedule_bundle))

        return

    def get_response_form_data(self):
        return self._schedule_bundles

# ------------------------------------ 기본 타임 테이블 모델 ------------------------------------------
class TimeTableModel(BaseModel):
    def __init__(self, database:Local_Database) -> None:
        super().__init__(database)
        self._tuser:TUser = TUser()
        self._key = -1
        
        self.__num_bias = 0
        self.__target_month= f'00년 0월'
        self.__target_week= f'0주차'
        
    # 로그인이 필수인 유저이거나, 로그인을 한 유저를 처리할 때 필수적으로 사용되는 부분
    def _set_tuser_with_tuid(self, tuid="") -> bool:
        # 유저를 먼져 부르고 해야됨 반드시
        if tuid == "" :
            # 만약 로그인한 상태가 아니면 그냥 빈 TUSER를 가지게 될것임
            if self._user.uid == "":
                return False
            # 만약 로그인한 상태가 아니면 그냥 빈 TUSER를 가지게 될것임
            else:
                tuid = self._user.uid
            
        
        tuser_data = self._database.get_data_with_id(target="tuid", id=tuid)
        # 만약 tuser가 등록된 적이 없는 init 상태라면 여기서 등록도 해야됨
        if tuser_data:
            self._tuser.make_with_dict(dict_data=tuser_data)
        else:
            # tuid와 uid는 그냥 동일하게 하겠음 그래야 중복이 없음
            new_tuser = TUser(tuid=self._user.uid)
            self._database.add_new_data(target_id="tuid", new_data=new_tuser.get_dict_form_data())
            self._tuser = new_tuser
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
    
    def set_target_date(self, date=datetime.today().strftime("%Y-%m-%d")):
        today = datetime.strptime(date, "%Y-%m-%d")
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
        # if bundle:
        #     date_obj = datetime.strptime(date, "%y년 %m월 %d일")
        # else:
        #     date_obj = datetime.strptime(date, "%Y/%m/%d")

        date_obj = datetime.strptime(date, "%Y/%m/%d")

        # 시간 데이터가 존재한다면 시간도 같이 붙여야 함
        if time != "":
            time_obj = datetime.strptime(time, "%H:%M")
            date_obj = datetime.combine(date=date_obj.date(), time=time_obj.time())

        if when == "end":
            return date_obj < datetime.now()
        elif when == "start":
            return date_obj > datetime.now()

    # 필터링 옵션을 주면 리스트를 필터링 합니다.
    def filtering_list_with_option(self, id_list:list, filter_option:str, search_type:str="sid"):
        if filter_option == "all" or filter_option == "":
            return id_list

        filtered_id_list = []

        schedule_id_type = ""
        if search_type == "schedule" or search_type=="sid":
            schedule_id_type = "sid"
        elif search_type == "schedule_bundle" or search_type == "sbid":
            schedule_id_type = "sbid"
        # elif search_type == "event" or search_type == "seid":
        #     schedule_id_type = "seid"

        searched_data = self._database.get_datas_with_ids(target_id=schedule_id_type, ids=id_list)

        for data in searched_data:
            if schedule_id_type == "sid":
                schedule = Schedule()
                schedule.make_with_dict(dict_data=data)

                if filter_option == "ended":
                    # 종료된 일정 서치
                    if self.__check_schedule_time(date=schedule.end_date, time=schedule.end_time, when="end"):
                        filtered_id_list.append(schedule.sid)
                elif filter_option == "in_progress":
                    # 일정이 끝나지 않았을 떄,
                    if not self.__check_schedule_time(date=schedule.end_date, time=schedule.end_time, when="end"):
                        # 현재 시작한 일정
                        if not self.__check_schedule_time(date=schedule.start_date, time=schedule.start_time, when="start"):
                            filtered_id_list.append(schedule.sid)
                elif filter_option == "not_start":
                    # 시작 전인 일정 서치
                    if self.__check_schedule_time(date=schedule.start_date, time=schedule.start_time, when="start"):
                        filtered_id_list.append(schedule.sid)

                elif filter_option == "not_end":
                    if not self.__check_schedule_time(date=schedule.end_date, time=schedule.end_time, when="end"):
                        filtered_id_list.append(schedule.sid)

            elif schedule_id_type == "sbid":
                schedule_bundle = ScheduleBundle()
                schedule_bundle.make_with_dict(dict_data=data)

                if filter_option == "ended":
                    # 종료된 일정 번들
                    if self.__check_schedule_time(date=schedule_bundle.date[1], when="end"):
                        filtered_id_list.append(schedule_bundle.sbid)
                elif filter_option == "in_progress":
                    # 종료되지 않은 일정 번들
                    if not self.__check_schedule_time(date=schedule_bundle.date[1], when="end"):
                        # 시작한 일정 번들
                        if not self.__check_schedule_time(date=schedule_bundle.date[0], when="start"):
                            filtered_id_list.append(schedule_bundle.sbid)
                elif filter_option == "not_start":
                    # 시작하지 않은 일정 번들
                    if self.__check_schedule_time(date=schedule_bundle.date[0], when="start"):
                        filtered_id_list.append(schedule_bundle.sbid)

                elif filter_option == "not_end":
                    if not self.__check_schedule_time(date=schedule_bundle.date[1], when="end"):
                        filtered_id_list.append(schedule_bundle.sbid)


        return filtered_id_list

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
            "target_month" : self.__target_month,
            "target_week" : self.__target_week
            }

        response = self._get_response_data(head_parser=head_parser, body=body)
        return response

class ScheduleRecommendKeywordModel(TimeTableModel):
    def __init__(self, database:Local_Database) -> None:
        super().__init__(database)
        self._recommend_keywords = []

    # 바이어스의 카테고리 데이터를 추천 검색어로 사용하는 방법
    def get_category_recommend(self, num_keywords:int):
        # 로그인이 된 상태라면 유저가 팔로우한 바이어스 위주로
        if self._user.uid != "":
            bias_datas = self._database.get_datas_with_ids(target_id="bid", ids=self._user.bids)
        # 비로그인 상태라면 모든 바이어스 데이터를 가져와서 랜덤하게 뽑겠다.
        else:
            bias_datas = self._database.get_all_data(target="bid")

        category_set = set()

        # 카테고리들을 set에다가 집어넣고 랜덤하게 키워드를 뽑는다.
        for bias_data in bias_datas:
            category_list = bias_data['category']
            category_set.update(category_list)

        if len(category_set) > num_keywords:
            self._recommend_keywords = random.sample(category_set, num_keywords)
        else:
            self._recommend_keywords = list(category_set)

        return

    def get_response_form_data(self, head_parser):
        body = {
            "recommend_keywords" : self._recommend_keywords
        }

        response = self._get_response_data(head_parser=head_parser, body=body)
        return response


# ------------------------------------- 스케쥴 모델 ------------------------------------------------
# 단일 스케줄을 반환할 때 사용하는 모델
# 사용할 일이 있을지는 모르는데, 아마 수정 같은 상황에 사용될것
class SingleScheduleModel(TimeTableModel):
    def __init__(self, database:Local_Database) -> None:
        super().__init__(database)
        self.__schedule = Schedule()
        self.__schedule_event = ScheduleEvent()
        self.__schedule_bundle = ScheduleBundle()

    def get_response_form_data(self, head_parser):
        body = {
            "schedule" : self.__schedule.get_dict_form_data(),
            "schedule_event" : self.__schedule_event.get_dict_form_data(),
            "schedule_bundle" : self.__schedule_bundle.get_dict_form_data(),
            "key" : self._key
            }

        response = self._get_response_data(head_parser=head_parser, body=body)
        return response

# 복수 스케줄을 반환할 때 사용하는 모델 NEW ( Search Engine 사용 )
# 아마 대부분이 여러개를 반환해야하니 이거 쓰면 될듯
class MultiScheduleModel(TimeTableModel):
    def __init__(self, database:Local_Database) -> None:
        super().__init__(database)
        self.__schedules:list = []
        self.__schedule_events:list = []
        self.__schedule_bundles:list = []
        self.__biases:list = []

    # 바이어스 서치 함수
    def __search_bias_list(self, keyword:str):
        # 4가지의 경우가 존재한다
        # 아티스트 닉네임, 카테고리, 플랫폼, 태그

        bias_datas = self._database.get_all_data(target="bid")
        search_list = []

        for bias_data in bias_datas:
            bias = Bias()
            bias.make_with_dict(bias_data)
            if keyword in bias.bname:
                search_list.append(bias.bid)
            elif keyword in bias.category:
                search_list.append(bias.bid)
            elif keyword in bias.tags:
                search_list.append(bias.bid)
            elif keyword in bias.agency:
                search_list.append(bias.bid)

        return search_list

    def set_schedules_with_sids(self, data_payload):
        self._make_send_data_with_ids(id_list=data_payload.sids)
        return

    # id_list는 서치한 데이터들의 고유 아이디
    # 전송용 데이터를 만드는 함수
    def _make_send_data_with_ids(self,id_list:list, search_type:str="schedule"):
        schedule_id_type = ""
        if search_type == "schedule" or search_type=="sid":
            schedule_id_type = "sid"
        elif search_type == "schedule_bundle" or search_type == "sbid":
            schedule_id_type = "sbid"
        elif search_type == "event" or search_type == "seid":
            schedule_id_type = "seid"
        elif search_type == "bias" or search_type == "bid":
            schedule_id_type = "bid"

        schedule_type_datas = self._database.get_datas_with_ids(target_id=schedule_id_type, ids=id_list)

        for data in schedule_type_datas:
            if schedule_id_type == "sid":
                schedule = Schedule()
                schedule.make_with_dict(data)
                self.__schedules.append(schedule)

            elif schedule_id_type == "seid":
                schedule_event = ScheduleEvent()
                schedule_event.make_with_dict(data)
                self.__schedule_events.append(schedule_event)

            elif schedule_id_type == "sbid":
                schedule_bundle = ScheduleBundle()
                schedule_bundle.make_with_dict(data)
                self.__schedule_bundles.append(schedule_bundle)

            elif schedule_id_type == "bid":
                bias = Bias()
                bias.make_with_dict(data)
                self.__biases.append(bias)

        # 데이터들을 전부 변환
        self._make_send_data_with_datas()

        return

    # 이미 데이터를 받아온 경우에 씀
    def _make_send_data_with_datas(self):
        # 데이터 변환 모델
        schedule_model = TimeScheduleModel()
        schedule_event_model = TimeEventModel()
        schedule_bundle_model = TimeScheduleBundleModel()
        schedule_bias_model = TimeBiasModel()

        # 이미 등록 했는지 확인하는 함수
        for schedule in self.__schedules:
            if schedule.sid in self._tuser.sids:
                schedule.is_already_have = True

            if schedule.sid in self._tuser.my_sids:
                schedule.is_owner = True

        # 데이터 변환
        schedule_model.get_tschedule_list(schedules=self.__schedules)
        schedule_event_model.get_tevent_list(events=self.__schedule_events)
        schedule_bundle_model.get_tschedule_bundle_list(schedule_bundles=self.__schedule_bundles)
        schedule_bias_model.get_tbias_list(biases=self.__biases)

        # 반환받은 건 딕셔너리 리스트
        self.__schedules = schedule_model.get_response_form_data()
        self.__schedule_events = schedule_event_model.get_response_form_data()
        self.__schedule_bundles = schedule_bundle_model.get_response_form_data()
        self.__biases = schedule_bias_model.get_response_form_data()

        return

    # 안 씀
    # 내가 이벤트 스케줄 데이터 뽑기를 날짜로
    # date는 날짜임 , 형태는 2025/03/06 임
    # date안넣으면 기본적으로 오늘자로 감
    # def set_my_event_in_by_day(self, date:str=""):
    #     if not date:
    #         date = datetime.today().strftime("%Y/%m/%d")
    #
    #     # 내가 추가한 이벤트를 다 가지고 옴
    #     schedule_event_datas = self._database.get_datas_with_ids(target_id="seid", ids=self._tuser.seids)
    #
    #     # 필요하면 갯수 제한도 두삼
    #     for schedule_event_data in schedule_event_datas:
    #         schedule_event = ScheduleEvent()
    #         schedule_event.make_with_dict(dict_data=schedule_event_data)
    #         # 여기서 날짜랑 맞는지 필터링 함
    #         if date==schedule_event.date:
    #             self.__schedule_events.append(schedule_event)
    #
    #     # 스케줄 이벤트 데이터 폼 수정
    #     self._make_send_data_with_datas()
    #
    #     return

    # 안 씀
    # 전체 이벤트 데이터 뽑기를 날짜로
    # date는 날짜임 , 형태는 2025/03/06 임
    # date안넣으면 기본적으로 오늘자로 감
    # def set_event_in_by_day(self, date:str=""):
    #
    #     if date == "":
    #         date = datetime.today().strftime("%Y/%m/%d")
    #
    #     # 이건 데이터 베이스에서 해당 날짜 이벤트만 전부다 뽑는거임
    #     schedule_event_datas = self._database.get_datas_with_key(target="seid", key="date", key_datas=[date])
    #
    #     # 필요하면 갯수 제한도 두삼
    #     for schedule_event_data in schedule_event_datas:
    #         schedule_event = ScheduleEvent()
    #         schedule_event.make_with_dict(dict_data=schedule_event_data)
    #         self.__schedule_events.append(schedule_event)
    #
    #     # 스케줄 이벤트 데이터 폼 수정
    #     self._make_send_data_with_datas()
    #
    #     return



    # 이거 로직 수정필요
    # schedule_data를 들고올 때, key가 잘못됨.
    # 전체 스케줄 데이터 뽑기를 날짜로
    # date는 날짜임 , 형태는 2025/03/06 임
    # date안넣으면 기본적으로 오늘자로 감
    # def set_schedule_in_by_day(self, date_str:str=''):
    #
    #     if date_str== '':
    #         date_str=datetime.today().strftime("%Y/%m/%d")
    #
    #     # 이건 데이터 베이스에서 해당 날짜 이벤트만 전부다 뽑는거임
    #     schedule_datas = self._database.get_datas_with_key(target="sid", key="date", key_datas=[date_str])
    #
    #     # 필요하면 갯수 제한도 두삼
    #     for schedule_data in schedule_datas:
    #         schedule= Schedule()
    #         schedule.make_with_dict(dict_data=schedule_data)
    #         self.__schedules.append(schedule)
    #
    #     # 스케줄 데이터 폼 수정
    #     self._make_send_data_with_datas()
    #
    #     return
    #
    ## 이번주에 노출할 스케줄의 리스트가 최신화 되었는지 확인
    ## 최신화 안되었으면 이번주 노출할 스케줄 리스트를 비움
    #def is_this_week_sids_r_updated(self):
    #if self._tuser.this_week_sids:
    #schedule_data = self._database.get_data_with_id(target="sid", id=self._tuser.this_week_sids[0])
    #schedule = Schedule().make_with_dict(dict_data=schedule_data)

    ## 오늘 날짜랑 비교해서 이번주에 홈에 노출할 스케줄인지 체크해야됨
    #today = datetime.today()
    #today_week_number = today.isocalendar()[1]

    #target_date = datetime.strptime(schedule.date, "%Y/%m/%d")
    #target_week_number = target_date.isocalendar()[1]

    ## 년도가 같으면?
    #if today.year == target_week_number:
    ## 이번주랑 주차가 다르면 싹다 비워버리면됨
    #if today_week_number != target_week_number:
    #self._tuser.this_week_sids.clear()
    #self._database.modify_data_with_id(target_id="tuid", target_data=self._tuser)
    ## 년도 다르면 걍 비우면됨
    #else:
    #self._tuser.this_week_sids.clear()
    #self._database.modify_data_with_id(target_id="tuid", target_data=self._tuser)
    #return

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
    def search_schedule_with_keyword(self, schedule_search_engine:SSE, keyword:str, search_type:str, search_columns:str,
                                      when:str, num_schedules:int, last_index:int=-1):
        searched_list = []

        if search_columns == "":
            search_columns_list= []
        else:
            search_columns_list = [i.strip() for i in search_columns.split(",")]


        if search_type == "schedule" or search_type == "sid":
            searched_list = schedule_search_engine.try_search_schedule_w_keyword(target_keyword=keyword, search_columns=search_columns_list)
            searched_list = schedule_search_engine.try_filtering_schedule_in_progress(sids=searched_list, when=when)
        elif search_type == "schedule_bundle" or search_type == "sbid":
            searched_list = schedule_search_engine.try_search_bundle_w_keyword(target_keyword=keyword, search_columns=search_columns_list)
            searched_list = schedule_search_engine.try_filtering_bundle_in_progress(sbids=searched_list, when=when)

        searched_list, self._key = self.paging_id_list(id_list=searched_list, last_index=last_index, page_size=num_schedules)
        self._make_send_data_with_ids(id_list=searched_list, search_type=search_type)

        return

    # 키워드를 통한 바이어스 서치
    def search_bias_with_keyword(self, keyword:str, num_biases:int ,last_index:int=-1):
        searched_list = self.__search_bias_list(keyword=keyword)
        searched_list, self._key = self.paging_id_list(id_list=searched_list, last_index=last_index, page_size=num_biases)

        self._make_send_data_with_ids(id_list=searched_list, search_type="bias")

    # 내가 선택한 스케줄들을 반환
    def get_my_selected_schedules(self, schedule_search_engine:SSE, bid:str, num_schedules:int, last_index:int=-1):
        searched_list = schedule_search_engine.try_search_selected_schedules(sids=self._tuser.sids, bid=bid)
        searched_list, self._key = self.paging_id_list(id_list=searched_list, last_index=last_index, page_size=num_schedules)
        self._make_send_data_with_ids(id_list=searched_list, search_type="schedule")

        return

    # 이번 주 일정을 들고 옮
    def get_weekday_schedules(self, schedule_search_engine:SSE):
        searched_list = schedule_search_engine.try_get_weekday_schedule_list(sids=self._tuser.sids)
        self._make_send_data_with_ids(id_list=searched_list, search_type="schedule")

        return

    # 내가 설정한 모든 스케쥴 불러오기
    def search_my_all_schedule(self, schedule_search_engine:SSE):
        # 데이터 불러오고
        searched_list = schedule_search_engine.try_search_selected_schedules(sids=self._tuser.sids)
        self._make_send_data_with_ids(id_list=searched_list, search_type="schedule")

        return

    # 탐색용 스케줄 불러오기
    def get_explore_schedule_with_category(self, schedule_search_engine:SSE, time_section:int,
                                           style:str, gender:str, num_schedules:int, last_index:int=-1):
        searched_list = schedule_search_engine.try_get_explore_schedule_list(time_section=time_section, style=style, gender=gender)
        searched_list, self._key = self.paging_id_list(id_list=searched_list, last_index=last_index, page_size=num_schedules)
        self._make_send_data_with_ids(id_list=searched_list, search_type="schedule")

        return

    def get_specific_schedules(self, schedule_search_engine:SSE, specific_date:str,
                               num_schedules:int, last_index:int=-1):
        searched_list = schedule_search_engine.try_get_schedules_in_specific_date(sids=["all"],
                                                                                  specific_date=specific_date,
                                                                                  return_id=True)
        searched_list, self._key = self.paging_id_list(id_list=searched_list, last_index=last_index, page_size=num_schedules)
        self._make_send_data_with_ids(id_list=searched_list, search_type="schedule")

        return



    # 내가 작성한 스케쥴 가져오기 (수정을 위해서)
    def get_written_schedule(self, sid:str):
        schedule_data = self._database.get_data_with_id(target="sid",id=sid)
        schedule=Schedule()
        schedule.make_with_dict(schedule_data)

        if schedule.sid in self._tuser.my_sids:
            schedule.is_owner = True

        self.__schedules.append(schedule.get_dict_form_data())

        return

    # 내가 작성한 스케줄 번들을 가져오기 (수정을 위해서)
    def get_written_bundle(self, sbid:str):
        schedule_bundle_data = self._database.get_data_with_id(target="sbid", id=sbid)
        schedule_bundle = ScheduleBundle()
        schedule_bundle.make_with_dict(schedule_bundle_data)

        schedule_datas = self._database.get_datas_with_ids(target_id="sid", ids=schedule_bundle.sids)
        self.__schedules.extend(schedule_datas)

        self.__schedule_bundles.append(schedule_bundle.get_dict_form_data())

        return

    # 바이어스 추천 로직
    # 근데 아직 추천할게 없어
    def get_recommend_bias_list(self, num_biases:int):
        # 바이어스 데이터 로드
        bias_datas = self._database.get_all_data(target="bid")

        for bias_data in bias_datas:
            bias = Bias()
            bias.make_with_dict(bias_data)
            self.__biases.append(bias)

        # 랜덤하게 뽑기 (만약 데이터가 많다면
        if len(self.__biases) > num_biases :
            self.__biases = random.sample(self.__biases, num_biases)

        self._make_send_data_with_datas()

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

    # 내가 팔로우한 바이어스에 대한 전송 폼을 만드는 함수
    def get_print_forms_my_bias(self):
        bias_datas = self._database.get_datas_with_ids(target_id="bid", ids=self._user.bids)
        for bias_data in bias_datas:
            bias = Bias()
            bias.make_with_dict(bias_data)
            self.__biases.append(bias)

        self._make_send_data_with_datas()

        return

    # 전송 데이터 만들기
    def get_response_form_data(self, head_parser):
        body = {
            "schedules" : self.__schedules,
            "schedule_events" : self.__schedule_events,
            "schedule_bundles" : self.__schedule_bundles,
            "biases": self.__biases,
            "key" : self._key
        }

        # pprint(body)
        response = self._get_response_data(head_parser=head_parser, body=body)
        return response


# 스케줄 추가 모델 New (Search_Engine) 사용
class AddScheduleModel(TimeTableModel):
    def __init__(self, database:Local_Database):
        super().__init__(database=database)
        self.__result = False

    # sid 만들기
    def __make_new_sid(self):
        while True:
            sid = self._make_new_id()
            if self._database.get_data_with_id(target="sid", id=sid):
                continue
            else:
                break
        return sid

    # sbid 만들기
    def __make_new_sbid(self):
        while True:
            sbid = self._make_new_id()
            if self._database.get_data_with_id(target="sbid", id=sbid):
                continue
            else:
                break
        return sbid

    # 코드 만들기
    def __make_schedule_code(self):
        # 영어 대문자와 숫자로 이루어진 6자리 코드 생성
        characters = string.ascii_uppercase + string.digits
        code = ''.join(random.choices(characters, k=6))
        return code

    # 모든 방송 플랫폼 찾는 함수
    def __find_all_broadcast_location(self, schedule_list:list):
        location = set()

        for schedule in schedule_list:
            location.update(schedule.location)

        return list(location)

    # 스케줄 번들 시작 날짜와 끝 날짜 찾기
    def __find_start_n_end_date(self, schedule_list:list, ):
        # 기준 날짜는 맨 처음 스케줄
        start_date = datetime.strptime(schedule_list[0].start_date, "%Y/%m/%d")
        end_date = datetime.strptime(schedule_list[0].end_date, "%Y/%m/%d")

        # 스케줄마다 확인해서 일정 번들 중 가장 빠른 시작날짜와 가장 늦은 끝 날짜를 찾는다.
        for schedule in schedule_list:
            other_start = datetime.strptime(schedule.start_date,"%Y/%m/%d")
            other_end = datetime.strptime(schedule.end_date,"%Y/%m/%d")

            # 시작일 은 가장 오래된 순서
            if start_date > other_start:
                start_date = other_start
            # 종료일은 스케쥴의 가장 나중에 끝나는 날
            if end_date < other_end:
                end_date = other_end

        # 문자열화
        # start_date_str = start_date.strftime("%y년 %m월 %d일")
        # end_date_str = end_date.strftime("%y년 %m월 %d일")
        start_date_str = start_date.strftime("%Y/%m/%d")
        end_date_str = end_date.strftime("%Y/%m/%d")

        # 반환
        return [start_date_str, end_date_str]



    # sids리스트를 추가하는 곳
    # 대충 일정 보고 끼워넣는 로직도 있으면 좋겠는데
    def add_schedule(self, sids):
        self._tuser.sids = list(set(self._tuser.sids + sids))
        self._database.modify_data_with_id(target_id='tuid', target_data=self._tuser.get_dict_form_data())
        self.__result = True
        return

    # 이벤트를 추가하는 곳
    def add_event(self, seid):
        seids = set(self._tuser.seids)
        seids.add(seid)
        self._tuser.seids = list(seids)

        self._database.modify_data_with_id(target_id='tuid', target_data=self._tuser.get_dict_form_data())
        self.__result = True
        return

    # 내 스케줄 목록에서 지워버리는 곳 (이번주 목록이면 여기서 함)
    def reject_from_my_week_schedule(self, sid):
        # 저장해야하는지 체크하는 플래장
        flag= False

        if sid in self._tuser.sids:
            self._tuser.sids.remove(sid)
            flag = True

        if flag:
            self._database.modify_data_with_id(target_id="tuid", target_data=self._tuser.get_dict_form_data())
            self.__result = True
        return



    # 이번주 타임 테이블에 노출시킬 스케줄을 선택하는 곳
    # date는 날짜임 , 형태는 2025/03/06 임
    def select_schedule_in_showcase(self, schedule_search_engine:SSE, date, bid):
        # 데이터 검색
        searched_sids = schedule_search_engine.try_search_schedule_in_showcase(sids=self._tuser.sids,
                                                                               date=date, bid=bid)

        schedule_datas = self._database.get_datas_with_ids(target_id="sid", ids=searched_sids)

        # 저장해야하는지 체크하는 플래그
        flag = False

        for schedule_data in schedule_datas:
            schedule = Schedule()
            schedule.make_with_dict(dict_data=schedule_data)
            # 없으면 추가하고 있으면 삭제하면됨
            if schedule.sid not in self._tuser.this_week_sids:
                self._tuser.this_week_sids.append(schedule.sid)
            else:
                self._tuser.this_week_sids.remove(schedule.sid)
            flag = True

        # 저장하는 곳
        if flag:
            self._database.modify_data_with_id(target_id="tuid", target_data=self._tuser.get_dict_form_data())
            self.__result = True

        return




    # 단일 스케줄 만들기
    def make_new_single_schedule(self, data_payload, bid):
        schedule = Schedule(
            sname=data_payload.sname,
            bid = bid,
            start_date=data_payload.start_date,
            start_time=data_payload.start_time,
            end_date=data_payload.end_date,
            end_time=data_payload.end_time,
            state=data_payload.state
        )

        bias_data = self._database.get_data_with_id(target="bid", id=schedule.bid)
        if bias_data:
            bias = Bias().make_with_dict(bias_data)
        else:
            bias = Bias()

        # location을 나누는 방법 ( 정규식을 이용해서 구두점, 콤마 등을 걸러냅니다.
        # ", "와 같은 케이스도 말끔히. 근데 이후의 공백이 있을 수 있다는 점이 있어 주의를 요합니다.
        # 또한 플랫폼이 아닌 다른 문자가 들어가는 불상사도 있을 수 있습니다. (이건 어찌할 방도가..)
        str_list = re.split(r'\W+', data_payload.location)
        location_list = [s for s in str_list if s]
        # pprint(str_list)

        schedule.sid = self.__make_new_sid()
        schedule.bname = bias.bname
        schedule.uid = self._user.uid
        schedule.uname = self._user.uname
        schedule.code = self.__make_schedule_code()
        schedule.update_datetime = datetime.today().strftime("%Y/%m/%d-%H:%M:%S")
        schedule.color_code = self._make_color_code()
        schedule.location = location_list

        return schedule

    # 스케줄 번들 만들기
    def make_new_schedule_bundle(self, schedule_list:list, sbname:str, bid:str):
        schedule_bundle = ScheduleBundle(
            sbname=sbname,
            bid=bid,
            sids= [schedule.sid for schedule in schedule_list]
        )

        bias_data = self._database.get_data_with_id(target="bid", id=bid)
        bias = Bias().make_with_dict(bias_data)

        schedule_bundle.sbid = self.__make_new_sbid()
        schedule_bundle.bname = bias.bname
        schedule_bundle.uid = self._user.uid
        schedule_bundle.uname = self._user.uname
        schedule_bundle.date = self.__find_start_n_end_date(schedule_list=schedule_list)
        schedule_bundle.location = self.__find_all_broadcast_location(schedule_list=schedule_list)
        schedule_bundle.code = self.__make_schedule_code()
        schedule_bundle.update_datetime = datetime.today().strftime("%Y/%m/%d-%H:%M:%S")

        return schedule_bundle

    # 복수 스케줄 만들기
    def make_new_multiple_schedule(self, schedule_search_engine:SSE, schedules:list, sname:str, bid:str, data_type:str):
        schedule_list = []
        schedules_object = None

        for make_schedule in schedules:
            schedule = self.make_new_single_schedule(data_payload=make_schedule, bid=bid)
            schedule_list.append(schedule)

        # 스케쥴 등록
        self.save_new_schedules(schedule_search_engine=schedule_search_engine, schedule=schedule_list)

        if data_type == "bundle":
            schedules_object = self.make_new_schedule_bundle(schedule_list=schedule_list, sbname=sname, bid=bid)

        return schedules_object



    # 복수 개의 (단일 포함) 스테줄 저장
    def save_new_schedules(self, schedule_search_engine:SSE, schedule:list):
        save_data = self._make_dict_list_data(list_data=schedule)
        schedule_search_engine.try_add_new_managed_schedule_list(new_schedules=schedule)    # 서치 엔진에다가 저장합니다.
        self._database.add_new_datas(target_id="sid", new_datas=save_data)                  # 데이터베이스에 먼저 저장

        # 스케쥴 데이터를 추가 할 때, Tuser도 업데이트함
        for s in schedule:
            self._tuser.sids.append(s.sid)
            self._tuser.my_sids.append(s.sid)


        self._database.modify_data_with_id(target_id="tuid", target_data=self._tuser.get_dict_form_data())

        self.__result = True
        return

    # 스케줄 번들 저장
    def save_new_multiple_schedule_object_with_type(self, schedule_search_engine:SSE, schedule_object, data_type:str):
        if data_type == "bundle":
            schedule_search_engine.try_add_new_managed_bundle(new_bundle=schedule_object)

            self._database.add_new_data(target_id="sbid", new_data=schedule_object.get_dict_form_data())
            # self._tuser.sbids.append(schedule_object.sbid)
            self._tuser.my_sbids.append(schedule_object.sbid)
            self._database.modify_data_with_id(target_id="tuid", target_data=self._tuser.get_dict_form_data())
            self.__result = True
        # elif data_type == "event":
        #     self._database.add_new_data(target_id="seid", new_data=schedule_object.get_dict_form_data())
        #     self._tuser.seids.append(schedule_object.seid)
        #     self._tuser.my_seids.append(schedule_object.seid)
        #     self._database.modify_data_with_id(target_id="tuid", target_data=self._tuser.get_dict_form_data())
        #     self.__result = True

        return

    # 수정한 스케줄들 저장
    def save_modified_schedule(self, schedule_search_engine:SSE, schedule:list):
        # save_datas = self._make_dict_list_data(list_data=schedule)

        # for s in schedule:
        #     sids.append(s.sid)

        for s in schedule:
            save_data = s.get_dict_form_data()
            if self._database.get_data_with_id(target="sid", id=s.sid):
                self._database.modify_data_with_id(target_id='sid', target_data=save_data)
            else:
                schedule_search_engine.try_add_new_managed_schedule(new_schedule=s)
                self._database.add_new_data(target_id="sid", new_data=save_data)
                self._tuser.sids.append(s.sid)
                self._database.modify_data_with_id(target_id='tuid', target_data=self._tuser.get_dict_form_data())

        # 서치 엔진에도 저장합니다.
        schedule_search_engine.try_modify_schedule_list(modify_schedule_list=schedule)

        self.__result = True
        return


    # 수정한 스케줄 번들 저장
    def save_modified_multiple_schedule_object_with_type(self, schedule_search_engine:SSE, schedule_object, data_type:str):
        if data_type == "bundle":
            if self._database.get_data_with_id(target="sbid"):
                self._database.modify_data_with_id(target_id="sbid", target_data=schedule_object.get_dict_form_data())
                # 서치 엔진에 저장
                schedule_search_engine.try_modify_bundle(modify_bundle=schedule_object)

                self.__result = True
            else:
                self._database.add_new_data(target_id="sbid", new_data=schedule_object.get_dict_form_data())
                # 서치 엔진에 저장
                schedule_search_engine.try_add_new_managed_bundle(new_bundle=schedule_object)

                self._tuser.my_sbids.append(schedule_object.sbid)
                self._database.modify_data_with_id(target_id='tuid', target_data=self._tuser.get_dict_form_data())
                self.__result = True



        return



    # 단일 스케줄 편집
    def modify_single_schedule(self, data_payload, sid:str):
        # pprint("Single_schedule_modify")

        schedule_data = self._database.get_data_with_id(target="sid", id=sid)
        schedule = Schedule()
        schedule.make_with_dict(schedule_data)

        bias_data = self._database.get_data_with_id(target="bid", id=data_payload.bid)
        bias = Bias().make_with_dict(bias_data)

        str_list = re.split(r'\W+', data_payload.location)
        str_list = [s for s in str_list if s]

        schedule.sname = data_payload.sname
        schedule.bid = data_payload.bid
        schedule.location = str_list
        schedule.bname = bias.bname
        schedule.start_date = data_payload.start_date
        schedule.start_time = data_payload.start_time
        schedule.end_date = data_payload.end_date
        schedule.end_time = data_payload.end_time
        schedule.state = data_payload.state
        schedule.update_datetime= datetime.today().strftime("%Y/%m/%d-%H:%M:%S")

        return schedule

    # 스케줄 번들을 수정
    def modify_schedule_bundle(self, schedule_list:list, sbid:str, sbname:str, bid:str):
        schedule_bundle_data = self._database.get_data_with_id(target="sbid", id=sbid)
        schedule_bundle = ScheduleBundle().make_with_dict(schedule_bundle_data)

        bias_data = self._database.get_data_with_id(target="bid", id=bid)
        bias = Bias().make_with_dict(bias_data)

        schedule_bundle.sbname = sbname
        schedule_bundle.bid = bid
        schedule_bundle.bname = bias.bname
        schedule_bundle.date = self.__find_start_n_end_date(schedule_list=schedule_list)
        schedule_bundle.location = self.__find_all_broadcast_location(schedule_list=schedule_list)
        schedule_bundle.update_datetime = datetime.today().strftime("%Y/%m/%d-%H:%M:%S")

        return schedule_bundle

    # 복수의 스케줄 수정 후 저장 ( Schedule 데이터에 sid가 들어감 )
    def modify_multiple_schedule(self, schedule_search_engine:SSE, schedules:list[Schedule], sname:str , sbid:str, bid:str, data_type:str):
        # pprint("Multi_schedule_modify")

        schedule_list = []
        schedule_object = None

        # 스케줄 데이터들을 편집
        for schedule in schedules:
            schedule = self.modify_single_schedule(data_payload=schedule, sid=schedule.sid)
            schedule_list.append(schedule)

        # 데이터 저장
        self.save_modified_schedule(schedule_search_engine=schedule_search_engine, schedule=schedule_list)

        # 번들데이터 만들기
        if data_type == "bundle":
            if self._database.get_data_with_id(target='sbid', id=sbid):
                schedule_object = self.modify_schedule_bundle(schedule_list=schedule_list, sbid=sbid, sbname=sname, bid=bid)
            else:
                schedule_object = self.make_new_schedule_bundle(schedule_list=schedule_list, sbname=sname, bid=bid)

        return schedule_object



    # 스케줄 삭제
    def delete_schedule(self, schedule_search_engine:SSE, sid:str):
        # pprint(sid)
        schedule_bundle_datas = self._database.get_all_data(target = "sbid")

        sb_sids:list[dict] = []
        modified_schedule_bundles:list[ScheduleBundle] = []
        sbids = []

        for schedule_bundle_data in schedule_bundle_datas:
            schedule_bundle= ScheduleBundle().make_with_dict(schedule_bundle_data)
            if sid in schedule_bundle.sids:
                schedule_bundle.sids.remove(sid)

                # 서치 엔진에 수정할 데이터들을 담음
                modified_schedule_bundles.append(schedule_bundle)

                sb_sids.append({"sids" : schedule_bundle.sids})
                sbids.append(schedule_bundle.sbid)


        tuser_datas = self._database.get_all_data(target="tuid")

        tu_sids:list[TUser] = []
        tuids = []

        for tuser_data in tuser_datas:
            tuser = TUser().make_with_dict(tuser_data)
            # 자기 자신에 대해서는 따로 처리하겠습니다
            if tuser.tuid == self._tuser.tuid:
                continue
            if sid in tuser.sids:
                tuser.sids.remove(sid)
                tu_sids.append({"sids" : tuser.sids})
                tuids.append(tuser.tuid)

        self._tuser.my_sids.remove(sid)
        self._tuser.sids.remove(sid)

        self._database.modify_datas_with_ids(target_id="sbid", ids=sbids, target_datas=sb_sids)
        self._database.modify_datas_with_ids(target_id="tuid", ids=tuids, target_datas=tu_sids)
        self._database.modify_data_with_id(target_id="tuid", target_data=self._tuser.get_dict_form_data())

        # 서치 엔진에서 편집합니다.
        schedule_search_engine.try_remove_schedule(sid=sid)
        schedule_search_engine.try_modify_bundle_list(modify_bundle_list=modified_schedule_bundles)
        self._database.delete_data_with_id(target="sid", id=sid)

        self.__result = True
        return

    # 스케줄 번들 삭제
    # 테스트 아직 안했음 주의 ( Modify 수정이 완료된 후에 하기로)
    def delete_bundle(self, schedule_search_engine:SSE, sbid:str):
        # 스케줄 데이터 삭제
        schedule_bundle_data = self._database.get_data_with_id(target='sbid', id=sbid)
        schedule_bundle = ScheduleBundle().make_with_dict(schedule_bundle_data)
        sids = schedule_bundle.sids

        # tuser에서 sid를 삭제
        tuser_datas = self._database.get_all_data(target="tuid")
        tu_sids : list[TUser] = []
        tuids = []

        # 각 Tuser마다 반복합니다
        for tuser_data in tuser_datas:
            tuser = TUser().make_with_dict(tuser_data)

            # 본인에 대해서는 따로 처리합니다
            if tuser.tuid == self._tuser.tuid:
                continue


            # 스케줄 번들 안에 있는 모든 sids에 대해 삭제를 진행합니다.
            tuser.sids = list(filter(lambda sid: sid not in sids, tuser.sids))      # 잘 됨
            # if sbid in tuser.sbids:
            #     tuser.sbids.remove(sbid)

            tu_sids.append({"sids": tuser.sids})
            tuids.append(tuser.tuid)

        # 본인에 대해 삭제
        self._tuser.sids = list(filter(lambda sid: sid not in sids, self._tuser.sids))
        self._tuser.my_sids = list(filter(lambda sid: sid not in sids, self._tuser.my_sids))
        self._tuser.my_sbids.remove(sbid)

        # 서치 엔진에서 삭제
        schedule_search_engine.try_remove_schedule_list(sids=sids)
        schedule_search_engine.try_remove_bundle(sbid=sbid)

        self._database.modify_datas_with_ids(target_id="tuid", ids=tuids, target_datas=tu_sids)
        self._database.modify_data_with_id(target_id="tuid", target_data=self._tuser.get_dict_form_data())

        self._database.delete_datas_with_ids(target="sid", ids=sids)
        self._database.delete_data_with_id(target="sbid", id=sbid)

        self.__result = True

        return


    def get_response_form_data(self, head_parser):
        body = {
            "result" : self.__result
        }

        response = self._get_response_data(head_parser=head_parser, body=body)
        return response


# 시간 구간 정보 (0-6, 6-12, 12-18, 18-24)
time_ranges = [(0, 6), (6, 12), (12, 18), (18, 24)]
weekday_names = ['월', '화', '수', '목', '금', '토', '일']

class ScheduleBlock(Schedule):
    def __init__(self, start_datetime=None):
        super().__init__()
        self.timeblocks = []
        self.color_code = "#D2D2D2"
        self.__overflowed = False
        self.start_datetime = start_datetime
        self.end_datetime = None

    def is_overflowed(self):
        return self.__overflowed

    # 이게 전송용 데이터 포멧
    def get_dict_form_data(self):
        super_dict_data = super().get_dict_form_data()
        super_dict_data['timeblocks'] = self.timeblocks
        super_dict_data['color_code'] = self.color_code
        return super_dict_data

class WeekDayDataBlock:
    def __init__(self, day, make_day_data:datetime, num_schedule:int):
        self.origin_date = make_day_data     # 년 월 일
        self.year = make_day_data.year       # 년
        self.month = make_day_data.month     # 월
        self.date = make_day_data.day        # 일
        self.day = day          # 요일
        self.num_schedule = num_schedule
        self.is_today = False

     # 이게 전송용 데이터 포멧
    def get_dict_form_data(self):
        return {
            'date' : self.date,     #  일
            'day' : self.day,       # 요일
            'num_schedule' : self.num_schedule,
            'is_today' : self.is_today
        }

class ScheduleBlockTreater():
    def __init__(self):
        self.__over_flowed_schedules = []

    # WeekDay Block 데이터 만들기
    def make_default_week_day_data(self, target_date:datetime, days):

        weekDayDateBlock_list = []

        # 오늘 날짜
        # 여기 마져 만들어야됨
        today = datetime.today()
        today = datetime.combine(today, time.min)

        # 5일 / 7일 분량
        for i in range(days):
            current_date = target_date + timedelta(days=i)

            # WeekDayDataBlock 생성
            day_block = WeekDayDataBlock(
                day=weekday_names[current_date.weekday()],
                make_day_data=current_date,
                num_schedule=0
            )                           
            # day_block.origin_date는 datetime에서 년, 월, 일을 포함함
            if day_block.origin_date== today:
                day_block.is_today = True

            weekDayDateBlock_list.append(day_block)

        return weekDayDateBlock_list

    def make_week_day_data(self, schedule_blocks):
        today = datetime.today()
        weekDayDateBlocks = []

        for schedule_block in schedule_blocks:
            schedule_block:ScheduleBlock = schedule_block

            # 목표 블럭을 찾고
            targetWeekDayDateBlock = None
            for weekDayDateBlock in weekDayDateBlocks:
                # 있으면 목표블럭
                if weekDayDateBlock.date == schedule_block.start_datetime.day:
                    targetWeekDayDateBlock = weekDayDateBlock

            # 없으면 지금찾던걸로 하나 만들어야됨
            if not targetWeekDayDateBlock:
                targetWeekDayDateBlock = WeekDayDataBlock(day=weekday_names[schedule_block.start_datetime.weekday()],
                                                       make_day_data=schedule_block.start_datetime,
                                                       num_schedule=0
                                                       )
                weekDayDateBlocks.append(targetWeekDayDateBlock)
            
            # 핵심 - 스케줄 수를 하나 늘려주면됨
            targetWeekDayDateBlock.num_schedule += 1

         # WeekDayDateBlocks를 date 기준으로 정렬
        sorted_block_list = sorted(weekDayDateBlocks, key=lambda x: x.date)

        # today와 같은 날짜부터 리스트를 자름
        today_weekday = today.weekday()
        trimmed_list = [block for block in sorted_block_list if block.date >= today_weekday]

        return trimmed_list

    def clear_over_flowed_schedule(self) -> list[ScheduleBlock]:
        schedule_blocks = []

        for schedule in self.__over_flowed_schedules:
            schedule_block = self.make_schedule_block(schedule=schedule)
            schedule_blocks.append(schedule_block)

        return schedule_blocks

    # 스케줄 블럭 등록
    def compare_week_day_block(self, schedule_blocks:list, weekday_blocks):
        # today = datetime.today()
        is_flag = False # 스케줄이 있는지 없는지 확인하는 플래그
        
        num_schedule_block = 0

        # 목표 블럭 찾기
        for weekDayBlock in weekday_blocks:
            is_flag = False
            # weekDayBlock:WeekDayDataBlock = weekDayBlock
            
            for schedule_block in schedule_blocks:
                schedule_block:ScheduleBlock = schedule_block
                
                # 있으면 목표 블럭
                if weekDayBlock.date == schedule_block.start_datetime.day:
                    weekDayBlock.num_schedule += 1
                    num_schedule_block += 1
                    is_flag = True
            
            # 만약 스케줄이 없다면
            # 가짜 빈 스케줄을 넣으면됨
            if not is_flag:
                start_datetime = f'{weekDayBlock.year}/{weekDayBlock.month}/{weekDayBlock.date}'
                schedule_block = ScheduleBlock(start_datetime=datetime.strptime(start_datetime, "%Y/%m/%d"))
                schedule_blocks.append(schedule_block)
                num_schedule_block += 1

        # 날짜 데이터를 바탕으로 정렬합니다.
        sorted_block_list = sorted(weekday_blocks, key=lambda x : x.origin_date)

        return sorted_block_list, num_schedule_block

    #  만들기
    def make_schedule_block(self, schedule:Schedule, sids:list=[]):
        schedule_block = ScheduleBlock()
        schedule_block.make_with_dict(schedule.get_dict_form_data())

        # 시작 및 종료 시간 합치기
        schedule_block.start_datetime = datetime.strptime(f"{schedule_block.start_date} {schedule_block.start_time}", "%Y/%m/%d %H:%M")
        schedule_block.end_datetime = datetime.strptime(f"{schedule_block.end_date} {schedule_block.end_time}", "%Y/%m/%d %H:%M")

        # 위크 데이트 블록 리스트에 날짜가 포함되었는지 확인하고 넣을 것
        schedule_block = self.__make_timeblocks(schedule_block=schedule_block)
        
        # 만약 추가하기 파트에서 선택한 임시 스케줄이라면 색깔을 바꿔서 보낼것임
        if schedule_block.sid in sids:
            # 아래의 컬러 코드가 우리 이미지 컬러코드(파스텔톤)
            schedule_block.color_code = "#D0E4FF"

        return schedule_block

    def __make_timeblocks(self, schedule_block:ScheduleBlock) -> ScheduleBlock:
        current_datetime = schedule_block.start_datetime
        first_block = True  # 첫 번째 블록인지 확인하는 플래그
        end_flag = False

        num_loop = 0

        while current_datetime < schedule_block.end_datetime:

            if num_loop >10000:
                break

            # 현재 시간의 구간 판별
            hour = current_datetime.hour

            if end_flag:
                break

            for i, (start_hour, end_hour) in enumerate(time_ranges):
                if start_hour <= hour < end_hour:

                    # 첫 번째 구간이 아닌 경우 제외
                    if (not first_block and i == 0):
                        end_flag = True
                        break

                    current_range_start = current_datetime.replace(hour=start_hour, minute=0, second=0, microsecond=0)

                    # 구간 끝나는 시간이 24이면 다음 날 00:00으로 설정
                    if end_hour == 24:
                        current_range_end = current_datetime.replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1)
                    else:
                        current_range_end = current_datetime.replace(hour=end_hour, minute=0, second=0, microsecond=0)

                    # 구간 종료 시간이 종료 시간보다 크면 종료 시간으로 제한
                    actual_end = min(schedule_block.end_datetime, current_range_end)

                    # 앞 부분 패딩 및 총 길이 계산
                    if current_datetime == current_range_start:
                        padding_minutes = 0
                    else:
                        padding_minutes = int((current_datetime - current_range_start).total_seconds() / 60)

                    total_minutes = int((actual_end - current_datetime).total_seconds() / 60)

                    schedule_block.timeblocks.append(
                        {
                        "time": i,
                        "start": padding_minutes,
                        "length": total_minutes
                    })

                    # 현재 시간을 다음 구간 시작으로 이동
                    current_datetime = actual_end
                    first_block = False# 첫 번째 구간이 끝났으므로 플래그 변경

                    break
            num_loop += 1

        # 하루를 넘어가면 넘어갔다고 표시하고 보관하기
        if schedule_block.start_datetime.day != schedule_block.end_datetime.day:
            overflowed_schedule = Schedule().make_with_dict(schedule_block.get_dict_form_data())
            overflowed_schedule.start_date = schedule_block.end_datetime.strftime("%Y/%m/%d")
            overflowed_schedule.start_time = "00:00"
            overflowed_schedule.end_date = schedule_block.end_datetime.strftime("%Y/%m/%d")
            overflowed_schedule.end_time = schedule_block.end_datetime.strftime("%H:%M")
            self.__over_flowed_schedules.append(overflowed_schedule)

        return schedule_block


    ## 쨍하고 밝은 색깔 코드 생성기
    #def __make_color_code(self):
        ## 더 쨍하고 밝은 색상을 위해 범위 설정
        #r = random.randint(170, 255)  # 밝은 색상 범위
        #g = random.randint(170, 255)
        #b = random.randint(170, 255)

        ## 흰색과의 혼합을 줄여 더 선명한 색상 유지
        #r = (r * 3 + 255) // 4
        #g = (g * 3 + 255) // 4
        #b = (b * 3 + 255) // 4

        #return f'#{r:02x}{g:02x}{b:02x}'
        
    
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
    def __init__(self, database:Local_Database) -> None:
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
        
    # 단일 스케줄의 데이터 폼을 받아내는 객체
    def __make_single_schedule_data_form(self, type, schedule:Schedule):
        schedule_form = {}
        
        # 24시간 형식의 문자열을 datetime 객체로 변환
        time_obj = datetime.strptime(schedule.start_time, "%H:%M")

        # 12시간 형식의 문자열로 변환
        time_12 = time_obj.strftime("%p %I:%M").lstrip("0").replace("AM", "AM").replace("PM", "PM")
        
        schedule_form["time"] = time_12
        schedule_form["type"] = type
        schedule_form["schedule_id"] = schedule.sid
        schedule_form["schedule_title"] = schedule.sname
        schedule_form["schedule_bias"] = schedule.bname
        schedule_form["schedule_bid"] = schedule.bid
        return schedule_form
    
    
    # 태그 데이터 넣어줘야됨
    def set_tag_data(self):
        target_tag:str = callable()
        
        self.__layer_data[0]["tag"]=target_tag
        pass
    
    
    # 날짜에 맞는 스케줄 데이터 불러오기
    def make_my_schedule_data(self, target_date, schedule_search_engine):
        self._tuser.sids = self._tuser.sids
        
        # 여기서 schedule_search_engine으로 검색해야됨
        # sids 전체애 대한 검색은 무조건 ["all"]로 해주시길 바람
        # specific_date의 자료형은 str 그대로 써도됩니다. managed_table에서 Datetime 객체로 변환시키도록 만들었음.
        # return_id = True -> sid list 반환, False -> managed_Schedule list 반환

        result_sids = schedule_search_engine.try_get_schedules_in_specific_date(sids=["all"], specific_date=target_date, return_id=False)
        result_sids = callable()
        
        schedule_datas = self._database.get_datas_with_ids(target_id="sid", ids= result_sids)
        
        # 다 만들면 보관
        for schedule_data in schedule_datas:
            schedule = Schedule().make_with_dict(dict_data=schedule_data)
            self.__schedules.append(schedule)
        
        return
    
    # 레이어 만들기
    def set_my_schedule_layer(self):
        # 핵심 시간 섹션
        options = [
            {"start": time(0, 0), "end": time(6, 0)},
            {"start": time(6, 0), "end": time(12, 0)},
            {"start": time(12, 0), "end": time(18, 0)},
            {"start": time(18, 0), "end": time(23, 59)},  # 하루의 끝을 23:59로 설정
        ]
        
        # 섹션마다 분류
        for single_schedule in self.__schedules:
            
            single_schedule:Schedule = single_schedule
            time_obj = datetime.strptime(single_schedule.start_time, "%H:%M")
            
        
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
    def make_recommand_schedule_data(self, target_date, schedule_search_engine):
        
        self._tuser.sids = self._tuser.sids
        
        # 여기서 schedule_search_engine으로 검색해야됨
        result_sids = callable()
        
        schedule_datas = self._database.get_datas_with_ids(target_id="sid", ids= result_sids)
        
        # 다 만들면 보관
        for schedule_data in schedule_datas:
            schedule = Schedule().make_with_dict(dict_data=schedule_data)
            self.__schedules.append(schedule)
        
        return       
            
            
     # 레이어 만들기
    def set_recommand_schedule_layer(self):
        # 핵심 시간 섹션
        options = [
            {"start": time(0, 0), "end": time(6, 0)},
            {"start": time(6, 0), "end": time(12, 0)},
            {"start": time(12, 0), "end": time(18, 0)},
            {"start": time(18, 0), "end": time(23, 59)},  # 하루의 끝을 23:59로 설정
        ]
        
        # 섹션마다 분류
        for single_schedule in self.__schedules:
            
            single_schedule:Schedule = single_schedule
            time_obj = datetime.strptime(single_schedule.start_time, "%H:%M")
            
        
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
        
        
    # 전송용 폼으로 교체
    def change_layer_form(self):
        for my_single_time_section, recommand_single_time_section, layer_data in map(self.__my_layer_data[1:4], self.__recommand_layer_data[1:4], self.__layer_data):
            temp_list = []
            for my_single_schedule in my_single_time_section['schedules']:
                temp_list.append(self.__make_single_schedule_data_form(type="구독", schedule=my_single_schedule))
            for recommand_single_schedule in recommand_single_time_section['schedules']:
                temp_list.append(self.__make_single_schedule_data_form(type="추천", schedule=recommand_single_schedule))
            layer_data['schedules'] = temp_list
                
        return
    
    
    def get_response_form_data(self, head_parser):
        body = {
            "schedule_layer" : self.__layer_data
            }

        response = self._get_response_data(head_parser=head_parser, body=body)
        return response

# 복수 스케줄을 반환할 때 사용하는 모델
# 아마 대부분이 여러개를 반환해야하니 이거 쓰면 될듯
class ScheduleChartModel(TimeTableModel):
    def __init__(self, database:Local_Database) -> None:
        super().__init__(database)
        self.__schedule_blocks = []
        self.__week_day_datas = []
        
    # 내가 추가한 스케줄 데이터 뽑기를 날짜로
    # date는 날짜임 , 형태는 2025/03/06 임
    # date안넣으면 기본적으로 오늘자로 감
    def set_my_schedule_in_by_day(self, target_date="", days=7, sids =[]):
        if not target_date:
            target_date = datetime.today().strftime("%Y-%m-%d")

        target_sids = []
        target_sids.extend(self._tuser.sids)
        target_sids.extend(sids)
        
        # 내가 추가한 스케줄을 다 가지고 옴
        schedule_datas = self._database.get_datas_with_ids(target_id="sid", ids=target_sids)
        
        #today = target_date + timedelta(days=12)
        # today = target_date - timedelta(days=3)

        temp_schedules:list[Schedule] = []

        # 필요하면 갯수 제한도 두삼
        for schedule_data in schedule_datas:
            schedule = Schedule()
            schedule.make_with_dict(dict_data=schedule_data)
    
                    
            temp_schedules.append(schedule)
            
        # 임시로 뽑은 애들 정렬치는 부분
        sids_schedules = []
        
        for schedule in temp_schedules:
            if schedule.sid in sids:
                sids_schedules.append(schedule)
                
        # 반드시 임시로 뽑은 애들중에서 min_date를 골라야했음
        min_date = None
        
        for sid_schedule in sids_schedules:
            # 날짜가 오늘부터 지정된 일수만큼 뒤까지 포함되는지 확인
            schedule_date = datetime.strptime(sid_schedule.start_date, "%Y/%m/%d")

            # 이거 미리보기 일 때 라는 조건문임
            if sids:
                # min_date를 가장 빠른 날짜로 설정
                if min_date is None or schedule_date < min_date:
                    min_date = schedule_date
        
        # 가장 빠른 날짜가 있으면 이걸로 보여줘야됨
        if min_date:
            target_date = min_date
        else:
            # 아니면 평범하게 오늘자로 하면됨 ==> 수정됨
            #target_date = datetime.strptime(target_date, ("%Y/%m/%d"))
            
            # 오늘이 포함된 주차에서 월요일을 골라야됨
            # 여기 서버 안끄면 초기화 안되는 쌉 버그가 생김
            target_date = self._get_monday_date(target_date=target_date)
        
        schedules= []
        
        for schedule in temp_schedules:
            if target_date + timedelta(days=days) > datetime.strptime(schedule.start_date, "%Y/%m/%d") >= target_date:
                schedules.append(schedule)
                    
                    
        schedule_block_treater = ScheduleBlockTreater()
        
        # 위크데이 블럭만드는 곳
        weekday_blocks = schedule_block_treater.make_default_week_day_data(target_date=target_date, days=days)

        # 스케줄 블럭 만드는 곳
        for schedule in schedules:
            schedule_block = schedule_block_treater.make_schedule_block(schedule=schedule, sids=sids)
            self.__schedule_blocks.append(schedule_block)
        
        # 오버 플로우된거 처리까지 해서 스케줄 블럭 완성하기
        over_flowed_schedule:list = schedule_block_treater.clear_over_flowed_schedule()
        self.__schedule_blocks.extend(over_flowed_schedule)
        
        # self.__week_day_datas = schedule_block_treater.make_week_day_data(schedule_blocks=self.__schedule_blocks)
        # 위크데이 블럭이랑 스케줄 불럭의 수를 받아와야됨 (가짜 블럭의 수도 포함됨)
        self.__week_day_datas, num_schedule_blocks = schedule_block_treater.compare_week_day_block(schedule_blocks=self.__schedule_blocks,
                                                                             weekday_blocks=weekday_blocks)
        
        # 정렬 순서는 맨 마지막에서 바로 앞으로
        self.__schedule_blocks = sorted(self.__schedule_blocks, key=lambda x : x.start_datetime)
        
        # 이제 안쓰는 블럭(날짜의 데이터는 버려야됨)
        self.__schedule_blocks = self.__schedule_blocks[:num_schedule_blocks]

        # 시작이 전날이고, 끝나는게 오늘이면 데이터가 안나오기 때문에
        # 결국 타임 블럭에서 하루 전날꺼를 구하고 그날 데이터를 버려야됨
        # 이코드가 추가되어야됨
        
        return
    
    def _get_monday_date(self, target_date: str) -> datetime:
        # 입력 날짜를 datetime 객체로 변환
        target_date = datetime.strptime(target_date, "%Y-%m-%d")
    
        # 오늘의 요일 계산 (0: 월요일, 6: 일요일)
        day_of_week = target_date.weekday()
    
        # 오늘 날짜에서 요일 값을 빼서 이번 주 월요일 계산
        monday_date = target_date - timedelta(days=day_of_week)
    
        # 월요일 날짜를 datetime 객체로 반환
        return monday_date
    
    def get_response_form_data(self, head_parser):
        body = {
            "schedule_blocks" : self._make_dict_list_data(list_data=self.__schedule_blocks),
            "week_day_datas" : self._make_dict_list_data(list_data=self.__week_day_datas),
            }

        response = self._get_response_data(head_parser=head_parser, body=body)
        return response


# 복수 스케줄을 반환할 때 사용하는 모델
# 아마 대부분이 여러개를 반환해야하니 이거 쓰면 될듯
# class MultiScheduleModel(TimeTableModel):
#     def __init__(self, database:Local_Database) -> None:
#         super().__init__(database)
#         self.__schedules:list = []
#         self.__schedule_events:list = []
#         self.__schedule_bundles:list = []
#         self.__biases:list = []
#
#     def set_schedules_with_sids(self, data_payload):
#         self._make_send_data_with_ids(id_list=data_payload.sids)
#         return
#
#     # id_list는 서치한 데이터들의 고유 아이디
#     # 전송용 데이터를 만드는 함수
#     def _make_send_data_with_ids(self,id_list:list, search_type:str="schedule"):
#         schedule_id_type = ""
#         if search_type == "schedule" or search_type=="sid":
#             schedule_id_type = "sid"
#         elif search_type == "schedule_bundle" or search_type == "sbid":
#             schedule_id_type = "sbid"
#         elif search_type == "event" or search_type == "seid":
#             schedule_id_type = "seid"
#         elif search_type == "bias" or search_type == "bid":
#             schedule_id_type = "bid"
#
#         schedule_type_datas = self._database.get_datas_with_ids(target_id=schedule_id_type, ids=id_list)
#
#         for data in schedule_type_datas:
#             if schedule_id_type == "sid":
#                 schedule = Schedule()
#                 schedule.make_with_dict(data)
#                 self.__schedules.append(schedule)
#
#             elif schedule_id_type == "seid":
#                 schedule_event = ScheduleEvent()
#                 schedule_event.make_with_dict(data)
#                 self.__schedule_events.append(schedule_event)
#
#             elif schedule_id_type == "sbid":
#                 schedule_bundle = ScheduleBundle()
#                 schedule_bundle.make_with_dict(data)
#                 self.__schedule_bundles.append(schedule_bundle)
#
#             elif schedule_id_type == "bid":
#                 bias = Bias()
#                 bias.make_with_dict(data)
#                 self.__biases.append(bias)
#
#         # 데이터들을 전부 변환
#         self._make_send_data_with_datas()
#
#         return
#
#     # 이미 데이터를 받아온 경우에 씀
#     def _make_send_data_with_datas(self):
#         # 데이터 변환 모델
#         schedule_model = TimeScheduleModel()
#         schedule_event_model = TimeEventModel()
#         schedule_bundle_model = TimeScheduleBundleModel()
#         schedule_bias_model = TimeBiasModel()
#
#         # 이미 등록 했는지 확인하는 함수
#         for schedule in self.__schedules:
#             if schedule.sid in self._tuser.sids:
#                 schedule.is_already_have = True
#
#             if schedule.sid in self._tuser.my_sids:
#                 schedule.is_owner = True
#
#         # 데이터 변환
#         schedule_model.get_tschedule_list(schedules=self.__schedules)
#         schedule_event_model.get_tevent_list(events=self.__schedule_events)
#         schedule_bundle_model.get_tschedule_bundle_list(schedule_bundles=self.__schedule_bundles)
#         schedule_bias_model.get_tbias_list(biases=self.__biases)
#
#         # 반환받은 건 딕셔너리 리스트
#         self.__schedules = schedule_model.get_response_form_data()
#         self.__schedule_events = schedule_event_model.get_response_form_data()
#         self.__schedule_bundles = schedule_bundle_model.get_response_form_data()
#         self.__biases = schedule_bias_model.get_response_form_data()
#
#         return
#
#     # 바이어스 서치 함수
#     def __search_bias_list(self, keyword:str):
#         # 4가지의 경우가 존재한다
#         # 아티스트 닉네임, 카테고리, 플랫폼, 태그
#
#         bias_datas = self._database.get_all_data(target="bid")
#         search_list = []
#
#         for bias_data in bias_datas:
#             bias = Bias()
#             bias.make_with_dict(bias_data)
#             if keyword in bias.bname:
#                 search_list.append(bias.bid)
#             elif keyword in bias.category:
#                 search_list.append(bias.bid)
#             elif keyword in bias.tags:
#                 search_list.append(bias.bid)
#             elif keyword in bias.agency:
#                 search_list.append(bias.bid)
#
#         return search_list
#
#     # 스케줄 데이터 서치 함수
#     def __find_schedule_data(self, keyword:str):
#         schedule_datas = self._database.get_all_data(target="sid")
#         # 왜 불편하게 id_list로 담나요?
#         # 페이징할 때 편합니다.
#         schedule_ids = []
#
#         # 찾기
#         for schedule_data in schedule_datas:
#             if keyword in schedule_data["code"]:
#                 schedule_ids.append(schedule_data['sid'])
#                 continue
#             # 스케쥴 이름으로 검색
#             elif keyword in schedule_data["sname"]:
#                 schedule_ids.append(schedule_data['sid'])
#                 continue
#             # 유저네임으로 검색하는 경우
#             elif keyword in schedule_data['uname']:
#                 schedule_ids.append(schedule_data['sid'])
#                 continue
#             # Bias 네임으로 검색하는 경우
#             elif keyword in schedule_data['bname']:
#                 schedule_ids.append(schedule_data['sid'])
#                 continue
#             # location에 대해서도 찾는다
#             for loca in schedule_data['location']:
#                 if keyword in loca:
#                     schedule_ids.append(schedule_data['sid'])
#                     continue
#
#
#         return schedule_ids
#
#     # 스케줄 번들 데이터 서치 함수
#     def __find_schedule_bundle_data(self, keyword:str):
#         schedule_bundle_datas = self._database.get_all_data(target="sbid")
#         schedule_bundle_ids = []
#
#         for schedule_bundle_data in schedule_bundle_datas:
#             # schedule_bundle = ScheduleBundle()
#             # schedule_bundle.make_with_dict(dict_data=schedule_bundle_data)
#
#             # 한번 담으면 더 이상 서치된 번들에 대해서는 중복 서치할 필요가 없으므로 Continue.
#
#             # 일정코드로 검색
#             if keyword in schedule_bundle_data['code']:
#                 schedule_bundle_ids.append(schedule_bundle_data['sbid'])
#                 continue
#             # 스케쥴 이름으로 검색
#             elif keyword in schedule_bundle_data['sbname']:
#                 schedule_bundle_ids.append(schedule_bundle_data['sbid'])
#                 continue
#             # 유저네임으로 검색하는 경우
#             elif keyword in schedule_bundle_data['uname']:
#                 schedule_bundle_ids.append(schedule_bundle_data['sbid'])
#                 continue
#             # Bias 네임으로 검색하는 경우
#             elif keyword in schedule_bundle_data['bname']:
#                 schedule_bundle_ids.append(schedule_bundle_data['sbid'])
#                 continue
#             for loca in schedule_bundle_data['location']:
#                 if keyword in loca:
#                     schedule_bundle_ids.append(schedule_bundle_data['sbid'])
#                     continue
#
#         return schedule_bundle_ids
#
#     # 스케줄 이벤트 데이터 서치 함수
#     def __find_schedule_event_data(self, keyword:str):
#         schedule_event_datas = self._database.get_all_data(target="seid")
#         schedule_event_ids = []
#
#         for schedule_event_data in schedule_event_datas:
#             # schedule_event = ScheduleEvent()
#             # schedule_event.make_with_dict(dict_data=schedule_event_data)
#
#             # 한번 담으면 더 이상 서치된 번들에 대해서는 중복 서치할 필요가 없으므로 Continue.
#             # 일정코드로 검색
#             if keyword in schedule_event_data['code']:
#                 schedule_event_ids.append(schedule_event_data['seid'])
#                 continue
#             # 스케쥴 이름으로 검색
#             elif keyword in schedule_event_data['sename']:
#                 schedule_event_ids.append(schedule_event_data['seid'])
#                 continue
#             # 유저네임으로 검색하는 경우
#             elif keyword in schedule_event_data['uname']:
#                 schedule_event_ids.append(schedule_event_data['seid'])
#                 continue
#             # Bias 네임으로 검색하는 경우
#             elif keyword in schedule_event_data['bname']:
#                 schedule_event_ids.append(schedule_event_data['seid'])
#                 continue
#
#         return schedule_event_ids
#
#     # 내가 선택한 스케쥴 데이터 서치 함수. bid에 따라 필터링도 함
#     def __find_my_selected_schedules(self, bid:str):
#         my_schedule_datas = self._database.get_datas_with_ids(target_id="sid", ids=self._tuser.sids)
#         schedule_id_list = []
#
#         for schedule_data in my_schedule_datas:
#             schedule = Schedule()
#             schedule.make_with_dict(dict_data=schedule_data)
#
#             if schedule.bid == bid:
#                 # 비어있는 BID = "" 이면 BID가 실제로 ""로 저장된 Schedule들을 반환한다.
#                 schedule_id_list.append(schedule.sid)
#
#         return schedule_id_list
#
#     # 안 씀
#     # 내가 이벤트 스케줄 데이터 뽑기를 날짜로
#     # date는 날짜임 , 형태는 2025/03/06 임
#     # date안넣으면 기본적으로 오늘자로 감
#     def set_my_event_in_by_day(self, date:str=""):
#
#         if not date:
#             date = datetime.today().strftime("%Y/%m/%d")
#
#         # 내가 추가한 이벤트를 다 가지고 옴
#         schedule_event_datas = self._database.get_datas_with_ids(target_id="seid", ids=self._tuser.seids)
#
#         # 필요하면 갯수 제한도 두삼
#         for schedule_event_data in schedule_event_datas:
#             schedule_event = ScheduleEvent()
#             schedule_event.make_with_dict(dict_data=schedule_event_data)
#             # 여기서 날짜랑 맞는지 필터링 함
#             if date==schedule_event.date:
#                 self.__schedule_events.append(schedule_event)
#
#         # 스케줄 이벤트 데이터 폼 수정
#         self._make_send_data_with_datas()
#
#         return
#
#     # 안 씀
#     # 전체 이벤트 데이터 뽑기를 날짜로
#     # date는 날짜임 , 형태는 2025/03/06 임
#     # date안넣으면 기본적으로 오늘자로 감
#     def set_event_in_by_day(self, date:str=""):
#
#         if date == "":
#             date = datetime.today().strftime("%Y/%m/%d")
#
#         # 이건 데이터 베이스에서 해당 날짜 이벤트만 전부다 뽑는거임
#         schedule_event_datas = self._database.get_datas_with_key(target="seid", key="date", key_datas=[date])
#
#         # 필요하면 갯수 제한도 두삼
#         for schedule_event_data in schedule_event_datas:
#             schedule_event = ScheduleEvent()
#             schedule_event.make_with_dict(dict_data=schedule_event_data)
#             self.__schedule_events.append(schedule_event)
#
#         # 스케줄 이벤트 데이터 폼 수정
#         self._make_send_data_with_datas()
#
#         return
#
#
#
#     # 이거 로직 수정필요
#     # schedule_data를 들고올 때, key가 잘못됨.
#     # 전체 스케줄 데이터 뽑기를 날짜로
#     # date는 날짜임 , 형태는 2025/03/06 임
#     # date안넣으면 기본적으로 오늘자로 감
#     def set_schedule_in_by_day(self, date=datetime.today().strftime("%Y/%m/%d")):
#         # 이건 데이터 베이스에서 해당 날짜 이벤트만 전부다 뽑는거임
#         schedule_datas = self._database.get_datas_with_key(target="sid", key="date", key_datas=[date])
#
#         # 필요하면 갯수 제한도 두삼
#         for schedule_data in schedule_datas:
#             schedule= Schedule()
#             schedule.make_with_dict(dict_data=schedule_data)
#             self.__schedules.append(schedule)
#
#         # 스케줄 데이터 폼 수정
#         self._make_send_data_with_datas()
#
#         return
#
#     ## 이번주에 노출할 스케줄의 리스트가 최신화 되었는지 확인
#     ## 최신화 안되었으면 이번주 노출할 스케줄 리스트를 비움
#     #def is_this_week_sids_r_updated(self):
#         #if self._tuser.this_week_sids:
#             #schedule_data = self._database.get_data_with_id(target="sid", id=self._tuser.this_week_sids[0])
#             #schedule = Schedule().make_with_dict(dict_data=schedule_data)
#
#             ## 오늘 날짜랑 비교해서 이번주에 홈에 노출할 스케줄인지 체크해야됨
#             #today = datetime.today()
#             #today_week_number = today.isocalendar()[1]
#
#             #target_date = datetime.strptime(schedule.date, "%Y/%m/%d")
#             #target_week_number = target_date.isocalendar()[1]
#
#             ## 년도가 같으면?
#             #if today.year == target_week_number:
#                 ## 이번주랑 주차가 다르면 싹다 비워버리면됨
#                 #if today_week_number != target_week_number:
#                     #self._tuser.this_week_sids.clear()
#                     #self._database.modify_data_with_id(target_id="tuid", target_data=self._tuser)
#             ## 년도 다르면 걍 비우면됨
#             #else:
#                 #self._tuser.this_week_sids.clear()
#                 #self._database.modify_data_with_id(target_id="tuid", target_data=self._tuser)
#         #return
#
#     # 내가 타임테이블에 노출시키려고 했던 schedule을 보여줌
#     # tuser의 this_week_sids를 기반으로 함
#     def set_schedule_by_this_week(self):
#         schedule_datas = self._database.get_datas_with_ids(target_id="sid", ids=self._tuser.this_week_sids)
#
#         # 오늘 날잡아야됨
#         today = datetime.today()
#         today_week_number = today.isocalendar()[1]
#
#         # 저장해야하는지 체크하는 플래그
#         flag = False
#
#         for schedule_data in schedule_datas:
#             schedule = Schedule()
#             schedule.make_with_dict(dict_data=schedule_data)
#
#             # 이거 이번주 맞는지 체크해야되서 일단 날짜를 객체로 만들어줌
#             target_date = datetime.strptime(schedule.date, "%Y/%m/%d")
#             target_week_number = target_date.isocalendar()[1]
#
#             # 년도가 같으면?
#             if today.year == target_week_number:
#                 # 이번주랑 주차가 다르면 싹다 비워버리면됨
#                 if today_week_number != target_week_number:
#                     self._tuser.this_week_sids.remove(schedule.sid)
#                     flag = True
#                     continue
#
#             # 년도 다르면 걍 비우면됨
#             else:
#                 self._tuser.this_week_sids.remove(schedule.sid)
#                 flag = True
#                 continue
#
#             # 리스트에 넣으면됨
#             self.__schedules.append(schedule)
#
#         # 업데이트 했으면 데베에 저장할것
#         if flag:
#             self._database.modify_data_with_id(target_id="tuid", target_data=self._tuser.get_dict_form_data())
#
#         # 스케줄 데이터 폼 수정
#         self._make_send_data_with_datas()
#         return
#
#     # 주차에 따른 내가 추가한 스케줄을 보여줌
#     def set_schedule_by_week(self, year="", week=0):
#         # 데이터 불러오고
#         schedule_datas = self._database.get_datas_with_ids(target_id="sid", ids=self._tuser.sids)
#
#         # 필터링 해야되는데 날짜 기준이 필요함
#         # year 가 없으면 그냥 이번주임
#
#         # 아래가 이번주 체크하는거고
#         if year =="":
#             today = datetime.today()
#             target_week_number = today.isocalendar()[1]
#             year = today.year
#         # 아래는 목표 주를 기준으로 체크
#         else:
#             target_week_number = week
#
#         for schedule_data in schedule_datas:
#             schedule = Schedule()
#             schedule.make_with_dict(dict_data=schedule_data)
#             # 날짜를 뽑아서 객체화 시키고
#             date = datetime.strptime(schedule.date, "%Y/%m/%d")
#             # 년도와 몇주차 비교해서 맞으면 넣어주면됨
#             if year == date.year and target_week_number == date.isocalendar()[1]:
#                 self.__schedules.append(schedule)
#
#         # 스케줄 데이터 폼 수정
#         self._make_send_data_with_datas()
#
#         return
#
#     # 키워드를 통해 검색합니다.
#     def search_schedule_with_keyword(self, keyword:str, search_type:str, filter_option:str,
#                                      num_schedules:int, last_index:int=-1):
#         searched_list = []
#
#         if search_type == "schedule" or search_type == "sid":
#             searched_list = self.__find_schedule_data(keyword=keyword)
#         elif search_type == "schedule_bundle" or search_type == "sbid":
#             searched_list = self.__find_schedule_bundle_data(keyword=keyword)
#         # elif search_type == "event" or search_type == "seid":
#         #     searched_list = self.__find_schedule_event_data(keyword=keyword)
#
#         filtered_searched_list = self.filtering_list_with_option(id_list=searched_list, search_type=search_type, filter_option=filter_option)
#         filtered_searched_list, self._key = self.paging_id_list(id_list=filtered_searched_list, last_index=last_index, page_size=num_schedules)
#
#         self._make_send_data_with_ids(id_list=filtered_searched_list, search_type=search_type)
#
#         return
#
#     # 키워드를 통한 바이어스 서치
#     def search_bias_with_keyword(self, keyword:str, num_biases:int ,last_index:int=-1):
#         search_list = self.__search_bias_list(keyword=keyword)
#         search_list, self._key = self.paging_id_list(id_list=search_list, last_index=last_index, page_size=num_biases)
#
#         self._make_send_data_with_ids(id_list=search_list, search_type="bias")
#
#     # 바이어스를 통한 내 스케쥴 관리
#     def search_my_schedule_with_bid(self, bid):
#         # 데이터 불러오고
#         schedule_datas = self._database.get_datas_with_ids(target_id="sid", ids=self._tuser.sids)
#
#         # 보낼 스케줄 정하는 곳
#         # 만약 등록된 순서가 뒤집히면 여기서 reverse 추가해야됨
#         for schedule_data in schedule_datas:
#             schedule = Schedule()
#             schedule.make_with_dict(dict_data=schedule_data)
#
#             if schedule.bid == bid:
#                 self.__schedules.append(schedule)
#
#         # # 데이터 불러오고
#         # schedule_events_datas = self._database.get_datas_with_ids(target_id="seid", ids=self._tuser.seids)
#         #
#         # # 보낼 이벤트 정하는 곳
#         # for schedule_event_data in schedule_events_datas:
#         #     schedule_event = ScheduleEvent()
#         #     schedule_event.make_with_dict(dict_data=schedule_event_data)
#         #
#         #     if schedule_event.bid == bid:
#         #         self.__schedule_events.append(schedule_event)
#
#         self._make_send_data_with_datas()
#
#         return
#
#     # 내가 선택한 스케줄들을 반환
#     def get_my_selected_schedules(self, bid, num_schedules:int, last_index:int=-1):
#         searched_list = self.__find_my_selected_schedules(bid=bid)
#         searched_list, self._key = self.paging_id_list(id_list=searched_list, last_index=last_index, page_size=num_schedules)
#
#         self._make_send_data_with_ids(id_list=searched_list, search_type="schedule")
#         return
#
#     # 이번 주 일정을 들고 옮
#     def get_weekday_schedules(self):
#         schedule_datas = self._database.get_datas_with_ids(target_id="sid", ids=self._tuser.sids)
#
#         monday, sunday = self._find_week_monday_N_sunday()
#
#         for schedule_data in schedule_datas:
#             schedule = Schedule()
#             schedule.make_with_dict(schedule_data)
#
#             start_date = datetime.strptime(schedule.start_date, "%Y/%m/%d")
#             end_date = datetime.strptime(schedule.end_date, "%Y/%m/%d")
#
#             if monday <= start_date <= sunday:
#                 self.__schedules.append(schedule)
#             elif monday <= end_date <= sunday:
#                 self.__schedules.append(schedule)
#
#         self._make_send_data_with_datas()
#
#         return
#
#
#     # 내가 설정한 모든 스케쥴 불러오기
#     def search_my_all_schedule(self):
#         # 데이터 불러오고
#         schedule_datas = self._database.get_datas_with_ids(target_id="sid", ids=self._tuser.sids)
#
#         # 보낼 스케줄 정하는 곳
#         # 만약 등록된 순서가 뒤집히면 여기서 reverse 추가해야됨
#         for schedule_data in schedule_datas:
#             schedule = Schedule()
#             schedule.make_with_dict(dict_data=schedule_data)
#             self.__schedules.append(schedule)
#
#         # 이벤트 데이터는 지금 사용 X
#         # # 데이터 불러오고
#         # schedule_events_datas = self._database.get_datas_with_ids(target_id="seid", ids=self._tuser.seids)
#         #
#         # # 보낼 이벤트 정하는 곳
#         # for schedule_event_data in schedule_events_datas:
#         #     schedule_event = ScheduleEvent()
#         #     schedule_event.make_with_dict(dict_data=schedule_event_data)
#         #     self.__schedule_events.append(schedule_event)
#
#         self._make_send_data_with_datas()
#         return
#
#     def get_written_schedule(self, sid:str):
#         schedule_data = self._database.get_data_with_id(target="sid",id=sid)
#         schedule=Schedule()
#         schedule.make_with_dict(schedule_data)
#
#         if schedule.sid in self._tuser.my_sids:
#             schedule.is_owner = True
#
#         self.__schedules.append(schedule.get_dict_form_data())
#
#         return
#
#     def get_written_bundle(self, sbid:str):
#         schedule_bundle_data = self._database.get_data_with_id(target="sbid", id=sbid)
#         schedule_bundle = ScheduleBundle()
#         schedule_bundle.make_with_dict(schedule_bundle_data)
#
#         schedule_datas = self._database.get_datas_with_ids(target_id="sid", ids=schedule_bundle.sids)
#         self.__schedules.extend(schedule_datas)
#
#         self.__schedule_bundles.append(schedule_bundle.get_dict_form_data())
#
#         return
#
#     # 바이어스 추천 로직
#     # 근데 아직 추천할게 없어
#     def get_recommend_bias_list(self, num_biases:int):
#         # 바이어스 데이터 로드
#         bias_datas = self._database.get_all_data(target="bid")
#
#         for bias_data in bias_datas:
#             bias = Bias()
#             bias.make_with_dict(bias_data)
#             self.__biases.append(bias)
#
#         # 랜덤하게 뽑기 (만약 데이터가 많다면
#         if len(self.__biases) > num_biases :
#             self.__biases = random.sample(self.__biases, num_biases)
#
#         self._make_send_data_with_datas()
#
#     # 전송 데이터 만들기
#     def get_response_form_data(self, head_parser):
#         body = {
#             "schedules" : self.__schedules,
#             "schedule_events" : self.__schedule_events,
#             "schedule_bundles" : self.__schedule_bundles,
#             "biases": self.__biases,
#             "key" : self._key
#             }
#
#         # pprint(body)
#         response = self._get_response_data(head_parser=head_parser, body=body)
#         return response



# 스케쥴 추가 모델
# class AddScheduleModel(TimeTableModel):
#     def __init__(self, database:Local_Database) -> None:
#         super().__init__(database)
#         self.__result = False
#
#     # sids리스트를 추가하는 곳
#     # 대충 일정 보고 끼워넣는 로직도 있으면 좋겠는데
#     def add_schedule(self, sids):
#         self._tuser.sids = list(set(self._tuser.sids + sids))
#         self._database.modify_data_with_id(target_id='tuid', target_data=self._tuser.get_dict_form_data())
#         self.__result = True
#         return
#
#     # 이벤트를 추가하는 곳
#     def add_event(self, seid):
#         seids = set(self._tuser.seids)
#         seids.add(seid)
#         self._tuser.seids = list(seids)
#
#         self._database.modify_data_with_id(target_id='tuid', target_data=self._tuser.get_dict_form_data())
#         self.__result = True
#         return
#
#     # 이번주 타임 테이블에 노출시킬 스케줄을 선택하는 곳
#     # date는 날짜임 , 형태는 2025/03/06 임
#     def select_schedule_in_showcase(self, date, bid):
#         # 스케줄 데이터를 가지고 오고
#         schedule_datas = self._database.get_datas_with_id(target_id="sid", ids=self._tuser.sids)
#
#         # 저장해야하는지 체크하는 플래그
#         flag = False
#
#         # 날짜를 비교해서 이사람이 본거 찾아야됨
#         # date는 날짜임 , 형태는 2025/03/06 임
#         for schedule_data in schedule_datas:
#             schedule = Schedule()
#             schedule.make_with_dict(dict_data=schedule_data)
#             if schedule.date == date and schedule.bid == bid:
#                 # 없으면 추가하고 있으면 삭제하면됨
#                 if schedule.sid not in self._tuser.this_week_sids:
#                     self._tuser.this_week_sids.append(schedule.sid)
#                 else:
#                     self._tuser.this_week_sids.remove(schedule.sid)
#                 flag = True
#                 return
#
#         # 저장하는 곳
#         if flag:
#             self._database.modify_data_with_id(target_id="tuid", target_data=self._tuser.get_dict_form_data())
#             self.__result = True
#
#         return
#
#     # 내 스케줄 목록에서 지워버리는 곳 (이번주 목록이면 여기서 함)
#     def reject_from_my_week_schedule(self, sid):
#         # 저장해야하는지 체크하는 플래장
#         flag= False
#
#         if sid in self._tuser.sids:
#             self._tuser.sids.remove(sid)
#             flag = True
#
#         if flag:
#             self._database.modify_data_with_id(target_id="tuid", target_data=self._tuser.get_dict_form_data())
#             self.__result = True
#         return
#
#     # sid 만들기
#     def __make_new_sid(self):
#         while True:
#             sid = self._make_new_id()
#             if self._database.get_data_with_id(target="sid", id=sid):
#                 continue
#             else:
#                 break
#         return sid
#
#     # sbid 만들기
#     def __make_new_sbid(self):
#         while True:
#             sbid = self._make_new_id()
#             if self._database.get_data_with_id(target="sbid", id=sbid):
#                 continue
#             else:
#                 break
#         return sbid
#
#     # 코드 만들기
#     def __make_schedule_code(self):
#         # 영어 대문자와 숫자로 이루어진 6자리 코드 생성
#         characters = string.ascii_uppercase + string.digits
#         code = ''.join(random.choices(characters, k=6))
#         return code
#
#     # 모든 방송 플랫폼 찾는 함수
#     def __find_all_broadcast_location(self, schedule_list:list):
#         location = set()
#
#         for schedule in schedule_list:
#             location.update(schedule.location)
#
#         return list(location)
#
#     # 스케줄 번들 시작 날짜와 끝 날짜 찾기
#     def __find_start_n_end_date(self, schedule_list:list, ):
#         # 기준 날짜는 맨 처음 스케줄
#         start_date = datetime.strptime(schedule_list[0].start_date, "%Y/%m/%d")
#         end_date = datetime.strptime(schedule_list[0].end_date, "%Y/%m/%d")
#
#         # 스케줄마다 확인해서 일정 번들 중 가장 빠른 시작날짜와 가장 늦은 끝 날짜를 찾는다.
#         for schedule in schedule_list:
#             other_start = datetime.strptime(schedule.start_date,"%Y/%m/%d")
#             other_end = datetime.strptime(schedule.end_date,"%Y/%m/%d")
#
#             # 시작일 은 가장 오래된 순서
#             if start_date > other_start:
#                 start_date = other_start
#             # 종료일은 스케쥴의 가장 나중에 끝나는 날
#             if end_date < other_end:
#                 end_date = other_end
#
#         # 문자열화
#         # start_date_str = start_date.strftime("%y년 %m월 %d일")
#         # end_date_str = end_date.strftime("%y년 %m월 %d일")
#         start_date_str = start_date.strftime("%Y/%m/%d")
#         end_date_str = end_date.strftime("%Y/%m/%d")
#
#         # 반환
#         return [start_date_str, end_date_str]
#
#     # 단일 스케줄 만들기
#     def make_new_single_schedule(self, data_payload, bid):
#         schedule = Schedule(
#             sname=data_payload.sname,
#             bid = bid,
#             start_date=data_payload.start_date,
#             start_time=data_payload.start_time,
#             end_date=data_payload.end_date,
#             end_time=data_payload.end_time,
#             state=data_payload.state
#         )
#
#         bias_data = self._database.get_data_with_id(target="bid", id=schedule.bid)
#         if bias_data:
#             bias = Bias().make_with_dict(bias_data)
#         else:
#             bias = Bias()
#
#         # location을 나누는 방법 ( 정규식을 이용해서 구두점, 콤마 등을 걸러냅니다.
#         # ", "와 같은 케이스도 말끔히. 근데 이후의 공백이 있을 수 있다는 점이 있어 주의를 요합니다.
#         # 또한 플랫폼이 아닌 다른 문자가 들어가는 불상사도 있을 수 있습니다. (이건 어찌할 방도가..)
#         str_list = re.split(r'\W+', data_payload.location)
#         str_list = [s for s in str_list if s]
#         pprint(str_list)
#
#         schedule.sid = self.__make_new_sid()
#         schedule.bname = bias.bname
#         schedule.uid = self._user.uid
#         schedule.uname = self._user.uname
#         schedule.code = self.__make_schedule_code()
#         schedule.update_datetime = datetime.today().strftime("%Y/%m/%d-%H:%M:%S")
#         schedule.color_code = self._make_color_code()
#         schedule.location = str_list
#
#         return schedule
#
#     # 스케줄 번들 만들기
#     def make_new_schedule_bundle(self, schedule_list:list, sbname:str, bid:str):
#         schedule_bundle = ScheduleBundle(
#             sbname=sbname,
#             bid=bid,
#             sids= [schedule.sid for schedule in schedule_list]
#         )
#
#         bias_data = self._database.get_data_with_id(target="bid", id=bid)
#         bias = Bias().make_with_dict(bias_data)
#
#         schedule_bundle.sbid = self.__make_new_sbid()
#         schedule_bundle.bname = bias.bname
#         schedule_bundle.uid = self._user.uid
#         schedule_bundle.uname = self._user.uname
#         schedule_bundle.date = self.__find_start_n_end_date(schedule_list=schedule_list)
#         schedule_bundle.location = self.__find_all_broadcast_location(schedule_list=schedule_list)
#         schedule_bundle.code = self.__make_schedule_code()
#         schedule_bundle.update_datetime = datetime.today().strftime("%Y/%m/%d-%H:%M:%S")
#
#         return schedule_bundle
#
#     # 단일 스테줄 저장
#     def save_new_schedules(self, schedule:list):
#         save_data = self._make_dict_list_data(list_data=schedule)
#         self._database.add_new_datas(target_id="sid", new_datas=save_data)
#
#         # 스케쥴 데이터를 추가 할 때, Tuser도 업데이트함
#         for s in schedule:
#             self._tuser.sids.append(s.sid)
#             self._tuser.my_sids.append(s.sid)
#         self._database.modify_data_with_id(target_id="tuid", target_data=self._tuser.get_dict_form_data())
#
#         self.__result = True
#         return
#
#     # 복수 스케줄 만들기
#     def make_new_multiple_schedule(self, schedules:list[Schedule], sname:str, bid:str, data_type:str):
#         schedule_list = []
#         schedules_object = None
#
#         for schedule in schedules:
#             schedule = self.make_new_single_schedule(data_payload=schedule, bid=bid)
#             schedule_list.append(schedule)
#
#         # 스케쥴 등록
#         self.save_new_schedules(schedule=schedule_list)
#
#         if data_type == "bundle":
#             schedules_object = self.make_new_schedule_bundle(schedule_list=schedule_list, sbname=sname, bid=bid)
#
#         return schedules_object
#
#     # 스케줄 번들 저장
#     def save_new_multiple_schedule_object_with_type(self, schedule_object, data_type:str):
#         if data_type == "bundle":
#             self._database.add_new_data(target_id="sbid", new_data=schedule_object.get_dict_form_data())
#             self._tuser.sbids.append(schedule_object.sbid)
#             self._tuser.my_sbids.append(schedule_object.sbid)
#             self._database.modify_data_with_id(target_id="tuid", target_data=self._tuser.get_dict_form_data())
#             self.__result = True
#         # elif data_type == "event":
#         #     self._database.add_new_data(target_id="seid", new_data=schedule_object.get_dict_form_data())
#         #     self._tuser.seids.append(schedule_object.seid)
#         #     self._tuser.my_seids.append(schedule_object.seid)
#         #     self._database.modify_data_with_id(target_id="tuid", target_data=self._tuser.get_dict_form_data())
#         #     self.__result = True
#
#         return
#
#     # # 스케줄 편집
#     # def modify_single_schedule(self, data_payload, sid:str):
#     #     schedule_data =
#
#     # 단일 스케줄 편집 저장
#     def modify_single_schedule(self, data_payload, sid:str):
#         pprint("Single_schedule_modify")
#
#         schedule_data = self._database.get_data_with_id(target="sid", id=sid)
#         schedule = Schedule()
#         schedule.make_with_dict(schedule_data)
#
#         bias_data = self._database.get_data_with_id(target="bid", id=data_payload.bid)
#         bias = Bias().make_with_dict(bias_data)
#
#         schedule.sname = data_payload.sname
#         schedule.bid = data_payload.bid
#         schedule.bname = bias.bname
#         schedule.start_date = data_payload.start_date
#         schedule.start_time = data_payload.start_time
#         schedule.end_date = data_payload.end_date
#         schedule.end_time = data_payload.end_time
#         schedule.state = data_payload.state
#         schedule.update_datetime= datetime.today().strftime("%Y/%m/%d-%H:%M:%S")
#
#         return schedule
#
#     # 복수의 스케줄 저장 ( Schedule 데이터에 sid가 들어감 )
#     def modify_multiple_schedule(self, schedules:list[Schedule], sname:str , sbid:str, bid:str, data_type:str):
#         pprint("Multi_schedule_modify")
#
#         schedule_list = []
#         schedule_object = None
#
#         # 스케줄 데이터들을 편집
#         for schedule in schedules:
#             schedule = self.modify_single_schedule(data_payload=schedule, sid=schedule.sid)
#             schedule_list.append(schedule)
#
#         # 데이터 저장
#         self.save_modified_schedule(schedule=schedule_list)
#
#         # 번들데이터 만들기
#         if data_type == "bundle":
#             if self._database.get_data_with_id(target='sid', id=sbid):
#                 schedule_object = self.modify_schedule_bundle(schedule_list=schedule_list, sbid=sbid, sbname=sname, bid=bid)
#             else:
#                 schedule_object = self.make_new_schedule_bundle(schedule_list=schedule_list, sbname=sname, bid=bid)
#
#         return schedule_object
#
#     # 스케줄 번들을 수정
#     def modify_schedule_bundle(self, schedule_list:list, sbid:str, sbname:str, bid:str):
#         schedule_bundle_data = self._database.get_data_with_id(target="sbid", id=sbid)
#         schedule_bundle = ScheduleBundle().make_with_dict(schedule_bundle_data)
#
#         bias_data = self._database.get_data_with_id(target="bid", id=bid)
#         bias = Bias().make_with_dict(bias_data)
#
#         schedule_bundle.sbname = sbname
#         schedule_bundle.bid = bid
#         schedule_bundle.bname = bias.bname
#         schedule_bundle.date = self.__find_start_n_end_date(schedule_list=schedule_list)
#         schedule_bundle.location = self.__find_all_broadcast_location(schedule_list=schedule_list)
#         schedule_bundle.update_datetime = datetime.today().strftime("%Y/%m/%d-%H:%M:%S")
#
#         return schedule_bundle
#
#     # 수정한 스케줄 저장
#     def save_modified_schedule(self, schedule:list):
#         save_datas = self._make_dict_list_data(list_data=schedule)
#         sids = []
#
#         # for s in schedule:
#         #     sids.append(s.sid)
#
#         for s_data in save_datas:
#             if self._database.get_data_with_id(target="sid", id=s_data['sid']):
#                 self._database.modify_data_with_id(target_id='sid', target_data=s_data)
#             # 새로운 스케줄을 저장하는 경우
#             else:
#                 self._database.add_new_data(target_id='sid', new_data=s_data)
#                 # 유저에게도 추가
#                 self._tuser.my_sids.append(s_data['sid'])
#                 self._tuser.sids.append(s_data['sid'])
#                 self._database.modify_data_with_id(target_id='tuid', target_data=self._tuser.get_dict_form_data())
#
#
#         # 일단 이건 스케줄 수정하는 거
#         # self._database.modify_datas_with_ids(target_id="sid", ids=sids, target_datas=save_datas)
#
#         # 이건 비효율적이긴 함
#         # for s_data in save_datas:
#         #     self._database.modify_data_with_id(target_id="sid", target_data=s_data)
#
#         self.__result = True
#         return
#
#     # 수정한 스케줄 번들 저장
#     def save_modified_multiple_schedule_object_with_type(self, schedule_object, data_type:str):
#         if data_type == "bundle":
#             if self._database.get_data_with_id(target="sbid"):
#                 self._database.modify_data_with_id(target_id="sbid", target_data=schedule_object.get_dict_form_data())
#                 self.__result = True
#             else:
#                 self._database.add_new_data(target_id="sbid", new_data=schedule_object.get_dict_form_data())
#                 self._tuser.my_sbids.append(schedule_object.sbid)
#                 self._database.modify_data_with_id(target_id='tuid', target_data=self._tuser.get_dict_form_data())
#                 self.__result = True
#         return
#
#     # 스케줄 삭제
#     def delete_schedule(self, sid:str):
#         pprint(sid)
#         schedule_bundle_datas = self._database.get_all_data(target = "sbid")
#
#         sb_sids:list[dict] = []
#         sbids = []
#
#         for schedule_bundle_data in schedule_bundle_datas:
#             schedule_bundle= ScheduleBundle().make_with_dict(schedule_bundle_data)
#             if sid in schedule_bundle.sids:
#                 schedule_bundle.sids.remove(sid)
#                 sb_sids.append({"sids" : schedule_bundle.sids})
#                 sbids.append(schedule_bundle.sbid)
#
#
#         tuser_datas = self._database.get_all_data(target="tuid")
#
#         tu_sids:list[TUser] = []
#         tuids = []
#
#         for tuser_data in tuser_datas:
#             tuser = TUser().make_with_dict(tuser_data)
#             if sid in tuser.sids:
#                 tuser.sids.remove(sid)
#                 tu_sids.append({"sids" : tuser.sids})
#                 tuids.append(tuser.tuid)
#
#         self._tuser.my_sids.remove(sid)
#
#         self._database.modify_datas_with_ids(target_id="sbid", ids=sbids, target_datas=sb_sids)
#         self._database.modify_datas_with_ids(target_id="tuid", ids=tuids, target_datas=tu_sids)
#         self._database.modify_data_with_id(target_id="tuid", target_data=self._tuser.get_dict_form_data())
#
#         self._database.delete_data_with_id(target="sid", id=sid)
#         self.__result = True
#         return
#
#     # 스케줄 번들 삭제
#     # 테스트 아직 안했음 주의 ( Modify 수정이 완료된 후에 하기로)
#     def delete_bundle(self, sbid:str):
#         # 스케줄 데이터 삭제
#         schedule_bundle_data = self._database.get_data_with_id(target='sbid', id=sbid)
#         schedule_bundle = ScheduleBundle().make_with_dict(schedule_bundle_data)
#         sids = schedule_bundle.sids
#
#         # tuser에서 sid를 삭제
#         tuser_datas = self._database.get_all_data(target="tuid")
#         tu_sids : list[TUser] = []
#         tuids = []
#
#         # 각 Tuser마다 반복합니다
#         for tuser_data in tuser_datas:
#             tuser = TUser().make_with_dict(tuser_data)
#             # 스케줄 번들 안에 있는 모든 sids에 대해 삭제를 진행합니다.
#             tuser.sids = list(filter(lambda sid: sid not in sids, tuser.sids))      # 잘 됨
#             # if sbid in tuser.sbids:
#             #     tuser.sbids.remove(sbid)
#
#             tu_sids.append({"sids": tuser.sids})
#             tuids.append(tuser.tuid)
#
#
#         self._tuser.my_sids = list(filter(lambda sid: sid not in sids, self._tuser.my_sids))
#         self._tuser.my_sbids.remove(sbid)
#
#
#         self._database.modify_datas_with_ids(target_id="tuid", ids=tuids, target_datas=tu_sids)
#         self._database.modify_data_with_id(target_id="tuid", target_data=self._tuser.get_dict_form_data())
#
#         self._database.delete_datas_with_ids(target="sid", ids=sids)
#         self._database.delete_data_with_id(target="sbid", id=sbid)
#
#         self.__result = True
#
#         return
#
#
#     def get_response_form_data(self, head_parser):
#         body = {
#             "result" : self.__result
#             }
#
#         response = self._get_response_data(head_parser=head_parser, body=body)
#         return response
#
#
