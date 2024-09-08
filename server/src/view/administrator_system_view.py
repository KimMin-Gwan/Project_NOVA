from typing import Any, Optional
from fastapi import FastAPI
from view.master_view import Master_View, RequestHeader
from view.parsers import Head_Parser
from controller import Administrator_Controller

class Administrator_Service_View(Master_View):
    def __init__(self, app:FastAPI, endpoint:str, database, head_parser:Head_Parser) -> None:
        super().__init__(head_parser=head_parser)
        self.__app = app
        self._endpoint = endpoint
        self.__database = database
        self.admin_route(endpoint)

    def admin_route(self, endpoint:str):
        @self.__app.get(endpoint+'/admin')

        def home():
            return 'Hello, This is Admin System'
        
        #reset point
        @self.__app.post('/admin/reset_league_point')
        def reset_league_point(raw_request:dict):
            request = ResetDatasRequest(raw_request)
            administrator_controller=Administrator_Controller()
            model = administrator_controller.reset_leagues_point(database=self.__database,
                                                                 request=request)
            response = model.get_response_form_data(self._head_parser)
            return response
        
        @self.__app.post('/admin/reset_daily')
        def reset_daily(raw_request:dict):
            request = ResetDatasRequest(raw_request)
            administrator_controller=Administrator_Controller()
            model = administrator_controller.reset_daily(database=self.__database,
                                                                 request=request)
            response = model.get_response_form_data(self._head_parser)
            return response
        
        #User
        @self.__app.post('/admin/user_load')
        def user_load(raw_request:dict):
            request = UserLoadRequset(raw_request)
            administrator_controller=Administrator_Controller()
            model = administrator_controller.user_editor(database=self.__database,
                                                                 request=request,
                                                                 type='load')
            response = model.get_response_form_data(self._head_parser)
            return response
        
        @self.__app.post('/admin/user_add')
        def user_add(raw_request:dict):
            request = UserAddRequset(raw_request)
            administrator_controller=Administrator_Controller()
            model = administrator_controller.user_editor(database=self.__database,
                                                                 request=request,
                                                                 type='add')
            response = model.get_response_form_data(self._head_parser)
            return response
        
        @self.__app.post('/admin/user_modify')
        def user_modify(raw_request:dict):
            request = UserModifyRequset(raw_request)
            administrator_controller=Administrator_Controller()
            model = administrator_controller.user_editor(database=self.__database,
                                                                 request=request,
                                                                 type='modify')
            response = model.get_response_form_data(self._head_parser)
            return response
        
        @self.__app.post('/admin/user_delete')
        def user_delete(raw_request:dict):
            request = UserDeleteRequset(raw_request)
            administrator_controller=Administrator_Controller()
            model = administrator_controller.user_editor(database=self.__database,
                                                                 request=request,
                                                                 type='delete')
            response = model.get_response_form_data(self._head_parser)
            return response
        
        #namecard
        @self.__app.post('/admin/namecard_load')
        def namecard_load(raw_request:dict):
            request = NamecardLoadDeleteRequset(raw_request)
            administrator_controller=Administrator_Controller()
            model = administrator_controller.namecard_editor(database=self.__database,
                                                                 request=request,
                                                                 type='load')
            response = model.get_response_form_data(self._head_parser)
            return response
        
        @self.__app.post('/admin/namecard_add')
        def namecard_add(raw_request:dict):
            request = NamecardAddModifyRequset(raw_request)
            administrator_controller=Administrator_Controller()
            model = administrator_controller.namecard_editor(database=self.__database,
                                                                 request=request,
                                                                 type='add')
            response = model.get_response_form_data(self._head_parser)
            return response
        
        @self.__app.post('/admin/namecard_modify')
        def namecard_modify(raw_request:dict):
            request = NamecardAddModifyRequset(raw_request)
            administrator_controller=Administrator_Controller()
            model = administrator_controller.namecard_editor(database=self.__database,
                                                                 request=request,
                                                                 type='modify')
            response = model.get_response_form_data(self._head_parser)
            return response
        
        @self.__app.post('/admin/namecard_delete')
        def namecard_delete(raw_request:dict):
            request = NamecardLoadDeleteRequset(raw_request)
            administrator_controller=Administrator_Controller()
            model = administrator_controller.namecard_editor(database=self.__database,
                                                                 request=request,
                                                                 type='delete')
            response = model.get_response_form_data(self._head_parser)
            return response

        #league
        @self.__app.post('/admin/league_load')
        def league_load(raw_request:dict):
            request = LeagueLoadDeleteRequset(raw_request)
            administrator_controller=Administrator_Controller()
            model = administrator_controller.league_editor(database=self.__database,
                                                                 request=request,
                                                                 type='load')
            response = model.get_response_form_data(self._head_parser)
            return response
        
        @self.__app.post('/admin/league_add')
        def league_add(raw_request:dict):
            request = LeagueAddModifyRequset(raw_request)
            administrator_controller=Administrator_Controller()
            model = administrator_controller.league_editor(database=self.__database,
                                                                 request=request,
                                                                 type='add')
            response = model.get_response_form_data(self._head_parser)
            return response
        
        @self.__app.post('/admin/league_modify')
        def league_modify(raw_request:dict):
            request = LeagueAddModifyRequset(raw_request)
            administrator_controller=Administrator_Controller()
            model = administrator_controller.league_editor(database=self.__database,
                                                                 request=request,
                                                                 type='modify')
            response = model.get_response_form_data(self._head_parser)
            return response
        
        @self.__app.post('/admin/league_delete')
        def league_delete(raw_request:dict):
            request = LeagueLoadDeleteRequset(raw_request)
            administrator_controller=Administrator_Controller()
            model = administrator_controller.league_editor(database=self.__database,
                                                                 request=request,
                                                                 type='delete')
            response = model.get_response_form_data(self._head_parser)
            return response
        
        #chat
        @self.__app.post('/admin/chat_load')
        def chat_load(raw_request:dict):
            request = ChatLoadDeleteRequset(raw_request)
            administrator_controller=Administrator_Controller()
            model = administrator_controller.chat_editor(database=self.__database,
                                                                 request=request,
                                                                 type='load')
            response = model.get_response_form_data(self._head_parser)
            return response
        
        @self.__app.post('/admin/chat_add')
        def chat_add(raw_request:dict):
            request = ChatAddModifyRequset(raw_request)
            administrator_controller=Administrator_Controller()
            model = administrator_controller.chat_editor(database=self.__database,
                                                                 request=request,
                                                                 type='add')
            response = model.get_response_form_data(self._head_parser)
            return response
        
        @self.__app.post('/admin/chat_modify')
        def chat_modify(raw_request:dict):
            request = ChatAddModifyRequset(raw_request)
            administrator_controller=Administrator_Controller()
            model = administrator_controller.chat_editor(database=self.__database,
                                                                 request=request,
                                                                 type='modify')
            response = model.get_response_form_data(self._head_parser)
            return response
        
        @self.__app.post('/admin/chat_delete')
        def chat_delete(raw_request:dict):
            request = ChatLoadDeleteRequset(raw_request)
            administrator_controller=Administrator_Controller()
            model = administrator_controller.chat_editor(database=self.__database,
                                                                 request=request,
                                                                 type='delete')
            response = model.get_response_form_data(self._head_parser)
            return response
        
        #bias
        @self.__app.post('/admin/bias_load')
        def bias_load(raw_request:dict):
            request = BiasLoadDeleteRequset(raw_request)
            administrator_controller=Administrator_Controller()
            model = administrator_controller.bias_editor(database=self.__database,
                                                                 request=request,
                                                                 type='load')
            response = model.get_response_form_data(self._head_parser)
            return response
        
        @self.__app.post('/admin/bias_add')
        def bias_add(raw_request:dict):
            request = BiasAddModifyRequset(raw_request)
            administrator_controller=Administrator_Controller()
            model = administrator_controller.bias_editor(database=self.__database,
                                                                 request=request,
                                                                 type='add')
            response = model.get_response_form_data(self._head_parser)
            return response
        
        @self.__app.post('/admin/bias_modify')
        def bias_modify(raw_request:dict):
            request = BiasAddModifyRequset(raw_request)
            administrator_controller=Administrator_Controller()
            model = administrator_controller.bias_editor(database=self.__database,
                                                                 request=request,
                                                                 type='modify')
            response = model.get_response_form_data(self._head_parser)
            return response
        
        @self.__app.post('/admin/bias_delete')
        def bias_delete(raw_request:dict):
            request = BiasLoadDeleteRequset(raw_request)
            administrator_controller=Administrator_Controller()
            model = administrator_controller.bias_editor(database=self.__database,
                                                                 request=request,
                                                                 type='delete')
            response = model.get_response_form_data(self._head_parser)
            return response
        
        #banner
        @self.__app.post('/admin/banner_load')
        def banner_load(raw_request:dict):
            request = BannerLoadDeleteRequset(raw_request)
            administrator_controller=Administrator_Controller()
            model = administrator_controller.banner_editor(database=self.__database,
                                                                 request=request,
                                                                 type='load')
            response = model.get_response_form_data(self._head_parser)
            return response
        
        @self.__app.post('/admin/banner_add')
        def banner_add(raw_request:dict):
            request = BannerAddRequset(raw_request)
            administrator_controller=Administrator_Controller()
            model = administrator_controller.banner_editor(database=self.__database,
                                                                 request=request,
                                                                 type='add')
            response = model.get_response_form_data(self._head_parser)
            return response
        
        @self.__app.post('/admin/banner_modify')
        def banner_modify(raw_request:dict):
            request = BannerModifyRequset(raw_request)
            administrator_controller=Administrator_Controller()
            model = administrator_controller.banner_editor(database=self.__database,
                                                                 request=request,
                                                                 type='modify')
            response = model.get_response_form_data(self._head_parser)
            return response
        
        @self.__app.post('/admin/banner_delete')
        def banner_delete(raw_request:dict):
            request = BannerLoadDeleteRequset(raw_request)
            administrator_controller=Administrator_Controller()
            model = administrator_controller.banner_editor(database=self.__database,
                                                                 request=request,
                                                                 type='delete')
            response = model.get_response_form_data(self._head_parser)
            return response
        

