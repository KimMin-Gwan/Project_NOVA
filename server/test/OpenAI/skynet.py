# -*- coding: utf-8 -*- 
#### Skynet 였던것 / 파일 이름 바꿔야함
import json

from openai import OpenAI
#API 키 
client = OpenAI(api_key="열쇠")

## 현재 자료의 문장이 완성형에 가까워 높은 문장 완성 성능을 보여주는 중
## 커뮤니티에 게시된 자연어들이 제대로 처리 되는지 확인 하려면 완전히 박살난 문장 형식의 글이나 문맥 파악이 불가능한 자료가 필요
## 초성, meme, 축약어 등 사전적 의미가 존재하지 않는 단어 처리 확인 필요
## 욕설로 도배된 자료 처리 확인 필요
## 많은(다양한) 데이터가 필요할 것으로 예상됨

## 02/06 
## 기호 처리를 잘 못하는걸로 보임 (예를들면 화살표)
## 글자가 변형된 단어 처리를 못함
## dlfjgrp Tmaus ahtdkfdkajrdma #이거 q:ㅂ, q는 ㅂ임 이렇게 알려줘도 안해줌 인터넷 단어 사전 프롬프트 같은걸 만들어서 import 해야되나?
## 한글 암호 해독기를 만들어야 검열기가 완성될것으로 예상됨

## 02/10
## 영어로 작성된걸 어찌 처리 해야할지 모르겟음

## 02/11 (신대홍)
## 한글자판으로 입력된 영어 같은 경우를 처리하는 프롬프트를 작성해봤습니다. 확인을 해봐야합니다
## 이제 다음은 영어 관련 문제긴한데.. 이 부분은 레딧같은데서 긁어와서 한번해보려고 합니다.

#gpt 사용 전 전처리 할 단어 찾기
def finder(context):  
    response = client.chat.completions.create(
        #gpt 모델
        model="gpt-4o-mini",
        #응답 형식
        response_format={ "type": "json_object" },
        #프롬프트 작성 하는 곳
        messages=[

        #응답 형식 요구 ( 대화 방식 지정 )
        {"role": "system", "content": "You are a helpful assistant designed to output JSON."},

        #주문사항
        {"role": "user", "content": "문장에서 고유명사를 찾아냅니다."},
        {"role": "user", "content": "의미를 알 수 없는 단어를 고유명사로 취급합니다."},
        {"role": "user", "content": "고유명사가 아닌 경우 응답에 포함하지 않습니다."},
        {"role": "user", "content": "응답은 context로 합니다."},
        {"role": "user", "content": "context에는 words가 있습니다."},
        {"role": "user", "content": "words는 list입니다."},
        #{"role": "user", "content": "고유명사가 영어인 경우 알파벳을 모두 분리합니다. "},
        #{"role": "user", "content": "context에는 input, word와 index가 있습니다."},
        #{"role": "user", "content": "input은 입력받은 문장 word는 고유명사 index는 위치입니다."},
        #{"role": "user", "content": "title과 content에서 고유명사의 index 위치를 찾습니다."},
        
        #답변 제공
        {"role": "assistant", "content": f"context에 포함된 고유명사들을 출력합니다. context:{context}"}
        ]

    )
    #결과
    result = response.choices[0].message.content
    
    #print(type(result))
    print(json.loads(result))
    return json.loads(result)

#전처리 실행(기본 기능을 사용하자)
def pre_v1(원본, 이거이름뭘로할까):
    #나중에 db로 뺴야됨
    words = {'q':'ㅂ','w':'ㅈ','e':'ㄷ','r':'ㄱ','t':'ㅅ','y':'ㅛ','u':'ㅕ','i':'ㅑ','o':'ㅐ','p':'ㅔ','a':'ㅁ','s':'ㄴ','d':'ㅇ','f':'ㄹ','g':'ㅎ','h':'ㅗ','j':'ㅓ','k':'ㅏ','l':'ㅣ','z':'ㅋ','x':'ㅌ','c':'ㅊ','v':'ㅍ','b':'ㅠ','n':'ㅜ','m':'ㅡ',
        '멍한청인지공능': '멍청한인공지능'}
    
    nouns = 이거이름뭘로할까
    
    for word in nouns:
        if word in words:
            원본 = 원본.replace(word, words[word])

    print(원본)
    return 원본

