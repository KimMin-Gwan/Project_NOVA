from openai import OpenAI
#API 키 
client = OpenAI(api_key="###############")

## 현재 자료의 문장이 완성형에 가까워 높은 문장 완성 성능을 보여주는 중
## 커뮤니티에 게시된 자연어들이 제대로 처리 되는지 확인 하려면 완전히 박살난 문장 형식의 글이나 문맥 파악이 불가능한 자료가 필요
## 초성, meme, 축약어 등 사전적 의미가 존재하지 않는 단어 처리 확인 필요
## 욕설로 도배된 자료 처리 확인 필요
## 많은(다양한) 데이터가 필요할 것으로 예상됨


#gpt 사용하기 (본문)
def rework(context):
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
        {"role": "user", "content": "비속어를 유사한 의미의 단어로 교체합니다."},
        {"role": "user", "content": "반말을 모두 존댓말로 교체합니다."},
        {"role": "user", "content": "텍스트에서 전달하고자 하는 의도 또는 의미가 변형되면 안됩니다."},
        {"role": "user", "content": "텍스트의 분위기 또한 파악하여 의미가 변형되지 않도록 해야합니다."},
        {"role": "user", "content": "텍스트는 title과 content로 이루어져 있습니다"},
        {"role": "user", "content": "텍스트의 title은 비어있을 수 있습니다. "},
        {"role": "user", "content": "의미를 파악할 땐 title과 content를 모두 고려합니다."},
        {"role": "user", "content": "텍스트의 title이 비어있을경우 content만 고려합니다."},
        {"role": "user", "content": "응답은 '원본'과 '변환문', 강도로 합니다."},        
        {"role": "user", "content": "응답의 원본과 변환문 또한 title과 content로 구성되어야 합니다."},
        {"role": "user", "content": "title과 content 모두 변환합니다."},
        {"role": "user", "content": "강도는 비속어 또는 욕설이 포함된 경우 2, 비속어는 포함되나 않으나 욕설이 없이 작성된 경우 1, 비속어 또는 욕설이 사용되지 않고 작성 된 경우 0을 반환합니다"},
        {"role": "user", "content": '고유 명사는 변환하지 않습니다.'},
        {"role": "user", "content": "변환된 문장엔 공격적인 단어가 적게 포함되어야 합니다."},

        #답변 제공
        {"role": "assistant", "content": f"context에 포함된 내용을 변환하여 응답합니다. context:{context}"}
        ]

    )
    #결과
    result = response.choices[0].message.content
        
    print(result)

#gpt 사용하기 (트렌드) /공사중
def trand(context):
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
        {"role": "user", "content": "주어진 텍스트를 요약해서 반환합니다."},
        {"role": "user", "content": "주어진 텍스트는 여러개의 텍스트를 가진 리스트입니다."},
        {"role": "user", "content": "리스트 안의 텍스트는 title과 content, conment로 이루어져 있습니다."},
        {"role": "user", "content": "각 텍스트 마다 title과 content, conment를 종합적으로 요약하여 주제를 정합니다."},
        {"role": "user", "content": "가장 많이 나온 주제를 메인 주제로 정합니다."},
        {"role": "user", "content": "그 외 많이 나온 주제를 서브 주제로 정합니다."},
        {"role": "user", "content": "메인 주제를 중심으로 요약문을 작성합니다."},
        {"role": "user", "content": "응답은 trand로 합니다."},
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
    'title' : '',
    'content' : '칸예가 입었으면 더 주목받을텐데 직접 입어라  쫄보새꺄'
}


#테스트용 실행
rework(context=context)
