from others.data_domain import TimTableUser, Schedule, ScheduleBundle
from others.managed_data_domain import ManagedScheduleTable, ManagedSchedule, ManagedScheduleBundle
from pprint import pprint

class ScheduleSearchEngine:
    def __init__(self, database):
        self.__database = database
        self.__managed_schedule_table = ManagedScheduleTable(database=database)


    def try_get_random_schedule(self):
        return self.__managed_schedule_table.get_random_schedule()




    def try_add_new_managed_schedule(self, new_schedule:Schedule):
        self.__managed_schedule_table.make_new_managed_schedule(schedule=new_schedule)
        return

    def try_add_new_managed_schedule_list(self, new_schedules:list[Schedule]):
        for new_schedule in new_schedules:
            self.__managed_schedule_table.make_new_managed_schedule(schedule=new_schedule)
        return

    def try_add_new_managed_bundle(self, new_bundle:ScheduleBundle):
        self.__managed_schedule_table.make_new_managed_bundle(bundle=new_bundle)
        return

    def try_add_new_managed_bundle_list(self, new_bundles:list[ScheduleBundle]):
        for new_bundle in new_bundles:
            self.__managed_schedule_table.make_new_managed_bundle(bundle=new_bundle)
        return



    def try_modify_schedule(self, modify_schedule:Schedule):
        self.__managed_schedule_table.modify_schedule_table(modify_schedule=modify_schedule)
        return

    def try_modify_schedule_list(self, modify_schedule_list:list[Schedule]):
        for modify_schedule in modify_schedule_list:
            self.__managed_schedule_table.modify_schedule_table(modify_schedule=modify_schedule)
        return

    def try_modify_bundle(self, modify_bundle:ScheduleBundle):
        self.__managed_schedule_table.modify_bundle_table(modify_bundle=modify_bundle)
        return

    def try_modify_bundle_list(self, modify_bundle_list:list[ScheduleBundle]):
        for modify_bundle in modify_bundle_list:
            self.__managed_schedule_table.modify_bundle_table(modify_bundle=modify_bundle)
        return




    def try_remove_schedule(self, sid:str):
        self.__managed_schedule_table.remove_schedule_in_table(sid=sid)
        return

    def try_remove_schedule_list(self, sids:list[str]):
        for sid in sids:
            self.__managed_schedule_table.remove_schedule_in_table(sid=sid)

    def try_remove_bundle(self, sbid:str=''):
        self.__managed_schedule_table.remove_bundle_in_table(sbid=sbid)

    def try_remove_bundle_list(self, sbids:list[str]=[]):
        for sbid in sbids:
            self.__managed_schedule_table.remove_bundle_in_table(sbid=sbid)


    def try_filtering_schedule_in_progress(self, when:str, sids:list=[]):
        sid_list = self.__managed_schedule_table.filtering_schedule_is_in_progress(selected_sids=sids,
                                                                                   when=when)
        return sid_list

    def try_get_weekday_schedules(self, sids:list=[]):
        sid_list = self.__managed_schedule_table.

    def try_filtering_bundle_in_progress(self, when:str, sbids:list=[]):
        sbid_list = self.__managed_schedule_table.filtering_bundle_is_in_progress(selected_sbids=sbids,
                                                                                  when=when)
        return sbid_list




    def try_search_schedule_w_keyword(self, target_keyword=""):
        sid_list = self.__managed_schedule_table.search_schedule_with_key(key=target_keyword)
        return sid_list

    def try_search_bundle_w_keyword(self, target_keyword=""):
        sbid_list = self.__managed_schedule_table.search_bundle_with_key(key=target_keyword)
        return sbid_list

    def try_search_my_selected_schedules(self, sids:list, bid=""):
        sid_list = self.__managed_schedule_table.search_my_selected_schedules(bid=bid, selected_sids=sids)
        return sid_list

    def try_search_my_selected_bundles(self, sbids:list, bid=""):
        sbid_list = self.__managed_schedule_table.search_my_selected_bundles(bid=bid, selected_sbids=sbids)
        return sbid_list

