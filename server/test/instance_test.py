from pprint import pprint

data = {
    "content": "사실 구라얌",
    "detail":"가세요라"
}


result = f"아니 그래서 이게 뭔데 씹덕아 {data}"

pprint(type(result))



# 인터페이스
class 포유류:
    def __init__(self):
        self.bname = "신대홍"
        self.bid = "1234"
        
class 토끼(포유류):
    def __init__(self):
        self.extra1 = "banana"
        
class 사슴(포유류):
    def __init__(self):
        self.extra2 = "hambugi hu"
        