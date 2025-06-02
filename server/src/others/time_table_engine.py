from others.data_domain import TimeTableUser, Schedule, ScheduleBundle
from others.managed_data_domain import ManagedScheduleTable, ManagedSchedule, ManagedScheduleBundle
from pprint import pprint
from typing import Union, List


# 스케줄 서치 엔진
# 새롭게 정비된 Managed_data_domain을 바탕으로 만들어집니다.
class ScheduleSearchEngine:
    def __init__(self, database):
        self.__database = database
        self.__managed_schedule_table = ManagedScheduleTable(database=database)

    # 랜덤한 스케줄을 반환합니다.
    def try_get_random_schedule(self):
        return self.__managed_schedule_table.get_random_schedule()



    # 새로운 스케줄을 테이블에 추가합니다.
    def try_add_new_managed_schedule(self, new_schedule:Schedule):
        self.__managed_schedule_table.make_new_managed_schedule(schedule=new_schedule)
        return

    # 새로운 스케줄들을 테이블에 추가하는 함수
    # 리스트로 받았지만 반복문으로 처리합니다.
    def try_add_new_managed_schedule_list(self, new_schedules:list[Schedule]):
        for new_schedule in new_schedules:
            self.__managed_schedule_table.make_new_managed_schedule(schedule=new_schedule)
        return

    # 새로운 스케줄 번들을 테이블에 추가합니다.
    def try_add_new_managed_bundle(self, new_bundle:ScheduleBundle):
        self.__managed_schedule_table.make_new_managed_bundle(bundle=new_bundle)
        return

    # 새로운 스케줄 번들들을 테이블에 추가합니다.
    # 리스트로 받은 것을 반복문으로 처리합니다.
    def try_add_new_managed_bundle_list(self, new_bundles:list[ScheduleBundle]):
        for new_bundle in new_bundles:
            self.__managed_schedule_table.make_new_managed_bundle(bundle=new_bundle)
        return


    # 수정한 스케줄을 테이블에 저장합니다.
    def try_modify_schedule(self, modify_schedule:Schedule):
        self.__managed_schedule_table.modify_schedule_table(modify_schedule=modify_schedule)
        return

    # 수정한 스케줄들을 테이블에 저장합니다.
    def try_modify_schedule_list(self, modify_schedule_list:list[Schedule]):
        for modify_schedule in modify_schedule_list:
            self.__managed_schedule_table.modify_schedule_table(modify_schedule=modify_schedule)
        return

    # 수정한 스케줄 번들을 테이블에 저장합니다.
    def try_modify_bundle(self, modify_bundle:ScheduleBundle):
        self.__managed_schedule_table.modify_bundle_table(modify_bundle=modify_bundle)
        return

    # 수정한 스케줄 번들 리스트를 테이블에 저장합니다.
    def try_modify_bundle_list(self, modify_bundle_list:list[ScheduleBundle]):
        for modify_bundle in modify_bundle_list:
            self.__managed_schedule_table.modify_bundle_table(modify_bundle=modify_bundle)
        return



    # 스케줄을 테이블에서 삭제합니다.
    def try_remove_schedule(self, sid:str):
        self.__managed_schedule_table.remove_schedule_in_table(sid=sid)
        return

    # 스케줄 리스트를 테이블에서 삭제합니다.
    def try_remove_schedule_list(self, sids:list[str]):
        for sid in sids:
            self.__managed_schedule_table.remove_schedule_in_table(sid=sid)

    # 스케줄 번들을 테이블에서 삭제합니다.
    def try_remove_bundle(self, sbid:str=''):
        self.__managed_schedule_table.remove_bundle_in_table(sbid=sbid)

    # 스케줄 번들들을 테이블에서 삭제합니다.
    def try_remove_bundle_list(self, sbids:list[str]):
        for sbid in sbids:
            self.__managed_schedule_table.remove_bundle_in_table(sbid=sbid)




    # 현재 진행 중인 스케줄을 필터링합니다
    def try_filtering_schedule_in_progress(self, when:str, sids:list=None, return_id:bool=True):
        if sids is None:
            sids = []
        sid_list = self.__managed_schedule_table.filtering_schedule_is_in_progress(selected_sids=sids,
                                                                                   when=when,
                                                                                   return_id=return_id)
        return sid_list

    # 진행 중인 스케줄 번들을 필터링 합니다
    def try_filtering_bundle_in_progress(self, when:str, sbids:list=None, return_id:bool=True):
        if sbids is None:
            sbids = []
        sbid_list = self.__managed_schedule_table.filtering_bundle_is_in_progress(selected_sbids=sbids,
                                                                                  when=when,
                                                                                  return_id=return_id)
        return sbid_list



    # 금주의 일정들을 얻습니다.
    def try_get_weekday_schedule_list(self, sids:list=None, return_id:bool=True):
        if sids is None:
            sids = []
        sid_list = self.__managed_schedule_table.filtering_weekday_schedule(selected_sids=sids, return_id=return_id)

        return sid_list

    # 금주의 일정 번들을 얻습니다.
    def try_get_weekday_bundle_list(self, sbids:list=None, return_id:bool=True):
        if sbids is None:
            sbids = []
        sbid_list = self.__managed_schedule_table.filtering_weekday_bundle(selected_sbids=sbids, return_id=return_id)

        return sbid_list



    # 탐색용 스케줄을 반환하는 함수
    def try_get_explore_schedule_list(self, time_section:int, style:str, gender:str, category:str, return_id:bool=True):
        sid_list = self.__managed_schedule_table.search_explore_schedule(time_section=time_section, style=style, category=category,
                                                                         gender=gender, return_id=return_id)
        return sid_list

    # 특정 날짜에 걸려있는 모든 스케줄 을
    def try_get_schedules_in_specific_date(self, sids:list=None, specific_date:str="", return_id:bool=True) -> Union[List[dict], List[None], List[str]]:
        # 모든 sid를 사용하려면 무조건 "all"을 붙이시오.
        if sids is None:
            sids = []

        sid_list = self.__managed_schedule_table.filtering_schedule_in_specific_date(selected_sids=sids, specific_date=specific_date, return_id=return_id)
        return sid_list


    # 키워드를 활용한 스케줄 검색 로직
    def try_search_schedule_w_keyword(self, search_columns:list, target_keyword:str="", return_id:bool=True):
        print("??")
        sid_list = self.__managed_schedule_table.search_schedule_with_key(key=target_keyword, search_columns=search_columns,
                                                                          return_id=return_id)
        
        return sid_list

    # 키워드를 활용한 스케줄 번들 검색 로직
    def try_search_bundle_w_keyword(self, search_columns:list, target_keyword:str="", return_id:bool=True):
        sbid_list = self.__managed_schedule_table.search_bundle_with_key(key=target_keyword, search_columns=search_columns,
                                                                         return_id=return_id)
        return sbid_list

    # sid를 넣으면 Managed_객체가 반환되도록 함.
    # 이건 단일 sid에 대해서 나눔
    def try_get_schedule_with_sid(self, sid:str, return_id:bool=False):
        search_sid_list = list(sid)
        managed_schedule_list = self.__managed_schedule_table.search_schedule_with_sids(sid=search_sid_list, return_id=return_id)

        return managed_schedule_list

    # 복수의 sid에 대해 Managed_객체 반환
    def try_get_schedule_with_sids(self, sids:list[str], return_id:bool=False):
        managed_schedule_list = self.__managed_schedule_table.search_schedule_with_sids(sids=sids, return_id=return_id)

        return managed_schedule_list

    # 단일 번들 객체에 대해 Managed_객체 반환
    def try_get_bundle_with_sbid(self, sbid:str, return_id:bool=False):
        search_sbid_list = list(sbid)
        managed_bundle_list = self.__managed_schedule_table.search_bundle_with_sbids(sbid=search_sbid_list, return_id=return_id)

        return managed_bundle_list

    # 복수 sbid에 대해 Managed_객체 반환
    def try_get_bundle_with_sbids(self, sbids:list[str], return_id:bool=False):
        managed_bundle_list = self.__managed_schedule_table.search_bundle_with_sbids(sbids=sbids, return_id=return_id)

        return managed_bundle_list


    # 선택한 스케줄을 반환하는 함수
    def try_search_selected_schedules(self, sids:list=None, bid="", return_id:bool=True):
        if sids is None:
            sids = []
        sid_list = self.__managed_schedule_table.search_my_selected_schedules(bid=bid, selected_sids=sids, return_id=return_id)
        return sid_list

    # 선택한 스케줄 번들을 반환하는 함수
    def try_search_selected_bundles(self, sbids:list=None, bid="", return_id:bool=True):
        if sbids is None:
            sbids = []
        sbid_list = self.__managed_schedule_table.search_my_selected_bundles(bid=bid, selected_sbids=sbids, return_id=return_id)
        return sbid_list

