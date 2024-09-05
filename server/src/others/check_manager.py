from others.data_domain import User, Bias, League
from datetime import datetime, timedelta
from others.league_manager import LeagueManager as LM


class CheckManager:
    def __init__(self):
        pass

    # 매일 매일 정각(12시)에 인증 초기화
    def reset_user_check(self, users:list):
        for user in users:
            user.group_daily_check_date = ""
            user.group_daily = False
            user.group_special = False
            user.solo_daily_check_date = ""
            user.solo_daily = False
            user.solo_special = False

    # 일일 최애 인증 시도
    def try_daily_check(self, user:User, bias:Bias, league_manager:LM):
        point = self._daily_check_update_user(user, bias_type=bias.type)
        bias.point += point  # 바이어스 포인트 업
        league_manager.try_update_league(bias=bias)
        return

    # 스페셜 최애 인증 시도
    def try_special_check(self, user:User, bias:Bias, league_manager:LM):
        point = self._special_check_update_user(user, bias_type=bias.type)
        bias.point += point  # 바이어스 포인트 업
        league_manager.try_update_league(bias=bias)
        return

    # 콤보 수를 올리기 위해 시간 채크하는 함수
    def _time_checker(self, last_check_date:str ) -> bool:
        if last_check_date == "":
            return True
        date_object = datetime.strptime(last_check_date, "%Y/%m/%d").date()
        today = datetime.today().date()
        difference = today - date_object
        if difference == timedelta(days=1):
            return True
        else:
            return False

    # 인증 날짜 최신화
    def _update_last_check_date(self):
        today = datetime.today()
        formmatted_date = today.strftime("%Y/%m/%d")
        return formmatted_date


    # 일일 최애 인증 시도에서 유저 데이터 변경
    def _daily_check_update_user(self, user:User, bias_type:str):
        result_point = 60
        if bias_type == "solo":
            result_point = result_point + (user.solo_combo * 10)
            user.solo_point += result_point # 포인트 업

            if self._time_checker(user.solo_daily_check_date):
                if user.solo_combo < 4:  # 4 보다 적으면 콤보 수 올려주기
                    user.solo_combo += 1
            else:
                user.solo_combo = 0
            user.solo_daily_check_date = self._update_last_check_date() # 날짜 업데이트
            user.solo_daily = True  # 데일리 체크 완료

        elif bias_type == "group":
            result_point = result_point + (user.group_combo * 10)
            user.group_point += result_point

            if self._time_checker(user.group_daily_check_date):
                if user.group_combo < 4:  # 4 보다 적으면 콤보 수 올려주기
                    user.group_combo += 1  # 포인트 업
            else:
                user.group_combo = 0

            user.group_daily_check_date = self._update_last_check_date() # 날짜 업데이트
            user.group_daily = True  # 데일리 체크 완료
        else:
            print("type error")
        return result_point

    # 특별시 최애 인증 시도에서 유저 데이터 변경
    def _special_check_update_user(self, user:User, bias_type:str):
        result_point = 20
        if bias_type == "solo":
            user.solo_point += result_point
            user.solo_special = True  # 데일리 체크 완료

        elif bias_type == "group":
            user.group_point += result_point
            user.group_special = True  # 데일리 체크 완료
        else:
            print("type error")

        return result_point

    ## 랭크 재정렬 함수
    #def _sort_rank(self, league:League, bias_list:list):
        #sorted_bias_list=sorted(bias_list, key=lambda x:x.point, reverse=False)

        #bid_list = []

        #for bias in sorted_bias_list:
            #bid_list.append(bias.bid)

        #league.bid_list = bid_list
        #return

    # 이미 체크 했는지 확인해야됨
    def is_already_check(self, user:User, bias:Bias) -> bool:
        if bias.type == "solo":
            if user.solo_daily:
                return False
        elif bias.type == "group":
            if user.group_daily:
                return False
        else: 
            return False
        return True


    # 이미 스페셜 체크 했는지 확인해야됨
    def is_already_special_check(self, user:User, bias:Bias) -> bool:
        if bias.type == "solo":
            if user.solo_special:
                return False
        elif bias.type == "group":
            if user.group_special:
                return False
        else: 
            return False
        return True
