from model.base_model import BaseModel
from model import Local_Database
from numpy.random.c_distributions import random_exponential
from others.data_domain import TimeTableUser as TUser
from others.data_domain import Schedule, ScheduleBundle, ScheduleEvent, Bias

from datetime import datetime
import random
import string

from pydantic_core.core_schema import time_schema


# ------------------------------------ 기본 타임 테이블 모델 ------------------------------------------
class TimeTableModel(BaseModel):
    def __init__(self, database:Local_Database) -> None:
        super().__init__(database)
        self._tuser:TUser = TUser()
        self._key = -1
        
        self.__num_bias = 0
        self.__target_date = f'00년 0월 0주차'
        
    # 로그인이 필수인 유저이거나, 로그인을 한 유저를 처리할 때 필수적으로 사용되는 부분
    def _set_tuser_with_tuid(self, tuid="") -> bool:
        # 유저를 먼져 부르고 해야됨 반드시
        if tuid == "" :
            if self._user.uid == "":
                return False
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

    # bias 세팅
    def set_num_bias(self):
        self.__num_bias= len(self._user.bids)
        return
    
    def set_target_date(self):
        today = datetime.today()
        shorted_year = today.year % 100
        
        first_day_of_month = datetime(today.year, today.month, 1)

        # 해당 날짜와 첫 번째 날의 주 번호 계산
        start_week = first_day_of_month.isocalendar()[1]  # 해당 달 첫 날의 주 번호
        current_week = today.isocalendar()[1]             # 해당 날짜의 주 번호

        # 현재 주가 3월 내의 몇 번째 주인지 계산
        week_in_month = current_week - start_week + 1
        
        # 만약 미래에 있는 사람이 2100에 산다면 이 곳의 코드를 고치면 됩니다
        self.__target_date = f'{shorted_year}년 {today.month}월 {week_in_month}주차'
        return
    
    # 컨트롤러에서 유저가 있는지 확인이 가능하게 하는 부분
    def is_tuser_alive(self):
        if self._tuser.tuid == "":
            return False
        else:
            return True

    def paging_id_list(self, id_list:list, last_index:int, page_size=8):

        # 최신순으로 정렬된 상태로 id_list를 받아오기 때문에, 인덱스 번호가 빠를수록 최신의 것
        # 만약에 페이지 사이즈보다 더 짧은 경우도 있을 수 있기에 먼저 정해놓는다.
        # 이러면 페이징된 리스트의 길이에 상관없이, 인덱스를 알아낼 수 있을 것

        paging_list = id_list[last_index + 1:]
        last_index_next = -1
        if len(id_list) != 0:
            last_index_next = id_list.index(id_list[-1])

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
            "target_date" : self.__target_date
            }

        response = self._get_response_data(head_parser=head_parser, body=body)
        return response

class ScheduleRecommendKeywordModel(TimeTableModel):
    def __init__(self, database:Local_Database) -> None:
        super().__init__(database)
        self._recommend_keywords = []

    # 바이어스의 카테고리 데이터를 추천 검색어로 사용하는 방법
    def get_category_recommend(self, num_keywords:int):
        bias_datas = []
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

        self._recommend_keywords = random.sample(category_set, num_keywords)

        return

    def get_response_form_data(self, head_parser):
        body = {
            "recommend_keywords" : self._recommend_keywords
        }

        response = self._get_response_data(head_parser=head_parser, body=body)
        return response

