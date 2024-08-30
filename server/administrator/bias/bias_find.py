from data.admin import *

class BiasFind(Admin):
    def __init__(self):
        super().__init__()
        self.__bid = ''
    
    def set_data(self):
        self.__bid = input('Bid: ')

    def get_data(self):
        return self.__bid