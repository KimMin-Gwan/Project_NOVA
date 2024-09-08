from model import *
from others import CustomError
class Administrator_Controller:
    def reset_leagues_point(self, database:Local_Database,request): 
        model = ResetDatasModel(database=database)

        try:
            #관리자 키 확인
            if not model.check_admin_key(request=request):
                return model
            #json 업로드
            model.upload_data()
            #유저 불러오기
            if not model.set_users():
                return model
            #bias 불러오기
            if not model.set_biases():
                return model
            #포인트,콤보 초기화
            if not model.reset_point():
                return model
            
        except CustomError as e:
            print("Error Catched : ", e.error_type)
            model.set_state_code(e.error_code) # 종합 에러

        except Exception as e:
            print("Error Catched : ", e.error_type)
            model.set_state_code(e.error_code) # 종합 에러

        finally:
            return model
        
    def reset_daily(self,database:Local_Database,request):
        model = ResetDatasModel(database=database)
        try:
            if not model.check_admin_key(request=request):
                return model
            if not model.set_users():
                return model
                
            model.set_users()

            if not model.reset_daily():
                return model
            
        except CustomError as e:
            print("Error Catched : ", e.error_type)
            model.set_state_code(e.error_code) # 종합 에러

        except Exception as e:
            print("Error Catched : ", e.error_type)
            model.set_state_code(e.error_code) # 종합 에러

        finally:
            return model
        
    def user_editor(self,database:Local_Database,request,type):
        model = UserEditModel(database=database)

        try:
            if not model.check_admin_key(request=request):
                return model
            
            if type == 'add':
                model.set_user_data(request=request)
                model.add_user()

            if type == 'load':
                model.load_user(request=request,type='email')

            if type == 'modify':
                model.load_user(request=request,type='uid')
                model.set_user_data(request=request)
                model.modify_user(request=request)

            if type == 'delete':
                model.delete_user(request=request)

        except CustomError as e:
            print("Error Catched : ", e.error_type)
            model.set_state_code(e.error_code) # 종합 에러

        except Exception as e:
            print("Error Catched : ", e.error_type)
            model.set_state_code(e.error_code) # 종합 에러

        finally:
            return model
    
    def namecard_editor(self,database:Local_Database,request,type):

        model = NamecardEditModel(database=database)

        try:
            if not model.check_admin_key(request=request):
                return model

            if type == 'add':
                model.set_namecard_data(request=request)
                model.add_namecard()

            if type == 'load':
                model.load_namecard(request=request)

            if type == 'modify':
                model.load_namecard(request=request)
                model.set_namecard_data(request=request)
                model.modify_namecard()

            if type == 'delete':
                model.delete_namecard(request=request)

        except CustomError as e:
            print("Error Catched : ", e.error_type)
            model.set_state_code(e.error_code) # 종합 에러

        except Exception as e:
            print("Error Catched : ", e.error_type)
            model.set_state_code(e.error_code) # 종합 에러

        finally:
            return model
        
    def league_editor(self,database:Local_Database,request,type):
        model = LeagueEditmodel(database=database)

        try:
            if not model.check_admin_key(request=request):
                return model

            if not model.check_admin_key(request=request):
                return model

            if type == 'add':
                model.set_league_data(request=request)
                model.add_league()

            if type == 'load':
                model.load_league(request=request)

            if type == 'modify':
                model.load_league(request=request)
                model.set_league_data(request=request)
                model.modify_league()

            if type == 'delete':
                model.delete_league(request=request)

        except CustomError as e:
            print("Error Catched : ", e.error_type)
            model.set_state_code(e.error_code) # 종합 에러

        except Exception as e:
            print("Error Catched : ", e.error_type)
            model.set_state_code(e.error_code) # 종합 에러

        finally:
            return model
        
    def chat_editor(self,database:Local_Database,request,type):
        model = ChatEditModel(database=database)

        try:
            if not model.check_admin_key(request=request):
                return model

            if not model.check_admin_key(request=request):
                return model

            if type == 'add':
                model.set_chat_data(request=request)
                model.add_chat()

            if type == 'load':
                model.load_chat(request=request)

            if type == 'modify':
                model.load_chat(request=request)
                model.set_chat_data(request=request)
                model.modify_chat()

            if type == 'delete':
                model.delete_chat(request=request)

        except CustomError as e:
            print("Error Catched : ", e.error_type)
            model.set_state_code(e.error_code) # 종합 에러

        except Exception as e:
            print("Error Catched : ", e.error_type)
            model.set_state_code(e.error_code) # 종합 에러

        finally:
            return model
        
    def bias_editor(self,database:Local_Database,request,type):
        model = BiasEditModel(database=database)

        try:
            if not model.check_admin_key(request=request):
                return model

            if type == 'add':
                model.set_bias_data(request=request)
                model.add_bias()

            if type == 'load':
                model.load_bias(request=request)

            if type == 'modify':
                model.load_bias(request=request)
                model.set_bias_data(request=request)
                model.modify_bias()

            if type == 'delete':
                model.delete_bias(request=request)

        except CustomError as e:
            print("Error Catched : ", e.error_type)
            model.set_state_code(e.error_code) # 종합 에러

        except Exception as e:
            print("Error Catched : ", e.error_type)
            model.set_state_code(e.error_code) # 종합 에러

        finally:
            return model
        
    def banner_editor(self,database:Local_Database,request,type):
        model = BannerEditModel(database=database)

        try:
            if not model.check_admin_key(request=request):
                return model

            if type == 'add':
                model.set_banner_data(request=request)
                model.add_banner()

            if type == 'load':
                model.load_banner(request=request)

            if type == 'modify':
                model.load_banner(request=request)
                model.set_banner_data(request=request)
                model.modify_banner()

            if type == 'delete':
                model.delete_banner(request=request)

        except CustomError as e:
            print("Error Catched : ", e.error_type)
            model.set_state_code(e.error_code) # 종합 에러

        except Exception as e:
            print("Error Catched : ", e.error_type)
            model.set_state_code(e.error_code) # 종합 에러

        finally:
            return model