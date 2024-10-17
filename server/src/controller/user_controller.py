from model import *
from others import UserNotExist, CustomError

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from fastapi import HTTPException, status

class UserController:      
        
    # 로그인 시도
    def try_login(self, database, request):

        model = LoginModel(database=database)
        # 유저가 있는지 확인

        if not model.set_user_with_email(request=request):
            return model

        model.request_login(request=request,user_data=model._user)
        if model.get_result() != "done":
            return model
        
        model.make_token(request=model._user)

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
            else:
                model.set_response()

        except CustomError as e:
            print("Error Catched : ", e.error_type)
            model.set_state_code(e.error_code) # 종합 에러

        except Exception as e:
            print("Error Catched : ", e.error_type)
            model.set_state_code(e.error_code) # 종합 에러

        finally:
            return model
        
    # 비밀번호 찾기 시도 이메일 전송
    # 1. 이메일을 전송
    # 2. 보안코드 확인
    def try_send_email_password(self, database, request, nova_verification):
        model = SendEmailModel(database=database)
        try:
            if model.set_user_with_email(request=request):
                mailsender = MailSender()
                temp_user = nova_verification.make_new_user(email=request.email)

                # 여기를 비밀번호 전용 이메일로 바꾸든지 해야됨
                mailsender.send_email_in_password_find(receiver_email=temp_user.email,verification_code=temp_user.verification_code)

            else:
                model.set_response_in_reverse()

        except CustomError as e:
            print("Error Catched : ", e.error_type)
            model.set_state_code(e.error_code) # 종합 에러

        except Exception as e:
            print("Error Catched : ", e.error_type)
            model.set_state_code(e.error_code) # 종합 에러

        finally:
            return model

    # 비밀번호 변경하기 임시 유저 로그인
    # 비밀번호 찾기 & 변경하기에 사용되는 엔드포인트
    # 여긴 일반 로그인이랑 세팅 똑같이 해야됨
    async def try_login_with_temp_user(self, database, request, nova_verification):
        model = LoginModel(database=database)

        # 존재하는 이메일인지 확인
        if not model.set_user_with_email(request=request.data_payload):
            raise request.forbidden_exception

        # 보안코드가 동일한지 확인
        if not await nova_verification.verificate_user(email=request.data_payload.email,
                                                        verification_code=request.data_payload.verification_code):
            raise request.forbidden_exception

        model.make_temp_user_token(request=request.data_payload)
        model.set_login_state(result="done")

        return model

    # 비밀번호 찾기에서 비밀번호 변경하기
    def try_find_password(self, database, request):
        model = ChangePasswordModel(database=database)
        try:
            # 유저가 있으면 세팅
            model.set_user_with_email(request=request.jwt_payload)

            model.try_change_password_with_temp_user(data_payload=request.data_payload)

        except CustomError as e:
            print("Error Catched : ", e.error_type)
            model.set_state_code(e.error_code) # 종합 에러

        except Exception as e:
            print("Error Catched : ", e.error_type)
            model.set_state_code(e.error_code) # 종합 에러

        finally:
            return model



    # 회원가입 시도
    # 1. 인증번호 맞는지 확인
    # 2. 맞으면 데이터 베이스에 새로운 유저 생성해서
    # 3. 데이터 베이스 저장( save 함수 쓰면됨)
    # 4. 다 되면 True반환
    # 5. 만약 인증번호 틀리면 False 반환 + 실패 사유 detail에 작성
    async def try_sign_up(self, database, request, nova_verification):
        model = SendEmailModel(database=database)
        try:
            if not await nova_verification.verificate_user(email=request.email, verification_code=request.verification_code):
                model.set_response()
            else:
                model.save_user(request=request)
                #model.make_token(request=request)

        except CustomError as e:
            print("Error Catched : ", e.error_type)
            model.set_state_code(e.error_code) # 종합 에러

        except Exception as e:
            print("Error Catched : ", e.error_type)
            model.set_state_code(e.error_code) # 종합 에러

        finally:
            return model
    
    def get_user_page(self, database, request):
        model = UserPageModel(database=database)
        try:
            # 유저가 있으면 세팅
            model.set_user_with_email(request=request.jwt_payload)
            model.set_solo_bias()
            model.set_group_bias()
            model.set_user_data_with_no_password()

        except CustomError as e:
            print("Error Catched : ", e.error_type)
            model.set_state_code(e.error_code) # 종합 에러

        except Exception as e:
            print("Error Catched : ", e.error_type)
            model.set_state_code(e.error_code) # 종합 에러

        finally:
            return model

    def try_change_nickname(self, database, request):
        model = ChangeNickNameModel(database=database)
        try:
            # 유저가 있으면 세팅
            model.set_user_with_email(request=request.jwt_payload)
            model.try_change_nickname(data_payload=request.data_payload)

        except CustomError as e:
            print("Error Catched : ", e.error_type)
            model.set_state_code(e.error_code) # 종합 에러

        except Exception as e:
            print("Error Catched : ", e.error_type)
            model.set_state_code(e.error_code) # 종합 에러

        finally:
            return model

    # 비밀번호 변경하기
    def try_change_password(self, database, request):
        model = ChangePasswordModel(database=database)
        try:
            # 유저가 있으면 세팅
            model.set_user_with_email(request=request.jwt_payload)

            model.try_change_password(data_payload=request.data_payload)

        except CustomError as e:
            print("Error Catched : ", e.error_type)
            model.set_state_code(e.error_code) # 종합 에러

        except Exception as e:
            print("Error Catched : ", e.error_type)
            model.set_state_code(e.error_code) # 종합 에러

        finally:
            return model

    def get_my_feed(self, database, request, feed_manager):
        model = MyFeedsModel(database=database)
        try:
            # 유저가 있으면 세팅
            model.set_user_with_email(request=request.jwt_payload)
            model.get_my_feed(feed_manager=feed_manager,
                              data_payload=request.data_payload)

        except CustomError as e:
            print("Error Catched : ", e.error_type)
            model.set_state_code(e.error_code) # 종합 에러

        except Exception as e:
            print("Error Catched : ", e.error_type)
            model.set_state_code(e.error_code) # 종합 에러

        finally:
            return model

    def get_my_comments(self, database, request, feed_manager):
        model = MyCommentsModel(database=database)
        try:
            # 유저가 있으면 세팅
            model.set_user_with_email(request=request.jwt_payload)
            model.get_my_comments(feed_manager=feed_manager,
                                    data_payload=request.data_payload)

        except CustomError as e:
            print("Error Catched : ", e.error_type)
            model.set_state_code(e.error_code) # 종합 에러

        except Exception as e:
            print("Error Catched : ", e.error_type)
            model.set_state_code(e.error_code) # 종합 에러

        finally:
            return model

    #def get_commented_feed(self, database, request, feed_manager):
        #model = MyFeedsModel(database=database)
        #try:
            ## 유저가 있으면 세팅
            #model.set_user_with_email(request=request.jwt_payload)
            #model.get_commented_feed(feed_manager=feed_manager,
                                    #data_payload=request.data_payload)

        #except CustomError as e:
            #print("Error Catched : ", e.error_type)
            #model.set_state_code(e.error_code) # 종합 에러

        #except Exception as e:
            #print("Error Catched : ", e.error_type)
            #model.set_state_code(e.error_code) # 종합 에러

        #finally:
            #return model

    def get_staring_feed(self, database, request, feed_manager):
        model = MyFeedsModel(database=database)
        try:
            # 유저가 있으면 세팅
            model.set_user_with_email(request=request.jwt_payload)
            model.get_staring_feed(feed_manager=feed_manager,
                                    data_payload=request.data_payload)

        except CustomError as e:
            print("Error Catched : ", e.error_type)
            model.set_state_code(e.error_code) # 종합 에러

        except Exception as e:
            print("Error Catched : ", e.error_type)
            model.set_state_code(e.error_code) # 종합 에러

        finally:
            return model

    def get_interactied_feed(self, database, request, feed_manager):
        model = MyFeedsModel(database=database)
        try:
            # 유저가 있으면 세팅
            model.set_user_with_email(request=request.jwt_payload)
            model.get_interactied_feed(feed_manager=feed_manager,
                                    data_payload=request.data_payload)

        except CustomError as e:
            print("Error Catched : ", e.error_type)
            model.set_state_code(e.error_code) # 종합 에러

        except Exception as e:
            print("Error Catched : ", e.error_type)
            model.set_state_code(e.error_code) # 종합 에러

        finally:
            return model

    def get_my_alert(self, database, request):
        model = MyAlertModel(database=database)
        try:
            # 유저가 있으면 세팅
            model.set_user_with_email(request=request.jwt_payload)
            model.set_alert_data(aid =request.data_payload.aid)
            model.set_last_aid()

        except CustomError as e:
            print("Error Catched : ", e.error_type)
            model.set_state_code(e.error_code) # 종합 에러

        except Exception as e:
            print("Error Catched : ", e.error_type)
            model.set_state_code(e.error_code) # 종합 에러

        finally:
            return model


