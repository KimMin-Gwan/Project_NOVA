from data.admin import *
from data.data_domain import NameCard

class NamecardAdd(Admin):
    def __init__(self):
        super().__init__()
        self.__namecard = NameCard()
    
    def set_data(self):
        try:
            #self.__user.ncid = '' #ncid는 서버에서 설정
            self.__namecard.ncname = input('ncname: ')
            self.__namecard.nccredit = int(input('nccredit: ') or '0')


            return True
        except:
            print('Wrong data')
            return False
    
    def get_data(self):
        return self.__namecard.get_dict_form_data()
