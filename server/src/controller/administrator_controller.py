from model import *
from model import Local_Database
from model.administrator_model import UserEditorModel, BiasEditorModel, FeedEditorModel, NameCardEditorModel
from others import CustomError

class Administrator_Controller:
    def user_editor(self, database, request, order):
        model = UserEditorModel(database=database)

        try:
            if not model.check_admin_key(request=request):
                return model

            if order == 'add':
                model.set_user_data(body_data=request)
                model.add_user()

            if order == 'load':
                model.load_user(target=request.email, target_type='email')

            if order == 'modify':
                model.load_user(target=request.uid, target_type='uid')
                model.set_user_data(body_data=request)
                model.modify_user()

            if order == 'delete':
                model.delete_user(uid=request.uid)

        except CustomError as e:
            print("Error Catched : ", e.error_type)
            model.set_state_code(e.error_code) # 종합 에러

        except Exception as e:
            print("Error Catched : ", e.error_type)
            model.set_state_code(e.error_code) # 종합 에러

        finally:
            return model

    def bias_editor(self, database, request, order):
        model = BiasEditorModel(database=database)

        try:
            if not model.check_admin_key(request=request):
                return model

            if order == 'add':
                model.set_bias_data(body_data=request)
                model.add_bias()

            if order == 'load':
                model.load_bias(bid=request.bid)

            if order == 'modify':
                model.load_bias(bid=request.bid)
                model.set_bias_data(body_data=request)
                model.modify_bias()

            if order == 'delete':
                model.delete_bias(uid=request.uid)

        except CustomError as e:
            print("Error Catched : ", e.error_type)
            model.set_state_code(e.error_code) # 종합 에러

        except Exception as e:
            print("Error Catched : ", e.error_type)
            model.set_state_code(e.error_code) # 종합 에러

        finally:
            return model

    def feed_editor(self, database, request, order):
        model = FeedEditorModel(database=database)

        try:
            if not model.check_admin_key(request=request):
                return model

            if order == 'add':
                model.set_feed_data(body_data=request)
                model.add_feed()

            if order == 'load':
                model.load_feed(fid=request.fid)

            if order == 'modify':
                model.load_feed(fid=request.fid)
                model.set_feed_data(body_data=request)
                model.modify_feed()

            if order == 'private':
                model.load_feed(fid=request.fid)
                model.set_private_feed()

            if order == 'block':
                model.load_feed(fid=request.fid)
                model.set_block_feed()

            if order == 'unblock':
                model.load_feed(fid=request.fid)
                model.set_unblock_feed()

            if order == 'delete':
                model.load_feed(fid=request.fid)
                model.delete_feed()

            if order == 'comment_load':
                model.load_comment(cid=request.cid)

            if order == 'comment_block':
                model.load_comment(cid=request.cid)
                model.set_block_comment()

            if order == 'comment_unblock':
                model.load_comment(cid=request.cid)
                model.set_unblock_comment()

            if order == 'comment_private':
                model.load_comment(cid=request.cid)
                model.set_private_comment()

            if order == 'comment_delete':
                model.load_comment(cid=request.cid)
                model.delete_comment()


        except CustomError as e:
            print("Error Catched : ", e.error_type)
            model.set_state_code(e.error_code) # 종합 에러

        except Exception as e:
            print("Error Catched : ", e.error_type)
            model.set_state_code(e.error_code) # 종합 에러

        finally:
            return model

    def namecard_editor(self, database, request, order):
        model = NameCardEditorModel(database=database)

        try:
            if not model.check_admin_key(request=request):
                return model

            if order == 'add':
                model.set_namecard_data(body_data=request)
                model.add_namecard()

            if order == 'load':
                model.load_namecard(ncid=request.ncid)

            if order == 'modify':
                model.load_namecard(ncid=request.ncid)
                model.set_namecard_data(body_data=request)
                model.modify_namecard()

            if order == 'delete':
                model.delete_namecard(ncid=request.ncid)

        except CustomError as e:
            print("Error Catched : ", e.error_type)
            model.set_state_code(e.error_code) # 종합 에러

        except Exception as e:
            print("Error Catched : ", e.error_type)
            model.set_state_code(e.error_code) # 종합 에러

        finally:
            return model
