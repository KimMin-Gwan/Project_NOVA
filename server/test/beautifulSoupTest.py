#from bs4 import BeautifulSoup, Tag
#import requests

#from pprint import pprint

#def extract_body_n_image(raw_data:str):
    #soup = BeautifulSoup(raw_data, "html.parser")

    ## <p> 태그의 첫 번째 텍스트 가져오기
    #p_body = soup.find_all("p")
    #body = []
    
    #for p_tag in p_body:
        #p_tag:Tag = p_tag
        #striped_data = p_tag.text.strip()
        #if striped_data:
            #body.append(striped_data)
        
    ##body = soup.p.text.strip()
    ## <img> 태그의 모든 src 속성 가져오기
    ## ImageBase64 코드의 형태로 저장됨
    #imgs = [img.get("src") for img in soup.find_all("img") if img.get("src")]
        
    #return body, imgs
    ## response.raise_for_status()
    
    
#def get_html(url:str):
    ## url = "https://www.naver.com"
    #response = requests.get(url)
    #response.raise_for_status()
    #pprint(response.text)
    #return response.text

#if __name__ == "__main__":
    ##url = "https://kr.object.ncloudstorage.com/nova-feed-project-body/0cb7-f17f-46ef-6ttHPf.html"
    #url = "https://chzzk.naver.com/video/7479846"
    #raw_data = get_html(url)
    ##print(raw_data)
    #body, imgs = extract_body_n_image(raw_data)
    #pprint(body)
    
    
    
import requests
from bs4 import BeautifulSoup

def fetch_html(url: str):
    response = requests.get(url)
    response.raise_for_status()
    response.encoding = 'utf-8'  # 명시적으로 UTF-8로 설정
    return response.text

if __name__ == "__main__":
    url = "https://chzzk.naver.com/video/7479846"
    thumbnail_url = fetch_html(url)
    print("Thumbnail URL:", thumbnail_url)