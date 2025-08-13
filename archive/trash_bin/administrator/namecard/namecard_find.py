from data.admin import *

class NamecardFind(Admin):
    def __init__(self):
        super().__init__()
        self.__ncid = ''
    
    def set_data(self):
        self.__ncid = input('NCid: ')
    
    def get_data(self):
        return self.__ncid