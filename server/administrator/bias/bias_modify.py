from data.admin import *
from data.data_domain import Bias

class BiasModify(Admin):
    def __init__(self):
        super().__init__()
        self.__bias = Bias()

    def set_data(self):
        self.__bias.bid = input('Target Bid: ')
        category_list = []
        group_list = []
        country_list = []
        nickname_list = []
        fanname_list = []
        group_memeber_bids = []
        try:
            while True:
                select = input('(0)exit / (1)type / (2)bname / (3)category / (4)birthday / \n(5)debut / (6)agency / (7)group / (8)lid / (9)point / \n(10)num_user / (11)x_account / (12)insta_account / (13)tiktok_account / (14)youtube_account / \n(15)homepage / (16)fan_cafe / (17)country / (18)nickname / (19)fanname / \n(20)group_member_bids \nselect: ')
                if select == '1' :
                    self.__bias.type = input('type: ')
                elif select == '2':
                    self.__bias.bname = input('bname: ')
                elif select == '3':
                    print('----Set Category List----')
                    print('입력 완료 후 0 입력')
                    while True:
                        category = input('category : ')
                        category_list.append(category)
                        if category == '0':
                            break
                    self.__bias.category = category_list

                elif select == '4':
                    self.__bias.birthday = input('birthday: ')
                elif select == '5':
                    self.__bias.debut = input('debut: ')
                elif select == '6':
                    self.__bias.agency = input('agency: ')
                elif select == '7':
                    print('----Set Group List----')
                    print('입력 완료 후 0 입력')
                    while True:
                        group = input('bid : ')
                        group_list.append(group)
                        if group == '0':
                            break
                    self.__bias.group = group_list

                elif select == '8':
                    self.__bias.lid = input('lid: ')
                elif select == '9':
                    self.__bias.point = int(input('point: ') or 0)
                elif select == '10':
                    self.__bias.num_user = int(input('num_user: ') or 0)
                elif select == '11':
                    self.__bias.x_account = input('x_account: ')
                elif select == '12':
                    self.__bias.insta_account = input('insta_account: ')
                elif select == '13':
                    self.__bias.tiktok_account = input('tiktok_account: ')
                elif select == '14':
                    self.__bias.youtube_account = input('youtube_account: ')
                elif select == '15':
                    self.__bias.homepage = input('homepage: ')
                elif select == '16':
                    self.__bias.fan_cafe = input('fan_cafe: ')
                elif select == '17':
                    print('----Set Country List----')
                    print('입력 완료 후 0 입력')
                    while True:
                        country = input('country : ')
                        country_list.append(country)
                        if country == '0':
                            break
                    self.__bias.country = input('country: ')

                elif select == '18':
                    print('----Set Nickname List----')
                    print('입력 완료 후 0 입력')
                    while True:
                        nickname = input('nickname : ')
                        nickname_list.append(nickname)
                        if nickname == '0':
                            break
                    self.__bias.nickname = input('nickname: ')

                elif select == '19':
                    print('----Set Fanname List----')
                    print('입력 완료 후 0 입력')
                    while True:
                        fanname = input('fanname : ')
                        fanname_list.append(fanname)
                        if fanname == '0':
                            break
                    self.__bias.fanname = input('fanname: ')

                elif select == '20':
                    print('----Set Group Memeber Bids----')
                    print('입력 완료 후 0 입력')
                    while True:
                        group_memeber_bid = input('group_memeber_bid : ')
                        group_memeber_bids.append(group_memeber_bid)
                        if group == '0':
                            break
                    self.__bias.group_memeber_bids = group_memeber_bids

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
        return self.__bias.get_dict_form_data()