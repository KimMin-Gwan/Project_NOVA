import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

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
url = "https://belabef.com/57/?idx=1077&utm_source=naver&utm_medium=naver_timeboard&utm_campaign=purchase_hb&utm_content=1077&utm_term=hb_time_1227_12_01"

extract_image(url)