#전처리 실행(인공지능의 힘을 쓰면)
#단어 교환까지 gpt한테 다 맡기자
def pre_v2(context):
    #나중에 db로 뺴야됨
    words = {
        '멍한청인지공능': '멍청한인공지능',
        'dkssud': '안녕',
    }

    
    response = client.chat.completions.create(
        #gpt 모델
        model="gpt-4o-mini",
        #응답 형식
        response_format={ "type": "json_object" },
        #프롬프트 작성 하는 곳
        messages=[

        #응답 형식 요구 ( 대화 방식 지정 )
        {"role": "system", "content": "You are a helpful assistant designed to output JSON."},

        #주문사항
        {"role": "user", "content": "문장에서 고유명사를 찾아냅니다."},
        {"role": "user", "content": "의미를 알 수 없는 단어를 고유명사로 취급합니다."},
        {"role": "user", "content": "고유명사가 아닌 경우 응답에 포함하지 않습니다."},
        {"role": "user", "content": "응답은 context로 합니다."},
        {"role": "user", "content": f"고유명사를 {words}에 맞게 변환합니다."},

        {"role": "user", "content": '주의사항 : 입력된 텍스트 중, 영단어가 포함되어 있을 수 있습니다. 이 경우, 문맥상 의미가 있는 경우면\
                                    해석한 결과를 내보내되, 그렇지않은 문맥상 단어의 의미가 불명확하거나 규칙성이 없는 배열의 단어같은 경우\
                                    한글 자판 입력 의도 (ex: dkssud = 안녕)일 수있으니, 이런식으로 한글 두벌식 자판 기준으로 단어를 변형하고 자동으로 변환합니다.'},

        #답변 제공
        {"role": "assistant", "content": f"context에 포함된 고유명사들을 변환하여 출력합니다. context:{context}"}
        ]

    )
    #결과
    result = response.choices[0].message.content
    
    #print(type(result))
    print(json.loads(result))
    return json.loads(result)
    
        

### 태그 뽑기
### 나중에

#gpt 사용하기 (본문)
def rework(context,words,word_bag):
    response = client.chat.completions.create(
        #gpt 모델
        model="gpt-4o-mini",
        #응답 형식
        response_format={ "type": "json_object" },
        #프롬프트 작성 하는 곳
        messages=[

        #응답 형식 요구 ( 대화 방식 지정 )
        {"role": "system", "content": "You are a helpful assistant designed to output JSON."},

        #주문사항
        {"role": "user", "content": "비속어를 유사한 의미의 단어로 교체합니다."},
        {"role": "user", "content": "반말을 모두 존댓말로 교체합니다."},
        {"role": "user", "content": "텍스트에서 전달하고자 하는 의도 또는 의미가 변형되면 안됩니다."},
        {"role": "user", "content": "텍스트의 분위기 또한 파악하여 의미가 변형되지 않도록 해야합니다."},
        {"role": "user", "content": "텍스트는 content로 이루어져 있습니다"},
        {"role": "user", "content": "응답은 '변환문'과 강도로 합니다."},        
        {"role": "user", "content": "응답의 변환문은 content로 구성되어야 합니다."},

        # 02/14 level 정상화
        {"role": "user", "content": "강도는 기본적으로 0입니다."},
        {"role": "user", "content": "반말로 작성된 경우 강도를 1로 합니다."},
        {"role": "user", "content": "비속어 또는 욕설이 사용되면 강도를 2로 합니다."},

        #{"role": "user", "content": "강도는 비속어 또는 욕설이 포함된 경우 2, 비속어는 포함되나 않으나 욕설이 없이 작성된 경우 1, 비속어 또는 욕설이 사용되지 않고 작성 된 경우 0을 반환합니다"}, #작동이 애매함
        {"role": "user", "content": '고유명사는 변환하지 않습니다.'},
        # {"role": "user", "content": '둘 이상의 단어가 합쳐진 단어가 있습니다. 이는 고유명사가 아닙니다.'}, #이상한 단어 분리해서 알아보라고 해보려고 한건데 안되는듯
        # {"role": "user", "content": '둘 이상의 단어가 합쳐진 단어는 해당 단어를 분해하여 어떤 단어가 사용됐는지 파악해 의미가 변하지 않도록 변환합니다.'},
        # {"role": "user", "content": '변환된 문장엔 일베용어가 사용되어선 안됩니다'}, #이거 정리해서 다 알려줘야 되나..?
        {"role": "user", "content": "변환된 문장엔 공격적인 단어가 적게 포함되어야 합니다."},

        # 02/12 추가 워드백 사용하기
        {"role": "user", "content": f"words:{words}, words 단어를 word_bag 맞게 변환합니다. word_bag:{word_bag} "},
        {"role": "user", "content": "word를 meaning에 맞게 변환합니다."},

        # 02/13 html태그 유지
        {"role": "user", "content": "HTML 태그는 변환하지 않습니다."},
        

        ### 02/12
        #단어 사전 사용하기
        #for a in b:
#        {"role": "user", "content": f'{}는 {}입니다. {}일 경우 ~~합니다,'},

        #답변 제공
        {"role": "assistant", "content": f"context에 포함된 내용을 변환하여 응답합니다. context:{context}"}
        ]

    )
    #결과
    result = response.choices[0].message.content
        
    print(json.loads(result))

