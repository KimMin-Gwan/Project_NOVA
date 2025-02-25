from typing import Any, Optional
from fastapi import FastAPI
from view.master_view import Master_View, RequestHeader
from view.parsers import Head_Parser
from controller import Administrator_Controller

class Administrator_System_View(Master_View):
    def __init__(self, app:FastAPI, endpoint:str, database, head_parser:Head_Parser) -> None:
        super().__init__(head_parser=head_parser)
        self.__app = app
        self._endpoint = endpoint
        self.__database = database
        self.admin_route(endpoint)

    def admin_route(self, endpoint:str):
        @self.__app.get(endpoint+'/admin')
        def home():
            return "Hello, This is Administrator System"

        # USER
        @self.__app.post('/admin/user_load')
        def user_load(raw_request:dict):
            request = UserLoadRequest(raw_request)
            administrator_controller = Administrator_Controller()
            model = administrator_controller.user_editor(database=self.__database, request=request, order='load')
            response = model.get_response_form_data(self._head_parser)
            return response

        @self.__app.post('/admin/user_add')
        def user_add(raw_request:dict):
            request = UserAddModifyRequest(raw_request)
            administrator_controller = Administrator_Controller()
            model = administrator_controller.user_editor(database=self.__database, request=request, order='add')
            response = model.get_response_form_data(self._head_parser)
            return response

        @self.__app.post('/admin/user_modify')
        def user_modify(raw_request:dict):
            request = UserAddModifyRequest(raw_request)
            administrator_controller = Administrator_Controller()
            model = administrator_controller.user_editor(database=self.__database, request=request, order='modify')
            response = model.get_response_form_data(self._head_parser)
            return response

        @self.__app.post('/admin/user_delete')
        def user_delete(raw_request:dict):
            request = UserDeleteRequest(raw_request)
            administrator_controller = Administrator_Controller()
            model = administrator_controller.user_editor(database=self.__database, request=request, order='delete')

        # FEED
        @self.__app.post('/admin/feed_load')
        def feed_load(raw_request:dict):
            request = FeedLoadDeleteRequest(raw_request)
            administrator_controller = Administrator_Controller()
            model = administrator_controller.feed_editor(database=self.__database, request=request, order='load')
            response = model.get_response_form_data(self._head_parser)
            return response

        @self.__app.post('/admin/feed_add')
        def feed_add(raw_request:dict):
            request = FeedAddModifyRequest(raw_request)
            administrator_controller = Administrator_Controller()
            model = administrator_controller.feed_editor(database=self.__database, request=request, order='add')
            response = model.get_response_form_data(self._head_parser)
            return response

        @self.__app.post('/admin/feed_modify')
        def feed_modify(raw_request:dict):
            request = FeedLoadDeleteRequest(raw_request)
            administrator_controller = Administrator_Controller()
            model = administrator_controller.feed_editor(database=self.__database, request=request, order='modify')
            response = model.get_response_form_data(self._head_parser)
            return response

        @self.__app.post('/admin/feed_delete')
        def feed_delete(raw_request:dict):
            request = FeedLoadDeleteRequest(raw_request)
            administrator_controller = Administrator_Controller()
            model = administrator_controller.feed_editor(database=self.__database, request=request, order='delete')
            response = model.get_response_form_data(self._head_parser)
            return response

        @self.__app.post('/admin/feed_block')
        def feed_block(raw_request:dict):
            request = FeedLoadDeleteRequest(raw_request)
            administrator_controller = Administrator_Controller()
            model = administrator_controller.feed_editor(database=self.__database, request=request, order='block')
            response = model.get_response_form_data(self._head_parser)
            return response

        @self.__app.post('/admin/feed_unblock')
        def feed_unblock(raw_request:dict):
            request = FeedLoadDeleteRequest(raw_request)
            administrator_controller = Administrator_Controller()
            model = administrator_controller.feed_editor(database=self.__database, request=request, order='unblock')
            response = model.get_response_form_data(self._head_parser)
            return response

        @self.__app.post('/admin/feed_private')
        def feed_private(raw_request:dict):
            request = FeedLoadDeleteRequest(raw_request)
            administrator_controller = Administrator_Controller()
            model = administrator_controller.feed_editor(database=self.__database, request=request, order='private')
            response = model.get_response_form_data(self._head_parser)
            return response

        # Comment
        @self.__app.post('/admin/comment_load')
        def comment_load(raw_request:dict):
            request = CommentLoadDeleteRequest(raw_request)
            administrator_controller = Administrator_Controller()
            model = administrator_controller.feed_editor(database=self.__database, request=request, order='comment_load')
            response = model.get_response_form_data(self._head_parser)
            return response

        @self.__app.post('/admin/comment_block')
        def comment_block(raw_request:dict):
            request = CommentLoadDeleteRequest(raw_request)
            administrator_controller = Administrator_Controller()
            model = administrator_controller.feed_editor(database=self.__database, request=request, order='comment_block')
            response = model.get_response_form_data(self._head_parser)
            return response

        @self.__app.post('/admin/comment_unblock')
        def comment_unblock(raw_request:dict):
            request = CommentLoadDeleteRequest(raw_request)
            administrator_controller = Administrator_Controller()
            model = administrator_controller.feed_editor(database=self.__database, request=request, order='comment_unblock')
            response = model.get_response_form_data(self._head_parser)
            return response

        @self.__app.post('/admin/comment_private')
        def comment_private(raw_request:dict):
            request = CommentLoadDeleteRequest(raw_request)
            administrator_controller = Administrator_Controller()
            model = administrator_controller.feed_editor(database=self.__database, request=request, order='comment_private')
            response = model.get_response_form_data(self._head_parser)
            return response

        @self.__app.post('/admin/comment_delete')
        def comment_delete(raw_request:dict):
            request = CommentLoadDeleteRequest(raw_request)
            administrator_controller = Administrator_Controller()
            model = administrator_controller.feed_editor(database=self.__database, request=request, order='comment_delete')
            response = model.get_response_form_data(self._head_parser)
            return response

        # BIAS
        @self.__app.post('/admin/bias_load')
        def bias_load(raw_request:dict):
            request = BiasLoadDeleteRequest(raw_request)
            administrator_controller = Administrator_Controller()
            model = administrator_controller.feed_editor(database=self.__database, request=request, order='load')
            response = model.get_response_form_data(self._head_parser)
            return response

        @self.__app.post('/admin/bias_add')
        def bias_add(raw_request:dict):
            request = BiasAddModifyRequest(raw_request)
            administrator_controller = Administrator_Controller()
            model = administrator_controller.feed_editor(database=self.__database, request=request, order='add')
            response = model.get_response_form_data(self._head_parser)
            return response

        @self.__app.post('/admin/bias_modify')
        def bias_modify(raw_request:dict):
            request = BiasAddModifyRequest(raw_request)
            administrator_controller = Administrator_Controller()
            model = administrator_controller.feed_editor(database=self.__database, request=request, order='modify')
            response = model.get_response_form_data(self._head_parser)
            return response

        @self.__app.post('/admin/bias_delete')
        def bias_delete(raw_request:dict):
            request = BiasLoadDeleteRequest(raw_request)
            administrator_controller = Administrator_Controller()
            model = administrator_controller.feed_editor(database=self.__database, request=request, order='delete')
            response = model.get_response_form_data(self._head_parser)
            return response

        # NAME CARD
        @self.__app.post('/admin/namecard_load')
        def namecard_load(raw_request:dict):
            request = NameCardLoadDeleteRequest(raw_request)
            administrator_controller=Administrator_Controller()
            model = administrator_controller.namecard_editor(database=self.__database, request=request, order='load')
            response = model.get_response_form_data(self._head_parser)
            return response

        @self.__app.post('/admin/namecard_add')
        def namecard_add(raw_request:dict):
            request = NameCardAddModifyRequest(raw_request)
            administrator_controller=Administrator_Controller()
            model = administrator_controller.namecard_editor(database=self.__database, request=request, order='add')
            response = model.get_response_form_data(self._head_parser)
            return response

        @self.__app.post('/admin/namecard_modify')
        def namecard_modify(raw_request:dict):
            request = NameCardAddModifyRequest(raw_request)
            administrator_controller=Administrator_Controller()
            model = administrator_controller.namecard_editor(database=self.__database, request=request, type='modify')
            response = model.get_response_form_data(self._head_parser)
            return response

        @self.__app.post('/admin/namecard_delete')
        def namecard_delete(raw_request:dict):
            request = NameCardLoadDeleteRequest(raw_request)
            administrator_controller=Administrator_Controller()
            model = administrator_controller.namecard_editor(database=self.__database, request=request, type='delete')
            response = model.get_response_form_data(self._head_parser)
            return response


