from data.admin import *
from data.data_domain import Chatting

class ChatAdd(Admin):
    def __init__(self):
        super().__init__()
        self.__chat = Chatting()
    
    def set_data(self):
        try:
            #self.__chat.cid = '' #cid는 서버에서 설정
            self.__chat.content = input('content: ')
            self.__chat.date = input('date: ')


            return True
        except:
            print('Wrong data')
            return False
    
    def get_data(self):
        return self.__chat.get_dict_form_data()
    

