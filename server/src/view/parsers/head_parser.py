''' Client data
header = {
    'request-type' :'default',
    'client-version' : 'v1.0.1',
    'client-ip' : '127.0.0.1',
    'uid' : '1234-abcd-5678',
    'endpoint' : '/endpoint'
}
'''
import re
class ModelSetting:
    def __init__(self, open_api_key, gpt_model):
        self.api_key = open_api_key
        self.model_v = gpt_model

class Configure_File_Reader:
    def __init__(self) -> None:
        self._host = ''
        self._port = 0
        self._version = ''
        self._open_api_key = ''
        self._gpt_model = ''
        self._mongo_db_key = ''
        self._jwt_secret_key = ''
        self._storage_access_key = ''
        self._storage_secret_key = ''
        self._chzzk_client_id = ''
        self._chzzk_client_secret = ''
        self._soop_client_id = ''
        self._soop_client_secret = ''

    def _extract_host_port(self, file_path='./configure.txt'):
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                if line.startswith('HOST'):
                    self._host = line.split('=')[1].strip()
                elif line.startswith('PORT'):
                    self._port = int(line.split('=')[1].strip())
                elif line.startswith('VERSION'):
                    self._version = line.split('=')[1].strip()
                elif line.startswith('open_api_key'):
                    self._open_api_key= line.split('=')[1].strip()
                elif line.startswith('gpt_model'):
                    self._gpt_model= line.split('=')[1].strip()
                elif line.startswith('mongo_db_key'):
                    match = re.search(pattern=r'key = (.*)',string=line)
                    self._mongo_db_key= match.group(1)
                elif line.startswith('jwt_secret_key'):
                    self._jwt_secret_key= line.split('=')[1].strip()
                elif line.startswith('storage_access_key'):
                    self._storage_access_key= line.split('=')[1].strip()
                elif line.startswith('storage_sectet_key'):
                    self._storage_secret_key= line.split('=')[1].strip()
                elif line.startswith('chzzk_client_id'):
                    self._chzzk_client_id= line.split('=')[1].strip()
                elif line.startswith('chzzk_client_secret'):
                    self._chzzk_client_secret= line.split('=')[1].strip()
                elif line.startswith('soop_client_id'):
                    self._soop_client_id= line.split('=')[1].strip()
                elif line.startswith('soop_client_secret'):
                    self._soop_client_secret= line.split('=')[1].strip()
                    
        self._model_setting = ModelSetting(
            open_api_key=self._open_api_key,
            gpt_model=self._gpt_model)

class Head_Parser(Configure_File_Reader):
    def __init__(self) -> None:
        super().__init__()
        self._extract_host_port('./configure.txt')
        self._header = {
            'request-type' : 'default',
            'server-version' : self._version,
            'state-code' : "100",
            'detail' : 'Default'
        }
        

    def get_header(self):
        return self._header