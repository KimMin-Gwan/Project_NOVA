from openai import OpenAI
#API 키 
client = OpenAI(api_key="여기에_API_키_입력")

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

#gpt 사용하기 (본문)
def rework(context):
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
        {"role": "user", "content": "텍스트는 title과 content로 이루어져 있습니다"},
        {"role": "user", "content": "텍스트의 title은 비어있을 수 있습니다. "},
        {"role": "user", "content": "의미를 파악할 땐 title과 content를 모두 고려합니다."}, #그냥 따로 하는듯
        {"role": "user", "content": "텍스트의 title이 비어있을경우 content만 고려합니다."},
        {"role": "user", "content": "응답은 '원본'과 '변환문', 강도로 합니다."},        
        {"role": "user", "content": "응답의 원본과 변환문 또한 title과 content로 구성되어야 합니다."},
        {"role": "user", "content": "title과 content 모두 변환합니다."},
        {"role": "user", "content": "강도는 비속어 또는 욕설이 포함된 경우 2, 비속어는 포함되나 않으나 욕설이 없이 작성된 경우 1, 비속어 또는 욕설이 사용되지 않고 작성 된 경우 0을 반환합니다"}, #작동이 애매함
        {"role": "user", "content": '고유명사는 변환하지 않습니다.'},
        {"role": "user", "content": '둘 이상의 단어가 합쳐진 단어가 있습니다. 이는 고유명사가 아닙니다.'}, #이상한 단어 분리해서 알아보라고 해보려고 한건데 안되는듯
        {"role": "user", "content": '둘 이상의 단어가 합쳐진 단어는 해당 단어를 분해하여 어떤 단어가 사용됐는지 파악해 의미가 변하지 않도록 변환합니다.'},
        {"role": "user", "content": '변환된 문장엔 일베용어가 사용되어선 안됩니다'}, #이거 정리해서 다 알려줘야 되나..?
        {"role": "user", "content": "변환된 문장엔 공격적인 단어가 적게 포함되어야 합니다."},

        #답변 제공
        {"role": "assistant", "content": f"context에 포함된 내용을 변환하여 응답합니다. context:{context}"}
        ]

    )
    #결과
    result = response.choices[0].message.content
        
    print(result)

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


#변환(검열)할 텍스트
context = {
    'title' : 'dkssudgktpdy',
    'content' : '멍한청인지공능'
}

trend_context = {
    'title' : '',
    'content' : '애플뮤직 주간 TOP 100 8위 (2/3) 지금까지의 순위 (2024년 7월 22일 - 12월 30일)\
    8 - ? - 5 - 5 - 6 - 5 - 6 - 6 - 8 - 9 - 10 - 11 - 7 - 9 - 10 - 15 - 11 - 14 - 15 - 18 - 1 - 1 - 1 - 2 - \
    2025년 1월 6일 - 2월 3일 현재 \
    1 - 1 - 3 - 4 - 8 \
    2024년 7월 22일 새로 나온 애플 뮤직 클래시컬 차트에 대해서: \
    이 주간 차트는 165개 이상의 국가로부터 수집한 Apple Music Classical 스트리밍, Apple Music 스트리밍, iTunes 다운로드, iTunes 곡 판매 및 Shazam 태그 등 5가지 데이터 소스를 결합해 클래식 음악의 최신 동향을 종합적으로 보여준다. \
    클래식 앨범 TOP 100은 매주 월요일 Apple Music Classical 홈 탭에서 업데이트된다. 각 차트에는 전주 금요일부터 목요일까지 1주일간의 활동이 반영된다. \
    4 \
    고정닉 0 \
    실베추공유신고, 댓글 : ',
}


#테스트용 실행
rework(context=context)
