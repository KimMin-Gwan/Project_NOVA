from data.admin import *
from data.data_domain import Chatting

class ChatModify(Admin):
    def __init__(self):
        super().__init__()
        self.__chat = Chatting()

    def set_data(self):
        self.__chat.cid = input('Target Cid: ')
        try:
            while True:
                select = input('(0)exit / (1)content / (2)date \nselect: ')
                if select == '1' :
                    self.__chat.content = input('content: ')
                elif select == '2':
                    self.__chat.date = input('date: ')

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
        return self.__chat.get_dict_form_data()