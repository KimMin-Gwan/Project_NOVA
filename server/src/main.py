from view import NOVA_Server 
from view.parsers import Configure_File_Reader
from model import Mongo_Database, Mongo_Database
from manager import ConnectionManager
from others import FeedManager, FeedSearchEngine, ScheduleSearchEngine
import asyncio
from uvicorn import run
#from others.ai_service import AIManger

YELLOW = "\033[33m"
RESET = "\033[0m"


import types
import traceback

# 원래 NoneType
NoneType = type(None)

def fake_get(self, *args, **kwargs):
    print(">>> None.get() 호출됨!")
    traceback.print_stack()
    raise AttributeError("'NoneType' object has no attribute 'get'")  # 원래 동작 유지

# NoneType에 get 속성 주입
NoneType.get = fake_get


class ContentKeyStorage:
    def __init__(self,
                 chzzk_client_id, chzzk_client_secret,
                 soop_client_id, soop_client_secret
                 ):
        self.chzzk_client_id = chzzk_client_id
        self.chzzk_client_secret= chzzk_client_secret
        self.soop_client_id = soop_client_id
        self.soop_client_secret= soop_client_secret



class Master(Configure_File_Reader):
    def __init__(self):
        super().__init__()
        self._extract_host_port()
        #self.abstract_loop = asyncio.get_event_loop()
        print(f'{YELLOW}INFO{RESET}<-[      Application startup.')
        print(f'{YELLOW}INFO{RESET}<-[      Application | Welcome to NOVA Server')
        print(f'{YELLOW}INFO{RESET}<-[      Application | Version : v{self._version}')

    async def server_start_up(self):
        #database = Mongo_Database() #디비 실행
        database = Mongo_Database(uri=self._mongo_db_key) #디비 실행
        
        #ai_manager = AIManger(model_setting=self._model_setting, database=database)

        connection_manager = ConnectionManager() # 웹소켓 매니저 실행
        
        feed_search_engine = FeedSearchEngine(database=database)
        schedule_search_engine = ScheduleSearchEngine(database=database)
        feed_manager= FeedManager(database=database,
                                  feed_search_engine=feed_search_engine)
        
        content_key_storage = ContentKeyStorage(
            chzzk_client_id=self._chzzk_client_id,
            chzzk_client_secret=self._chzzk_client_secret,
            soop_client_id=self._soop_client_id,
            soop_client_secret=self._soop_client_secret
        )
        
        nova_server = NOVA_Server(
            database=database,
            feed_manager=feed_manager,
            feed_search_engine=feed_search_engine,
            schedule_search_engine=schedule_search_engine,
            jwt_secret_key = self._jwt_secret_key,
            connection_manager=connection_manager,
            content_key_storage=content_key_storage
            )
        
        #app = nova_server.get_app()

        loop = asyncio.get_event_loop()
        uvicorn_task = loop.run_in_executor(None, nova_server.run_server, self._host, self._port)
        #uvicorn_task = asyncio.create_task(nova_server.run_server(host=self._host, port=self._port))
        #feed_search_task = feed_search_engine.make_task()()
        
        verification_task = nova_server.make_task()()

        try:
            await asyncio.gather(
                uvicorn_task,
                #feed_search_task,
                verification_task
            )
        except KeyboardInterrupt:
            print("Server is shutting down gracefully...")

        
if __name__ == '__main__':
    server_master = Master()
    asyncio.run(server_master.server_start_up())

