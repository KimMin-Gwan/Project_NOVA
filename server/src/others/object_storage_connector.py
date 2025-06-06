from requests import get
import requests
import boto3 
import time
import glob
import os
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO
import imageio
from io import BytesIO
from PIL import Image
import cv2
import numpy as np
import re
from urllib.parse import urlparse

access_key = 
secret_key = 


# 건들지 않음
# Project Body (프로젝트 상세보기 화면 받아옴)
class ObjectStorageConnection:
    def __init__(self):
        self.__project_bucket = "nova-project-image"
        self.__feed_bucket= "nova-feed-project-body"
        self.__notice_bucket= "nova-notice-body"
        self.__profile_bucket= "nova-profile-bucket"

    # 오브젝트 스토리지와 연결할때는 이것을 실행해야함
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

    # 프로젝트 바디 부분 불러오는 부분
    def get_project_body(self, pid):
        self.__init_boto3()
        target_url = self.__endpoint_url + "/" + self.__project_bucket + "/" + pid + ".html"
        response = get(url=target_url)
        html_content = response.content.decode("utf-8")
        #html_content = response.content
        return html_content
    
    # 피드 바디 데이터 불러오는 부분
    def get_feed_body(self, fid):
        self.__init_boto3()
        target_url = self.__endpoint_url + "/" + self.__feed_bucket + "/" + fid + ".html"
        response = get(url=target_url)
        html_content = response.content.decode("utf-8")
        #html_content = response.content
        return html_content
    
    # 피드 바디 데이터 불러오는 부분
    def get_notice_body(self, nid):
        self.__init_boto3()
        target_url = self.__endpoint_url + "/" + self.__notice_bucket + "/" + nid + ".html"
        response = get(url=target_url)
        html_content = response.content.decode("utf-8")
        #html_content = response.content
        return html_content
    
    def make_new_profile_image(self, uid:str, image_name:str, image):
        
        # 자주 사용되는 이미지 확장자들
        valid_extensions = ['.png', '.jpg', '.jpeg', '.PNG']  
    
        # 이미지 확장자가 주어진 확장자 중 하나인지 검사
        if not any(image_name.lower().endswith(ext) for ext in valid_extensions):
            return False
            
        self.__init_boto3()
        
        path = './model/local_database/temp_profile_image/'
        
        extension = image_name.split('.')[-1]
        
        file_name = f"{uid}.png"
        
        pil_image = Image.open(BytesIO(image))
        file_path = path + file_name
        
        pil_image.save(file_path, format='PNG')
        
        self.__s3.upload_file(  file_path,
                                self.__profile_bucket,
                                file_name,
                                ExtraArgs={'ACL': 'public-read'})
        
        self.delete_specific_file(path=path, file_name=file_name)
        return True
        
    
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

        #self.delete_temp_file(path)
        
        # 단일 파일만 제거
        self.delete_specific_file(path=path, file_name=file_name)

        return url
        
    def delete_temp_file(self, path):
        time.sleep(0.1)
        files = glob.glob(os.path.join(path, '*'))
        for file in files:
            if os.path.isfile(file):
                os.remove(file)
        return
    
    def delete_specific_file(self, path, file_name):
        time.sleep(0.1)
        target_file = os.path.join(path, file_name)
        if os.path.isfile(target_file):
            os.remove(target_file)
        else:
            print(f"{file_name} does not exist.")

    # 오브젝트 바디 커넥트에서 데이터를 분리하는 함수
    # raw_data = String화 되어 파싱 된 것. <p> tag~
    def extract_body_n_image(self, raw_data:str):
        soup = BeautifulSoup(raw_data, "html.parser")
        
        try:
            
            # <p> 태그의 첫 번째 텍스트 가져오기
            p_body = soup.find_all("p")
            body = []
    
            for p_tag in p_body:
                striped_data = p_tag.text.strip()
                if striped_data:
                    body.append(striped_data)
        
            # <img> 태그의 모든 src 속성 가져오기
            # ImageBase64 코드의 형태로 저장됨
            imgs = [img.get("src") for img in soup.find_all("img") if img.get("src")]
        except Exception as e:
            return ["불러오기에 실패했습니다."], []
        
        return body, imgs
        # response.raise_for_status()


