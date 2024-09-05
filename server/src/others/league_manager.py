from others.data_domain import League, Bias
from others.socket_manager import ConnectionManager
#from model import Local_Database
import sys
import time


# 해야하는 일
# 1. 생성된 리그를 모두 가지고 메모리에 올리기
# 2. 리그 데이터 무결성 유지
# 3. 리그 데이터 변경에 따른 사용자의 전송 플래그 조정(여기서 하는게 아닐지도 모름)
# -> 여기 데이터들은 데이터 베이스에 저장하지 않음 (가공이 끝난 데이터를 저장하고 이곳에 무결성 시킬것)

class LeagueManager:
    def __init__(self, connection_manager:ConnectionManager):
        self.__managed_leagues = []
        self.__connection_manager = connection_manager

    def init_league_manager(self, database):
        league_datas = []
        league_datas = database.get_all_data(target="lid")

        for league_data in league_datas:
            managed_league = ManagedLeague()
            managed_league.make_with_dict(dict_data=league_data)
            bias_datas = database.get_datas_with_ids(target_id="bid", ids=managed_league.bid_list)
            bias_list = []
            for bias_data in bias_datas:
                bias = Bias()
                bias.make_with_dict(bias_data)
                bias_list.append(bias)
            managed_league.init_league_data(bias_list=bias_list)
            self.__managed_leagues.append(managed_league)

        print(f'INFO<-[      {len(self.__managed_leagues)} NOVA LEAGUE NOW READY.')
        return
    
    # 인증을 통해 포인트가 바뀌는 현상을 표시 -> bias 데이터를 받아와서 처리
    # 처리가 끝나고 나면 해당 리그를 관측중인 소켓 유저들에게 전송 플레그를 올려야함
    def try_update_league(self, bias:Bias):
        target_league = ManagedLeague()
        # 목표 리그 검색
        for league in self.__managed_leagues:
            if league.lid == bias.lid:
                target_league = league
                break

        target_league.update_point_n_rank(bias=bias)
        self.__connection_manager.targeting_broadcast(
            target=target_league.lname,
            message=target_league.get_league_data_ws_form())
        return

    # 리그 일반 정보 제공(일반 요청 처리 용 )
    def get_league_data(self, lid):
        target_league = ManagedLeague()
        for league in self.__managed_leagues:
            if league.lid == lid:
                target_league = league
                break
        
        result = target_league.get_league_data_json_form()
        return result

    # 리그 일반 정보 제공(일반 요청 처리 용 )
    def get_league_data(self, lid):
        target_league = ManagedLeague()
        for league in self.__managed_leagues:
            if league.lid == lid:
                target_league = league
                break
        
        result = target_league.get_league_data_json_form()
        return result

    # 리그의 메타 정보 제공(웹 소켓용)
    def get_ws_meta_league_data(self, league_name):
        target_league = ManagedLeague()
        # 목표를 검색 (이름으로 )
        for league in self.__managed_leagues:
            if league.lname == league_name:
                target_league = league
                break

        return target_league.get_meta_data_ws_form()

    # 리그의 일반 정보 제공(웹 소켓용)
    def get_ws_league_data(self, league_name):
        target_league = ManagedLeague()
        # 목표를 검색 (이름으로 )
        for league in self.__managed_leagues:
            if league.lname == league_name:
                target_league = league
                break
        
        return target_league.get_league_data_ws_form()

# 리그 데이터 특징
class ManagedLeague(League):
    def __init__(self):
        self.__bias_list = []
        self.__mutex = False

    # 동시사용 금지를 위한 체크
    def __waiting(self):
        while True:
            if self.__mutex:
                time.sleep(0.001) # 누가 사용중이면 0.001초 후에 재시도
            else:
                break
        return

    # 포인트와 랭크 업데이트 
    def update_point_n_rank(self, bias:Bias):
        self.__waiting()
        self.__mutex = True

        for managed_bias in self.__bias_list:
            if managed_bias.bid == bias.bid:
                managed_bias.make_with_dict(bias.get_dict_form_data())
        self.__sort_league()
        self.__mutex = False
        return True

    # 리그 내부를 재정렬
    def __sort_league(self):
        self.__bias_list = sorted(self.__bias_list, key=lambda x:x.point, reverse=True)
        priv_point = sys.maxsize
        now_rank = 0
        set_rank = 0
        for bias in self.__bias_list:
            bias:ManagedBias = bias
            now_point = bias.point
            if now_point < priv_point:
                now_rank = now_rank + set_rank + 1
                set_rank = 0
                priv_point = now_point
            elif now_point == priv_point:
                set_rank += 1
            else:
                print("data align set badly")
                return False
            bias.rank = now_rank
        return True

    # 초기 데이터를 이용해서 관리 가능한 형태의 bais 리스트를 만들고 보관한다
    def init_league_data(self, bias_list):
        for bias in bias_list:
            m_bias = ManagedBias(rank = 1)
            m_bias.make_with_dict(bias.get_dict_form_data())
            self.__bias_list.append(m_bias)

    # 리그 메타 정보 접근자 (웹소켓용)
    # lid.lname.num_bias.min.max
    # 데이터의 끝은 /로 표시
    def get_meta_data_ws_form(self):
        return f'{self.lid}.{self.lname}.{str(self.num_bias)}.{str(self.tier[0])}.{str(self.tier[1])}/'

    # 리그 정보 접근자(웹소켓용)
    # rank.bid.bname.point 
    # 데이터 간격은 뛰어쓰기로 표시
    # 데이터의 끝은 /로 표시
    def get_league_data_ws_form(self):
        send_data = ""

        for bias in self.__bias_list:
            bias:ManagedBias = bias
            send_data += f'{bias.rank}.{bias.bid}.{bias.bname}.{bias.point} '
        
        send_data += "/"
        return send_data

    def get_meta_data_json_form(self):
        return self.get_dict_form_data()

    def get_league_data_json_form(self):
        result = []

        for bias in self.__bias_list:
            dict_form_data = bias.get_dict_form_data()
            dict_form_data['rank'] = bias.rank
            result.append(dict_form_data)
        
        return result


# 관리 가능함 Bias 를 만든다
class ManagedBias(Bias):
    def __init__(self, rank = 0):
        self.rank = rank

    def __call__(self):
        print(f"bid: {self.bid}")
        print(f"type: {self.type}")
        print(f"bname: {self.bname}")
        print(f"category: {', '.join(self.category)}")
        print(f"birthday: {self.birthday}")
        print(f"debut: {self.debut}")
        print(f"agency: {self.agency}")
        print(f"group: {', '.join(self.group)}")
        print(f"lid: {self.lid}")
        print(f"point: {self.point}")
        print(f"num_user: {self.num_user}")
        print(f"x_account: {self.x_account}")
        print(f"insta_account: {self.insta_account}")
        print(f"tiktok_account: {self.tiktok_account}")
        print(f"youtube_account: {self.youtube_account}")
        print(f"homepage: {self.homepage}")
        print(f"fan_cafe: {self.fan_cafe}")
        print(f"country: {', '.join(self.country)}")
        print(f"nickname: {', '.join(self.nickname)}")
        print(f"fanname: {', '.join(self.fanname)}")
        print(f"group_member_bids: {', '.join(self.group_member_bids)}")