# 트렌드 변형 중....
#gpt 사용하기 (트렌드) /공사중
def trend(context):
    response = client.chat.completions.create(
        #gpt 모댈
        model="gpt-4o-mini",
        #응답 형식
        response_format={ "type": "json_object" },
        #프롬프트 작성 하는 곳
        messages=[
        #응답 형식 요구 ( 대화 방식 지정 )
        {"role": "system", "content": "You are a helpful assistant designed to output JSON."},

        #주문사항

        # 목적
        {"role": "user", "content": "주어진 텍스트를 요약해서 반환합니다."},

        # 제공 정보 요약
        {"role": "user", "content": "주어진 텍스트는 여러개의 텍스트를 가진 리스트입니다."},
        {"role": "user", "content": "리스트 안의 텍스트는 title과 content로 이루어져 있습니다."},
        {"role": "user", "content": "각 텍스트 마다 title과 content를 종합 및 요약해 주제를 정하게 됩니다."},

        # 주제 분석 방법
        {"role": "user", "content": "텍스트를 읽고 현재의 글 주제 분야를 키워드로 제시해 주세요."},
        {"role": "user", "content": "현재 주제의 대분류에 대한 정보를 포함시켜 주세요. Ex) 기술, 음악, 의료 등."},
        {"role": "user", "content": "위에서 요약한 키워드는 Keyword라는 항목으로 표시를 해주세요."},
        {"role": "user", "content": "다음부터 나오는 명령들은 위에서 진행한 키워드 요약이 아닌 내용 요약으로 진행해 주세요. "},
        {"role": "user", "content": "가장 많이 나온 주제, 공통된 주제를 메인 주제로 정합니다."},
        {"role": "user", "content": "그 외 많이 나온 주제나 요약해 나온 메인 주제의 하위 분류 주제를 서브 주제로 정합니다."},
        {"role": "user", "content": "메인 주제를 중심으로 요약문을 작성합니다."},
        {"role": "user", "content": "응답은 trend로 합니다."},
        {"role": "user", "content": "요약된 문장엔 공격적인 단어가 적게 포함되어야 합니다."},

        #답변 제공
        {"role": "assistant", "content": f"context에 포함된 내용을 요약하여 응답합니다. context:{context}"}
        ]
    )

    result = response.choices[0].message.content
    print(result)

#gpt 사용하기 (댓글) /공사중
def comment(context):
    response = client.chat.completions.create(
        #gpt 모댈
        model="gpt-4o-mini",
        #응답 형식
        response_format={ "type": "json_object" },
        #프롬프트 작성 하는 곳
        messages=[
        #응답 형식 요구 ( 대화 방식 지정 )
        {"role": "system", "content": "You are a helpful assistant designed to output JSON."},

        #주문사항
        {"role": "user", "content": "요약된 문장엔 공격적인 단어가 적게 포함되어야 합니다."},

        #답변 제공
        {"role": "assistant", "content": f"context에 포함된 내용을 변환하여 응답합니다. context:{context}"}
        ]
    )

