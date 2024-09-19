''' Client data
header = {
    'request-type' :'default',
    'client-version' : 'v1.0.1',
    'client-ip' : '127.0.0.1',
    'uid' : '1234-abcd-5678',
    'endpoint' : '/endpoint'
}
'''

class Configure_File_Reader:
    def __init__(self) -> None:
        self._host = ''
        self._port = 0
        self._version = ''
        self._num_fclass = 0
        self._fclasses = []

    def _extract_host_port(self, file_path='./configure.txt'):
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                if line.startswith('HOST'):
                    self._host = line.split('=')[1].strip()
                elif line.startswith('PORT'):
                    self._port = int(line.split('=')[1].strip())
                elif line.startswith('VERSION'):
                    self._version = line.split('=')[1].strip()
                elif line.startswith('num_fclass'):
                    self._num_fclass = int(line.split('=')[1].strip())
                elif line.startswith('fclass'):
                    # fclass 데이터를 2차원 배열로 저장
                    fclass_data = line.split('=')[1].strip().strip('[]').split(',')
                    fclass_data = [item.strip() for item in fclass_data]
                    self._fclasses.append(fclass_data)

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