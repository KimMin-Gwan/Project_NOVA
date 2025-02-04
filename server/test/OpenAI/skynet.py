from openai import OpenAI
#API 키 
client = OpenAI(api_key="#######")

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
        {"role": "user", "content": "강도는 비속어가 포함된 경우 2, 비속어는 포함되지 않으나 반말로 작성된 경우 1, 비속어 나 반말이 사용되지 않고 올바른 문장으로 작성 된 경우 0을 반환합니다"},
        {"role": "user", "content": "변환된 문장엔 공격적인 단어가 적게 포함되어야 합니다."},

        #답변 제공
        {"role": "assistant", "content": f"context에 포함된 내용을 변환하여 응답합니다. context:{context}"}
        ]

    )
    #결과
    result = response.choices[0].message.content
        
    print(result)

#gpt 사용하기 (트렌드)
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

#gpt 사용하기 (댓글)
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

#gpt 사용하기 (질문)
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
    'content' : 'ㅎㅇ'
}


#테스트용 실행
rework(context=context)