class TimeTableBiasModel(TimeTableModel):
    def __init__(self, database:Local_Database) -> None:
        super().__init__(database)
        self._biases = [] # 홈 전용 및 검색 전용
        self._ad_true_biases = []
        self._key = -1

    # Time Schedule에 쓰는 Bias 데이터를 만드는 함수
    def _tbias_data(self, bias:Bias):
        Sbias_data = {}

        Sbias_data["bid"] = bias.bid
        Sbias_data["bname"] = bias.bname
        Sbias_data["category"] = bias.category
        Sbias_data["tags"] = bias.tags
        Sbias_data["main_time"] = bias.main_time
        Sbias_data["is_ad"] = bias.is_ad

        return Sbias_data

    # Time Bias를 담는 리스트를 만듦
    def _get_tbias_list(self, bias_list):
        # bias_datas = self._database.get_datas_with_ids(target_id="bid", ids=bids)
        #
        # for bias_data in bias_datas:
        #     bias=Bias()
        #     bias.make_with_dict(dictionary=bias_data)
        #     Sbias_data = self._tbias_data(bias)
        tbias_list = []

        for bias in bias_list:
            schedule_bias_data = self._tbias_data(bias)
            tbias_list.append(schedule_bias_data)

        return tbias_list

    # # 광고로 등록된 바이어스 추천 리스트를 샘플링 (광고)
    # 수정해야하긴 해서 일단 원형을 남기고 나중에 광고를 붙인다면 그 때 다시하겠습니다.
    def _random_sampling_ad_true_bias(self, bias_list, random_samples):
        # 광고로 등록된 애들
        ad_true_bias = []
        for bias in bias_list:
            if bias.is_ad == True:
                ad_true_bias.append(bias)
        # 광고로 뽑힌 사람들
        random_ad_true_list = random.sample(ad_true_bias, random_samples)

        return random_ad_true_list

    # 바이어스 추천 리스트
    def get_recommend_bias_list(self, random_samples):
        bias_datas = self._database.get_all_data(target="bid")
        bias_list = []

        for bias_data in bias_datas:
            bias = Bias()
            bias.make_with_dict(bias_data)
            bias_list.append(bias)

        self._biases = random.sample(bias_list, random_samples)

        # ad_true_samples = int(random_samples * 0.3)
        # # 최애 랜덤 샘플링 (광고, 비광고 구분)
        # ad_true_bias_list = self._random_sampling_ad_true_bias(bias_list=bias_list, random_samples=ad_true_samples)
        #
        # # 이렇게 하는 이유
        # # AD = True인 최애를 뽑았는데 그 개수가 부족하여 자리가 남는경우를 대비해서 더 뽑는거
        # # 전체 랜덤 수 = 5, 뽑아야 할 AD_True 명 수 = 2, 실제로 나온 거 1
        # # 뽑아야 할 것 = 4 ( 5 - 1 )
        # # 만약 AD_true = 0이면 5명 뽑아야 함
        # random_bias_samples = random_samples - len(ad_true_bias_list)
        #
        # # 랜덤해서 뽑되, 광고로 뽑힌 사람은 제외한다
        # remain_bias_list = [bias for bias in bias_list if bias not in ad_true_bias_list]
        # random_remain_bias_list = random.sample(remain_bias_list, random_bias_samples)
        #
        # # 메인에 등록될 광고 최애 + 랜덤 최애 추천
        # full_list = ad_true_bias_list + random_remain_bias_list
        # self._biases = self._get_tbias_list(full_list)

        return

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
                search_list.append(bias)
            elif keyword in bias.category:
                search_list.append(bias)
            elif keyword in bias.tags:
                search_list.append(bias)
            elif keyword in bias.agency:
                search_list.append(bias)

        return search_list

    # 바이어스 키워드 서치
    def search_bias_with_keyword(self, keyword:str, last_index:int, num_bias:int):
        search_bias_list = self.__search_bias_list(keyword=keyword)
        self._biases, self._key = self.paging_id_list(id_list=search_bias_list, last_index=last_index, page_size=num_bias)
        return


    def get_response_form_data(self, head_parser):
        body = {
            "biases" : self._biases,
            "key" : self._key
        }

        response = self._get_response_data(head_parser=head_parser, body=body)
        return response

