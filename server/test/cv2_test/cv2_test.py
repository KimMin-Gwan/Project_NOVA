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
        # 1. 투명한 백그라운드 PNG 이미지 불러오기 (Pillow 이미지로 처리)
        img = self.__name_card_backgroud_image()

        # 2. 바이어스 이미지 받아오기 (투명한 PNG 파일, Pillow 이미지로 처리)
        bias_img = Image.open(f"./{bias.bid}.png").convert("RGBA")

        # 3. 폰트 설정 (시스템 폰트 경로)
        font_path = os.path.abspath('./NanumGothic-ExtraBold.ttf')
        font = ImageFont.truetype(font_path, 40)

        # 4. 이미지를 numpy 배열에서 Pillow 이미지로 변환
        img_pil = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB)).convert("RGBA")

        # 5. 배경 이미지 크기를 42% 줄이기
        new_size = (int(img_pil.width * 0.58), int(img_pil.height * 0.58))  # 가로와 세로 70%로 줄임
        img_pil = img_pil.resize(new_size, Image.ANTIALIAS)

        # 텍스트 내용
        text1 = f"{bias.bname}님 오늘도 팬이에요!"
        text2 = "2024년 09월 28일 오후 8시에 인증 완료"
        text3 = bias.bname

        draw = ImageDraw.Draw(img_pil)

        # 텍스트 크기 계산
        text1_size = draw.textsize(text1, font=font)

        text3_size = draw.textsize(text3, font=font)
        text3_x = (img_pil.width - text3_size[0]) // 2

        draw.text((text3_x, 60), text3, font=font, fill=(255, 255, 255, 255))  # RGBA 색상

        # 중앙 위치 계산
        text1_x = (img_pil.width - text1_size[0]) // 2

        check_img = Image.open(f"./check_image.png").convert("RGBA")
        check_img_size = (int(check_img.width * 0.4), int(check_img.height * 0.4))
        check_img = check_img.resize(check_img_size, Image.ANTIALIAS)

        # 6. 이미지에 한글 텍스트 추가 (Pillow 이미지로 처리)
        draw = ImageDraw.Draw(img_pil)
        draw.text((text1_x, 750), text1, font=font, fill=(255, 255, 255, 255))  # RGBA 색상

        font_path = os.path.abspath('./NanumGothic-Regular.ttf')
        font = ImageFont.truetype(font_path, 18)
        text2_size = draw.textsize(text2, font=font)
        text2_x = (img_pil.width - text2_size[0]) // 2

        draw.text((text2_x, 800), text2, font=font, fill=(255, 255, 255, 255))

        # 7. 바이어스 이미지를 백그라운드 이미지에 합성 (투명 배경으로 합성)
        #bias_img_resized = bias_img#.resize((100, 100), Image.ANTIALIAS)
        img_pil.paste(bias_img, (178, 210), bias_img)  # 투명 배경 처리
        img_pil.paste(check_img, (300, 540), check_img)  # 투명 배경 처리

        # 8. 이미지를 다시 OpenCV 형식으로 변환하여 저장
        img = cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGBA2BGR)

        # 9. 이미지 저장 (배경 투명 이미지로 저장)
        cv2.imwrite(f'./output_name_card.png', img)

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
