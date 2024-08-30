from data.admin import *
from data.data_domain import Bias

class BiasAdd(Admin):
    def __init__(self):
        super().__init__()
        self.__bias = Bias()

    def set_data(self):
        category_list = []
        group_list = []
        country_list = []
        nickname_list = []
        fanname_list = []
        group_memeber_bids = []
        try:
            #self.__bias.bid = '' #bid 서버에서 설정
            self.__bias.type = input('type: ')
            self.__bias.bname = input('bname: ')

            print('----Set Category List----')
            print('입력 완료 후 0 입력')
            while True:
                category = input('category : ')
                if category == '0':
                    break
                category_list.append(category)
                
            self.__bias.category = category_list

            self.__bias.birthday = input('birthday: ')
            self.__bias.debut = input('debut: ')
            self.__bias.agency = input('agency: ')

            print('----Set Group List----')
            print('입력 완료 후 0 입력')
            while True:
                group = input('bid : ')
                if group == '0':
                    break
                group_list.append(group)
                
            self.__bias.group = group_list

            self.__bias.lid = input('lid: ')
            self.__bias.point = int(input('point: '))
            self.__bias.num_user = int(input('num_user: '))
            self.__bias.x_account = input('x_account: ')
            self.__bias.insta_account = input('insta_account: ')
            self.__bias.tiktok_account = input('tiktok_account: ')
            self.__bias.youtube_account = input('youtube_account: ')
            self.__bias.homepage = input('homepage: ')
            self.__bias.fan_cafe = input('fan_cafe: ')

            print('----Set Country List----')
            print('입력 완료 후 0 입력')
            while True:
                country = input('country : ')
                if country == '0':
                    break
                country_list.append(country)
                
            self.__bias.country = input('country: ')

            print('----Set Nickname List----')
            print('입력 완료 후 0 입력')
            while True:
                nickname = input('nickname : ')
                if nickname == '0':
                    break
                nickname_list.append(nickname)
                
            self.__bias.nickname = input('nickname: ')

            print('----Set Fanname List----')
            print('입력 완료 후 0 입력')
            while True:
                fanname = input('fanname : ')
                if fanname == '0':
                    break
                fanname_list.append(fanname)
                
            self.__bias.fanname = input('fanname: ')

            print('----Set Group Memeber Bids----')
            print('입력 완료 후 0 입력')
            while True:
                group_memeber_bid = input('group_memeber_bid : ')
                if group == '0':
                    break
                group_memeber_bids.append(group_memeber_bid)
                
            self.__bias.group_memeber_bids = group_memeber_bids

            return True
        except:
            print('Wrong data')
            return False
        
    def get_data(self):
        return self.__bias.get_dict_form_data()