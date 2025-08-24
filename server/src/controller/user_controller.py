from model import *
from others import UserNotExist, CustomError, MailSender

from pprint import pprint

class UserController:
    # 로그인 시도
    def try_login(self, database, request, secret_key):

        model = LoginModel(database=database)
        # 유저가 있는지 확인

        if not model.set_user_with_email(request=request):
            return model

        model.request_login(request=request,user_data=model._user)
        if model.get_result() != "done":
            return model
        
        model.make_token(request=model._user, secret_key=secret_key)

        return model

    # 이메일 인증
    # 1. 데이터 베이스에 이미 있는 email인지 확인
    # 2. 이미 있는 이메일이 아니면 nova_verifiaction으로 임시 유저 생성
    # 3. 생성한 임시 유저로 이메일 보내기
    # 4. 이메일 보내는건 아래에 작성된 이메일 보내기 클래스 사용
    # 5. 이메일 전송 완료되면 True 반환
    # 6. 이미 있는 email이면 False 반환
    def try_send_email(self, database, request, nova_verification):
        model = SendEmailModel(database=database)
        try:
            if not model.set_user_with_email(request=request):
                mailsender = MailSender()
                temp_user = nova_verification.make_new_user(email=request.email)

                mailsender.send_email(receiver_email=temp_user.email,verification_code=temp_user.verification_code)
                model.set_response(result=True, detail="이메일이 전송되었습니다. 코드는 10분 동안 유효합니다.")
            else:
                model.set_response(result=False, detail="이미 존재하는 이메일 입니다.")
        except:
            model.set_response(result=False, detail="알 수 없는 오류가 발생했습니다. 관리자에게 문의하세요.")
            
        finally:
            return model
        
    # 비밀번호 찾기 시도 이메일 전송
    # 1. 이메일을 전송
    # 2. 보안코드 확인
    def try_send_email_password(self, database, request, nova_verification):
        model = SendEmailModel(database=database)
        if model.set_user_with_email(request=request):
            mailsender = MailSender()
            temp_user = nova_verification.make_new_user(email=request.email)

            # 여기를 비밀번호 전용 이메일로 바꾸든지 해야됨
            mailsender.send_email_in_password_find(receiver_email=temp_user.email,verification_code=temp_user.verification_code)

        else:
            model.set_response_in_reverse()
                
        return model

    # 비밀번호 변경하기 임시 유저 로그인
    # 비밀번호 찾기 & 변경하기에 사용되는 엔드포인트
    # 여긴 일반 로그인이랑 세팅 똑같이 해야됨
    async def try_login_with_temp_user(self, database, request, nova_verification, secret_key):
        model = LoginModel(database=database)

        # 존재하는 이메일인지 확인
        if not model.set_user_with_email(request=request.data_payload):
            raise request.forbidden_exception
        # 보안코드가 동일한지 확인

        if not await nova_verification.verificate_user(email=request.data_payload.email,
                                                        verification_code=request.data_payload.verification_code):
            raise request.forbidden_exception
        model.make_temp_user_token(request=request.data_payload, secret_key=secret_key)
        model.set_login_state(result="done")

        return model

    # 비밀번호 찾기에서 비밀번호 변경하기
    def try_find_password(self, database, request):
        model = ChangePasswordModel(database=database)
        # 유저가 있으면 세팅
        model.set_user_with_email(request=request.jwt_payload)

        model.try_change_password_with_temp_user(data_payload=request.data_payload)

        return model

    # 이메일 중복 검사 기능
    # 유저 데이터베이스에서 이메일을 서치해서 중복된 이메일이 있는지 확인합니다
    # 만약 이메일이 중복된다면 False를, 중복되지 않는다면 True를 반환합니다.
    def try_check_email_duplicate(self, database, request):
        model = SendEmailModel(database=database)
        # 이메일 체크
        model.check_email_duplicate(email=request.data_payload.email)
        return model

    # 회원가입 시도
    # 1. 인증번호 맞는지 확인
    # 2. 맞으면 데이터 베이스에 새로운 유저 생성해서
    # 3. 데이터 베이스 저장( save 함수 쓰면됨)
    # 4. 다 되면 True반환
    # 5. 만약 인증번호 틀리면 False 반환 + 실패 사유 detail에 작성
    async def try_sign_up(self, database, request, nova_verification, feed_search_engine):
        model = SendEmailModel(database=database)
        try:
            if not await nova_verification.verificate_user(email=request.email, verification_code=request.verification_code):
                model.set_response(result=False, detail="잘못된 인증 코드입니다.")
            
            else:
                model.save_user(request=request, feed_search_engine=feed_search_engine)
                model.set_response(result=True, detail="회원가입 성공")
                
        except:
            model.set_response(result=False, detail="알 수 없는 오류가 발생했습니다. 관리장에게 문의하세요.")
            
        finally:
            return model

    # 유저 페이지 맨 처음에 띄울 것
    def try_get_user_page(self, database, request):
        model = UserPageModel(database=database)

        model.set_user_with_email(request=request.jwt_payload)
        model.get_user_data()

        return model

    # 타입별 Feed 불러오기
    def try_get_my_feeds_with_type(self, database, request, feed_manager):
        model = MyFeedsModel(database=database)

        # 유저가 있으면 세팅함
        model.set_user_with_email(request=request.jwt_payload)
        if request.data_payload.type == "post":
            model.get_my_feeds(feed_manager=feed_manager, last_index=request.data_payload.key)
        elif request.data_payload.type == "like":
            model.get_liked_feeds(feed_manager=feed_manager, last_index=request.data_payload.key)

        return model

    # 댓글 데이터 불러오기
    def try_get_my_comments(self, database, request, feed_manager):
        model = MyCommentsModel(database=database)
        
        model.set_user_with_email(request=request.jwt_payload)
        # model.set_user_with_email(request=request.data_payload)
        model.get_my_comments(feed_manager=feed_manager, last_index=request.data_payload.key)

        return model

    # 마이페이지 프로필 가져오기
    def try_get_my_profile(self, database, request):
        model = MyProfileModel(database=database)

        model.set_user_with_email(request=request.jwt_payload)
        model.get_my_profile()

        return model

    # 닉네임 변경
    def try_change_nickname(self, database, request):
        model = ChangeNickNameModel(database=database)
        
        # 유저가 있으면 세팅
        model.set_user_with_email(request=request.jwt_payload)
        model.try_change_nickname(data_payload=request.data_payload)

        return model

    # 비밀번호 변경하기
    def try_change_password(self, database, request):
        model = ChangePasswordModel(database=database)
        
        # 유저가 있으면 세팅
        model.set_user_with_email(request=request.jwt_payload)
        model.try_change_password(data_payload=request.data_payload)

        return model

    # 프로필 사진 바꾸기 기능
    def try_change_profile_photo(self, database, request):
        model = ChangeProfilePhotoModel(database=database)
        
        # 유저 검색 (없으면 죽여야됨)
        if not model.set_user_with_email(request=request.jwt_payload):
            raise request.credentials_exception
        
        # 프로필 사진 바꾸기
        model.try_change_profile_photo(data_payload=request.data_payload)

        return model

    def try_resign(self, database, request):
        model = DeleteUserModel(database=database)

        # 유저 검색 (없으면 죽여야됨)
        if not model.set_user_with_email(request=request.jwt_payload):
            raise request.credentials_exception
        # 프로필 사진 바꾸기
        model.try_delete_user()

        return model