from data.admin import *

class LeagueFind(Admin):
    def __init__(self):
        super().__init__()
        self.__lid = ''
    
    def set_data(self):
        self.__lid = input('Lid: ')
    
    def get_data(self):
        return self.__lid