class ResetDatasRequest(RequestHeader):
    def __init__(self, request) -> None:
        super().__init__(request)
        body = request['body']
        self.admin_key = body['admin_key']

class UserLoadRequset(RequestHeader):
    def __init__(self, request) -> None:
        super().__init__(request)
        body = request['body']
        self.admin_key = body['admin_key']
        self.email = body['data']

class UserAddRequset(RequestHeader):
    def __init__(self, request) -> None:
        super().__init__(request)
        body = request['body']
        self.admin_key = body['admin_key']
        data = body['data']

        self.uname = data['uname']
        self.age = data['age']
        self.email = data['email']
        self.password = data['password']
        self.gender = data['gender']
        self.solo_point = data['solo_point']
        self.group_point = data['group_point']
        self.solo_combo = data['solo_combo']
        self.group_combo = data['group_combo']
        self.credit = data['credit']
        self.solo_bid = data['solo_bid']
        self.group_bid = data['group_bid']
        self.chatting = data['items']['chatting']
        self.saver = data['items']['saver']
        self.solo_daily = data['solo_daily']
        self.solo_special = data['solo_special']
        self.group_daily = data['group_daily']
        self.group_special = data['group_special']
        self.sign = data['sign']
        self.select_name_card = data['select_name_card']
        self.name_card_list = data['name_card_list']
        
