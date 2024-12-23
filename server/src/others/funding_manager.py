## 이제부터 이 파일에는 펀딩과 관련된 시스템이 모두 작성될 것임
## 파일이 길어지더라도 이 파일 안에 모두 담을 수 있다면 베스트
## 단, 결제의 경우는 이곳에서 처리하지 않고 별도로 존제함

# FundingProjectManger가 하는일은 다음과 같다.
# 1. 검색 요청에 대한 검색결과 반환 -> ProjectSearchEngine
# 2. 새로운 프로젝트 작성에 대한 도움 -> MakeNewProejctManager
# 3. 프로젝트 후원에 대한 모든 행동 -> ProjectInvesingManager
# 4. 프로젝트 추천 및 통계 시스템  ->  ProjectrecommendManager

# 위 시스템은 모두 각각의 클래스로 구분될 것임

#from model import Local_Database
from others.data_domain import Project
from bintrees import AVLTree
from requests import get
from datetime import date, datetime

class FundingProjectManager:
    def __init__(self, database):
        #self.__database:Local_Database = database
        self.__database = database

        self.__project_search_engine = ProjectSearchEngine(database=database)
        self.__storage_connection = ObjectStorageConnection()
        #self.__project_investing_mananger = ProjectInverstingManager()
        #self.__project_recommend_manager = ProjectrecommendManager()

    def _calculate_deadline(self, project):
        deadline_diff = datetime.strptime(project.expire_date, "%Y/%m/%d").date() - date.today()
        # print(deadline_diff.days)
        return deadline_diff.days

    # 테스트용으로 사용되는 프로젝트 임시 반환 함수(갯수만큼 드림)
    def get_sample_project(self, num_project):
        project_datas = self.__database.get_all_data(target="pid")
        projects = []

        for project_data in project_datas:
            project = Project()
            project.make_with_dict(dict_data=project_data)
            projects.append(project)

        return projects[:num_project]

    # 프로젝트 바디 데이터를 GET 하는 함수
    def get_project_body_data(self, pid):
        body_data = self.__storage_connection.get_project_body(pid=pid)
        return body_data

    # 미완성부분
    def get_projects_with_tags(self, tag:str, num_project):
        project_datas = self.__database.get_all_data(target="pid")

    # 최애의 펀딩 프로젝트들을 가져옴
    def get_projects_by_bias(self, num_project):
        project_datas = self.__database.get_datas_with_key(target="pid", key="ptype", key_datas=["bias"])
        projects = []

        for project_data in project_datas:
            project = Project()
            project.make_with_dict(project_data)
            projects.append(project)

        # 가장 최근에 생성 된 프로젝트들은 PID가 가장 크다. 따라서, 시간 순 정렬을 PID로 할 수있다.
        # project에 기재된 정보는 모두 문자열이므로 형변환을 취해야한다.
        projects_sorted = sorted(projects, key=lambda p: int(p.pid), reverse=True)

        return projects_sorted[:num_project]

    # 팬들의 펀딩 프로젝트들을 가져옴
    def get_projects_by_fan(self, num_project):
        project_datas = self.__database.get_datas_with_key(target="pid", key="ptype", key_datas=["fan"])
        projects = []

        for project_data in project_datas:
            project = Project()
            project.make_with_dict(project_data)
            projects.append(project)

        # 가장 최근에 생성 된 프로젝트들은 PID가 가장 크다. 따라서, 시간 순 정렬을 PID로 할 수있다.
        # project에 기재된 정보는 모두 문자열이므로 형변환을 취해야한다.
        projects_sorted = sorted(projects, key=lambda p: int(p.pid), reverse=True)

        return projects_sorted[:num_project]

    # 가장 인기가 많은 프로젝트들을 가져옴
    def get_projects_best(self):
        project_datas = self.__database.get_all_data(target="pid")
        projects = []

        for project_data in project_datas:
            project = Project()
            project.make_with_dict(project_data)

            # 프로젝트들 중 성공한 프로젝트들을 반환함
            # 성공한 기준은 목표금액과 현재 펀딩액을 비교해, 펀딩액이 목표액을 넘긴 경우를 반환함
            if project.now_progress >= project.goal_progress:
                projects.append(project)

        return projects

    # 완료된 펀딩 프로젝트 표시
    def get_done_projects(self, num_project):
        # 가지고 있는 모든 프로젝트들을 들고와서
        project_datas = self.__database.get_all_data(target="pid")
        projects = []
        result_list = []

        # 프로젝트가 목표가 달성되어 있는지 확인, 펀딩 목표금액을 달성한 상태에서 펀딩이 마감되면 목표 달성이라고 판정한다.
        # 즉, 펀딩이 마감된 프로젝트만 선별해야한다.
        for project_data in project_datas:
            project = Project()
            project.make_with_dict(project_data)

            # 프로젝트가 남은 기한이 음수인지 확인. 당일까지는 계속 열어둘 것으로 한다. 만약 시간까지 고려한다면 이게 바뀌게 되겠지
            # 현재는 펀딩이 마감된 프로젝트만 골라야하므로, 음수만 고려하는 방안으로 작성함
            if self._calculate_deadline(project) < 0:
                projects.append(project)

        # 프로젝트 펀딩이 목표금액을 넘긴 경우를 찾아온다.
        for proj in projects:
            if proj.now_progress >= proj.goal_progress:
                result_list.append(proj)

        # 이렇게 가져온 성공한 프로젝트는 가장 최근의 날짜를 가진 것이 먼저오도록 한다.
        projects_sorted = sorted(result_list, key=lambda p: p.pid, reverse=True)

        # num_project의 개수가 -1이라면 찾은 값 모두를 들고와야 한다.
        if num_project == -1:
            return projects_sorted
        return projects_sorted[:num_project]

    # 마감기한이 별로 남지 않은 프로젝트 표시
    def get_near_projects(self, num_project):
        project_datas = self.__database.get_all_data(target="pid")
        projects = []
        result_list = []

        # 마감이 끝나지 않았는지 확인하여 프로젝트를 추가한다. (날짜가 지난 프로젝트들은 모두 꺼내면 안된다.)
        for project_data in project_datas:
            project = Project()
            project.make_with_dict(project_data)
            # 현재 프로젝트 중, 이미 목표가 달성한 프로젝트에 대해서는 제외한다.
            if self._calculate_deadline(project) >= 0:
                projects.append(project)

        # 프로젝트 종료 날짜가 아직 멀었다면, 값이 크다
        # 여기서, 날짜가 가장 빨리오는 순서대로 해야한다.
        projects_sorted = sorted(projects, key=lambda p: datetime.strptime(p.expire_date, "%Y/%m/%d").date())

        if num_project == -1:
            return projects_sorted

        return projects_sorted[:num_project]

