import datetime
import boto3
import cv2
import time
import os
import glob
import copy
from PIL import Image, ImageDraw, ImageFont
import numpy as np

class Bias():
    def __init__(self, bid="", type="", bname="", category=[], birthday="", debut="",
                 agency="", group=[], lid="", point=0, num_user=0, x_account="",
                 insta_account="", tiktok_account="", youtube_account="", homepage="",
                 fan_cafe="", country=[], nickname=[], fanname = [], group_member_bids=[]):
        self.bid = bid
        self.type = type
        self.bname = bname
        self.category = copy.copy(category)
        self.birthday = birthday
        self.debut = debut
        self.agency = agency
        self.group = copy.copy(group)
        self.lid = lid
        self.point = point
        self.num_user = num_user
        self.x_account = x_account
        self.insta_account = insta_account
        self.tiktok_account = tiktok_account
        self.youtube_account = youtube_account
        self.homepage = homepage
        self.fan_cafe = fan_cafe
        self.country = copy.copy(country)
        self.nickname = copy.copy(nickname)
        self.fanname = copy.copy(fanname)
        self.group_memeber_bids = copy.copy(group_member_bids)


    def make_with_dict(self, dict_data):
        try:
            self.bid = dict_data['bid']
            self.type = dict_data['type']
            self.bname = dict_data['bname']
            self.category = copy.copy(dict_data['category'])
            self.birthday = dict_data['birthday']
            self.debut = dict_data['debut']
            self.agency = dict_data['agency']
            self.group = copy.copy(dict_data['group'])
            self.lid = dict_data['lid']
            self.point = dict_data['point']
            self.num_user = dict_data['num_user']
            self.x_account = dict_data['x_account']
            self.insta_account = dict_data['insta_account']
            self.tiktok_account = dict_data['tiktok_account']
            self.youtube_account = dict_data['youtube_account']
            self.homepage = dict_data['homepage']
            self.fan_cafe = dict_data['fan_cafe']
            self.country = copy.copy(dict_data['country'])
            self.nickname = copy.copy(dict_data['nickname'])
            self.fanname = copy.copy(dict_data['fanname'])
            self.group_memeber_bids = copy.copy(dict_data['group_member_bids'])
        except Exception as e:
            print(e)

    def get_dict_form_data(self):
        return {
            "bid": self.bid,
            "type": self.type,
            "bname": self.bname,
            "category": copy.copy(self.category),
            "birthday": self.birthday,
            "debut": self.debut,
            "agency": self.agency,
            "group": copy.copy(self.group),
            "lid": self.lid,
            "point": self.point,
            "num_user": self.num_user,
            "x_account": self.x_account,
            "insta_account": self.insta_account,
            "tiktok_account": self.tiktok_account,
            "youtube_account": self.youtube_account,
            "homepage": self.homepage,
            "fan_cafe": self.fan_cafe,
            "country": copy.copy(self.country),
            "nickname": copy.copy(self.nickname),
            'fanname':copy.copy(self.fanname),
            'group_member_bids':copy.copy(self.group_memeber_bids)
        }

class NameCardMaker:
    def __init__(self):
        self.__path = './model/local_database/'
        self.__service_name = 's3'
        self.__endpoint_url = 'https://kr.object.ncloudstorage.com'
        self.__region_name = 'kr-standard'
        self.__access_key = 'eeJ2HV8gE5XTjmrBCi48'
        self.__secret_key = 'zAGUlUjXMup1aSpG6SudbNDzPEXHITNkEUDcOGnv'
        self.__s3 = boto3.client(self.__service_name,
                           endpoint_url=self.__endpoint_url,
                           aws_access_key_id=self.__access_key,
                      aws_secret_access_key=self.__secret_key)

    def make_name_card(self, bias: Bias, user): 
        # 1. 백그라운드 이미지 불러오기
        img = self.__name_card_backgroud_image()

        # 2. 바이어스 이미지 받아오기
        self.__s3.download_file('nova-bias-circle-image', f'{bias.bid}.png', f'./{bias.bid}.png')
        time.sleep(0.1)
        bias_img = cv2.imread(f"./{bias.bid}.png")
        #bias_img = cv2.resize(bias_img, (100, 100))  # 100x100 크기로 리사이즈

        # 3. 한글 폰트를 사용해 텍스트를 추가 (Pillow 사용)
        # OpenCV 이미지를 Pillow 이미지로 변환
        img_pil = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

        # 폰트 설정 (나눔고딕 폰트를 사용할 경우)
        font_path = './NanumGothic-Regular.ttf'  # 나눔고딕 폰트 경로
        font = ImageFont.truetype(font_path, 40)

        # 이미지에 한글 텍스트 삽입
        draw = ImageDraw.Draw(img_pil)
        draw.text((300, 200), f"{bias.bname}님 오늘도 팬이에요!", font=font, fill=(0, 150, 0))  # 한글 텍스트
        draw.text((400, 400), "2024년 09월 28일 오후 8시에 인증 완료", font=font, fill=(255, 255, 255))  # 날짜 텍스트

        # Pillow 이미지를 다시 OpenCV 이미지로 변환
        img = cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)

        # 4. 바이어스 이미지 합성 (OpenCV)
        img[100:200, 100:200] = bias_img

        # 5. 이미지 이름 만들기
        image_name = self.__make_name_url(bias.bid, "test_user")

        # 6. 이미지 저장
        cv2.imwrite(f'./{image_name}.png', img)

        # 7. 이미지 업로드 (S3에 업로드 할 경우)
        # self.__s3.upload_file(f'{self.__path}temp_files/{image_name}.png', "nova-name-card", f"{image_name}.png", ExtraArgs={'ACL': 'public-read'})

        # 함수 반환값으로 파일 주소를 반환할 수도 있음
        return True

    # 명함의 백그라운드 이미지 선택
    def __name_card_backgroud_image(self):
        path = "./background.png"
        img = cv2.imread(path)
        return img

    # 명함의 파일 이름 생성기
    def __make_name_url(self, bid, uid) -> str:
        now = datetime.datetime.now()
        date = now.strftime('%Y-%m-%d')
        name_card_url = f'{bid}-{uid}-{date}'
        return name_card_url

    # 임시 이미지 파일 지우기
    def delete_temp_image(self):
        # 파일이 작성되기까지 대기 시간
        time.sleep(0.1)

        # 디렉토리 내의 모든 파일을 찾음
        directory_path = self.__path + "temp_files/"
        files = glob.glob(os.path.join(directory_path, '*'))
        for file in files:
            if os.path.isfile(file):
                os.remove(file)
        return
    

name_card_maker = NameCardMaker()
bias = Bias(bid="1002", bname="고세구")
name_card_maker.make_name_card(bias=bias, user= None)