#gpt 사용하기 (질문) /공사중
def autoqna(context):
    response = client.chat.completions.create(
        #gpt 모댈
        model="gpt-4o-mini",
        #응답 형식
        response_format={ "type": "json_object" },
        #프롬프트 작성 하는 곳
        messages=[
        #응답 형식 요구 ( 대화 방식 지정 )
        {"role": "system", "content": "You are a helpful assistant designed to output JSON."},

        #주문사항
        {"role": "user", "content": "문장엔 공격적인 단어가 적게 포함되어야 합니다."},

        #답변 제공
        {"role": "assistant", "content": f"context에 알맞은 답변을 찾아 응답합니다. context:{context}"}
        ]
    )

##태그를 찾아보아요 (1.예시글 2. 타이틀? 문장 1개 이상의 태그가 나와야 함)
def hashtag (context):
    response = client.chat.completions.create(
        #gpt 모댈
        model="gpt-4o-mini",
        #응답 형식
        response_format={ "type": "json_object" },
        #프롬프트 작성 하는 곳
        messages=[
        #응답 형식 요구 ( 대화 방식 지정 )
        {"role": "system", "content": "You are a helpful assistant designed to output JSON."},

        #주문사항
        {"role": "user", "content": "주어진 문장에서 태그를 추출합니다."},
        {"role": "user", "content": "태그는 문장 전체 또는 각 단어에서 추출합니다."},
        {"role": "user", "content": "태그는 문맥에서 가장 중요한걸로 추출합니다."},
        {"role": "user", "content": "고유명사는 중요한 태그일 가능성이 있습니다."},
        {"role": "user", "content": "응답에 최소 1개 이상의 태그가 있어야 합니다."},
        {"role": "user", "content": "모든 태그는 명사입니다."},
        {"role": "user", "content": "응답은 tags로 합니다."},
        {"role": "user", "content": "응답은 tags는 list 입니다."},

        #답변 제공
        {"role": "assistant", "content": f"context에 포함된 내용에서 태그를 추출하여 응답합니다. context:{context}"}
        ]
    )

    #결과
    result = response.choices[0].message.content
        
    print(json.loads(result))

##주제를 분석 해보아요 (간단 태그 검색??)
def 너가무엇을원하는것인지알아야겠다 (context):
    response = client.chat.completions.create(
        #gpt 모댈
        model="gpt-4o-mini",
        #응답 형식
        response_format={ "type": "json_object" },
        #프롬프트 작성 하는 곳
        messages=[
        #응답 형식 요구 ( 대화 방식 지정 )
        {"role": "system", "content": "You are a helpful assistant designed to output JSON."},

        #주문사항
        {"role": "user", "content": "주어진 문장에서 찾고자 하는 것을 유추합니다."},
        {"role": "user", "content": "유추해낸 것은 태그와도 같습니다."},
        {"role": "user", "content": "모든 태그는 명사입니다."},
        {"role": "user", "content": "응답은 tags로 합니다."},
        {"role": "user", "content": "응답은 tags는 list 입니다."},

        #답변 제공
        {"role": "assistant", "content": f"context에 포함된 내용에서 태그를 만들어 응답합니다. context:{context}"}
        ]
    )

    #결과
    result = response.choices[0].message.content
        
    print(json.loads(result))



###글을 작성 해 보아요
def writer(body_data,주제):
    response = client.chat.completions.create(
        #gpt 모댈
        model="gpt-4o-mini",
        #응답 형식
        response_format={ "type": "json_object" },
        #프롬프트 작성 하는 곳
        messages=[
        #응답 형식 요구 ( 대화 방식 지정 )
        {"role": "system", "content": "You are a helpful assistant designed to output JSON."},

        #주문사항
        #{"role": "user", "content": "주어진 게시글들을 요약합니다"},
        {"role": "user", "content": "주제에 맞게 주어진 게시글들을 요약합니다"},
        {"role": "user", "content": f"주제는 {주제}입니다"},
        {"role": "user", "content": "요약문은 5줄 이내로 작성합니다."},
        {"role": "user", "content": "1줄은 대략 35글자 입니다."},
        {"role": "user", "content": "응답은 body_data로 합니다."},
        {"role": "user", "content": "응답의 데이터 타입은 string입니다."},
        {"role": "user", "content": "요약문은 존댓말로 작성합니다."},

        #답변 제공
        {"role": "assistant", "content": f"body_data를 요악하여 반환합니다. body_data:{body_data}"}
        ]
    )

    #결과
    result = response.choices[0].message.content
        
    print(json.loads(result))
