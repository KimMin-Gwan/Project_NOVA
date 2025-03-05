from model.base_model import BaseModel
from model import Local_Database
from others.data_domain import TimeTableUser as TUser
from others.data_domain import Schedule, ScheduleBundle, ScheduleEvent

from datetime import datetime

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
        
    def get_response_form_data(self, head_parser):
        body = {
            #"tuser" : self._tuser,
            "num_bias" : self.__num_bias,
            "target_date" : self.__target_date
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
    
    # 내가 이벤트 스케줄 데이터 뽑기를 날짜로
    # date는 날짜임 , 형태는 2025/03/06 임
    # date안넣으면 기본적으로 오늘자로 감
    def set_my_event_in_by_day(self, date=datetime.today().strftime("%Y/%m/%d")):
        # 내가 추가한 이벤트를 다 가지고 옴
        schedule_event_datas = self._database.get_datas_with_ids(target_id="seid", ids=self._tuser.seids)
        
        # 필요하면 갯수 제한도 두삼
        for shedule_event_data in schedule_event_datas:
            schedule_event = ScheduleEvent()
            schedule_event.make_with_dict(dict_data=schedule_event)
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
    
    # 내가 추가한 스케줄 데이터 뽑기를 날짜로
    # date는 날짜임 , 형태는 2025/03/06 임
    # date안넣으면 기본적으로 오늘자로 감
    def set_my_schedule_in_by_day(self, date=datetime.today().strftime("%Y/%m/%d")):
        # 내가 추가한 이벤트를 다 가지고 옴
        schedule_datas = self._database.get_datas_with_ids(target_id="sid", ids=self._tuser.seids)
        
        # 필요하면 갯수 제한도 두삼
        for schedule_data in schedule_datas:
            schedule = Schedule()
            schedule.make_with_dict(dict_data=schedule_data)
            # 여기서 날짜랑 맞는지 필터링 함
            if date== schedule.date:
                self.__schedules.append(schedule)
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
            self._database.modify_data_with_id(target_id="tuid", target_data=self._tuser)
            
        return
    
    # 주차에 따른 내가 추가한 스케줄을 보여줌
    def set_schedule_by_week(self, year="", week=0):
        # 데이터 불러오고
        schedule_datas = self._database.get_datas_with_ids(target_id="sid", ids=self._tuser.seids)
        
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
    
    
    
    def get_response_form_data(self, head_parser):
        body = {
            "result" : self.__result
            }

        response = self._get_response_data(head_parser=head_parser, body=body)
        return response
    
    