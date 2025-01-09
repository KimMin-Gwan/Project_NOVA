from requests import get
import boto3 
import time
import glob
import os


# 건들지 않음
# Project Body (프로젝트 상세보기 화면 받아옴)
class ObjectStorageConnection:
    def __init__(self):
        self.__project_bucket = "nova-project-image"
        self.__feed_bucket= "nova-feed-project-body"

    def __init_boto3(self):
        self.__service_name = 's3'
        self.__endpoint_url = 'https://kr.object.ncloudstorage.com'
        self.__region_name = 'kr-standard'
        self.__access_key = 'eeJ2HV8gE5XTjmrBCi48'
        self.__secret_key = 'zAGUlUjXMup1aSpG6SudbNDzPEXHITNkEUDcOGnv'
        self.__s3 = boto3.client(self.__service_name,
                                 endpoint_url=self.__endpoint_url,
                                 aws_access_key_id=self.__access_key,
                                 aws_secret_access_key=self.__secret_key)

    # 프로젝트 바디 부분 불러오는 부분
    def get_project_body(self, pid):
        
        pid = "5"
        target_url = self.__project_endpoint + pid + ".html"
        response = get(url=target_url)
        html_content = response.content.decode("utf-8")
        #html_content = response.content
        return html_content
    
    # 피드 바디 데이터 불러오는 부분
    def get_feed_body(self, fid):
        print("??????")
        
        target_url = self.__endpoint_url + "/" + self.__feed_bucket + fid + ".html"
        print("why this code did not works shit ")
        response = get(url=target_url)
        print("??")
        print(response)
        html_content = response.content.decode("utf-8")
        #html_content = response.content
        
        print(html_content)
        return html_content
    
    # 피드 바디 데이터 만들기
    def make_new_feed_body_data(self, fid, body):
        self.__init_boto3()

        # 파일 이름 생성 (e.g., saved_file.html)
        path = './model/local_database/feed_temp_file/'
        file_name = f"{fid}.html"
        file_path = path + file_name

        # HTML 파일로 저장
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(body)

        self.__s3.upload_file(file_path,
                                self.__feed_bucket,
                                file_name,
                                ExtraArgs={'ACL': 'public-read'})

        url = self.__endpoint_url + "/" + self.__feed_bucket + "/" + file_name

        self.delete_temp_file(path)

        return url
        
    def delete_temp_file(self, path):
        time.sleep(0.1)
        files = glob.glob(os.path.join(path, '*'))
        for file in files:
            if os.path.isfile(file):
                os.remove(file)
        return

