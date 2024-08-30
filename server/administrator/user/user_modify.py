from data.admin import *

from data.data_domain import User
from data.data_domain import Item


class UserModify(Admin):
    def __init__(self):
        super().__init__()
        self.__user = User()
    
    def set_data(self):
        self.__user.uid = input('Target Uid: ')
        items = Item()
        name_card_list = []
        try:
            while True:
                select = input('(0)exit / (1)uname / (2)age / (3)email / (4)password / \n(5)gender / (6)solo_point / (7)group_point / (8)solo_combo / (9)group_combo / \n(10)credit / (11)solo_bid / (12)group_bid / (13)items / (14)solo_daily / \n(15)solo_special / (16)group_daily / (17)group_special / (18)sign / (19)select_name_card / \n(20)name_card_list \nselect: ')
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
                    self.__user.solo_bid = input('solo_bid: ')
                elif select == '12' :
                    self.__user.group_bid = input('group_bid: ')
                elif select == '13' :
                    items.chatting = input('chatting: ')
                    items.saver = input('saver: ')
                    self.__user.items = items
                elif select == '14' :
                    self.__user.solo_daily = input('solo_daily: ')
                elif select == '15' :
                    self.__user.solo_special = input('solo_special: ')
                elif select == '16' :
                    self.__user.group_daily = input('group_daily: ')
                elif select == '17' :
                    self.__user.group_special = input('group_special: ')
                elif select == '18' :
                    self.__user.sign = input('sign: ')
                elif select == '19' :
                    self.__user.select_name_card = input('select_name_card: ')
                elif select == '20' :
                    print('----Set Name Card List----')
                    print('입력 완료 후 0 입력')
                    while True:
                        name_card = input('name_card : ')
                        name_card_list.append(name_card)
                        if name_card == '0':
                            break
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