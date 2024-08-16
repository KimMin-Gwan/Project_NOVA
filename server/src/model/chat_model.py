# from model.base_model import BaseModel
# from model import Local_Database
# from others.data_domain import  Chatting
# from others import CoreControllerLogicError
# import json

# class ChatModel(BaseModel):
#     def __init__(self, database:Local_Database) -> None:
#         super().__init__(database)
#         self.__chat = Chatting()

#     def set_chat_data(self,request) -> bool: 
#         try:
            
#             self.__chat.make_with_dict(request)

#             return True
        
#         except Exception as e:
#             raise CoreControllerLogicError(error_type="set_group_leagues | " + str(e))
        
#     def save_chat(self,request):
#         self._database.add_new_data(target_id='cid',new_data={
#             "cid" : self.__chat.cid,
#             "uid" : self.__chat.uid,
#             "content" : self.__chat.content,
#             "date" : self.__chat.date
#         })

#     def load_chat(self):
#         self.__saved_chat_data = self._database.get_all_data(target='cid')
