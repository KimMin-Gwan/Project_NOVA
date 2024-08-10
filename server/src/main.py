from view import NOVA_Server 
from view.parsers import Configure_File_Reader
from model import Local_Database


class Master(Configure_File_Reader):
    def __init__(self):
        self._extract_host_port()
        print('INFO<-[      Application startup.')
        print(f'INFO<-[      Application | Welcome to NOVA Server')
        print(f'INFO<-[      Application | Version : v{self._version}')

    def server_start_up(self):
        database = Local_Database() #디비 실행
        cheese_server = NOVA_Server(database=database)
        cheese_server.run_server(self._host, self._port)
        
if __name__ == '__main__':
    server_master = Master()
    server_master.server_start_up()

