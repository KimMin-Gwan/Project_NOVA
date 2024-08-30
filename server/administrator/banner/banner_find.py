from data.admin import *

class BannerFind(Admin):
    def __init__(self):
        super().__init__()
        self.__baid = ''
    
    def set_data(self):
        self.__baid = input('Baid: ')
    
    def get_data(self):
        return self.__baid