class HTMLEXtractor:
    # 외부 사이트에서 가장 상단의 이미지나 섬네일을 가지고 오는 함수
    def extract_external_webpage_image_data(self, url):
        image = self.__extract_image(url=url)
        return image
    
    def __get_youtube_thumbnail_url(self, video_url):
        """유튜브 썸네일 URL 추출"""
        match = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11})", video_url)
        if match:
            video_id = match.group(1)
            return f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg"
        else:
            return "유효한 유튜브 영상 URL이 아닙니다."

    def __fetch_top_image(self, url):
        """유튜브가 아닌 사이트에서 최상단 이미지 추출"""
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
            }
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')

            # 1. Open Graph (og:image) 메타 태그에서 이미지 추출
            og_image = soup.find("meta", property="og:image")
            if og_image and og_image.get("content"):
                return og_image["content"]

            # 2. 첫 번째 <img> 태그에서 이미지 추출
            img_tag = soup.find("img")
            if img_tag and img_tag.get("src"):
                return img_tag["src"]

            return "이미지를 찾을 수 없습니다."

        except requests.exceptions.RequestException as e:
            return f"요청 중 오류가 발생했습니다: {e}"

    def __extract_image(self, url):
        # URL을 분석하여 적합한 처리 수행
        parsed_url = urlparse(url)

        if "youtube.com" in parsed_url.netloc or "youtu.be" in parsed_url.netloc:
            # 유튜브 링크일 경우
            thumbnail = self.__get_youtube_thumbnail_url(url)
            return thumbnail
        else:
            # 유튜브가 아닌 경우
            top_image = self.__fetch_top_image(url)
            print("최상단 이미지 URL:", top_image)
            return top_image
    
    # 외부에서 사이트에서 title 데이터 추출하는 함수
    def extract_external_webpage_title_tag(self, url):
        title = "주소 제목"
        result = False
        
        # URL이 비어있거나 None인지 확인
        if not url:
            return result, url, title
    
        # URL 유효성 검증
        if not self.__is_valid_url(url):
            return result, url, title
    
        # 스키마가 없는 경우 http:// 추가
        parsed_url = urlparse(url)
        if not parsed_url.scheme:
            url = f"http://{url}"
        
        try:
            # URL에서 HTML 가져오기
            response = requests.get(url, timeout=10)

            # BeautifulSoup 객체 생성
            soup = BeautifulSoup(response.text, 'html.parser')
            # <title> 태그 내용 추출
            title = soup.title.string if soup.title else "Page Title"
        except requests.exceptions.RequestException as e:
            return result, url, f"Error fetching URL : {e}"
        result = True
        
        return result, url, title
    
    # "https://chatgpt.com/c/67a4260b-1100-8013-916d-d0cb06b0a1e4" 이런 사이트에서 chatgpt.com 만 긁어오는 함수
    def extract_link_domain_string(self, url):
        # 정규 표현식으로 도메인 추출
        #url.split("//")[-1].split("/")[0] #안되면 이걸 쓰면된대
        match = re.search(r"https?://([^/]+)", url)
        
        if match:
            domain = match.group(1)
            return domain
        
        return ""
    
    # url 정규식 검사
    def __is_valid_url(self, url) -> bool:
        try:
            spilted_data = url.split(".")
            
            if len(spilted_data) <= 1:
                return False
            else:
                return True
            #result = urlparse(url)
            ## 스키마(http, https)와 네트워크 위치(netloc) 확인
            #return all([result.netloc])
        except ValueError:
            return False
        
    
