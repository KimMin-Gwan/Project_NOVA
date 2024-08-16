from model.base_model import BaseModel
from model import Local_Database
from others.data_domain import Chatting
from others import CoreControllerLogicError

class ChatListModel(BaseModel):
    def __init__(self, database:Local_Database) -> None:
        super().__init__(database)
        self.__chattings = [] 

    def set_chat_list(self) -> bool:
            try:     
                chat_list= self._database.get_all_data(target='cid')

                for chat in chat_list:
                    chatting = Chatting()
                    chatting.make_with_dict(dict_data=chat)
                    self.__chattings.append(chatting)


                return True
            except Exception as e:
                raise CoreControllerLogicError(error_type="set_chat_list | " + str(e))
            
    def get_response_form_data(self, head_parser):
        try:
            body = {
                'chatting_list' : self.__chattings
            }

            response = self._get_response_data(head_parser=head_parser, body=body)
            return response

        except Exception as e:
            raise CoreControllerLogicError("response making error | " + e)