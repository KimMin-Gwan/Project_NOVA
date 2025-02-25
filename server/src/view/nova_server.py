from fastapi import FastAPI
from view.core_system_view import Core_Service_View
from view.user_system_view import User_Service_View
from view.sub_system_view import Sub_Service_View 
from view.funding_system_view import Funding_Service_View
from view.administrator_system_view import Administrator_System_View
from view.parsers import Head_Parser
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timedelta
from others import TempUser
#from threading import Thread
import asyncio
import random

class NOVA_Server:
    def __init__(self, database, connection_manager,
                  league_manager, feed_manager, feed_search_engine,
                  funding_project_manager, ai_manager
                  ) -> None:
        self.__app = FastAPI()

        self.__app.add_middleware(
            CORSMiddleware,
            allow_origins=[
                "http://127.0.0.1:6000",
                "http://127.0.0.1:4000",
                "http://localhost:6000",
                "http://127.0.0.1:4001",
                "http://localhost:4001",
                "http://127.0.0.1:3000",
                "http://localhost:3000"],  # 원격 호스트의 웹소켓 연결을 허용할 도메인 설정
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

        head_parser = Head_Parser()
        self.nova_verification = NOVAVerification()

        self.__core_system_view = Core_Service_View( app=self.__app,
                                                   endpoint='/core_system',
                                                   database=database,
                                                   head_parser=head_parser,
                                                   connection_manager= connection_manager,
                                                   league_manager=league_manager,
                                                   feed_manager=feed_manager,
                                                   feed_search_engine=feed_search_engine,
                                                   ai_manager=ai_manager
                                                   )
        self.__user_system_view = User_Service_View( app=self.__app,
                                                     endpoint='/user_system',
                                                   database=database,
                                                   nova_verification=self.nova_verification,
                                                   head_parser=head_parser,
                                                   feed_manager=feed_manager,
                                                   feed_search_engine=feed_search_engine
                                                   )
        self.__sub_system_view = Sub_Service_View( app=self.__app,
                                                     endpoint='/sub_system',
                                                   database=database,
                                                   head_parser=head_parser,
                                                   feed_search_engine=feed_search_engine
                                                   )
        self.__funding_system_view = Funding_Service_View( app=self.__app,
                                                     endpoint='/nova_fund_system',
                                                   database=database,
                                                   head_parser=head_parser,
                                                   funding_project_manager=funding_project_manager
                                                   )
        self.__administrator_system_view = Administrator_System_View( app=self.__app,
                                                     endpoint='/administrator_system',
                                                   database=database,
                                                   head_parser=head_parser)
        self.__core_system_view()
        self.__user_system_view()
        self.__sub_system_view()
        self.__funding_system_view()
        self.__administrator_system_view()

    def make_task(self):
        return self.nova_verification.make_task()

    def get_app(self):
        return self.__app

    def run_server(self, host='127.0.0.1', port=6000):
        uvicorn.run(app=self.__app, host=host, port=port)


class NOVAVerification:
    def __init__(self):
        self.__temp_user = []  # TempUser 
        #  exp 채커
        #exp_checker = Thread(target=self._check_expiration)
        #exp_checker.start()

    def make_task(self):
        return self.check_expiration
    
    def get_temp_user(self):
        for data in self.__temp_user:
            data()
        return
    
    # 이메일 인증하는 사람 추가 tempUser 반환
    def make_new_user(self, email):
        verification_code = self.__make_verification_code()
        exp = self.__make_expiration_time()

        # 중복이 있으면 그거 바꿔서 다시 저장
        for user in self.__temp_user:
            if user.email == email:
                user.verification_code = verification_code
                user.exp = exp
                return user

        # 중복이 아니고 첨하는 거면 새로 만들어서 어팬드
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
        return datetime.now() + timedelta(minutes=10)

    # 인증 코드와 해당 유저가 일치하는지 검사
    async def verificate_user(self, email, verification_code):
        target_user = None
        for user in self.__temp_user:
            if user.email == email:
                target_user = user

        # 인증 시도한 사람이 없으면 False 반환
        if not target_user:
            return False
        
        # 인증시간 만료되면 False (3분)
        if datetime.now() > target_user.exp:
            return False

        # 인증 번호가 맞으면 임시 유저에서 지우고 True 반환
        if int(target_user.verification_code) == int(verification_code):
            self.__temp_user.remove(target_user)
            return True
        # 인증 번호가 안맞으면 False 반환
        else:
            return False
        
    # 만료시간 체크해서 제거
    async def check_expiration(self):
        try:
            while True:
                await asyncio.sleep(1)
                for user in self.__temp_user:
                    if datetime.now() > user.exp:
                        self.__temp_user.remove(user)
        except KeyboardInterrupt:
            print("Shutting down due to KeyboardInterrupt.")



