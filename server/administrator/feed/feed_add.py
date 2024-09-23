from data.admin import *
from data.data_domain import Feed

class FeedAdd(Admin):
    def __init__(self):
        super().__init__()
        self.__feed = Feed()
    
    def set_data(self):
        try:
            choice = []
            result = []
            attend = []
            category = []
            comment = []
            
            #self.fid = fid
            self.__feed.uid = input('uid: ' )
            self.__feed.nickname = input('nickname: ' )
            self.__feed.title = input('title: ' )
            self.__feed.body = input('body: ' )
            self.__feed.date = input('date: ' )
            self.__feed.fclass = input('fclass: ' )
            self.__feed.class_name = input('class_name: ' )

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

            self.__feed.state = input('state: ' ) 

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


            return True
        except:
            print('Wrong data')
            return False
    
    def get_data(self):
        return self.__feed.get_dict_form_data()
    