class TimeScheduleModel(TimeTableModel):
    def __init__(self, database:Local_Database) -> None:
        super().__init__(database)
        self._schedules = []
        self._key = -1

    # 스케쥴 Send Data 만드는 함수
    def _time_schedule(self, schedule:Schedule):
        time_schedule_data = {}

        time_schedule_data["sid"] = schedule.sid
        time_schedule_data["detail"] = schedule.sname
        time_schedule_data["bid"] = schedule.bid
        time_schedule_data["bname"] = schedule.bname
        time_schedule_data["uid"] = schedule.uid
        time_schedule_data["uname"] = schedule.uname
        time_schedule_data["start_time"] = self._calculate_day_hour_time(schedule.start_time)
        time_schedule_data["end_time"] = self._calculate_day_hour_time(schedule.end_time)
        time_schedule_data["start_date"] = self._transfer_date_str(schedule.start_date)
        time_schedule_data["end_date"] = self._transfer_date_str(schedule.end_date)
        time_schedule_data["update_time"] = self._cal_update_time(schedule.update_time)
        time_schedule_data["location"] = schedule.location
        time_schedule_data["code"] = schedule.code
        time_schedule_data["color_code"] = schedule.color_code

    # 스케쥴 리스트 만드는 함수
    def get_tschedule_list(self, sids):
        schedule_datas = self._database.get_datas_with_ids(target_id="sid", ids=sids)

        for schedule_data in schedule_datas:
            schedule = Schedule()
            schedule.make_with_dict(dict_data=schedule_data)
            self._schedules.append(self._time_schedule(schedule))

        return

    def get_response_form_data(self, head_parser):
        body = {
            "schedules" : self._schedules,
            "key" : self._key
        }

        response = self._get_response_data(head_parser=head_parser, body=body)
        return response

class TimeEventModel(TimeTableModel):
    def __init__(self, database:Local_Database) -> None:
        super().__init__(database)
        self._events = []
        self._key = -1

    # Event 보낼 거 만드는 함수
    def _tevent_data(self, event:ScheduleEvent):
        time_event_data = {}

        time_event_data["seid"] = event.seid
        time_event_data["sename"] = event.sename
        time_event_data["bid"] = event.bid
        time_event_data["bname"] = event.bname
        time_event_data["uid"] = event.uid
        time_event_data["uname"] = event.uname
        time_event_data["date"] = self._transfer_date_str(event.date)
        time_event_data["start"] = self._calculate_day_hour_time(event.start_time)
        time_event_data["end"] = self._calculate_day_hour_time(event.end_time)
        time_event_data["sids"] = event.sids
        time_event_data["location"] = event.location

    # 이벤트 딕셔너리 데이터 리스트를 만드는 곳
    def get_tevent_list(self, seids):
        event_datas = self._database.get_datas_with_ids(target_id="seid", ids=seids)

        for event_data in event_datas:
            event = ScheduleEvent()
            event.make_with_dict(dict_data=event_data)
            self._events.append(self._tevent_data(event))

        return

    def get_response_form_data(self, head_parser):
        body = {
            "events" : self._events,
            "key" : self._key
        }

        response = self._get_response_data(head_parser=head_parser, body=body)
        return response

