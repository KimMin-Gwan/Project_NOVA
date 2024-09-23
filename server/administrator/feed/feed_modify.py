from data.admin import *
from data.data_domain import Feed

class FeedModify(Admin):
    def __init__(self):
        super().__init__()
        self.__feed = Feed()

    def set_data(self):
        self.__feed.fid = input('Target Fid: ')
        try:
            while True:
                choice = []
                result = []
                attend = []
                category = []
                comment = []

                select = input('(0)exit / (1)uid / (2)nickname / (3)title / (4)body / (5)date \n(6)fclass / (7)class_name / (8)choice / (9)result / (10)state \n(11)attend / (12)category comment \nselect: ')
                if select == '1' :
                    self.__feed.uid = input('uid: ' )
                elif select == '2':
                    self.__feed.nickname = input('nickname: ' )
                elif select == '3':
                    self.__feed.title = input('title: ' )
                elif select == '4':
                    self.__feed.body = input('body: ' )
                elif select == '5':
                    self.__feed.date = input('date: ' )
                elif select == '6':
                    self.__feed.fclass = input('fclass: ' )
                elif select == '7':
                    self.__feed.class_name = input('class_name: ' )
                elif select == '8':
                    print('----Set choice List----')
                    print('입력 완료 후 exit 입력')
                    while True:
                        temp = input('choice : ')
                        if temp == '':
                            break
                        if temp == 'exit':
                            break
                        choice.append(temp)
                    self.__feed.choice = choice
                elif select == '9':
                    print('----Set result List----')
                    print('입력 완료 후 exit 입력')
                    while True:
                        temp = input('result : ')
                        if temp == '':
                            break
                        if temp == 'exit':
                            break
                        result.append(temp)
                    self.__feed.result = result
                elif select == '10':
                    self.__feed.state = input('state: ' ) 
                elif select == '11':
                    print('----Set attend List----')
                    print('입력 완료 후 exit 입력')
                    while True:
                        temp = input('attend : ')
                        if temp == '':
                            break
                        if temp == 'exit':
                            break
                        attend.append(temp)
                    self.__feed.attend = attend
                elif select == '12':
                    print('----Set category List----')
                    print('입력 완료 후 exit 입력')
                    while True:
                        temp = input('category : ')
                        if temp == '':
                            break
                        if temp == 'exit':
                            break
                        category.append(temp)
                    self.__feed.category = category
                elif select == '13':
                    print('----Set comment List----')
                    print('입력 완료 후 exit 입력')
                    while True:
                        temp = input('comment : ')
                        if temp == '':
                            break
                        if temp == 'exit':
                            break
                        comment.append(temp)
                    self.__feed.comment =comment 

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
        return self.__feed.get_dict_form_data()