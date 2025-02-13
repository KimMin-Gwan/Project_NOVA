from bs4 import BeautifulSoup

# HTML 데이터
html_data = """
<html>
<body>
<img src="data:image/jpeg;base64,/image1"/>
<img src="data:image/jpeg;base64,/image2"/>
<p>텍스트 데이터</p>
<img src="data:image/jpeg;base64,/image3"/>
</body>
</html>
"""

# HTML 파싱
soup = BeautifulSoup(html_data, 'html.parser')

original_sources = []

# <img> 태그 src 제거
img_tags = soup.find_all('img')
for img in img_tags:
    original_sources.append(img.attrs['src'])
    img.attrs = {}  # src 속성 제거


# 필터링 후 HTML 출력
filtered_html = str(soup)
print(filtered_html)

# 2. <p> 태그 수정
p_tag = soup.find('p')  # 첫 번째 <p> 태그를 찾음
if p_tag:  # 태그가 존재하면
    p_tag.string = "변형된 텍스트 데이터"  # 텍스트 수정


# (필요 시) src 복원
for img, original_src in zip(soup.find_all('img'), original_sources):
    img['src'] = original_src

# src 복원된 HTML 출력
restored_html = str(soup)
print(restored_html)