#    # html에서 img 태그 안에 있는 src 데이터를 지우는 함수
    #def remove_img_src_data_in_html(self, html_data):
        
        #soup = BeautifulSoup(html_data, 'html.parser')
        
        #img_tags = soup.find_all('img')
        #for img in img_tags:
            #img.attrs = {}
        
        #filtered_html = str(soup)
        
        #return filtered_html
    def remove_img_src_data_in_html(self, html_data):
        soup = BeautifulSoup(html_data, 'html.parser')

        # 모든 <img> 태그에서 src 속성만 제거
        img_tags = soup.find_all('img')
        for img in img_tags:
            if 'src' in img.attrs:  # src 속성이 있는 경우만 제거
                del img.attrs['src']

        # XML 호환성을 위해 'self-closing' 형태로 변환
        for img in img_tags:
            if not img.attrs:  # 속성이 없는 경우
                img.replace_with(BeautifulSoup('<img />', 'html.parser').img)

        filtered_html = str(soup)
        return filtered_html

    
    # 원본 html 데이터랑 추출해서 변형한 데이터를 같이 넣고 img src를 맞춰주는 함수
    def restore_img_src_data_in_html(self, raw_html, p_html):
        soup = BeautifulSoup(raw_html, 'html.parser')
        
        original_sources = []
        
        img_tags = soup.find_all('img')
        for img in img_tags:
            original_sources.append(img.attrs['src'])
            img.attrs = {}
        
        restored_soup = BeautifulSoup(p_html, 'html.parser')
        
        # (필요 시) src 복원
        for img, original_src in zip(restored_soup.find_all('img'), original_sources):
            img['src'] = original_src

        # src 복원된 HTML 출력
        restored_html = str(restored_soup)
        
        return restored_html
    
        
