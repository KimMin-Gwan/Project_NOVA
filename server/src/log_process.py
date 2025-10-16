from requests import get
import requests
import boto3
import time
import glob
import os
from bs4 import BeautifulSoup
from io import BytesIO
from io import BytesIO
from urllib.parse import urlparse
import logging
from datetime import datetime
import shutil

import schedule

# Ncloud Object Storage 설정
access_key = "your_access_key"
secret_key = "your_secret_key"


class LogProcessor:
    def __init__(self):
        self.__log_s3_path = ''             # 스토리지에 저장 시, 로그의 s3 경로
        self.__access_log_local_path = './... /access.log'        # 저장되는 access.log 로그의 위치
        self.__error_log_local_path = './... /error.log'        # 저장되는 error.log 로그의 위치

        self.__access_log_local_storage_path = './model/local_database/log/access/'
        self.__error_log_local_storage_path = './model/local_database/log/error/'

        self.__access_log_xz_file_path = ''
        self.__error_log_xz_file_path = ''

        self.__access_log_bucket = 'nova-access-log-bucket'  # 스토리지 버킷 이름
        self.__error_log_bucket = 'nova-error-log-bucket'  # 스토리지 버킷 이름


        self.buffer = []

    # boto3 초기화
    def __init_boto3(self):
        self.__service_name = 's3'
        self.__endpoint_url = 'https://kr.object.ncloudstorage.com'
        self.__region_name = 'kr-standard'
        self.__access_key = access_key
        self.__secret_key = secret_key
        self.__s3 = boto3.client(self.__service_name,
                                 endpoint_url=self.__endpoint_url,
                                 aws_access_key_id=self.__access_key,
                                 aws_secret_access_key=self.__secret_key)
            
    # 로그 파일 존재 여부 확인
    def is_exist_file(self, path):
        if not os.path.exists(path):
            return False 
        return True
    
    # 오리지널 로그 파일을 읽어서 버퍼 리스트로 저장합니다.
    def __load_log_file(self, path):
        try:
            with open(path, 'r') as f:
                self.buffer = f.readlines()
            return True
        
        except Exception as e:
            logging.error(f"Error to Load Log files: {str(e)}")
            return False

    # 로컬 로그 파일을 저장하는 작업
    def __save_log_file(self, path):
        try:
            timestamp = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
            filename = f"log_{timestamp}.txt"

            file_path = os.path.join(path, filename)

            with open(file_path, 'w') as f:
                f.write(self.buffer)
            
            return True
        
        except Exception as e:
            logging.error(f"Error to Save Log files: {str(e)}")
            return False

    # 로그 파일 초기화
    def __clear_log_file(self, path):
        try:
            with open(path, 'w') as f:
                f.write("")
            return True

        except Exception as e:
            logging.error(f"Error to Clear Log files: {str(e)}")
            return False

    # 폴더 초기화
    def __clear_folder(self, folder_path:str):
        shutil.rmtree(folder_path, ignore_errors=True)
        os.makedirs(folder_path, exist_ok=True)
        return

    # 로그 파일 압축 (tar.xz 파일 생성)
    def compress_log_files(self, log_name:str, folder_path:str) -> bool:
        try:
            datestamp = datetime.now().strftime("%Y-%m-%d")
            filename = f"{log_name}_{datestamp}.tar.xz" # tar.xz 파일 이름
            shutil.make_archive(filename, 'xztar', folder_path) # tar.xz 파일 생성
            xz_file_path = os.path.join(folder_path, filename) # tar.xz 파일 경로
            return xz_file_path

        except Exception as e:
            logging.error(f"Error to Compress Log files: {str(e)}")
            return None

    # 로그 파일 제작
    def make_log_file(self):
        # Access 로그 파일 만들기
        self.__load_log_file(self.__access_log_local_path)  #  버퍼 로드
        self.__save_log_file(self.__access_log_local_storage_path) # 버퍼 저장
        self.__clear_log_file(self.__access_log_local_path) # 로그 파일 초기화
        self.buffer = [] # 버퍼 초기화

        # Error 로그 파일 만들기
        self.__load_log_file(self.__error_log_local_path)  #  버퍼 로드
        self.__save_log_file(self.__error_log_local_storage_path) # 버퍼 저장
        self.__clear_log_file(self.__error_log_local_path) # 로그 파일 초기화
        self.buffer = [] # 버퍼 초기화

        return

    # 로그 파일 업로드
    def upload_log_files_to_s3(self) -> bool:
        try:
            self.__init_boto3()

            access_upload_success = False
            error_upload_success = False

            # Access 로그 파일 업로드 (독립적으로 처리)
            if self.is_exist_file(self.__access_log_xz_file_path):
                try:
                    file_name = os.path.basename(self.__access_log_xz_file_path)
                    self.__s3.upload_file(
                        self.__access_log_xz_file_path,
                        self.__access_log_bucket,
                        file_name
                    )
                    access_upload_success = True
                except Exception as e:
                    logging.error(f"Error to Upload Access Log compressed file to S3: {str(e)}")
            else:
                logging.warning("Pass to Upload Access Log compressed file to S3")

            # Error 로그 파일 업로드 (독립적으로 처리)
            if self.is_exist_file(self.__error_log_xz_file_path):
                try:
                    file_name = os.path.basename(self.__error_log_xz_file_path)
                    self.__s3.upload_file(
                        self.__error_log_xz_file_path,
                        self.__error_log_bucket,
                        file_name
                    )
                    error_upload_success = True
                except Exception as e:
                    logging.error(f"Error to Upload Error Log compressed file to S3: {str(e)}")
            else:
                logging.warning("Pass to Upload Error Log compressed file to S3")

            all_success = access_upload_success and error_upload_success
            xor_success = access_upload_success ^ error_upload_success # XOR

            if all_success:
                logging.info("Uploaded Log Compressed File. (All files uploaded successfully)")
            elif xor_success:
                logging.info("Uploaded Log Compressed File. (Some files may fail to upload)")
            else:
                logging.warning("Failed to Upload Log Compressed File.")

            return True

        except Exception as e:
            logging.error(f"Error to Upload Log files to S3: {str(e)}")
            return False

    # 로그 폴더 초기화
    def clear_log_folders(self):
        self.__clear_folder(self.__access_log_local_storage_path)
        self.__clear_folder(self.__error_log_local_storage_path)
        return

    # 업로드 프로세스
    def upload_process(self):
        self.__access_xz_file_path = self.compress_log_files(log_name="supernova_access_log", folder_path=self.__access_log_local_storage_path)
        self.__error_xz_file_path = self.compress_log_files(log_name="supernova_error_log", folder_path=self.__error_log_local_storage_path)

        self.upload_log_files_to_s3()
        self.clear_log_folders()

        return

    # 로그 제작 프로세스 실행
    def make_log_file_process(self):
        self.make_log_file()
        return


