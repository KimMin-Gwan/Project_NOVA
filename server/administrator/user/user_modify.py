from data.admin import *

from data.data_domain import User
from data.data_domain import Item


class UserModify(Admin):
    def __init__(self):
        super().__init__()
        self.__user = User()
    
    def set_data(self):
        self.__user.uid = input('데이터 수정 대상 Uid: ')
        #items = Item()
        name_card_list = []
        try:
            while True:
                print('(0)exit / (1)uname / (2)age / (3)email / (4)password / \n(5)gender / (6)solo_point / (7)group_point / (8)solo_combo / (9)group_combo / \n(10)credit / (11)bids / (13)items / (14)solo_daily / \n(15)solo_special / (16)group_daily / (17)group_special / (18)sign / (19)select_name_card / \n(20)name_card_list')
                select = input('입력: ')
                if select == '1' :
                    self.__user.uname = input('uname: ')
                elif select == '2' :
                    self.__user.age = int(input('age: '))
                elif select == '3' :
                    self.__user.email = input('email: ')
                elif select == '4' :
                    self.__user.password = input('password: ')
                elif select == '5' :
                    self.__user.gender = input('gender: ')
                elif select == '6' :
                    self.__user.solo_point = int(input('solo_point: '))
                elif select == '7' :
                    self.__user.group_point = int(input('group_point: '))
                elif select == '8' :
                    self.__user.solo_combo = int(input('solo_combo: '))
                elif select == '9' :
                    self.__user.group_combo = int(input('group_combo: '))
                elif select == '10' :
                    self.__user.credit = int(input('credit: '))
                elif select == '11' :
                    self.__user.bids = input('bids: ')
                elif select == '13' :
                    self.__user.items.chatting = input('chatting: ')
                    self.__user.items.saver = input('saver: ')
                    #self.__user.items = items
                elif select == '14' :
                    self.__user.solo_daily = bool(input('solo_daily(Enter: False): '))
                elif select == '15' :
                    self.__user.solo_special = bool(input('solo_special(Enter: False): '))
                elif select == '16' :
                    self.__user.group_daily = bool(input('group_daily(Enter: False): '))
                elif select == '17' :
                    self.__user.group_special = bool(input('group_special(Enter: False): '))
                elif select == '18' :
                    self.__user.sign = input('sign: ')
                elif select == '19' :
                    self.__user.select_name_card = input('select_name_card: ')
                elif select == '20' :
                    print('----Set Name Card List----')
                    print('입력 완료 후 exit 입력')
                    while True:
                        name_card = input('name_card : ')
                        if name_card == '':
                            break
                        if name_card == 'exit':
                            break
                        name_card_list.append(name_card)
                        
                    self.__user.name_card_list = name_card_list
                    
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
        return self.__user.get_dict_form_data()