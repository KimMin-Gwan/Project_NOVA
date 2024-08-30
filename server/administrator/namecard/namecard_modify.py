from data.admin import *
from data.data_domain import NameCard


class NameCardModify(Admin):
    def __init__(self):
        super().__init__()
        self.__namecard = NameCard()
    
    def set_data(self):
        self.__namecard.ncid = input('Target NCid: ')
        try:
            while True:
                select = input('(0)exit / (1)ncname / (2)nccredit \nselect: ')
                if select == '1' :
                    self.__namecard.ncname = input('ncname: ')
                elif select == '2':
                    self.__namecard.nccredit = int(input('nccredit: '))

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
        return self.__namecard.get_dict_form_data()