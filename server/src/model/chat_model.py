from model.base_model import BaseModel
from model import Local_Database
from others.data_domain import  Chatting, ReceivedChat
from others import CoreControllerLogicError
import datetime
import json

class ChatModel(BaseModel):
    def __init__(self, database:Local_Database) -> None:
        super().__init__(database)
        self.__received_chat = ReceivedChat()


    def set_chat_data(self,request) -> bool: 
        try:
            chat_data = json.loads(request)
            self.__received_chat.make_with_dict(chat_data)
            
            return True
        
        except Exception as e:
            raise CoreControllerLogicError(error_type="set_group_leagues | " + str(e))
    
    def check_item(self,request):
        if request.items.chatting == 0:
            return False
        else:
            self._database.modify_data_with_id(target_id='uid',target_data={
                'uid': request.uid,
                "uname": request.uname,
                "age": request.age,
                "email": request.email,
                "gender" : request.gender,
                'point':request.point + self.__point,
                'combo':self.__combo,
                "credit" : request.credit,
                "solo_bid" : request.solo_bid,
                "group_bid" : request.group_bid,
                "items" : request.items, #---
                'daily': request.daily,
                "special" : request.special                
            })

        
    def save_chat(self,request):
        currnet_date = datetime.datetime.now()
        date = currnet_date.strftime('%Y/%M/%D')
        chats = self._database.get_all_data(target='cid')

        self._database.add_new_data(target_id='cid',new_data={
            "cid" : str(len(chats) + 1),
            "uid" : request.uid,
            "content" : self.__received_chat.message,
            "date" : date
        })

    def get_chat_data(self):
        return self.__received_chat