class UserModifyRequset(RequestHeader):
    def __init__(self, request) -> None:
        super().__init__(request)
        body = request['body']
        self.admin_key = body['admin_key']
        data = body['data']
        self.uid = data['uid']
        self.uname = data['uname']
        self.age = data['age']
        self.email = data['email']
        self.password = data['password']
        self.gender = data['gender']
        self.solo_point = data['solo_point']
        self.group_point = data['group_point']
        self.solo_combo = data['solo_combo']
        self.group_combo = data['group_combo']
        self.credit = data['credit']
        self.solo_bid = data['solo_bid']
        self.group_bid = data['group_bid']
        self.chatting = data['items']['chatting']
        self.saver = data['items']['saver']
        self.solo_daily = data['solo_daily']
        self.solo_special = data['solo_special']
        self.group_daily = data['group_daily']
        self.group_special = data['group_special']
        self.sign = data['sign']
        self.select_name_card = data['select_name_card']
        self.name_card_list = data['name_card_list']

class UserDeleteRequset(RequestHeader):
    def __init__(self, request) -> None:
        super().__init__(request)
        body = request['body']
        self.admin_key = body['admin_key']
        self.uid = body['data']

class NamecardLoadDeleteRequset(RequestHeader):
    def __init__(self, request) -> None:
        super().__init__(request)
        body = request['body']
        self.admin_key = body['admin_key']
        self.ncid = body['data']