class UserLoadRequest(RequestHeader):
    def __init__(self, request) -> None:
        super().__init__(request)
        body = request['body']
        self.admin_key = body['admin_key']
        self.email = body['data']

class UserAddModifyRequest(RequestHeader):
    def __init__(self, request) -> None:
        super().__init__(request)
        body = request['body']
        data = body['data']
        self.admin_key = body['admin_key']

        try:
            self.uid = data['uid']
        except:
            pass

        self.uname = data['uname']
        self.age = data['age']
        self.email = data['email']
        self.password = data['password']
        self.gender = data['gender']
        self.bids = data['bids']
        self.credit = data['credit']

class UserDeleteRequest(RequestHeader):
    def __init__(self, request) -> None:
        super().__init__(request)
        body = request['body']
        self.admin_key = body['admin_key']
        self.uid = body['data']

class FeedLoadDeleteRequest(RequestHeader):
    def __init__(self, request) -> None:
        super().__init__(request)
        body = request['body']
        self.admin_key = body['admin_key']
        self.fid = body['data']

class FeedAddModifyRequest(RequestHeader):
    def __init__(self, request) -> None:
        super().__init__(request)
        body = request['body']
        data = body['data']
        self.admin_key = body['admin_key']

        try:
            self.fid = data['fid']
        except:
            pass

        self.uid = data['uid']
        self.nickname = data['nickname']
        self.title = data['title']
        self.body = data['body']
        self.fclass = data['fclass']
        self.date = data['date']
        self.hashtag = data['hashtag']
        self.bid = data['bid']
        self.image = data['image']
        self.board_type = data['board_type']
        self.level = data['level']
        self.raw_body = data['raw_body']

