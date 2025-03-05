from model.base_model import BaseModel
from model import Local_Database
from others.data_domain import TimeTableUser as TUser
from others.data_domain import Schedule, ScheduleBundle, ScheduleEvent

class TimeTableModel(BaseModel):
    def __init__(self, database:Local_Database) -> None:
        super().__init__(database)
        self._tuser:TUser = TUser()
        
    # 로그인이 필수인 유저이거나, 로그인을 한 유저를 처리할 때 필수적으로 사용되는 부분
    def _set_tuser_with_tuid(self, tuid="") -> bool:
        # 유저를 먼져 부르고 해야됨 반드시
        if tuid == "" :
            if self._user.uid == "":
                return False
            else:
                tuid = self._user.uid
            
        
        tuser_data = self._database.get_data_with_id(target="tuid", id=tuid)
        # 만약 tuser가 등록된 적이 없는 init 상태라면 여기서 등록도 해야됨
        if tuser_data:
            self._tuser.make_with_dict(dict_data=tuser_data)
        else:
            # tuid와 uid는 그냥 동일하게 하겠음 그래야 중복이 없음
            new_tuser = TUser(tuid=self._user.uid)
            self._database.add_new_data(target_id="tuid", new_data=new_tuser.get_dict_form_data())
            self._tuser = new_tuser
        return True
        
        
    def get_response_form_data(self, head_parser):
        body = {
            "tuser" : self._tuser,
            }

        response = self._get_response_data(head_parser=head_parser, body=body)
        return response
