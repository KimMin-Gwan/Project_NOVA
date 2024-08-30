from data.admin import *

class UserFindEmail(Admin):
    def __init__(self):
        super().__init__()
        self.__email = ''
    
    def set_data(self):
        self.__email = input('Email: ')
    
    def get_data(self):
        return self.__email

class UserFindUid(Admin):
    def __init__(self):
        super().__init__()
        self.__uid = ''
    
    def set_data(self):
        self.__uid = input('UID: ')
    
    def get_data(self):
        return self.__uid