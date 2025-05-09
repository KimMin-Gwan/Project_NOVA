from view import NOVA_Server 
from view.parsers import Configure_File_Reader
from model import Local_Database, Mongo_Database
from manager import ConnectionManager
from others import FeedManager, FeedSearchEngine, ScheduleSearchEngine, FundingProjectManager
import asyncio
from uvicorn import run
from others.ai_service import AIManger



class Master(Configure_File_Reader):
    def __init__(self):
        super().__init__()
        self._extract_host_port()
        #self.abstract_loop = asyncio.get_event_loop()
        print('INFO<-[      Application startup.')
        print(f'INFO<-[      Application | Welcome to NOVA Server')
        print(f'INFO<-[      Application | Version : v{self._version}')

    async def server_start_up(self):
        #database = Local_Database() #디비 실행
        database = Mongo_Database(uri=self._mongo_db_key) #디비 실행
        
        ai_manager = AIManger(model_setting=self._model_setting, database=database)

        connection_manager = ConnectionManager() # 웹소켓 매니저 실행
        #league_manager = LeagueManager(connection_manager=connection_manager)
        #league_manager.init_league_manager(database=database) # 리그 매니저 초기화
        feed_search_engine = FeedSearchEngine(database=database)
        schedule_search_engine = ScheduleSearchEngine(database=database)
        feed_manager= FeedManager(database=database,
                                  feed_search_engine=feed_search_engine)
        funding_project_manager = FundingProjectManager(database=database)
        
        nova_server = NOVA_Server(
            database=database,
            feed_manager=feed_manager,
            feed_search_engine=feed_search_engine,
            schedule_search_engine=schedule_search_engine,
            funding_project_manager=funding_project_manager,
            ai_manager = ai_manager,
            jwt_secret_key = self._jwt_secret_key,
            connection_manager=connection_manager
            )
        
        #app = nova_server.get_app()

        loop = asyncio.get_event_loop()
        uvicorn_task = loop.run_in_executor(None, nova_server.run_server, self._host, self._port)
        #uvicorn_task = asyncio.create_task(nova_server.run_server(host=self._host, port=self._port))
        feed_search_task = feed_search_engine.make_task()()
        verification_task = nova_server.make_task()()

        try:
            await asyncio.gather(
                uvicorn_task,
                feed_search_task,
                verification_task
            )
        except KeyboardInterrupt:
            print("Server is shutting down gracefully...")

        
if __name__ == '__main__':
    server_master = Master()
    asyncio.run(server_master.server_start_up())

