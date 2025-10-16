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
        self.__access_log_local_path = '/home/nova/Project_NOVA/server/log/access.log'          # 저장되는 access.log 로그의 위치
        self.__error_log_local_path = '/home/nova/Project_NOVA/server/log/error.log'            # 저장되는 error.log 로그의 위치

        self.__access_log_local_storage_path = '/home/nova/Project_NOVA/server/log/access/'     # 따로 만들어진 로그파일 저장 경로 1 
        self.__error_log_local_storage_path = '/home/nova/Project_NOVA/server/log/error/'       # 따로 만들어진 로그파일 저장 경로 2

        self.__access_log_xz_file_path = ''     # 로그 파일 압축 경로 1
        self.__error_log_xz_file_path = ''      # 로그 파일 압축 경로 2 

        self.__access_log_bucket = 'nova-access-log-bucket'     # 스토리지 버킷 이름
        self.__error_log_bucket = 'nova-error-log-bucket'       # 스토리지 버킷 이름

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
        # 로그 파일 압축
        self.__access_xz_file_path = self.compress_log_files(log_name="supernova_access_log", folder_path=self.__access_log_local_storage_path)
        self.__error_xz_file_path = self.compress_log_files(log_name="supernova_error_log", folder_path=self.__error_log_local_storage_path)

        # S3 업로드
        self.upload_log_files_to_s3()
        self.clear_log_folders()        # 로그 파일 삭제 (압축 파일마저 삭제)

        # 압축 파일 경로 초기화
        self.__access_xz_file_path = ''
        self.__error_xz_file_path = ''

        return

    # 로그 제작 프로세스 실행
    def make_log_file_process(self):
        self.make_log_file()
        return

def main():
    log_processor = LogProcessor()
    try:
        schedule.every().day.at("03:00").do(log_processor.upload_process)
        schedule.every(5).minutes.do(log_processor.make_log_file_process)

        print("스케줄이 설정되었습니다:")
        print("- 매일 03:00에 로그 업로드")
        print("- 5분마다 로그 파일 생성")

        # 스케줄 실행
        while True:
            schedule.run_pending()
            time.sleep(60)  # 1분마다 체크 (CPU 사용량 절약)

    except KeyboardInterrupt:
        print("\nLog Process stopped by user")
    except Exception as e:
        print(f"오류 발생: {str(e)}")
    finally:
        print("Log Process ended")

    return
    
if __name__ == "__main__":
    main()



