## 이제부터 이 파일에는 펀딩과 관련된 시스템이 모두 작성될 것임
## 파일이 길어지더라도 이 파일 안에 모두 담을 수 있다면 베스트
## 단, 결제의 경우는 이곳에서 처리하지 않고 별도로 존제함

# FundingProjectManger가 하는일은 다음과 같다.
# 1. 검색 요청에 대한 검색결과 반환 -> ProjectSearchEngine
# 2. 새로운 프로젝트 작성에 대한 도움 -> MakeNewProejctManager
# 3. 프로젝트 후원에 대한 모든 행동 -> ProjectInvesingManager
# 4. 프로젝트 추천 및 통계 시스템  ->  ProjectRecommandManager

# 위 시스템은 모두 각각의 클래스로 구분될 것임

#from model import Local_Database
from others.data_domain import Project

class FundingProjectManager:
    def __init__(self, database):
        #self.__database:Local_Database = database
        self.__database = database

        #self.__project_search_engine = ProjectSearchEngine()
        #self.__make_new_project_manager = MakeNewProjectManage()
        #self.__project_investing_mananger = ProjectInverstingManager()
        #self.__project_recommand_manager = ProjectRecommandManager()

    # 테스트용으로 사용되는 프로젝트 임시 반환 함수(갯수만큼 드림)
    def get_sample_project(self, num_project):
        project_datas = self.__database.get_all_data(target="pid")
        projects = []

        for project_data in project_datas:
            project = Project()
            project.make_with_dict(dict_data=project_data)
            projects.append(project)

        return projects[:num_project]
    
    # 아니 ㄹㅇ 파이썬 버전을 올려야하나? 나 왜 3.7.9 냐
    # 서버랑 버전이  안 맞아서 점점 더 두려워진다...
    # 가상환경 구축을 왜 하는지 알 수 있는 대목
