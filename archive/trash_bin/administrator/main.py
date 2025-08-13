from banner.banner_add import *
from banner.banner_find import *
from banner.banner_modify import *
from bias import *
from bias.bias_add import *
from bias.bias_find import *
from bias.bias_modify import *
from feed.feed_add import *
from feed.feed_find import *
from feed.feed_modify import *
from league.league_add import *
from league.league_find import *
from league.league_modify import *
from namecard.namecard_add import *
from namecard.namecard_find import *
from namecard.namecard_modify import *
from user.user_add import *
from user.user_find import *
from user.user_modify import *


if __name__ == '__main__':
    while True:
        select_action = input('(0)exit / (1)Data Control / (2)Bucket Control \nEnter: ')
        if select_action == '0':
            break
        elif select_action == '1': #)데이터 확인 추가 수정 삭제
            while True:
                print('(0)exit / (1)User / (2)Namecard / (3)League / (4)Feed / (5)Bias / (6)Banner')
                select_module = input('입력: ')

                if select_module == '1': # User
                    print('User')
                    print('(0)exit / (1)추가 / (2) 특정 유저 정보 가져오기 / (3)수정 / (4)삭제 ')
                    select_fun = input('입력: ')
                    if select_fun == '1': # Add
                        client = UserAdd()
                        if not client.set_data():
                            continue
                        if not client._check_data(client.get_data()):
                            continue 
                        client._request(client.get_data(),endpoint='/user_add')

                    elif select_fun == '2': # Load
                        client = UserFindEmail()
                        client.set_data()
                        client._request(client.get_data(),endpoint='/user_load')

                    elif select_fun == '3': # Modify
                        client = UserModify()
                        if not client.set_data(): #먼저 서버에서 기존의 데이터를 받아오고 그걸 바탕을 수정하도록 해야함
                            continue
                        if not client._check_data(client.get_data()):
                            continue 
                        client._request(client.get_data(),endpoint='/user_modify')

                    elif select_fun == '4': # Delete
                        client = UserFindUid()
                        client.set_data()
                        client._request(client.get_data(),endpoint='/user_delete')    

                    elif select_module == '0':
                        break

                    else:
                        print('Try Again')
                        continue
                    
                elif select_module == '2': # Namecard
                    print('NameCard')
                    print('(0)exit / (1)추가 / (2) 특정 정보 가져오기 / (3)수정 / (4)삭제 ')
                    select_fun = input('입력: ')
                    if select_fun == '1': # Add
                        client = NamecardAdd()
                        if not client.set_data():
                            continue
                        if not client._check_data(client.get_data()):
                            continue 
                        client._request(client.get_data(),endpoint='/namecard_add')

                    elif select_fun == '2': # Load
                        client = NamecardFind()
                        client.set_data()
                        client._request(client.get_data(),endpoint='/namecard_load')

                    elif select_fun == '3': # Modify
                        client = NameCardModify()
                        if not client.set_data():
                            continue
                        if not client._check_data(client.get_data()):
                            continue 
                        client._request(client.get_data(),endpoint='/namecard_modify')

                    elif select_fun == '4': # Delete
                        client = NamecardFind()
                        client.set_data()
                        client._request(client.get_data(),endpoint='/namecard_delete')

                    elif select_module == '0':
                        break

                    else:
                        print('Try Again')
                        continue

                elif select_module == '3': # League
                    print('League')
                    print('(0)exit / (1)추가 / (2) 특정 정보 가져오기 / (3)수정 / (4)삭제 ')
                    select_fun = input('입력: ')
                    if select_fun == '1': # Add
                        client = LeagueAdd()
                        if not client.set_data():
                            continue
                        if not client._check_data(client.get_data()):
                            continue 
                        client._request(client.get_data(),endpoint='/league_add')

                    elif select_fun == '2': # Load
                        client = LeagueFind()
                        client.set_data()
                        client._request(client.get_data(),endpoint='/league_load')

                    elif select_fun == '3': # Modify
                        client = LeagueModify()
                        if not client.set_data():
                            continue
                        if not client._check_data(client.get_data()):
                            continue 
                        client._request(client.get_data(),endpoint='/league_modify')

                    elif select_fun == '4': # Delete
                        client = LeagueFind()
                        client.set_data()
                        client._request(client.get_data(),endpoint='/league_delete')

                    elif select_module == '0':
                        break

                    else:
                        print('Try Again')
                        continue

                elif select_module == '4': # Feed)
                    print('Feed')
                    print('(0)exit / (1)추가 / (2) 특정 정보 가져오기 / (3)수정 / (4)삭제 ')
                    select_fun = input('입력: ')
                    if select_fun == '1': # Add
                        client = FeedAdd()
                        if not client.set_data():
                            continue
                        if not client._check_data(client.get_data()):
                            continue 
                        client._request(client.get_data(),endpoint='/feed_add')

                    elif select_fun == '2': # Load
                        client = FeedFind()
                        client.set_data()
                        client._request(client.get_data(),endpoint='/feed_load')

                    elif select_fun == '3': # Modify
                        client = FeedModify()
                        if not client.set_data():
                            continue
                        if not client._check_data(client.get_data()):
                            continue 
                        client._request(client.get_data(),endpoint='/feed_modify')

                    elif select_fun == '4': # Delete
                        client = FeedFind()
                        client.set_data()
                        client._request(client.get_data(),endpoint='/feed_delete')

                    elif select_module == '0':
                        break

                    else:
                        print('Try Again')
                        continue

                elif select_module == '5': # Bias
                    print('Bias')
                    print('(0)exit / (1)추가 / (2) 특정 정보 가져오기 / (3)수정 / (4)삭제 ')
                    select_fun = input('입력: ')
                    if select_fun == '1': # Add
                        client = BiasAdd()
                        if not client.set_data():
                            continue
                        if not client._check_data(client.get_data()):
                            continue 
                        client._request(client.get_data(),endpoint='/bias_add')

                    elif select_fun == '2': # Load
                        client = BiasFind()
                        client.set_data()
                        client._request(client.get_data(),endpoint='/bias_load')

                    elif select_fun == '3': # Modify
                        client = BiasModify()
                        client.set_data()
                        client._request(client.get_data(),endpoint='/bias_modify')

                    elif select_fun == '4': # Delete
                        client = BiasFind()
                        client.set_data()
                        client._request(client.get_data(),endpoint='/bias_delete')
                        
                    elif select_module == '0':
                        break

                    else:
                        print('Try Again')
                        continue

                elif select_module == '6': # Banner
                    print('Banner')
                    print('(0)exit / (1)추가 / (2) 특정 정보 가져오기 / (3)수정 / (4)삭제 ')
                    select_fun = input('입력: ')
                    if select_fun == '1': # Add
                        client = BannerAdd()
                        if not client.set_data():
                            continue
                        if not client._check_data(client.get_data()):
                            continue 
                        client._request(client.get_data(),endpoint='/banner_add')

                    elif select_fun == '2': # Load
                        client = BannerFind()
                        client.set_data()
                        client._request(client.get_data(),endpoint='/banner_load')

                    elif select_fun == '3': # Modify
                        client = BannerModify()
                        client.set_data()
                        client._request(client.get_data(),endpoint='/banner_modify')

                    elif select_fun == '4': # Delete
                        client = BannerFind()
                        client.set_data()
                        client._request(client.get_data(),endpoint='/banner_delete')
                    
                    elif select_module == '0':
                        break

                    else:
                        print('Try Again')
                        continue

                elif select_module == '0':
                    break

                else:
                    print('Try Again')
                    continue

        elif select_action == '2': #Bucket 
            client = Admin()
            data = None
            while True:
                select_act = input('(0)exit / (1)Reset Point \nEnter: ')
                if select_act == '0':
                    break
                elif select_act == '1':
                    select = input('진행하시겠습니까? (y/n)\nEnter:')
                    if select == 'y' : client._request(data,endpoint='/reset_league_point')
                    else: continue
                elif select_act == '2':
                    select = input('진행하시겠습니까? (y/n)\nEnter:')
                    if select == 'y' : client._request(data,endpoint='/reset_daily')
                    else: continue
                else:
                    print('Try Again')
                    continue
        else:
            print('Try Again')
            continue