def main():
    log_processor = LogProcessor()


    schedule.every().day.at("03:00").do(log_processor.upload_process)
    schedule.every(5).minutes.do(log_processor.make_log_file_process)
    
    while True:
        schedule.run_pending()
        time.sleep(1)
    
    return
    
if __name__ == "__main__":
    main()















    # def read_nohup_log(self):
    #     """nohup.out 파일에서 새로운 로그 내용을 읽어옴"""
    #     try:
    #         if not os.path.exists(self.__nohup_log_path):
    #             logging.warning(f"nohup 로그 파일이 존재하지 않습니다: {self.__nohup_log_path}")
    #             return None

    #         with open(self.__nohup_log_path, 'r', encoding='utf-8', errors='ignore') as f:
    #             f.seek(self.__last_position)
    #             new_content = f.read()

    #             if new_content:
    #                 self.__last_position = f.tell()
    #                 return new_content.strip()
    #             else:
    #                 return None

    #     except Exception as e:
    #         logging.error(f"로그 파일 읽기 오류: {str(e)}")
    #         return None

    # def create_log_file(self, log_content):
    #     """로그 내용을 새로운 파일로 생성"""
    #     try:
    #         self.__ensure_directories()

    #         # 현재 날짜와 시간으로 파일명 생성
    #         timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    #         filename = f"log_{timestamp}.txt"
    #         file_path = os.path.join(self.__processed_logs_dir, filename)

    #         with open(file_path, 'w', encoding='utf-8') as f:
    #             f.write(log_content)

    #         self.__log_path = file_path
    #         return file_path

    #     except Exception as e:
    #         logging.error(f"로그 파일 생성 오류: {str(e)}")
    #         return None

    # def upload_to_object_storage(self):
    #     """생성된 로그 파일을 Object Storage에 업로드"""
    #     try:
    #         if not self.__log_path or not os.path.exists(self.__log_path):
    #             logging.error("업로드할 로그 파일이 존재하지 않습니다.")
    #             return False

    #         self.__init_boto3()

    #         # 파일명에서 확장자 제거 후 타임스탬프로 저장
    #         filename = os.path.basename(self.__log_path)
    #         timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    #         object_name = f"logs/{timestamp}_{filename}"

    #         self.__s3.upload_file(
    #             self.__log_path,
    #             self.__log_bucket,
    #             object_name,
    #             ExtraArgs={'ACL': 'public-read'}
    #         )

    #         logging.info(f"로그 파일 업로드 완료: {object_name}")
    #         return True

    #     except Exception as e:
    #         logging.error(f"Object Storage 업로드 오류: {str(e)}")
    #         return False

    # def clear_nohup_log(self):
    #     """nohup.out 파일의 내용을 초기화"""
    #     try:
    #         # 파일 내용을 비움
    #         with open(self.__nohup_log_path, 'w') as f:
    #             f.write("")

    #         # 마지막 위치도 초기화
    #         self.__last_position = 0
    #         logging.info("nohup 로그 파일 초기화 완료")

    #     except Exception as e:
    #         logging.error(f"nohup 로그 파일 초기화 오류: {str(e)}")

    # def process_logs(self):
    #     """전체 로그 처리 프로세스 실행"""
    #     try:
    #         # 1. 새로운 로그 내용 읽기
    #         log_content = self.read_nohup_log()

    #         if not log_content:
    #             logging.info("새로운 로그 내용이 없습니다.")
    #             return False

    #         # 2. 로그 파일 생성
    #         log_file = self.create_log_file(log_content)

    #         if not log_file:
    #             logging.error("로그 파일 생성에 실패했습니다.")
    #             return False

    #         # 3. Object Storage에 업로드
    #         if not self.upload_to_object_storage():
    #             logging.error("로그 파일 업로드에 실패했습니다.")
    #             return False

    #         # 4. 원본 로그 파일 초기화
    #         self.clear_nohup_log()

    #         logging.info("로그 처리 완료")
    #         return True

    #     except Exception as e:
    #         logging.error(f"로그 처리 중 오류 발생: {str(e)}")
    #         return False

    # def save_log(self, log_content):
    #     """기존 호환성을 위한 메서드"""
    #     self.__init_boto3()

    #     if not self.__log_path:
    #         return False

    #     self.__s3.upload_file(
    #         self.__log_path,
    #         self.__log_bucket,
    #         self.__log_path,
    #         ExtraArgs={'ACL': 'public-read'}
    #     )
    #     return True


# 사용 예시 및 테스트 함수
def main():
    """메인 실행 함수"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

    processor = LogProcessor()

    # 주기적으로 로그 처리 (예: 5분마다)
    while True:
        processor.process_logs()
        time.sleep(300)  # 5분 대기


if __name__ == "__main__":
    main()