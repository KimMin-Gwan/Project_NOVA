from typing import Union, Optional
from others.data_domain import User, Bias, Schedule
import pandas as pd

# 이건 인터페이스임 -> 모듈 대가리임
# 필요한 시스템을 구성해보자
# 1. 추천 시스템 -> 특정 input에 대한 적절한 output을 골라주는 시스템
#   - bias, schedule에 대한 추천 결과가 나와야함 (결과값은 반드시 1개)
#   - param은 user, bias, keyword(string) 정보가 포함될 수 있음

# 2. 광고 시스템 -> 사용자에 최적화된 광고를 제공하거나 랜덤하게 제공하는 서비스
#   - 비동기 시스템으로 구축해서 실시간 처리 가능하게 할 것
#   - 비동기 시스템인 만큼 시스템 종료와 함께 데이터가 DB에 저장되게 해야됨
#   - 내부 광고에서는 bias가 설정한 광고 정보에 대한 내용이 제출될 것임
#   - 외부 광고에서는 client가 설정한 광고 정보에 대한 내용이 제출될 것임

# 두 시스템은 공통적으로 중복 제거 기능이 포함되어 있어야함.
# 두 시스템은 공통적으로 평시에 데이터 베이스에 요청을 하지 않아야함

# 추천 시스템 기능 목록
# 1. bias 추천 - user 정보를 기반으로
# 2. bias 추천 - bias 정보를 기반으로
# 3. bias 추천 - keyword를 기반으로
# 4. schedule 추천 - user 정보를 기반으로
# 5. schedule 추천 - bias 정보를 기반으로
# 6. schedule 추천 - keyword를 기반으로

# 광고 시스템 기능 목록
# 1. 포인트 충전 및 소모 기능
# 2. 내부 광고 노출 기능
# 3. 외부 광고 노출 기능
# 4. 내부 광고 설정 기능
# 5. 외부 광고 설정 기능

# *결제 기능은 별도

class NOVA_AD:
    def __init__(self, database):
        self._db = database
        
class SearchResult:
    def __init__(self, body:Optional[Union[Bias,Schedule]]):
        self.flag = False
        self.body = body

# 광고 시스템에서도 쓸수 있게 구성할 것
class SystemBase:
    def __init__(self, database, keyword_bag):
        self._db = database
        self._keyword_bag = keyword_bag
        
    # 중복검사기 (단일 개체)
    def _check_duplicate_single_data(self, base_list:list, target_data:Union[str, float, int]) -> tuple:
        flag = False
        index = []
        
        for i, single_target_data in enumerate(target_data):
            if single_target_data in base_list:
                flag = True
                index.append(i)
            else:
                continue
        
        return flag, index
    
    # 중복검사기 (리스트 개체)
    def _check_duplicate_multi_data(self, base_list:list, target_data:Union[tuple, list]=[]):
        flag = False
        
        if target_data in base_list:
            flag = True
        else:
            flag = False
        
        return flag
    

# 검색에 사용될 키워드 백
# 예시 -> lol, 롤, 리그오브레전드, 유희왕, 오버워치, 옵치, overwatch => "게임" 카테고리
class KeywordBag:
    def __init__(self):
        self.__keyword_df = pd.DataFrame()
    
    
        
class RecommendSystem(SystemBase):
    def __init__(self, database):
        super().__init__(database=database)
        
    # search_type으로 Bias를 받을건지 Schedule을 받을 건지 정해야됨
    def recommand_based_random(self, history:list=[], search_type=Union[Bias, Schedule]) -> SearchResult:
        
        if isinstance(search_type, Bias):
            result = callable()
        
        elif isinstance(search_type, Schedule):
            result = callable()
        
        
        return SearchResult()

    # search_type으로 Bias를 받을건지 Schedule을 받을 건지 정해야됨
    def recommand_based_user(self, user:User, history:list=[], search_type=Union[Bias, Schedule]) -> SearchResult:
        
        if isinstance(search_type, Bias):
            result = callable(user)
        
        elif isinstance(search_type, Schedule):
            result = callable(user)
        
        
        return SearchResult()

    def recommand_based_bias(self, bias:Bias, history:list=[], search_type=Union[Bias, Schedule]) -> SearchResult:
        if isinstance(search_type, Bias):
            result = callable(bias)
        
        elif isinstance(search_type, Schedule):
            result = callable(bias)
        
        
        return SearchResult()

    def recommand_based_keyword(self, keyword:str, history:list=[], search_type=Union[Bias, Schedule]) -> SearchResult:
        if isinstance(search_type, Bias):
            result = callable(keyword)
        
        elif isinstance(search_type, Schedule):
            result = callable(keyword)
        
        
        return SearchResult()