class TimeScheduleBundleModel(TimeTableModel):
    def __init__(self, database:Local_Database) -> None:
        super().__init__(database)
        self._schedule_bundles = []
        self._key = -1

    def _transfer_date_str_list(self, sid_list):
        schedule_datas = self._database.get_datas_with_ids(target_id="sid", ids=sid_list)
        date_list = []

        for schedule_data in schedule_datas:
            schedule = Schedule()
            schedule.make_with_dict(dict_data=schedule_data)

            date = schedule.date.strftime("%y년 %m월 %d일")
            date_list.append(date)

        return date_list


    def _time_schedule_bundle(self, schedule_bundle:ScheduleBundle):
        time_schedule_bundle_data = {}

        time_schedule_bundle_data["sbid"] = schedule_bundle.sbid
        time_schedule_bundle_data["sbname"] = schedule_bundle.sbname
        time_schedule_bundle_data["bid"] = schedule_bundle.bid
        time_schedule_bundle_data["bname"] = schedule_bundle.bname
        time_schedule_bundle_data["uid"] = schedule_bundle.uid
        time_schedule_bundle_data["uname"] = schedule_bundle.uname
        time_schedule_bundle_data["sids"] = schedule_bundle.sids
        time_schedule_bundle_data["date"] = self._transfer_date_str_list(schedule_bundle.sids)
        time_schedule_bundle_data["location"] = schedule_bundle.location

    def get_tschedule_bundle_list(self, sbids):
        schedule_bundle_datas = self._database.get_datas_with_ids(target_id="sbid", ids=sbids)

        for schedule_bundle_data in schedule_bundle_datas:
            schedule_bundle = ScheduleBundle()
            schedule_bundle.make_with_dict(dict_data=schedule_bundle_data)

            self.schedule_bundles.append(self._time_schedule_bundle(schedule_bundle_data))

        return

    def get_response_form_data(self, head_parser):
        body = {
            "schedule_bundle" : self.schedule_bundles,
            "key": self._key
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
    
# 복수 스케줄을 반환할 때 사용하는 모델 
# 아마 대부분이 여러개를 반환해야하니 이거 쓰면 될듯
class MultiScheduleModel(TimeTableModel):
    def __init__(self, database:Local_Database) -> None:
        super().__init__(database)
        self.__schedules:list[Schedule] = []
        self.__schedule_events:list[ScheduleEvent] = []
        self.__schedule_bundles:list[ScheduleBundle] = []

    # id_list는 서치한 데이터들의 고유 아이디
    def _make_schedule_data(self,id_list:list, search_type:str="schedule"):
        schedule_id_type = ""
        if search_type == "schedule":
            schedule_id_type = "sid"
        elif search_type == "schedule_bundle":
            schedule_id_type = "sbid"
        elif search_type == "event":
            schedule_id_type = "seid"

        schedule_type_datas = self._database.get_datas_with_ids(target_id=schedule_id_type, ids=id_list)

        for data in schedule_type_datas:
            if schedule_id_type == "sid":
                send_data = Schedule()
                send_data.make_with_dict(data)
                self.__schedules.append(send_data)

            elif schedule_id_type == "seid":
                send_data = ScheduleEvent()
                send_data.make_with_dict(data)
                self.__schedule_events.append(send_data)

            elif schedule_id_type == "sbid":
                send_data = ScheduleBundle()
                send_data.make_with_dict(data)
                self.__schedule_bundles.append(send_data)

        return

    def _find_schedule_data(self, keyword:str):
        schedule_datas = self._database.get_all_data(target="sid")
        # 왜 불편하게 id_list로 담나요?
        # 페이징할 때 편합니다.
        schedule_ids = []

        # 찾기
        for schedule_data in schedule_datas:
            # 일정코드로 검색하는 경우
            if keyword in schedule_data["code"]:
                schedule_ids.append(schedule_data['sid'])
                continue
            # 스케쥴 이름으로 검색
            elif keyword in schedule_data["sname"]:
                schedule_ids.append(schedule_data['sid'])
                continue
            # 유저네임으로 검색하는 경우
            elif keyword in schedule_data['uname']:
                schedule_ids.append(schedule_data['sid'])
                continue
            # Bias 네임으로 검색하는 경우
            elif keyword in schedule_data['bname']:
                schedule_ids.append(schedule_data['sid'])
                continue

        return schedule_ids

    def _find_schedule_bundle_data(self, keyword:str):
        schedule_bundle_datas = self._database.get_all_data(target="sbid")
        schedule_bundle_ids = []

        for schedule_bundle_data in schedule_bundle_datas:
            # schedule_bundle = ScheduleBundle()
            # schedule_bundle.make_with_dict(dict_data=schedule_bundle_data)

            # 한번 담으면 더 이상 서치된 번들에 대해서는 중복 서치할 필요가 없으므로 Continue.

            # 일정코드로 검색
            if keyword in schedule_bundle_data['code']:
                schedule_bundle_ids.append(schedule_bundle_data['sbid'])
                continue
            # 스케쥴 이름으로 검색
            elif keyword in schedule_bundle_data['sbname']:
                schedule_bundle_ids.append(schedule_bundle_data['sbid'])
                continue
            # 유저네임으로 검색하는 경우
            elif keyword in schedule_bundle_data['uname']:
                schedule_bundle_ids.append(schedule_bundle_data['sbid'])
                continue
            # Bias 네임으로 검색하는 경우
            elif keyword in schedule_bundle_data['bname']:
                schedule_bundle_ids.append(schedule_bundle_data['sbid'])
                continue

        return schedule_bundle_ids

    def _find_schedule_event_data(self, keyword:str):
        schedule_event_datas = self._database.get_all_data(target="seid")
        schedule_event_ids = []

        for schedule_event_data in schedule_event_datas:
            # schedule_event = ScheduleEvent()
            # schedule_event.make_with_dict(dict_data=schedule_event_data)

            # 한번 담으면 더 이상 서치된 번들에 대해서는 중복 서치할 필요가 없으므로 Continue.
            # 일정코드로 검색
            if keyword in schedule_event_data['code']:
                schedule_event_ids.append(schedule_event_data['seid'])
                continue
            # 스케쥴 이름으로 검색
            elif keyword in schedule_event_data['sbname']:
                schedule_event_ids.append(schedule_event_data['seid'])
                continue
            # 유저네임으로 검색하는 경우
            elif keyword in schedule_event_data['uname']:
                schedule_event_ids.append(schedule_event_data['seid'])
                continue
            # Bias 네임으로 검색하는 경우
            elif keyword in schedule_event_data['bname']:
                schedule_event_ids.append(schedule_event_data['seid'])
                continue

        return schedule_event_ids
    # 내가 이벤트 스케줄 데이터 뽑기를 날짜로
    # date는 날짜임 , 형태는 2025/03/06 임
    # date안넣으면 기본적으로 오늘자로 감
    def set_my_event_in_by_day(self, date=datetime.today().strftime("%Y/%m/%d")):
        # 내가 추가한 이벤트를 다 가지고 옴
        schedule_event_datas = self._database.get_datas_with_ids(target_id="seid", ids=self._tuser.seids)
        
        # 필요하면 갯수 제한도 두삼
        for schedule_event_data in schedule_event_datas:
            schedule_event = ScheduleEvent()
            schedule_event.make_with_dict(dict_data=schedule_event_data)
            # 여기서 날짜랑 맞는지 필터링 함
            if date== schedule_event.date:
                self.__schedule_events.append(schedule_event)
        return
    
    # 전체 이벤트 데이터 뽑기를 날짜로
    # date는 날짜임 , 형태는 2025/03/06 임
    # date안넣으면 기본적으로 오늘자로 감
    def set_event_in_by_day(self, date=datetime.today().strftime("%Y/%m/%d")):
        # 이건 데이터 베이스에서 해당 날짜 이벤트만 전부다 뽑는거임
        schedule_event_datas = self._database.get_datas_with_key(target="seid", key="date", key_datas=[date])
        
        # 필요하면 갯수 제한도 두삼
        for shedule_event_data in schedule_event_datas:
            schedule_event = ScheduleEvent()
            schedule_event.make_with_dict(dict_data=schedule_event)
            self.__schedule_events.append(schedule_event)
        return
    
    
    # 전체 스케줄 데이터 뽑기를 날짜로
    # date는 날짜임 , 형태는 2025/03/06 임
    # date안넣으면 기본적으로 오늘자로 감
    def set_schedule_in_by_day(self, date=datetime.today().strftime("%Y/%m/%d")):
        # 이건 데이터 베이스에서 해당 날짜 이벤트만 전부다 뽑는거임
        schedule_datas = self._database.get_datas_with_key(target="sid", key="date", key_datas=[date])
        
        # 필요하면 갯수 제한도 두삼
        for shedule_data in schedule_datas:
            schedule= Schedule()
            schedule.make_with_dict(dict_data=schedule)
            self.__schedules.append(schedule)
        return
    
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
    
    # 내가 타임테이블에 노출시키려고 했던 schedule을 보여줌
    # tuser의 this_week_sids를 기반으로 함
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
            
        return
    
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
        return

    # 키워드를 통해 검색합니다.
    def search_schedule_with_keyword(self, keyword:str, search_type:str, last_index=-1, num_schedules=8):
        searched_list = []

        if search_type == "schedule":
            searched_list = self._find_schedule_data(keyword=keyword)
        elif search_type == "schedule_bundle":
            searched_list = self._find_schedule_bundle_data(keyword=keyword)
        elif search_type == "event":
            searched_list = self._find_schedule_event_data(keyword=keyword)

        searched_list, self._key = self.paging_id_list(id_list=searched_list,
                                                            last_index=last_index,
                                                            page_size=num_schedules)

        self._make_schedule_data(id_list=searched_list, search_type=search_type)
        return

    def search_my_schedule_with_bid(self, bid):
        # 데이터 불러오고
        schedule_datas = self._database.get_datas_with_ids(target_id="sid", ids=self._tuser.sids)
        
        # 보낼 스케줄 정하는 곳
        # 만약 등록된 순서가 뒤집히면 여기서 reverse 추가해야됨
        for schedule_data in schedule_datas:
            schedule = Schedule()
            schedule.make_with_dict(dict_data=schedule_data)
            
            if schedule.bid == bid:
                self.__schedules.append(schedule)
                
        # 데이터 불러오고
        schedule_events_datas = self._database.get_datas_with_ids(target_id="seid", ids=self._tuser.seids)
        
        # 보낼 이벤트 정하는 곳
        for schedule_event_data in schedule_events_datas:
            schedule_event = ScheduleEvent()
            schedule_event.make_with_dict(dict_data=schedule_event_data)
            
            if schedule_event.bid == bid:
                self.__schedule_events.append(schedule_event)
        return
        
    def search_my_all_schedule(self):
        # 데이터 불러오고
        schedule_datas = self._database.get_datas_with_ids(target_id="sid", ids=self._tuser.sids)
        
        # 보낼 스케줄 정하는 곳
        # 만약 등록된 순서가 뒤집히면 여기서 reverse 추가해야됨
        for schedule_data in schedule_datas:
            schedule = Schedule()
            schedule.make_with_dict(dict_data=schedule_data)
            self.__schedules.append(schedule)
                
        # 데이터 불러오고
        schedule_events_datas = self._database.get_datas_with_ids(target_id="seid", ids=self._tuser.seids)
        
        # 보낼 이벤트 정하는 곳
        for schedule_event_data in schedule_events_datas:
            schedule_event = ScheduleEvent()
            schedule_event.make_with_dict(dict_data=schedule_event_data)
            self.__schedule_events.append(schedule_event)
        return
    
    def get_response_form_data(self, head_parser):
        body = {
            "schedules" : self._make_dict_list_data(list_data=self.__schedules),
            "schedule_events" : self._make_dict_list_data(list_data=self.__schedule_events),
            "schedule_bundles" : self._make_dict_list_data(list_data=self.__schedule_bundles),
            "key" : self._key
            }

        response = self._get_response_data(head_parser=head_parser, body=body)
        return response
    
    
class AddScheduleModel(TimeTableModel):
    def __init__(self, database:Local_Database) -> None:
        super().__init__(database)
        self.__result = False
        
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
    
    # 이번주 타임 테이블에 노출시킬 스케줄을 선택하는 곳
    # date는 날짜임 , 형태는 2025/03/06 임
    def select_schedule_in_showcase(self, date, bid):
        # 스케줄 데이터를 가지고 오고
        schedule_data = self._database.get_data_with_id(target="sid", id=self._tuser.sids)
        
        # 저장해야하는지 체크하는 플래그
        flag = False
        
        # 날짜를 비교해서 이사람이 본거 찾아야됨
        # date는 날짜임 , 형태는 2025/03/06 임
        for schedule in schedule_data:
            schedule = Schedule()
            schedule.make_with_dict(dict_data=schedule)
            if schedule.date == date and schedule.bid == bid:
                # 없으면 추가하고 있으면 삭제하면됨
                if schedule.sid not in self._tuser.this_week_sids:
                    self._tuser.this_week_sids.append(schedule.sid)
                else:
                    self._tuser.this_week_sids.remove(schedule.sid)
                flag = True
                return
        
        # 저장하는 곳
        if flag:
            self._database.modify_data_with_id(target_id="tuid", target_data=self._tuser.get_dict_form_data())
            self.__result = True
        
        return
    
    # 내 스케줄 목록에서 지워버리는 곳 (이번주 목록이면 여기서 함)
    def reject_from_my_week_schedule(self, sid):
        # 저장해야하는지 체크하는 플래장
        flag= False
        
        if sid in self._tuser.sids:
            self._tuser.sids.remove(sid)
            flag = True
            
        if sid in self._tuser.this_week_sids:
            self._tuser.this_week_sids.remove(sid)
            flag = True
        
        if flag: 
            self._database.modify_data_with_id(target_id="tuid", target_data=self._tuser.get_dict_form_data())
            self.__result = True
        return
    
    # sid 만들기
    def __make_new_sid(self):
        while True:
            sid = self._make_new_id()
            if self._database.get_data_with_id(target="sid", id=sid):
                continue
            else:
                break
        return sid
    
    # 코드 만들기
    def __make_schedule_code(self):
        # 영어 대문자와 숫자로 이루어진 6자리 코드 생성
        characters = string.ascii_uppercase + string.digits
        code = ''.join(random.choices(characters, k=6))
        return code
    
    # 단일 스케줄 만들기
    def make_new_single_schedule(self, data_payload, bid):
        schedule = Schedule(
            sname=data_payload.sname,
            location=data_payload.location,
            bid = bid,
            start_date=data_payload.start_date,
            start_time=data_payload.start_time,
            end_date=data_payload.end_date,
            end_time=data_payload.end_time,
            state=data_payload.state
        )
        
        schedule.sid = self.__make_new_sid()
        schedule.code = self.__make_schedule_code()
        
        bias_data = self._database.get_data_with_id(target="bid", id=schedule.bid)
        bias = Bias().make_with_dict(bias_data)
        
        schedule.bname = bias.bname
        schedule.uid = self._user.uid
        schedule.uname = self._user.uname
        schedule.update_datetime = datetime.today().strftime("%Y/%m/%d-%H:%M:%S")
        return schedule
    
    # 단일 스테줄 저장
    def save_new_schedules(self, schedule:list):
        save_data = self._make_dict_list_data(list_data=schedule)
        self._database.add_new_datas(target_id="sid", new_datas=save_data)
        self.__result = True
        return
    
    # 복수 스케줄 만들기
    def make_new_multiple_schedule(self, schedules:list[Schedule], bid:str):
        schedule_list = []
        
        for schedule in schedules:
            schedule = self.make_new_single_schedule(data_payload=schedule, bid=bid)
            schedule_list.append(schedule)
        
        return schedule_list
        
    
    def get_response_form_data(self, head_parser):
        body = {
            "result" : self.__result
            }

        response = self._get_response_data(head_parser=head_parser, body=body)
        return response
    
    
import random 
from datetime import timedelta

# 시간 구간 정보 (0-6, 6-12, 12-18, 18-24)
time_ranges = [(0, 6), (6, 12), (12, 18), (18, 24)]
weekday_names = ['월', '화', '수', '목', '금', '토', '일']
    
class ScheduleBlock(Schedule):
    def __init__(self):
        self.timeblocks = []
        self.color_code = "#D2D2D2"
        self.__overflowed = False
        self.__remain_time = Schedule()
        self.start_datetime = datetime()
        self.end_datetime = datetime()
    
    def is_overflowed(self):
        return self.__overflowed
    
    def get_remain_schedule(self):
        return self.__remain_time
        
        
    # 이게 전송용 데이터 포멧
    def get_dict_form_data(self):
        super_dict_data = super().get_dict_form_data()
        super_dict_data['timeblocks'] = self.timeblocks
        super_dict_data['color_code'] = self.color_code
        return super_dict_data
        
class WeekDayDataBlock:
    def __init__(self, date, day, num_schedule):
        self.date = date
        self.day = day
        self.num_schedule = num_schedule
        
     # 이게 전송용 데이터 포멧
    def get_dict_form_data(self):
        return {
            'date' : self.date,
            'day' : self.day,
            'num_schedule' : self.num_schedule
        }
    
class ScheduleBlockTreater():
    def __init__(self):
        self.__over_flowed_schedules = []
        
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
                targetWeekDayDateBlock = WeekDayDataBlock(date=weekday_names[schedule_block.start_datetime.weekday()],
                                                       day = schedule_block.start_datetime.day,
                                                       num_schedule=0
                                                       )
            
            # 핵심 - 스케줄 수를 하나 늘려주면됨
            weekDayDateBlock.num_schedule += 1
        
         # WeekDayDateBlocks를 date 기준으로 정렬
        sorted_block_list = sorted(weekDayDateBlocks, key=lambda x: x.date)

        # today와 같은 날짜부터 리스트를 자름
        today_weekday = today.weekday()
        trimmed_list = [block for block in sorted_block_list if block.date >= today_weekday]
        
        return trimmed_list
        
        
    def claer_over_flowed_schedule(self) -> list[ScheduleBlock]:
        schedule_blocks = []
        
        for schedule in self.__over_flowed_schedules:
            schedule_block = self.make_schedule_block(schedule=schedule)
            schedule_blocks.append(schedule_block)
        
        return schedule_blocks
    
    #  만들기
    def make_schedule_block(self, schedule:Schedule):
        schedule_block = ScheduleBlock()
        schedule_block.make_with_dict(schedule.get_dict_form_data())
        
        # 시작 및 종료 시간 합치기
        schedule_block.start_datetime = datetime.strptime(f"{schedule_block.start_date} {schedule_block.start_time}", "%Y/%m/%d %H:%M")
        schedule_block.end_datetime = datetime.strptime(f"{schedule_block.end_date} {schedule_block.end_time}", "%Y/%m/%d %H:%M")
        
        # 위크 데이트 블록 리스트에 날짜가 포함되었는지 확인하고 넣을 것
        schedule_block = self.__make_timeblocks(schedule_block=schedule_block)
        
        schedule_block.color_code = self.__make_color_code()
        return schedule_block
    
    def __make_timeblocks(self, schedule_block:ScheduleBlock) -> ScheduleBlock:
        current_datetime = schedule_block.start_datetime
        first_block = True  # 첫 번째 블록인지 확인하는 플래그
        end_flag = False
        
        while current_datetime < schedule_block.end_datetime:
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

        # 하루를 넘어가면 넘어갔다고 표시하고 보관하기
        if schedule_block.start_datetime.day != schedule_block.end_datetime.day:
            overflowed_schedule = Schedule().make_with_dict(schedule_block.get_dict_form_data())
            overflowed_schedule.start_date = schedule_block.end_datetime.strftime("%Y/%m/%d")
            overflowed_schedule.start_time = "00:00"
            overflowed_schedule.end_date = schedule_block.end_datetime.strftime("%Y/%m/%d")
            overflowed_schedule.end_time = schedule_block.end_datetime.strftime("%H:%M") 
            self.__over_flowed_schedules.append(overflowed_schedule)

        return schedule_block
    
        
    # 쨍하고 밝은 색깔 코드 생성기
    def __make_color_code(self):
        # 더 쨍하고 밝은 색상을 위해 범위 설정
        r = random.randint(170, 255)  # 밝은 색상 범위
        g = random.randint(170, 255)
        b = random.randint(170, 255)
    
        # 흰색과의 혼합을 줄여 더 선명한 색상 유지
        r = (r * 3 + 255) // 4
        g = (g * 3 + 255) // 4
        b = (b * 3 + 255) // 4
    
        return f'#{r:02x}{g:02x}{b:02x}'
    
    
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
    def set_my_schedule_in_by_day(self, target_date=datetime.today().strftime("%Y/%m/%d")):
        
        # 내가 추가한 스케줄을 다 가지고 옴
        schedule_datas = self._database.get_datas_with_ids(target_id="sid", ids=self._tuser.sids)
        
        today = target_date - timedelta(days=2)
        
        schedules = []
        
        # 필요하면 갯수 제한도 두삼
        for schedule_data in schedule_datas:
            schedule = Schedule()
            schedule.make_with_dict(dict_data=schedule_data)
            # 여기서 날짜랑 맞는지 필터링 함
            if datetime.strptime(schedule.start_date, "%Y/%m/%d") > today:
                schedules.append(schedule)
                
        schedule_block_treater = ScheduleBlockTreater()
        
        
        for schedule in schedules:
            schedule_block = schedule_block_treater.make_schedule_block(schedule=schedule)
            self.__schedule_blocks.append(schedule_block)
            
        over_flowed_schedule:list = schedule_block_treater.claer_over_flowed_schedule()
        
        self.__schedule_blocks.extend(over_flowed_schedule)
        
        self.__week_day_datas = schedule_block_treater.make_week_day_data(schedule_blocks=self.__schedule_blocks)
        
        # 시작이 전날이고, 끝나는게 오늘이면 데이터가 안나오기 때문에
        # 결국 타임 블럭에서 하루 전날꺼를 구하고 그날 데이터를 버려야됨
        # 이코드가 추가되어야됨
        
        return
    
    def get_response_form_data(self, head_parser):
        body = {
            "schedule_blocks" : self._make_dict_list_data(list_data=self.__schedule_blocks),
            "week_day_datas" : self._make_dict_list_data(list_data=self.__week_day_datas),
            }

        response = self._get_response_data(head_parser=head_parser, body=body)
        return response