class NamecardAddModifyRequset(RequestHeader):
    def __init__(self, request) -> None:
        super().__init__(request)
        body = request['body']
        self.admin_key = body['admin_key']
        data = body['data']

        self.ncid = data['ncid']
        self.ncname = data['ncname']
        self.nccredit = data['nccredit']
        
class LeagueLoadDeleteRequset(RequestHeader):
    def __init__(self, request) -> None:
        super().__init__(request)
        body = request['body']
        self.admin_key = body['admin_key']
        self.lid = body['data']

class LeagueAddModifyRequset(RequestHeader):
    def __init__(self, request) -> None:
        super().__init__(request)
        body = request['body']
        self.admin_key = body['admin_key']
        data = body['data']

        self.lid = data['lid']
        self.lname = data['lname']
        self.bid_list = data['bid_list']
        self.tier = data['tier']
        self.num_bias = data['num_bias']
        self.state = data['state']
        self.type = data['type']

class ChatLoadDeleteRequset(RequestHeader):
    def __init__(self, request) -> None:
        super().__init__(request)
        body = request['body']
        self.admin_key = body['admin_key']
        self.cid = body['data']

class ChatAddModifyRequset(RequestHeader):
    def __init__(self, request) -> None:
        super().__init__(request)
        body = request['body']
        self.admin_key = body['admin_key']
        data = body['data']

        self.cid = data['cid']
        self.uid = data['uid']
        self.content = data['content']
        self.date = data['date']

class BiasLoadDeleteRequset(RequestHeader):
    def __init__(self, request) -> None:
        super().__init__(request)
        body = request['body']
        self.admin_key = body['admin_key']
        self.bid = body['data']

class BiasAddModifyRequset(RequestHeader):

    def __init__(self, request) -> None:
        super().__init__(request)
        body = request['body']
        self.admin_key = body['admin_key']
        data = body['data']

        self.bid = data['bid']
        self.type = data['type']
        self.bname = data['bname']
        self.category = data['category']
        self.birthday = data['birthday']
        self.debut = data['debut']
        self.agency = data['agency']
        self.group = data['group']
        self.lid = data['lid']
        self.point = data['point']
        self.num_user = data['num_user']
        self.x_account = data['x_account']
        self.insta_account = data['insta_account']
        self.tiktok_account = data['tiktok_account']
        self.youtube_account = data['youtube_account']
        self.homepage = data['homepage']
        self.fan_cafe = data['fan_cafe']
        self.country = data['country']
        self.nickname = data['nickname']
        self.fanname = data['fanname']
        self.group_memeber_bids = data['group_member_bids']

class BannerLoadDeleteRequset(RequestHeader):
    def __init__(self, request) -> None:
        super().__init__(request)
        body = request['body']
        self.admin_key = body['admin_key']
        self.baid = body['data']

class BannerAddRequset(RequestHeader):
    def __init__(self, request) -> None:
        super().__init__(request)
        body = request['body']
        self.admin_key = body['admin_key']
        data = body['data']
        self.baid = data['baid']
        self.ba_url = data['ba_url']

class BannerModifyRequset(RequestHeader):
    def __init__(self, request) -> None:
        super().__init__(request)
        body = request['body']
        self.admin_key = body['admin_key']
        data = body['data']
        self.baid = data['baid']
        self.ba_url = data['ba_url']