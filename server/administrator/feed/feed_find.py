from data.admin import *

class FeedFind(Admin):
    def __init__(self):
        super().__init__()
        self.__fid = ''
    
    def set_data(self):
        self.__fid = input('Fid: ')

    def get_data(self):
        return self.__fid