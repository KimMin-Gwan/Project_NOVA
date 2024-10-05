import datetime
import boto3
import cv2
import time
import os
import glob
import copy

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



# 명함 제조기
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

    def make_name_card(self, bias:Bias, user:User): 
        # 네임카드 만드는 부분
        # 네임카드 포함 내용은 아래와 같다
        # 내용 : user.uid, bias.name, bias.fanname, user.solo_point(group_point), 최애 사진
        #        user.solo_combo(group_combo), 오늘 날짜 등... 넣고싶은거 아무거나 넣어도댐

        # 1. 백그라운드 이미지  불러오기
        img = self.__name_card_backgroud_image(user.select_name_card)

        # 2. 바이어스 이미지 받아오기
        self.__s3.download_file('nova-images',f'{bias.bid}.PNG',f'{self.__path}temp_files/{bias.bid}.png')
        time.sleep(0.1)
        bias_img = cv2.imread(f"{self.__path}temp_files/{bias.bid}.png")
        bias_img = cv2.resize(bias_img, (100, 100))  # 예를 들어 100x100 크기로 리사이즈

        # 3. 글자 붙혀넣기
        cv2.putText(img,f"{user.uid}", (300,200), cv2.FONT_HERSHEY_COMPLEX, 1, (0,150,0), 1)   # 중심 위치 300,200인 폰트가 FONT_HERSHEY_COMPLEX인, 크기 1의, 약한 초록색의 ,두께 3인 글씨
        cv2.putText(img,f"{bias.bname}", (400,400), cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 1)
        #이미지 합성
        img[100:200, 100:200] = bias_img

        # 4. 이미지 이름 만들기
        image_name = self.__make_name_url(bias.bid, user.uid)

        # 4. 이미지 저장
        cv2.imwrite(f'{self.__path}temp_files/{image_name}.png', img)

        # 호출문은 아래와 같음 (날짜는 알아서 모율 내에서 계산할것)
        # modul.make_name_card(self._bias, self._user)
        # 5. 이미지 업로드
        self.__s3.upload_file(f'{self.__path}temp_files/{image_name}.png', "nova-name-card", f"{image_name}.png",ExtraArgs={'ACL':'public-read'})

        #name_card_url = f"https://kr.object.ncloudstorage.com/nova-name-card/{card_name}.png"
        # 함수 반환값을 파일 주소를 반환 할것

        self.delete_temp_image()
        return True
        # 아래가 실제 사용 예시
        #self.__name_card_url = modul.get_name_card_url()

    # 명함의 백그라운드 이미지 선택(name_card_id는 user에서 제공)
    def __name_card_backgroud_image(self, name_card_id):
        path = self.__path + "name_card/" + "background.png"
        img = cv2.imread(path)
        return img

    # 명함의 파일 이름 생성기
    # 네임카드 파일 이름은 bid-uid-날짜
    # 예시 : 1001-1234-abcd-5678-24-08-21.png
    def __make_name_url(self, bid, uid) -> str:
        now = datetime.datetime.now()
        date = now.strftime('%Y-%m-%d')
        name_card_url = f'{bid}-{uid}-{date}'
        return name_card_url

    # img 이미지 이름 가지고 오기
    def get_name_card_name(self, bias:Bias, user) -> str:
        image_name = self.__make_name_url(bias.bid, user.uid)
        return image_name

    # cloud의 url 가지고 오기
    def get_name_card_url(self, bias:Bias, user) ->str:
        image_name = self.get_name_card_name(bias, user)
        name_card_url = f"{self.__endpoint_url}/nova-name-card/{image_name}.png"
        return name_card_url

    # 임시 이미지 파일 지우기
    def delete_temp_image(self):
        # 파일이 작성되기 까지 대기 시간
        time.sleep(0.1)

        # 디렉토리 내의 모든 파일을 찾음
        directory_path = self.__path + "temp_files/"
        files = glob.glob(os.path.join(directory_path, '*'))
        for file in files:
            # 파일인지 확인 후 삭제
            if os.path.isfile(file):
                os.remove(file)
        return
    