class CommentLoadDeleteRequest(RequestHeader):
    def __init__(self, request) -> None:
        super().__init__(request)
        body = request['body']
        self.admin_key = body['admin_key']
        self.cid = body['data']

class BiasLoadDeleteRequest(RequestHeader):
    def __init__(self, request) -> None:
        super().__init__(request)
        body = request['body']
        self.admin_key = body['admin_key']
        self.bid = body['bid']

class BiasAddModifyRequest(RequestHeader):
    def __init__(self, request) -> None:
        super().__init__(request)
        body = request['body']
        data = body['data']
        self.admin_key = body['admin_key']

        try:
            self.bid = data['bid']
        except:
            pass

        self.bname = data['bname']
        self.category = data['category']
        self.birthday = data['birthday']
        self.debut = data['debut']
        self.agency = data['agency']
        self.group = data['group']
        self.num_user = data['num_user']
        self.board_types = data['board_types']
        self.x_account = data['x_account']
        self.insta_account = data['insta_account']
        self.tictok_account = data['tictok_account']
        self.youtube_account = data['youtube_account']
        self.homepage = data['homepage']
        self.fan_cafe = data['fan_cafe']
        self.country = data['country']
        self.fanname = data['fanname']

class NameCardLoadDeleteRequest(RequestHeader):
    def __init__(self, request) -> None:
        super().__init__(request)
        body = request['body']
        self.admin_key = body['admin_key']
        self.ncid = body['ncid']

class NameCardAddModifyRequest(RequestHeader):
    def __init__(self, request) -> None:
        super().__init__(request)
        body = request['body']
        data = body['data']
        self.admin_key = body['admin_key']

        self.ncid = data['ncid']
        self.ncname = data['ncname']
        self.nccredit = data['nccredit']
