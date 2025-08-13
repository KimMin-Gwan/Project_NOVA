from data.admin import *
from data.data_domain import Banner


class BannerModify(Admin):
    def __init__(self):
        super().__init__()
        self.__banner = Banner()
    
    def set_data(self):
        self.__banner.baid = input('Target Baid: ')
        try:
            while True:
                select = input('(0)exit / (1)ba_url \nselect: ')
                if select == '1' :
                    self.__banner.ba_url = input('ba_url: ')

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
        return self.__banner.get_dict_form_data()