import datetime
import boto3
import cv2


def make_name_card(bias,user):
        
        service_name = 's3'
        endpoint_url = 'https://kr.object.ncloudstorage.com'
        region_name = 'kr-standard'
        access_key = 'eeJ2HV8gE5XTjmrBCi48'
        secret_key = 'zAGUlUjXMup1aSpG6SudbNDzPEXHITNkEUDcOGnv'
        s3 = boto3.client(service_name,
                        endpoint_url=endpoint_url,
                        aws_access_key_id=access_key,
                    aws_secret_access_key=secret_key)
        # 네임카드 만드는 부분
        # 네임카드 포함 내용은 아래와 같다
        # 내용 : user.uid, bias.name, bias.fanname, user.solo_point(group_point), 최애 사진
        #        user.solo_combo(group_combo), 오늘 날짜 등... 넣고싶은거 아무거나 넣어도댐
        
        # 네임카드 파일 이름은 bid-uid-날짜
        # 예시 : 1001-1234-abcd-5678-24-08-21.png
        now = datetime.datetime.now()
        date = now.strftime('%Y-%m-%d')
        name_card_url = f'{bias}-{user}-{date}.png'

        #s3.download_file('nova-images','1001.PNG','/temp_imgs')

        img = cv2.imread("./temp_imgs/00043.png")
        
        cv2.putText(img,f"{uid}", (300,200), cv2.FONT_HERSHEY_COMPLEX, 1, (0,150,0), 1)   # 중심 위치 300,200인 폰트가 FONT_HERSHEY_COMPLEX인, 크기 1의, 약한 초록색의 ,두께 3인 글씨
        name = 'test'
        cv2.putText(img,f"{name}", (400,400), cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 1)
        #이미지 합성
        #base_image[y시작:y끝, x시작:x끝] = 추가 이미지
        cv2.imwrite(name_card_url,img)
        # 호출문은 아래와 같음 (날짜는 알아서 모율 내에서 계산할것)
        # modul.make_name_card(self._bias, self._user)
        s3.upload_file(f'./{name_card_url}', "nova-name-card", f"{name_card_url}",ExtraArgs={'ACL':'public-read'})

        # 함수 반환값을 파일 주소를 반환 할것
        print( name_card_url)
        # 아래는 모듈 내부 예시
        #name_card_url = f"https://kr.object.ncloudstorage.com/nova-name-card/{card_name}.png"

        # 파일 이름 뽑는 함수도 하나 만들어 둘것

        # 아래가 실제 사용 예시
        #self.__name_card_url = modul.get_name_card_url()

def get_name_card_url( user, bias):
        now = datetime.datetime.today().isoformat()
        name_card_url = f'{bias}-{user}-{now}.png'
        print(name_card_url)

        

    # 이미 만들어진 name카드를 호출하는 함수
    # 이미 호출한 사람이 다시 호출을 시도할 때 줄 내용
def get_name_card( user, bias):

        # 이것도 모듈에서 제공하는것으로합니다
        # 호출문 예시 (함수이름은 바꿔도 됨)
        # self.name_card_url = self.get_name_card_url_with_uid_n_bid(self._user.uid, self._bias.bid)
        now = datetime.datetime.today().isoformat()
        name_card_url = f'{bias}-{user}-{now}.png'
        print(name_card_url)


bid='1001'#
uid = '1234-abcd-5678'#

make_name_card(bias=bid,user=uid)