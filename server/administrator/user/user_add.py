from data.admin import *
from data.data_domain import User
from data.data_domain import Item

class UserAdd(Admin):
    def __init__(self):
        super().__init__()
        self.__user = User()
    
    def set_data(self):
        items = Item()
        name_card_list = []
        try:
            #self.__user.uid = '' #uid는 서버에서 설정
            self.__user.uname = input('uname: ')
            self.__user.age = int(input('age: '))
            self.__user.email = input('email: ')
            self.__user.password = input('password: ')
            self.__user.gender = input('gender: ')
            self.__user.solo_point = int(input('solo_point: '))
            self.__user.group_point = int(input('group_point: '))
            self.__user.solo_combo = int(input('solo_combo: '))
            self.__user.group_combo = int(input('group_combo: '))
            self.__user.credit = int(input('credit: '))
            self.__user.solo_bid = input('solo_bid: ')
            self.__user.group_bid = input('group_bid: ')
            items.chatting = input('chatting: ')
            items.saver = input('saver: ')
            self.__user.items = items
            self.__user.solo_daily = input('solo_daily: ')
            self.__user.solo_special = input('solo_special: ')
            self.__user.group_daily = input('group_daily: ')
            self.__user.group_special = input('group_special: ')
            self.__user.sign = input('sign: ')
            self.__user.select_name_card = input('select_name_card: ')

            print('----Set Name Card List----')
            print('입력 완료 후 exit 입력')
            while True:
                name_card = input('name_card : ')
                name_card_list.append(name_card)
                if name_card == 'exit':
                    break
            self.__user.name_card_list = name_card_list

            return True
        except:
            print('Wrong data')
            return False
    
    def get_data(self):
        return self.__user.get_dict_form_data()