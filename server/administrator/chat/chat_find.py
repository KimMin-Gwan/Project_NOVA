from data.admin import *

class ChatFind(Admin):
    def __init__(self):
        super().__init__()
        self.__cid = ''
    
    def set_data(self):
        self.__cid = input('Cid: ')

    def get_data(self):
        return self.__cid