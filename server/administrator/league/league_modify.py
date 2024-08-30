from data.admin import *
from data.data_domain import League

class LeagueModify(Admin):
    def __init__(self):
        super().__init__()
        self.__league = League()

    def set_data(self):
        self.__league.lid = input('Target Lid: ')
        bid_list = []
        tiers = []
        try:
            while True:
                select = input('(0)exit / (1)lname / (2)bid_list / (3)tier / (4)num_bias / (5)state / (6)type \nselect: ')
                if select == '1' :
                    self.__league.lname = input('lname: ')
                elif select == '2':
                    print('----Set Bid List----')
                    print('입력 완료 후 0 입력')
                    while True:
                        bid = input('bid : ')
                        bid_list.append(bid)
                        if bid == '0':
                            break
                    self.__league.bid_list = bid_list

                elif select == '3':
                    print('----Set Tier----')
                    print('입력 완료 후 0 입력')
                    while True:
                        tier = input('tier : ')
                        tiers.append(bid)
                        if tier == '0':
                            break
                    self.__league.tier = tiers

                elif select == '4':
                    self.__league.num_bias = int(input('num_bias: '))
                elif select == '5':
                    self.__league.state = input('state: ')
                elif select == '6':
                    self.__league.type =input('type: ')

                elif select == '0':
                    break
                else:
                    print('Try Again')
                    continue

            return True
        except:
            print('Wrong data')
            return False
    def get_data(self):
        return self.__league.get_dict_form_data()