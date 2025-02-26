import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
    
# selenium의 webdriver를 사용하기 위한 import
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# selenium으로 키를 조작하기 위한 import
from selenium.webdriver.common.keys import Keys

# 페이지 로딩을 기다리는데에 사용할 time 모듈 import
import time

def get_youtube_thumbnail_url(video_url):
    """유튜브 썸네일 URL 추출"""
    match = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11})", video_url)
    if match:
        video_id = match.group(1)
        return f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg"
    else:
        return "유효한 유튜브 영상 URL이 아닙니다."

def fetch_top_image(url):
    """유튜브가 아닌 사이트에서 최상단 이미지 추출"""
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        
        print("===== HTML 코드 시작 =====")
        print(soup.prettify())
        print("===== HTML 코드 끝 =====")

        # 1. Open Graph (og:image) 메타 태그에서 이미지 추출
        og_image = soup.find("meta", property="og:image")
        if og_image and og_image.get("content"):
            return og_image["content"]

        # 2. 첫 번째 <img> 태그에서 이미지 추출
        img_tag = soup.find("img")
        if img_tag and img_tag.get("src"):
            return img_tag["src"]


        # 영영 못 찾으면 이걸로
        html = fetch_dynamic_content(url=url)
        
        soup = BeautifulSoup(html, 'html.parser')
        
        print("===== HTML 코드 시작 =====")
        print(soup.prettify())
        print("===== HTML 코드 끝 =====")

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

def fetch_dynamic_content(url):
    # Chrome WebDriver 옵션 설정
    driver = webdriver.Chrome() 
    
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # 브라우저 창을 표시하지 않음
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--no-sandbox")  # Linux에서 권장
    chrome_options.add_argument("--disable-dev-shm-usage")  # 공유 메모리 사용 비활성화 (Linux)
    
    # WebDriver 경로 설정 (ChromeDriver 다운로드 필요)
    #service = Service("/path/to/chromedriver")  # 여기에 ChromeDriver 경로를 입력하세요
    driver = webdriver.Chrome(options=chrome_options)

    try:
        # URL 열기
        driver.get(url)
        time.sleep(3)  # JavaScript가 실행될 시간을 기다림

        # 페이지 소스 가져오기
        page_source = driver.page_source
        return page_source
    finally:
        driver.quit()

def extract_image(url):
    """URL을 분석하여 적합한 처리 수행"""
    parsed_url = urlparse(url)
    if "youtube.com" in parsed_url.netloc or "youtu.be" in parsed_url.netloc:
        # 유튜브 링크일 경우
        thumbnail = get_youtube_thumbnail_url(url)
        print("유튜브 썸네일 URL:", thumbnail)
    else:
        # 유튜브가 아닌 경우
        top_image = fetch_top_image(url)
        print("최상단 이미지 URL:", top_image)

# 테스트 URL 입력
url = "https://chzzk.naver.com/9ea9f350b31faa4305009e095533ef2f"

extract_image(url)