#변환(검열)할 텍스트

# trend_context = {
#     'title' : '',
#     'content' : '애플뮤직 주간 TOP 100 8위 (2/3) 지금까지의 순위 (2024년 7월 22일 - 12월 30일)\
#     8 - ? - 5 - 5 - 6 - 5 - 6 - 6 - 8 - 9 - 10 - 11 - 7 - 9 - 10 - 15 - 11 - 14 - 15 - 18 - 1 - 1 - 1 - 2 - \
#     2025년 1월 6일 - 2월 3일 현재 \
#     1 - 1 - 3 - 4 - 8 \
#     2024년 7월 22일 새로 나온 애플 뮤직 클래시컬 차트에 대해서: \
#     이 주간 차트는 165개 이상의 국가로부터 수집한 Apple Music Classical 스트리밍, Apple Music 스트리밍, iTunes 다운로드, iTunes 곡 판매 및 Shazam 태그 등 5가지 데이터 소스를 결합해 클래식 음악의 최신 동향을 종합적으로 보여준다. \
#     클래식 앨범 TOP 100은 매주 월요일 Apple Music Classical 홈 탭에서 업데이트된다. 각 차트에는 전주 금요일부터 목요일까지 1주일간의 활동이 반영된다. \
#     4 \
#     고정닉 0 \
#     실베추공유신고, 댓글 : ',
# }


#테스트용 실행

### 전처리 v1 (단어 뽑아서 처리 후 변환)
# finder_context = {
#     #'title' : 'dkssudgktpdy hello',
#     'content' : '포켓몬 스바 이 새끼 프레임방어되는거맞지? '
# }

# #finder(context=finder_context)
# 이름짓기귀찮은데아무튼찾아낸고유명사랑원본문장 = finder(context=finder_context)
# content = pre_v1(원본 = 이름짓기귀찮은데아무튼찾아낸고유명사랑원본문장['context']['input'], 이거이름뭘로할까 = 이름짓기귀찮은데아무튼찾아낸고유명사랑원본문장['context']['words'])

# reworkd_context = {
#     'title' : '',
#     'content' : f'{content}'
# }
# rework(context=reworkd_context)


# ### 전처리 v2 (ai가 다 함)
# finder_context = {
#     #'title' : 'dkssudgktpdy hello',
#     'content' : 'hello dkssud 안녕하세요 멍한청인지공능 푸하하 dkssudgkek'
# }
# content = pre_v2(finder_context)



#태그내놔
# tag_context = {
#     'content' : '포켓몬 스바 이 새끼 프레임방어되는거맞지?'
# }
# hashtag(context=tag_context)

# rework_context = {
#     'title' : '',
#     'content' : '포켓몬 스바 이 새끼 프레임방어되는거맞지?'
# }
###테스트용 워드백
words_bag=[{
    'word':'유튜브',
    'meaning': '',
},
{
    'word':'발라드',
    'meaning': '서양 고전음악의 한 장르',
},
{
    'word':'노래',
    'meaning': '',
},
{
    'word':'가수',
    'meaning': '노래 부르는 것을 직업으로 삼은 사람',
},
{
    'word':'스바',
    'meaning': '스칼렛 바이올렛',
}]
##변환기
# context = {
#     'content' : '디젤가방이뿌다'
# }
# rework(context=context,words=finder(context=context),word_bag=words_bag)
#<p></p>    <p></p>     <p></p>     <p></p>     <p><br></p>     <p><br></p>
###이거왜 이렇게 많아지는건지 너무 많은데 나중에정리해야겠다 주제파악하기
# title_context = {
#     'content' : '유튜브에 자주 나오는 발라드 노래 가수'
# }

# 너가무엇을원하는것인지알아야겠다(context=title_context)