class ImageDescriper:
    def __init__(self):
        self.__feed_temp_path = './model/local_database/feed_temp_image'
        self.__report_temp_path = './model/local_database/report_temp_image'
        self.__service_name = 's3'
        self.__endpoint_url = 'https://kr.object.ncloudstorage.com'
        self.__region_name = 'kr-standard'
        self.__access_key = access_key
        self.__secret_key = secret_key
        self.__s3 = boto3.client(self.__service_name,
                                 endpoint_url=self.__endpoint_url,
                                 aws_access_key_id=self.__access_key,
                                 aws_secret_access_key=self.__secret_key)
        self.__feed_bucket_name = "nova-feed-images"
        self.__default_image = "https://kr.object.ncloudstorage.com/nova-feed-images/super_nova.png"
        self.__bias_image_bucket = "nova-bias-profile-images"
        self.__report_image_bucket = "nova-report-images"

    def __set_images_to_byte(self, images: list):
        pil_images = []
        for image in images:
            try:
                pil_image = Image.open(BytesIO(image))
                pil_images.append(pil_image)
            except Exception as e:
                print(f"Error opening image with PIL: {e}")
        return pil_images

    def __set_images_to_cv2(self, images: list):
        cv2_images = []
        for pil_image in images:
            try:
                cv2_image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
                cv2_images.append(cv2_image)
            except Exception as e:
                print(f"Error converting PIL to CV2: {e}")
        return cv2_images

    def __process_gif_with_imageio(self, image: bytes):
        try:
            gif_images = imageio.mimread(image)
            cv2_images = [cv2.cvtColor(frame, cv2.COLOR_RGB2BGR) for frame in gif_images]
            return cv2_images
        except Exception as e:
            print(f"Error processing GIF with imageio: {e}")
            return []

    def __process_cv2img_to_gif(self, cv2_images: list):
        try:
            gif_images = [cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) for frame in cv2_images]
            return gif_images

        except Exception as e:
            print(f"Error processing GIF with imageio: {e}")
            return []

    def get_default_image_url(self):
        return [self.__default_image], True
    
    def try_report_image_upload(self, rid: str, image_names: list, images):
        try:
            urls = []

            for i, image in enumerate(images):
                try:
                    image_name:str = image_names[i]
                    # Check if GIF or other unsupported formats
                    if image_name.lower().endswith('.gif'):
                        # 걍 gif 이미지 통째로 저장하는걸로 해★결
                        # PIL를 이용해서 쇼부를 본다
                        gif_file = Image.open(BytesIO(image))
                        temp_path = f"{self.__report_temp_path}/{rid}_{image_name}"

                        gif_file.save(
                            temp_path,
                            save_all=True,
                            loop=gif_file.info.get("loop", 0),         # 원본 루프 설정 유지
                            duration=gif_file.info.get("duration", 100)  # 원본 지속 시간 유지
                        )

                        # if not os.path.exists(temp_path):
                        #     print(f"GIF 파일 생성 실패: {temp_path}")

                        self.__s3.upload_file(temp_path,
                                              self.__report_image_bucket,
                                              f"{rid}_{image_name}",
                                              ExtraArgs={'ACL': 'public-read'})
                        urls.append(f"{self.__endpoint_url}/{self.__report_image_bucket}/{rid}_{image_name}")

                    else:
                        # Process other formats
                        pil_image = Image.open(BytesIO(image))
                        temp_path = f"{self.__report_temp_path}/{rid}_{image_name}"
                        pil_image.save(temp_path)
                        self.__s3.upload_file(temp_path,
                                              self.__report_image_bucket,
                                              f"{rid}_{image_name}",
                                              ExtraArgs={'ACL': 'public-read'})
                        urls.append(f"{self.__endpoint_url}/{self.__report_image_bucket}/{rid}_{image_name}")
                except Exception as e:
                    print(f"Error processing image {image_names[i]}: {e}")

            #self.delete_temp_image()
            # 단일 파일만 제거
            self.delete_specific_file(path=self.__report_temp_path, file_name=f"{rid}_{image_name}")
            
            return urls, True

        except Exception as e:
            print(f"Error in try_feed_image_upload: {e}")
            return "Something Goes Bad", False

    def try_feed_image_upload(self, fid: str, image_names: list, images):
        try:
            urls = []

            for i, image in enumerate(images):
                try:
                    image_name:str = image_names[i]
                    # Check if GIF or other unsupported formats
                    if image_name.lower().endswith('.gif'):
                        # 걍 gif 이미지 통째로 저장하는걸로 해★결
                        # PIL를 이용해서 쇼부를 본다
                        gif_file = Image.open(BytesIO(image))
                        temp_path = f"{self.__feed_temp_path}/{fid}_{image_name}"

                        gif_file.save(
                            temp_path,
                            save_all=True,
                            loop=gif_file.info.get("loop", 0),         # 원본 루프 설정 유지
                            duration=gif_file.info.get("duration", 100)  # 원본 지속 시간 유지
                        )

                        # if not os.path.exists(temp_path):
                        #     print(f"GIF 파일 생성 실패: {temp_path}")

                        self.__s3.upload_file(temp_path,
                                              self.__feed_bucket_name,
                                              f"{fid}_{image_name}",
                                              ExtraArgs={'ACL': 'public-read'})
                        urls.append(f"{self.__endpoint_url}/{self.__feed_bucket_name}/{fid}_{image_name}")

                    else:
                        # Process other formats
                        pil_image = Image.open(BytesIO(image))
                        temp_path = f"{self.__feed_temp_path}/{fid}_{image_name}"
                        pil_image.save(temp_path)
                        self.__s3.upload_file(temp_path,
                                              self.__feed_bucket_name,
                                              f"{fid}_{image_name}",
                                              ExtraArgs={'ACL': 'public-read'})
                        urls.append(f"{self.__endpoint_url}/{self.__feed_bucket_name}/{fid}_{image_name}")
                except Exception as e:
                    print(f"Error processing image {image_names[i]}: {e}")

            #self.delete_temp_image()
            # 단일 파일만 제거
            self.delete_specific_file(path=self.__feed_temp_path, file_name=f"{fid}_{image_name}")
            
            return urls, True

        except Exception as e:
            print(f"Error in try_feed_image_upload: {e}")
            return "Something Goes Bad", False
        

    def delete_temp_image(self):
        time.sleep(0.1)
        files = glob.glob(os.path.join(self.__feed_temp_path, '*'))
        for file in files:
            if os.path.isfile(file):
                os.remove(file)
        return
    
    def delete_specific_file(self, path, file_name):
        time.sleep(0.1)
        target_file = os.path.join(path, file_name)
        if os.path.isfile(target_file):
            os.remove(target_file)
        else:
            print(f"{file_name} does not exist.")