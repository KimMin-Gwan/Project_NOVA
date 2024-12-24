from data.admin import *
from data.data_domain import User
from data.data_domain import Item

class UserAdd(Admin):
    def __init__(self):
        super().__init__()
        self.__user = User()
    
    def set_data(self):
        #items = Item()
        name_card_list = []
        try:
            #self.__user.uid = '' #uid는 서버에서 설정
            print('*필수 입력')
            print('데이터를 추가 할 필요가 없으면 엔터')
            self.__user.uname = input('*uname: ')
            self.__user.age = int(input('*age: '))
            self.__user.email = input('*email: ')
            self.__user.password = input('*password: ')
            self.__user.gender = input('*gender(m/f): ')

            
            self.__user.solo_point = int(input('solo_point: ') or '0')
            self.__user.group_point = int(input('group_point: ') or '0')
            self.__user.solo_combo = int(input('solo_combo: ') or '0')
            self.__user.group_combo = int(input('group_combo: ') or '0')
            self.__user.credit = int(input('credit: ') or '0')

            self.__user.bids = input('bids: ')

            #아이템 설정
            self.__user.items.chatting = int(input('chatting: ') or '0')
            self.__user.items.saver = int(input('saver: ') or '0')
            #self.__user.items = items

            #일일 출석체크인데 이걸 생성때 추가 할 이유가 있을까?
            # self.__user.solo_daily = input('solo_daily: ') or False
            # self.__user.solo_special = input('solo_special: ') or False
            # self.__user.group_daily = input('group_daily: ') or False
            # self.__user.group_special = input('group_special: ') or False

            self.__user.sign = input('sign: ')
            self.__user.select_name_card = input('select_name_card: ')

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

            return True
        except:
            print('Wrong data')
            return False
    
    def get_data(self):
        return self.__user.get_dict_form_data()