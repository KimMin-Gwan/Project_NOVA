from bs4 import BeautifulSoup
import requests
from urllib.parse import urlparse



# 외부에서 사이트에서 title 데이터 추출하는 함수
def func1(url):
    # URL에서 HTML 가져오기
    response = requests.get(url)

    # BeautifulSoup 객체 생성
    soup = BeautifulSoup(response.text, 'html.parser')

    # <title> 태그 내용 추출
    title = soup.title.string if soup.title else "Page Title"
        
    return title


url = 'https://www.youtube.com/watch?v=rsK6k8Zyfy4'

print(func1(url = url))