from fastapi import HTTPException, status
YELLOW = "\033[33m"
RESET = "\033[0m"
class Master_View():
    def __init__(self, head_parser) -> None:
        self._head_parser = head_parser
        self._endpoint = ''
        self._credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not Validate credentials",
            headers={"WWW-Authenticate" : "Bearer"}
        )

    def __call__(self) -> None:
        print(f'{YELLOW}INFO{RESET}<-[      Server Route http://Server_HOST:PORT{self._endpoint} Ready.')



class RequestHeader:
    def __init__(self, request) -> None:
        header = request['header']

        self.request_type = header['request-type']
        self.client_version = header['client-version']
        self.client_ip = header['client-ip']
        self.uid = header['uid']
        self.endpoint = header['endpoint']