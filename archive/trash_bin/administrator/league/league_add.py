from data.admin import *
from data.data_domain import League

class LeagueAdd(Admin):
    def __init__(self):
        super().__init__()
        self.__league = League()

    def set_data(self):
        bid_list = []
        tiers = []
        try:
            #self.__league.lid = '' #lid는 서버에서 설정
            self.__league.lname = input('lname: ')

            print('----Set Bid List----')
            print('입력 완료 후 0 입력')
            while True:
                bid = input('bid : ')
                if bid == '':
                    break
                if bid == '0':
                    break
                bid_list.append(bid)
                
            self.__league.bid_list = bid_list

            print('----Set Tier----')
            print('입력 완료 후 0 입력')
            while True:
                tier = int(input('tier : ') or 0)
                if tier == None:
                    break
                if tier == 0:
                    break
                tiers.append(tier)
                
            self.__league.tier = tiers

            self.__league.num_bias = int(input('num_bias: ') or 0)
            self.__league.state = input('state(active / inactive): ' or 'inactive')
            self.__league.type =input('type(solo / group): ' or 'solo')

            return True
        except:
            print('Wrong data')
            return False
    def get_data(self):
        return self.__league.get_dict_form_data()