### 요약기
#실험용 string
body_data=[
    '즐겜모드냐고 물어보는 새끼는 뭐야 나는 언제나 즐겜모드야시발 즐겁지도 않은데 점수올리자고 게임을 하라는거니?? 나는 시발 즐겜해서 이점수왔으니꺼 꼬우면 니가 더 올라가서 안만나면 될거아니야 시발아 니가 여기대보다 잘하는 실력이면 나정도는 충분히 들어 씹새야',
    '공격력팔 너무 마구잡이로 만들어 놓은거 같음 화살통만 몇개씩 추가하더니 정작 아무거나 주워먹는 에이든 말고는 아무도 안써',
    '아군 띠띠는 왜 궁을 나타폰처럼 쓰는걸까 적어도 cc연계는 하고 던져'   ,
    '유스티나 궁 근데 존나 쎄더라 브루저 새끼들 들어오다가 궁 쳐맞으면 반피 날아감',
    '결국엔 브루저루크도 핑퐁위주로 가야할것같은데 결국엔 블탄깡공<<< 이새끼임',
    '니키의 저주에 걸렸음 점수랑 tk는 오르는데 평딜이 수직하락 중임',
    '진짜 개맛없는 1등 한판 했다 1등 하고 45점 먹기',
    '유스티나 너프 심한거아니냐 E벽넘기 추가해줘야 할 거 같은데',#양심없음
    '유스티나가 어케 너프되든 딜이 약한편이 될순 없긴해 사거리 6m대 노cc 메이지라는 족쇄가 좆이 아니라서 결국 딜은 계속 셀거임. 근데 딜이 총성능은 아니니까 성능이 내려갈순 없는건 아니지',
    '시셀라는 동물 어케잡지 큐 두번굴리면 내피가 걸래가',
    '근딜 무기 바꾸니까 너무 헷갈리는데? 사거리랑 공속 바뀌니까 카이팅 느낌이 너무 달라',
    '이겜 뉴비배척 심함? 방금 두 판 하고 왔는데 엄마 토막당함 롤이랑 비슷하노 애들이',
    '히스이 원험으로 어디까지 랭크 갈 수 있을까 해봤는데 한 3시즌 랭크 쉬었더니 답답해서 랭크 못하겤ㅅ음... 걍 골드까지만 이바로 올리고 일망우나 할거인',
    '뎁마 뭔가 해줘픽같아 이리저리 휘젓고 다녀도 결국 판깔기에 지나지 않고 딜러차이로 귀결되는거보면 리턴값이 아쉬운거 같음 어직 깨달음이 부족한걸까',
    '이리가 보호막한테 유독 관대함 보호막 파괴 스킬도 적고 템 잇는거도 보호막 대상 피해 강화임',
    '게임 졸라 스릴넘친다 하루 안했다고 머리 백지되1서 사출 당하다가 데미갓 되고 다시 점수 먹어서 이터달고 존나 스릴넘치네 낭떠러지 끄트머리에서 균형잡기 하는 느낌이야',
    '신캐 찍어내는 꼬라지 보면 이겜은 2만 동접도 과분함 스킬 구상할 때 오타쿠 동아리에서 이러면 존나 사기일듯 ㅋㅋ 하면서 찍어내는 수준이라 ',
    '메테오 못벗어나겠다 갤평티 찍기가 이렇게나 힘들단 말이냐..',
    '일겜에서 탈출하는건 또 간만이네 그럴거면 그냥 머리박는게 낫지않나 싶긴한데',
    '카티야 선픽 나올때마다 게임지네 평원딜 재능없는새끼들이 잡으니까 답이없다 그냥',
    '오늘 랭크했는데 2판 다 내가 실수해서 사출당함 오늘은 날이 아니네',
    '이겜에 티어가 의미가 있다고 생각함?',
    '유스티나 아직 쎈데? 너프 체감이 안됨 물론 쳐맞을때 이야기임',
    '달 시스템 << 누가 만든거냐 솔로시절 보는데 진짜 이게 겜 맞냐? 그당시에 어캐 했는지 모르겠네',
    '바바라 이거 왤캐쎔? 진짜 말도 안되게 쎄네 숙련도 이슈로 그냥 풀피에다 ree 박고 교전 지긴했는데 풀피여도 체력이 그냥 다 사라지는데 이거 맞음??',
    '블붕이들 왤캐 뒤틀려있노,, 당연히 탱커보다 딜러가 어렵잔우,, 0데스 딜량1등 시야점수1등은 탱커가 있든없는 잘한거 맞으니까 10점 더 주자는게 그렇게 아니꼽니',


]
#요약기 실행
writer(body_data=body_data,주제='이터널 리턴')