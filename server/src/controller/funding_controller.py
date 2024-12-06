from model.funding_model import *
from model import Local_Database, BaseModel
from fastapi import HTTPException, status
from others import FundingProjectManager

class Funding_Controller:
    # 홈화면에서 맞춤 태그 제공
    def get_home_banner(self,
        database:Local_Database,
        request,
        funding_project_manager:FundingProjectManager) -> BaseModel:

        model = FundingProjectBannerModel(database=database)

        # 유저가 있으면 세팅
        if request.jwt_payload != "":
            model.set_user_with_email(request=request.jwt_payload)

        ## 해야되는일 여기 적으면 됨
        #model.get_sample_tag(
            #funding_project_manager=funding_project_manager,
            #fid=request.data_payload.fid,
            #num_project=num_project)

        model.get_sample_project(
            num_project=3,
            funding_project_manager=funding_project_manager
            )
        
        model.set_banner_items()

        return model

    # 홈화면에서 맞춤 태그 제공
    def get_recommend_tag(self,
        database:Local_Database,
        request,
        funding_project_manager:FundingProjectManager,
        num_project=1) -> BaseModel:

        model = FundingProjectTagModel(database=database)

        # 유저가 있으면 세팅
        if request.jwt_payload != "":
            model.set_user_with_email(request=request.jwt_payload)

        ## 해야되는일 여기 적으면 됨
        #model.get_sample_tag(
            #funding_project_manager=funding_project_manager,
            #fid=request.data_payload.fid,
            #num_project=num_project)

        # 샘플
        model.get_sample_tag()

        return model

    # 추천 프로젝트 제공
    def try_test_func(self,
        database:Local_Database,
        funding_project_manager:FundingProjectManager,
        num_project=1) -> BaseModel:

        model = FundingProjectModel(database=database)

        # 샘플
        model.get_sample_project(
            num_project=num_project,
            funding_project_manager=funding_project_manager
            )

        return model

    # 추천 프로젝트 제공
    def get_sample_project(self,
        database:Local_Database,
        request,
        funding_project_manager:FundingProjectManager,
        num_project=1) -> BaseModel:

        model = FundingProjectModel(database=database)

        # 유저가 있으면 세팅
        if request.jwt_payload != "":
            model.set_user_with_email(request=request.jwt_payload)

        ## 해야되는일 여기 적으면 됨
        #model.try_search_feed_with_fid(
            #funding_project_manager=funding_project_manager,
            #fid=request.data_payload.fid,
            #num_project=num_project)

        # 샘플
        model.get_sample_project(
            num_project=num_project,
            funding_project_manager=funding_project_manager
            )

        return model
    
    # 베스트 프로젝트 모두 보기에서 필요한 데이터
    # 다른건 없고 [프로젝트 성공 사례의 횟수] 이걸 주면되는듯
    def get_best_funding_section(self,
        database:Local_Database,
        funding_project_manager:FundingProjectManager):

        model = HomeBestFundingSectionModel(database=database)

        # 프로젝트 성공 사례의 횟수를 받아와야됨

        return model


    # 홈화면의 노바 펀딩 알아보기에서 줄것
    # 1. 최애 펀딩 알아보기 조회수
    # 2. 일반 펀딩 알아보기 조회수
    # 3. 성공하는 펀딩 기술 조회수
    def get_nova_funding_info(self,
        database:Local_Database,
        funding_project_manager:FundingProjectManager):

        model = HomeFundingInfoSectionModel(database=database)

        # 프로젝트 성공 사례의 횟수를 받아와야됨

        return model
    
    def try_upload_new_project(self,
        database:Local_Database, 
        request,
        funding_project_manager:FundingProjectManager
        ):
        model = EditProjectModel()
        
    def get_project_detail(self,
        database:Local_Database, 
        request,
        funding_project_manager:FundingProjectManager
        ) -> BaseModel:

        model = ProjectDetailModel(database=database)

        if model.get_project_meta_data(request.data_payload.pid):
            model.get_project_body_data(project_manager=funding_project_manager)

        return model
    

