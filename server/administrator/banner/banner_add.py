from data.admin import *
from data.data_domain import Banner

class BannerAdd(Admin):
    def __init__(self):
        super().__init__()
        self.__banner = Banner()

    def set_data(self):
        try:
            #self.__banner.baid = '' #baid 서버에서 설정
            self.__banner.ba_url = input('ba_url: ')

            return True
        except:
            print('Wrong data')
            return False
    
    def get_data(self):
        return self.__banner.get_dict_form_data()