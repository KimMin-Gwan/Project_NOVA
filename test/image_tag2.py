# selenium의 webdriver를 사용하기 위한 import
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# selenium으로 키를 조작하기 위한 import
from selenium.webdriver.common.keys import Keys

# 페이지 로딩을 기다리는데에 사용할 time 모듈 import
import time

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

# 테스트 URL
url = "https://chzzk.naver.com/9ea9f350b31faa4305009e095533ef2f"
html_content = fetch_dynamic_content(url)

# HTML 출력
print(html_content)