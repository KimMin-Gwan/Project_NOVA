import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from fastapi import HTTPException, status

from others import Bias

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
            
    # 전송하는 함수
    # send_email(보낼 주소, 인증번호)
    def alert_new_bias(self, bias:Bias, info):
        receiver_email = "youths0828@naver.com"
        
        # 이메일 메시지 구성
        message = MIMEMultipart("alternative")
        message["Subject"] = f"새로운 스트리머 등록 요청 {bias.bname}"
        message["From"] = self.sender_email
        message["To"] = receiver_email
        
        # HTML 본문 작성 (인증번호 포함)
        html_content = f"""
        <!DOCTYPE html>
        <html lang="ko">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>새로운 스트리머 등록 요청</title>
            <style>
                body {{
                    font-family: 'Arial', sans-serif;
                    background-color: #f4f4f4;
                    margin: 0;
                    padding: 0;
                }}
                .email-container {{
                    max-width: 600px;
                    margin: 40px auto;
                    background-color: #ffffff;
                    padding: 30px;
                    border: 1px solid #dddddd;
                    border-radius: 8px;
                    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
                }}
                .header {{
                    text-align: center;
                    margin-bottom: 20px;
                }}
                .header h2 {{
                    font-size: 22px;
                    color: #333333;
                    margin: 0;
                }}
                .content {{
                    font-size: 16px;
                    color: #555555;
                    line-height: 1.7;
                }}
                .content p {{
                    margin: 10px 0;
                }}
                .highlight-box {{
                    background-color: #f9f9f9;
                    border-left: 4px solid #007bff;
                    padding: 15px;
                    margin: 20px 0;
                }}
                .highlight-box p {{
                    margin: 5px 0;
                    font-weight: bold;
                }}
                .footer {{
                    text-align: center;
                    font-size: 13px;
                    color: #999999;
                    margin-top: 40px;
                    border-top: 1px solid #dddddd;
                    padding-top: 10px;
                }}
            </style>
        </head>
        <body>
            <div class="email-container">
                <div class="header">
                    <h2>새로운 스트리머 등록 요청이 도착했습니다.</h2>
                </div>
                <div class="content">
                    <p>다음 스트리머에 대한 등록 요청이 서버에 접수되었습니다.</p>

                    <div class="highlight-box">
                        <p>이름: {bias.bname}</p>
                        <p>플랫폼: {bias.platform}</p>
                        <p>정보: {info}</p>
                    </div>

                    <p>요청 내용을 검토하시고, 등록 상태를 <strong>CONFIRMED</strong>로 변경해 주세요.</p>
                </div>
                <div class="footer">
                    이 메일은 시스템에 의해 자동 발송되었습니다.
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
    def send_email_new_bias_added(self, receiver_email, bias:Bias, info):
        
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
            <title>새로운 스트리머 등록 요청</title>
            <style>
                body {{
                    font-family: 'Arial', sans-serif;
                    background-color: #f4f4f4;
                    margin: 0;
                    padding: 0;
                }}
                .email-container {{
                    max-width: 600px;
                    margin: 40px auto;
                    background-color: #ffffff;
                    padding: 30px;
                    border: 1px solid #dddddd;
                    border-radius: 8px;
                    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
                }}
                .header {{
                    text-align: center;
                    margin-bottom: 20px;
                }}
                .header h2 {{
                    font-size: 22px;
                    color: #333333;
                    margin: 0;
                }}
                .content {{
                    font-size: 16px;
                    color: #555555;
                    line-height: 1.7;
                }}
                .content p {{
                    margin: 10px 0;
                }}
                .highlight-box {{
                    background-color: #f9f9f9;
                    border-left: 4px solid #007bff;
                    padding: 15px;
                    margin: 20px 0;
                }}
                .highlight-box p {{
                    margin: 5px 0;
                    font-weight: bold;
                }}
                .footer {{
                    text-align: center;
                    font-size: 13px;
                    color: #999999;
                    margin-top: 40px;
                    border-top: 1px solid #dddddd;
                    padding-top: 10px;
                }}
            </style>
        </head>
        <body>
            <div class="email-container">
                <div class="header">
                    <h2>새로운 스트리머 등록 요청이 완료되었습니다.</h2>
                </div>
                <div class="content">
                    <p>다음 스트리머에 대한 등록 요청이 서버에 정상적으로 접수되었습니다.</p>

                    <div class="highlight-box">
                        <p>이름: {bias.bname}</p>
                        <p>플랫폼: {bias.platform}</p>
                        <p>정보: {info}</p>
                    </div>

                    <p>소중한 시간을 내어 등록해 주셔서 감사합니다.</p>

                    <p>요청하신 내용은 운영진이 확인 후, 검토 절차를 거쳐 정식 등록 여부가 결정됩니다.</p>

                    <p>등록하신 대상이 내부 기준에 부합하지 않는 경우, 요청이 반려될 수 있습니다.</p>
                </div>
                <div class="footer">
                    이 메일은 시스템에 의해 자동 발송되었습니다.
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