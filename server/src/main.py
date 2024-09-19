from view import NOVA_Server 
from view.parsers import Configure_File_Reader
from model import Local_Database
from others import ConnectionManager, LeagueManager,FeedManager


class Master(Configure_File_Reader):
    def __init__(self):
        super().__init__()
        self._extract_host_port()
        print('INFO<-[      Application startup.')
        print(f'INFO<-[      Application | Welcome to NOVA Server')
        print(f'INFO<-[      Application | Version : v{self._version}')

    def server_start_up(self):
        database = Local_Database() #디비 실행
        connection_manager = ConnectionManager() # 웹소켓 매니저 실행
        league_manager = LeagueManager(connection_manager=connection_manager)
        league_manager.init_league_manager(database=database) # 리그 매니저 초기화
        feed_manager= FeedManager(database=database, fclasses=self._fclasses)
        feed_manager.init_feed_data()

        cheese_server = NOVA_Server(
            database=database,
            connection_manager=connection_manager,
            league_manager=league_manager,
            feed_manager=feed_manager
            )
        cheese_server.run_server(self._host, self._port)
        
if __name__ == '__main__':
    server_master = Master()
    server_master.server_start_up()

