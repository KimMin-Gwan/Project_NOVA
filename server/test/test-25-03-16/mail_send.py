import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class TempUser:
    def __init__(self, email="", verification_code = "",
                exp = "",
                 ):
        self.email = email
        self.verification_code = verification_code
        self.exp = exp

class NOVAVerification:
    def __init__(self):
        self.__temp_user = []  # TempUser 
        # exp 채커
        exp_checker = Thread(target=self._check_expiration)
        exp_checker.start()
    
    # 이메일 인증하는 사람 추가 tempUser 반환
    def make_new_user(self, email):
        verification_code = self.__make_verification_code()
        exp = self.__make_expiration_time()
        tempUser = TempUser(email=email,
                             verification_code=verification_code,
                             exp=exp)
        self.__temp_user.append(tempUser)
        return tempUser

    # 인증코드 랜덤 생성 (1000 ~ 9999)
    def __make_verification_code(self):
        return str(random.randint(1000, 9999))

    # 만료 시간 생성(현재시간 + 3분)
    def __make_expiration_time(self):
        return datetime.now() + timedelta(minutes=3)

    # 인증 코드와 해당 유저가 일치하는지 검사
    def verificate_user(self, email, verification_code):
        target_user = None
        for user in self.__temp_user:
            if user.email == email:
                target_user = user

        # 인증 시도한 사람이 없으면 False 반환
        if not target_user:
            return False

        # 인증 번호가 맞으면 임시 유저에서 지우고 True 반환
        if target_user.verification_code == verification_code:
            self.__temp_user.remove(target_user)
            return True
        # 인증 번호가 안맞으면 False 반환
        else:
            return False
        
    # 만료시간 체크해서 제거
    def _check_expiration(self):
        while True:
            time.sleep(1)
            for user in self.__temp_user:
                if datetime.now() > user.exp:
                    self.__temp_user.remove(user)
            



# 예시 사용법
#verification_code = str(random.randint(1000, 9999))
#receiver_email = "alsrhks2508@yu.ac.kr"

#mail_sender = MailSender()
#mail_sender.send_email(receiver_email, verification_code)


class MailSender:
    def __init__(self):
        # 이메일 발신자와 SMTP 서버 설정
        self.sender_email = "alsrhks2508@naver.com"  # 테스트용
        self.sender_password = "NQQLN3WW3KMU"  # 내꺼임...
        self.smtp_server = "smtp.naver.com"  # naver smtp 하루1000통
        self.smtp_port = 587  # 나중에 gmail 의 smtp 포트 쓸것

        
    def send_email(self, receiver_email, verification_code):
        # 이메일 메시지 구성
        message = MIMEMultipart("alternative")
        message["Subject"] = "회원가입 인증 코드 테스트"
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
            print("이메일 전송 성공!")
        except Exception as e:
            print(f"이메일 전송 실패: {e}")
        finally:
            server.quit()