# 이메일 전송
class MailSender:
    def __init__(self):
        # 이메일 발신자와 SMTP 서버 설정
        self.sender_email = "alsrhks2508@naver.com"  # 테스트용
        self.sender_password = "NQQLN3WW3KMU"  # 내꺼임...
        self.smtp_server = "smtp.naver.com"  # naver smtp 하루1000통
        self.smtp_port = 587  # 나중에 gmail 의 smtp 포트 쓸것

    # 전송하는 함수
    # send_email(보낼 주소, 인증번호)
    def send_email_in_password_find(self, receiver_email, verification_code):
        # 이메일 메시지 구성
        message = MIMEMultipart("alternative")
        message["Subject"] = "노바 플랫폼 비밀번호 찾기 | 보안 코드"
        message["From"] = self.sender_email
        message["To"] = receiver_email
        # HTML 본문 작성 (인증번호 포함)
        html_content = f"""
        <!DOCTYPE html>
        <html lang="ko">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>노바 플랫폼 비밀번호 찾기 보안코드</title>
            <style>
                body {{
                    font-family: 'Arial', sans-serif;
                    background-color: #f4f4f4;
                    margin: 0;
                    padding: 0;
                }}
                .email-container {{
                    max-width: 600px;
                    margin: 0 auto;
                    background-color: #ffffff;
                    padding: 20px;
                    border: 1px solid #dddddd;
                    border-radius: 8px;
                    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
                }}
                .header {{
                    text-align: center;
                    padding: 10px 0;
                    border-bottom: 1px solid #dddddd;
                }}
                .header h1 {{
                    font-size: 24px;
                    margin: 0;
                    color: #333333;
                }}
                .content {{
                    padding: 20px;
                    text-align: center;
                    line-height: 1.6;
                }}
                .content p {{
                    font-size: 16px;
                    color: #555555;
                    margin-bottom: 20px;
                }}
                .button-container {{
                    text-align: center;
                    margin: 20px 0;
                }}
                .button {{
                    background-color: #007bff;
                    color: #ffffff;
                    padding: 12px 20px;
                    border-radius: 5px;
                    text-decoration: none;
                    font-size: 16px;
                }}
                .button:hover {{
                    background-color: #0056b3;
                }}
                .footer {{
                    text-align: center;
                    font-size: 14px;
                    color: #aaaaaa;
                    margin-top: 30px;
                    border-top: 1px solid #dddddd;
                    padding-top: 10px;
                }}
            </style>
        </head>
        <body>
            <div class="email-container">
                <div class="header">
                    <h1>노바 플랫폼 비밀번호 찾기 이메일입니다</h1>
                </div>
                <div class="content">
                    <p>안녕하세요, 지지자님!</p>
                    <p>아래 인증 코드를 입력하여 비밀번호 찾기를 진행해주세요.</p>
                    <div class="button-container">
                        <p style="font-size: 24px; font-weight: bold;">인증 코드: {verification_code}</p>
                    </div>
                </div>
                <div class="footer">
                    <p>이 메일은 발신 전용입니다. 비밀번호 찾기에 문제가 있으시면 고객센터로 연락해 주세요.</p>
                </div>
            </div>
        </body>
        </html>
        """
        # MIMEText 객체로 HTML 본문 생성
        part = MIMEText(html_content, "html")

        # 이메일에 HTML 본문 추가
        message.attach(part)
        server = smtplib.SMTP(self.smtp_server, self.smtp_port)
        # SMTP 서버에 연결 및 이메일 전송
        try:
            server.starttls()  # TLS 보안 연결
            server.login(self.sender_email, self.sender_password)
            server.sendmail(self.sender_email, receiver_email, message.as_string())
        except Exception as e:
            print(f"이메일 전송 실패: {e}")
        finally:
            server.quit()

    # 전송하는 함수
    # send_email(보낼 주소, 인증번호)
    def send_email(self, receiver_email, verification_code):
        # 이메일 메시지 구성
        message = MIMEMultipart("alternative")
        message["Subject"] = "노바 플랫폼 회원 가입 | 보안 코드"
        message["From"] = self.sender_email
        message["To"] = receiver_email
        # HTML 본문 작성 (인증번호 포함)
        html_content = f"""
        <!DOCTYPE html>
        <html lang="ko">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>회원가입 인증 이메일</title>
            <style>
                body {{
                    font-family: 'Arial', sans-serif;
                    background-color: #f4f4f4;
                    margin: 0;
                    padding: 0;
                }}
                .email-container {{
                    max-width: 600px;
                    margin: 0 auto;
                    background-color: #ffffff;
                    padding: 20px;
                    border: 1px solid #dddddd;
                    border-radius: 8px;
                    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
                }}
                .header {{
                    text-align: center;
                    padding: 10px 0;
                    border-bottom: 1px solid #dddddd;
                }}
                .header h1 {{
                    font-size: 24px;
                    margin: 0;
                    color: #333333;
                }}
                .content {{
                    padding: 20px;
                    text-align: center;
                    line-height: 1.6;
                }}
                .content p {{
                    font-size: 16px;
                    color: #555555;
                    margin-bottom: 20px;
                }}
                .button-container {{
                    text-align: center;
                    margin: 20px 0;
                }}
                .button {{
                    background-color: #007bff;
                    color: #ffffff;
                    padding: 12px 20px;
                    border-radius: 5px;
                    text-decoration: none;
                    font-size: 16px;
                }}
                .button:hover {{
                    background-color: #0056b3;
                }}
                .footer {{
                    text-align: center;
                    font-size: 14px;
                    color: #aaaaaa;
                    margin-top: 30px;
                    border-top: 1px solid #dddddd;
                    padding-top: 10px;
                }}
            </style>
        </head>
        <body>
            <div class="email-container">
                <div class="header">
                    <h1>노바 플랫폼 회원가입을 환영합니다!</h1>
                </div>
                <div class="content">
                    <p>안녕하세요, 지지자님!</p>
                    <p>아래 인증 코드를 입력하여 회원가입을 완료해 주세요.</p>
                    <div class="button-container">
                        <p style="font-size: 24px; font-weight: bold;">인증 코드: {verification_code}</p>
                    </div>
                    <p>회원가입 절차를 계속 진행해 주세요.</p>
                </div>
                <div class="footer">
                    <p>이 메일은 발신 전용입니다. 로그인에 문제가 있으시면 고객센터로 연락해 주세요.</p>
                </div>
            </div>
        </body>
        </html>
        """
        # MIMEText 객체로 HTML 본문 생성
        part = MIMEText(html_content, "html")

        # 이메일에 HTML 본문 추가
        message.attach(part)
        server = smtplib.SMTP(self.smtp_server, self.smtp_port)
        # SMTP 서버에 연결 및 이메일 전송
        try:
            server.starttls()  # TLS 보안 연결
            server.login(self.sender_email, self.sender_password)
            server.sendmail(self.sender_email, receiver_email, message.as_string())
        except Exception as e:
            print(f"이메일 전송 실패: {e}")
        finally:
            server.quit()
