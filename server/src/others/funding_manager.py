## 이제부터 이 파일에는 펀딩과 관련된 시스템이 모두 작성될 것임
## 파일이 길어지더라도 이 파일 안에 모두 담을 수 있다면 베스트
## 단, 결제의 경우는 이곳에서 처리하지 않고 별도로 존제함

# FundingProjectManger가 하는일은 다음과 같다.
# 1. 검색 요청에 대한 검색결과 반환 -> ProjectSearchEngine
# 2. 새로운 프로젝트 작성에 대한 도움 -> MakeNewProejctManager
# 3. 프로젝트 후원에 대한 모든 행동 -> ProjectInvesingManager
# 4. 프로젝트 추천 및 통계 시스템  ->  ProjectrecommendManager

# 위 시스템은 모두 각각의 클래스로 구분될 것임

from model import Local_Database
from others.data_domain import Project
from bintrees import AVLTree

class FundingProjectManager:
    def __init__(self, database):
        #self.__database:Local_Database = database
        self.__database = database

        #self.__project_search_engine = ProjectSearchEngine()
        #self.__make_new_project_manager = MakeNewProjectManage()
        #self.__project_investing_mananger = ProjectInverstingManager()
        #self.__project_recommend_manager = ProjectrecommendManager()

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


# 관리를 위한 프로젝트 데이터 도메인

class ManagedProject:
    def __init__(self, pid="", pname="", uid="", progress="",
                 expire_date="", make_date="", ptype="default"):
        self.pid = pid  # 프로젝트 아이디
        # 이거 필요한가? 
        self.pname = pname # 프로젝트 이름  
        self.uid = uid   # 유저 아이디
        self.progress =progress # 달성률
        self.expire_date = expire_date
        self.make_date = make_date
        self.ptype = ptype


class ProjectSearchEngine:
    def __init__(self, database):
        self.__database:Local_Database = database

        self.__project_table = []  # 최신 기준으로  정렬
        self.__project_avltree = AVLTree()  # 검색을 위한 트리
        self.__endpoint = 0  # 이건 아직 펀딩중인 프로젝트의 마지막 엔드 포인트

    # 테이블 초기화 함수
    def __init_table(self, database:Local_Database):
        # 데이터 만들기
        project_datas = database.get_all_data(target="pid")
        projects = []
        for project_data in project_datas:
            project = Project()
            project.make_with_dict(project_data)
            projects.append(project)

        # 관리용 프로젝트 생성
        for single_project in projects:
            managed_project = self.__set_new_manage_project(project=single_project)
            # 테이블에도ㅓㅓ 넣고
            # avltree에도 넣어야됨

            self.__project_avltree.insert(key=managed_project.pid, value=managed_project)
            self.__project_table.append(managed_project)

        num_project = len(self.__project_table)

        print(f'INFO<-[      {num_project} NOVA FEED IN SEARCH ENGINE NOW READY.')
        return

    # 새로운 관리용 프로젝트 만들기
    def __set_new_manage_project(self, project:Project):
            managed_project = ManagedProject()
            managed_project.pid = project.pid
            managed_project.uid = project.uid
            managed_project.pname = project.pname
            managed_project.progress = project.int_progress
            managed_project.make_date = project.make_date
            managed_project.expire_date = project.expire_date
            return managed_project


    # 1. 프로젝트 이름으로 검색하기 -> 단일
    def try_get_project_with_pname(self, pname, ptype="all", num_project=1, index=-1):
        result_pid = []
        result_index= -1

        if index == -1:
            index = len(self.__project_table)

        search_range = self.__project_table[:index][::-1]

        if index < 0 or index > len(self.__project_table):
            return result_pid, -3

        count = 0

        for i, managed_project in enumerate(search_range):
            managed_project:ManagedProject = managed_project

            if count == num_project:
                break

            if ptype == "all":
                if managed_project.pname == pname:
                    result_pid.append(managed_project.pid)
                else:
                    continue
            else:
                if managed_project.ptype == ptype:
                    if managed_project.pname == pname:
                        result_pid.append(managed_project.pid)
                    else:
                        continue
                else:
                    continue

            result_index = index - 1 - i  # 실제 self.__feed_table에서의 인덱스 계산
            count += 1

        return result_pid, result_index

    # 2. 프로젝트 최신순위로 검색
    def try_get_project_with_uname(self, ptype="all", num_project=1, index=-1):
        result_pid = []
        result_index= -1

        if index == -1:
            index = len(self.__project_table)

        search_range = self.__project_table[:index][::-1]

        if index < 0 or index > len(self.__project_table):
            return result_pid, -3

        count = 0

        for i, managed_project in enumerate(search_range):
            managed_project:ManagedProject = managed_project

            if count == num_project:
                break

            if ptype == "all":
                result_pid.append(managed_project.pid)
            else:
                if managed_project.ptype == ptype:
                    result_pid.append(managed_project.pid)
                else:
                    continue

            result_index = index - 1 - i  # 실제 self.__feed_table에서의 인덱스 계산
            count += 1

        return result_pid, result_index


    



            


