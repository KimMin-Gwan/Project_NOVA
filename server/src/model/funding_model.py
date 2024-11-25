from model.base_model import BaseModel
from model import Local_Database
#from others.data_domain import Alert
from others import FundingProjectManager, Project
from pprint import pprint

class ProjectBanner:
    def __init__(self):
        pass

class FundingProjectBannerModel(BaseModel):
    def __init__(self, database:Local_Database) -> None:
        super().__init__(database)
        self._project = []
        self._banner = []

    def get_sample_project(self, num_project, funding_project_manager:FundingProjectManager):
        self._project = funding_project_manager.get_sample_project(num_project=num_project)
        return
    
    # 배너 데이터로 만들어서 주기
    def set_banner_items(self):
        pass

    def get_response_form_data(self, head_parser):
        body = {
            'banner' : self._make_dict_list_data(list_data=self._banner),
        }

        response = self._get_response_data(head_parser=head_parser, body=body)
        return response


# 펀딩 프로젝트 관련 데이터는 다 이걸로 보냄
class FundingProjectModel(BaseModel):
    def __init__(self, database:Local_Database) -> None:
        super().__init__(database)
        self._project = []
        self._key = -1

    def get_sample_project(self, num_project, funding_project_manager:FundingProjectManager):
        self._project = funding_project_manager.get_sample_project(num_project=num_project)
        self._project = self._set_progress(project_list=self._project)
        return

    # 유저가 참여한 프로젝트 인지 확인할것
    # 유저가 참여한 프로젝트인지 확인할 필요가 있을 때 이 함수를 통할 것
    def _is_user_interacted(self, user, project:list):
        result = project
        return result

    # 참여도에 대한 백불율 조사
    # 지금은 integaer 값이 나옴
    # 필요하면 round로 하삼
    def _set_progress(self, project_list:list):
        for project in project_list:
            project:Project = project

            now = project.now_progress
            goal = project.goal_progress

            if goal > 0:
                percentage = int((now/goal) * 100)
                #percentage = round((now/goal) * 100, 2)
            else:
                percentage = 0
    
            project.int_progress = percentage

        return project_list

    def get_response_form_data(self, head_parser):
        body = {
            'project' : self._make_dict_list_data(list_data=self._project),
            'key' : self._key
        }

        response = self._get_response_data(head_parser=head_parser, body=body)
        return response


# 이건 펀딩 프로젝트에서 맞춤 태그 줄때 쓰는거
class FundingProjectTagModel(BaseModel):
    def __init__(self, database:Local_Database) -> None:
        super().__init__(database)
        self._tag = []

    def get_sample_tag(self):
        self._tag = ["시연", "귀여움", "QWER"]
        return

    def get_response_form_data(self, head_parser):
        body = {
            'tag' : self._tag
        }

        response = self._get_response_data(head_parser=head_parser, body=body)
        return response


# 베스트 프로젝트 모두 보기에서 필요한 데이터
# 다른건 없고 [프로젝트 성공 사례의 횟수] 이걸 주면되는듯
class HomeBestFundingSectionModel(BaseModel):
    def __init__(self, database:Local_Database) -> None:
        super().__init__(database)
        self._num_project = 12

    def get_response_form_data(self, head_parser):
        body = {
            'num_project' : self._num_project
        }

        response = self._get_response_data(head_parser=head_parser, body=body)
        return response


# 홈화면의 노바 펀딩 알아보기에서 줄것
# 1. 최애 펀딩 알아보기 조회수
# 2. 일반 펀딩 알아보기 조회수
# 3. 성공하는 펀딩 기술 조회수
class HomeFundingInfoSectionModel(BaseModel):
    def __init__(self, database:Local_Database) -> None:
        super().__init__(database)
        self._bias_funding_view= 22
        self._fan_funding_view= 4850
        self._good_funding_view= 410

    def get_response_form_data(self, head_parser):
        body = {
            'bias_funding_view' : self._bias_funding_view,
            'fan_funding_view' : self._fan_funding_view,
            'good_funding_view' : self._good_funding_view
        }

        response = self._get_response_data(head_parser=head_parser, body=body)
        return response