# 건들지 않음
# Project Body (프로젝트 상세보기 화면 받아옴)
class ObjectStorageConnection:
    def __init__(self):
        self.__endpoint = "https://kr.object.ncloudstorage.com/nova-project-image/"

    def get_project_body(self, pid):
        
        pid = "5"

        url = self.__endpoint + pid + ".html"
        response = get(url=url)
        html_content = response.content.decode("utf-8")
        #html_content = response.content
        return html_content



# 관리를 위한 프로젝트 데이터 도메인
class ManagedProject:
    def __init__(self, pid="", pname="", uid="", progress="",
                 expire_date="", make_date="", ptype="default", ftype="",
                 body_url= ""):
        self.pid = pid  # 프로젝트 아이디
        # 이거 필요한가? 
        self.pname = pname # 프로젝트 이름  
        self.uid = uid   # 유저 아이디
        self.progress =progress # 달성률
        self.expire_date = expire_date
        self.make_date = make_date
        self.ptype = ptype # 최애 or 덕질
        self.ftype = ftype # 모금 or 참여
        self.body_url =body_url 

class ProjectSearchEngine:
    def __init__(self, database):
        #self.__database:Local_Database = database
        self.__database = database

        self.__project_table = []  # 최신 기준으로  정렬
        self.__project_avltree = AVLTree()  # 검색을 위한 트리

        self.__endpoint = 0  # 이건 아직 펀딩중인 프로젝트의 마지막 엔드 포인트
        self.__init_table(database=database)

    # string to datetime
    def __get_date_str_to_object(self, str_date):
        #date_obj = datetime.strptime(str_date, "%Y/%m/%d-%H:%M:%S")
        date_obj = datetime.strptime(str_date, "%Y/%m/%d")
        return date_obj

    # datetime to string
    def __get_date_object_to_str(self, object:datetime):
        #formatted_str = object.strftime("%Y/%m/%d-%H:%M:%S")
        formatted_str = object.strftime("%Y/%m/%d")
        return formatted_str

    # 테이블 초기화 함수
    #def __init_table(self, database:Local_Database):
    def __init_table(self, database):
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

        # 연산에 속도 향상을 위해 주로 연산하는 범위를 지정
        index = 0
        now = datetime.now()
        for i, managed_project in enumerate(self.__project_table[::-1]):
            managed_project:ManagedProject = managed_project
            if managed_project.expire_date > now:
                index = i
        # 유효 기간이 끝난 데이터가 있는 제일 끝 데이터를 쓸것
        self.__endpoint = index 
        print(f'INFO<-[      {num_project} NOVA PROJECT IN SEARCH ENGINE NOW READY.')
        print(f"INFO<-[      {self.__endpoint} IS THE LAST PROJECT THAT WORKING")
        return

    # 새로운 관리용 프로젝트 만들기
    def __set_new_manage_project(self, project:Project):
            managed_project = ManagedProject()
            managed_project.pid = project.pid
            managed_project.uid = project.uid
            managed_project.pname = project.pname
            managed_project.progress = project.int_progress
            managed_project.make_date = self.__get_date_str_to_object(project.make_date)
            managed_project.expire_date = self.__get_date_str_to_object(project.expire_date)
            managed_project.ptype = project.ptype
            managed_project.ftype = project.ftype
            managed_project.body_url = project.body_url
            return managed_project

    # 0. 프로젝트 ID로 검색하기 -> 단일
    def try_get_project_with_pid(self, pid):
        return self.__project_avltree.get(key=pid)

    # 1. 프로젝트 이름으로 검색하기 -> 단일
    # 이건 유사도 검사해서 나오게 세팅해야됨
    def try_get_project_with_pname(self, pname):
        return

    # 2. 프로젝트 최신순위로 검색
    # ptype == "bias", "fan"
    def try_get_project_as_latest(self, ptype="all", ftype="all", num_project=1, index=-1):
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
                if ftype == "all":
                    result_pid.append(managed_project.pid)
                else:
                    if managed_project.ftype == ftype:
                        result_pid.append(managed_project.pid)
                    else:
                        continue
            else:
                if managed_project.ptype == ptype:
                    if ftype == "all":
                        result_pid.append(managed_project.pid)
                    else:
                        if managed_project.ftype == ftype:
                            result_pid.append(managed_project.pid)
                        else:
                            continue
                else:
                    continue

            result_index = index - 1 - i  # 실제 self.__feed_table에서의 인덱스 계산
            count += 1

        return result_pid, result_index

    # 3. 프로젝트 마감 순위로 검색
    # ptype == "bias", "fan"
    def try_get_project_not_expired(self, ptype="all", ftype ="all", num_project=1, index=-1):
        result_pid = []
        result_index= -1

        # 1. 마감 순위로 테이블을 만들어야됨
        # 2. 그걸 기준으로 데이터를 찾아낼 것
        # 3. 인덱스도 모두 여기서 만든 테이블을 기준으로 줘야됨
        
        # 엔드포인트를 넘어간 인덱스는 있을 수 없지 않을까? 
        if index > self.__endpoint:
            return result_pid, -3


        # 우선 만료안된 프로젝트 기준으로 자르고
        filtered_range = self.__project_table[:self.__endpoint][::-1]

        now = datetime.now()

        search_range = []

        # 만료가 안된 애들만 집어넣어야됨
        for managed_project in filtered_range:
            managed_project:ManagedProject=managed_project
            if managed_project.expire_date > now:
                search_range.append(managed_project)

        # 처음 받는 데이터면 index는 만료안된 마지막 프로젝트로
        if index == -1:
            index = len(search_range)

        # 이제 조사할 만큼 잘라야됨
        search_range = self.__project_table[:index]

        # 말도안되는 경우 필터링
        if index < 0 or index > len(self.__project_table):
            return result_pid, -3

        # 찾아서 넣기
        count = 0
        for i, managed_project in enumerate(search_range):
            managed_project:ManagedProject = managed_project

            if count == num_project:
                break

            if ptype == "all":
                if ftype == "all":
                    result_pid.append(managed_project.pid)
                else:
                    if managed_project.ftype == ftype:
                        result_pid.append(managed_project.pid)
                    else:
                        continue
            else:
                if managed_project.ptype == ptype:
                    if ftype == "all":
                        result_pid.append(managed_project.pid)
                    else:
                        if managed_project.ftype == ftype:
                            result_pid.append(managed_project.pid)
                        else:
                            continue
                else:
                    continue

            # 실제 self.__feed_table에서의 인덱스 계산
            result_index = index - 1 - i 
            count += 1

        return result_pid, result_index

    
    # 3. 프로젝트 이미 달성한 애들만
    # ptype == "bias", "fan"
    def try_get_project_with_achievement(self, ptype="all", ftype="all", num_project=1, index=-1):
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
                if ftype =="all":
                    if managed_project.progress > 100:
                        result_pid.append(managed_project.pid)
                    else:
                        continue
                else:
                    if managed_project.ftype == ftype:
                        if managed_project.progress > 100:
                            result_pid.append(managed_project.pid)
                        else:
                            continue
                    else:
                        continue
            else:
                if managed_project.ptype == ptype:
                    if ftype == "all":
                        if managed_project.progress > 100:
                            result_pid.append(managed_project.pid)
                        else:
                            continue
                    else:
                        if managed_project.ftype == ftype:
                            if managed_project.progress > 100:
                                result_pid.append(managed_project.pid)
                            else:
                                continue
                        else:
                            continue
                else:
                    continue

            result_index = index - 1 - i  # 실제 self.__feed_table에서의 인덱스 계산
            count += 1

        return result_pid, result_index

