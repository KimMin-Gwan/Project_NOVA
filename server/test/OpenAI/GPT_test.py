import os.path

from openai import OpenAI
import pandas as pd
#API 키

client = OpenAI(api_key="#############################")
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
            {"role": "assistant", "content": f"context에 포함된 내용을 요약하여 응답합니다. context:{context}"},
            {"role": "assistant", "content": f"\
                원문 : {context}\
                trend : [\
                    main_topic : 글을 요약해서 얻은 메인 주제 키워드\
                    sub_topic : 글을 요약해 얻은 서브 주제들\
                ]\
                trend_reason : 글의 요약을 통해 유추한 결과를 자세히 서술하는 곳\
            "}]
    )

    result = response.choices[0].message.content
    print(result)

def mood(context):
    response = client.chat.completions.create(
        # GPT 모델
        model="gpt-4o-mini",
        # 응답 형식
        response_format={ "type": "json_object" },

        messages=[
            #응답 형식 요구 ( 대화 방식 지정 )
            {"role": "system", "content": "You are a helpful assistant designed to output JSON."},

            #주문사항

                # 목적
            {"role": "user", "content": "주어진 텍스트를 요약해서 반환합니다."},

                # 제공 정보 요약
            {"role": "user", "content": "주어진 텍스트는 여러 개의 텍스트를 포함하는 문장입니다."},
            {"role": "user", "content": "리스트 안의 텍스트는 title과 content로 이루어져 있습니다."},
            {"role": "user", "content": "각 텍스트 마다 title과 content를 종합 및 요약해 주제를 정하게 됩니다."},
            {"role": "user", "content": "은어가 포함된 부분은 최대한 표준어로 바꿔 주십시오."},

                # 분석 방법
            {"role": "user", "content": "직역으로 해석하여 감정을 분석하는 경우는 최대한 피해주십시오."},
            {"role": "user", "content": "글에 대한 감정 요약은 최대한 단어의 형식을 띠고, 가장 대표적으로 느껴지는 감정으로 대답해주면 된다."},
            {"role": "user", "content": "커뮤니티 글에서는 제목에 내용을 적고 context에는 의미없는 단어를 넣는 경우가 있다. 따라서, 요약할 때는 제목도 눈여겨보면서 요약하면 좋겠다."},
            {"role": "user", "content": "글에 대한 감정 요약에 대한 이유를 자세하게 설명해 줘."},
            {"role": "user", "content": "글에 대한 응답은 mood로 합니다."},
            {"role": "user", "content": "요약된 문장엔 공격적인 단어가 적게 포함되어야 합니다."},

            # 답변 제공
            {"role": "assistant", "content": f"context에 포함된 내용을 변환하여 응답합니다. context:{context}"},
            {"role": "assistant", "content": f"응답의 형식은 다음을 지켜주십시오."},
            {"role": "assistant", "content": f"\
                원문 : {context}\
                mood : 요약해서 나온 mood 결과,\
                mood_reason : 글의 요약을 통해 유추한 결과\
            "}
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
    result = response.choices[0].message.content
    print(result)

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
    result = response.choices[0].message.content
    print(result)


#변환(검열)할 텍스트
context = {
    'title' : '',
    'content' : '칸예가 입었으면 더 주목받을텐데 직접 입어라  쫄보새꺄'
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

mood_context = {
    "title" : "하 환율 사고나니까 개 나락가네 ㅋㅋㅋㅋㅋㅋㅋㅋㅋ",
    "content" : "개빡친당  벌써 10원이나 내렸누  씁"
}

def get_dataframe():
    df = pd.read_csv("gpt_test_body.csv", encoding='euc-kr', index_col="index")

    grouped_community_df = df.groupby('topic')
    community_dfs = {category : group for category, group in grouped_community_df}
    # for category, group in grouped_community_df:
    #     print(f"\ncategory가 '{category}'인 데이터:")
    # print(community_dfs["기타 국내 드라마 갤러리"])
    data_community_csv = community_dfs[community_dfs['topic'].nunique()]



def gpt_research_trends():
    df = pd.read_csv("gpt_test_body.csv", encoding='euc-kr', index_col="index")

    grouped_community_df = df.groupby('topic')
    community_dfs = {category : group for category, group in grouped_community_df}
    data_community_csv = community_dfs['닌텐도 마이너 갤러리'].to_csv(encoding='euc-kr', index=False)

    # for category, group in grouped_community_df:
    #     print(f"\ncategory가 '{category}'인 데이터:")
    # print(community_dfs["기타 국내 드라마 갤러리"])
    # print(df)

    prompt_text = f"""
    아래의 데이터는 커뮤니티 사이트에서 긁어온 한 페이지의 글에 대한 정보입니다.
    다음의 글들을 통해  현재 어떤 트렌드가 유행하고 있는지 요약해 주십시오.
    현재 body는 글의 제목과 내용이 붙어 있습니다.
    붙여 기재한 이유는 글 제목에 내용을 쓰고, 내용란에는 쓸모없는 내용을 붙이는 경우가 있기 때문입니다. (예시: title='오늘 점심 추천 좀', body='ㅈㄱㄴ')
    {data_community_csv}
"""

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
            {"role": "user", "content": prompt_text},
            # {"role": "user", "content": "주어진 텍스트는 여러개의 텍스트를 가진 리스트입니다."},
            # {"role": "user", "content": "리스트 안의 텍스트는 title과 content로 이루어져 있습니다."},
            # {"role": "user", "content": "각 텍스트 마다 title과 content를 종합 및 요약해 주제를 정하게 됩니다."},

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
            {"role": "assistant", "content": f"답변의 형식은 다음을 꼭 지켜주시길 바랍니다."},
            {"role": "assistant", "content": f"\
                trend : [\
                    main_topic : 글을 요약해서 얻은 메인 주제 키워드\
                    sub_topic : 글을 요약해 얻은 서브 주제들\
                ]\
                trend_reason : 글의 요약을 통해 유추한 결과를 자세히 서술하는 곳\
            "}]
    )


    result = response.choices[0].message.content
    print(result)

def get_research_mood():
    df = pd.read_csv("gpt_test_body.csv", encoding='euc-kr', index_col="index")

    grouped_community_df = df.groupby('topic')
    community_dfs = {category : group for category, group in grouped_community_df}
    data_community_csv = community_dfs['닌텐도 마이너 갤러리'].to_csv(encoding='euc-kr', index=False)

    # for category, group in grouped_community_df:
    #     print(f"\ncategory가 '{category}'인 데이터:")
    # print(community_dfs["기타 국내 드라마 갤러리"])
    # print(df)

    prompt_text = f"""
    아래의 데이터는 커뮤니티 사이트에서 긁어온 한 페이지의 글에 대한 정보입니다.
    다음의 글들을 통해  현재 어떤 트렌드가 유행하고 있는지 요약해 주십시오.
    현재 body는 글의 제목과 내용이 붙어 있습니다.
    붙여 기재한 이유는 글 제목에 내용을 쓰고, 내용란에는 쓸모없는 내용을 붙이는 경우가 있기 때문입니다. (예시: title='오늘 점심 추천 좀', body='ㅈㄱㄴ')
    {data_community_csv}
"""

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
            {"role": "user", "content": prompt_text},
            # {"role": "user", "content": "주어진 텍스트는 여러개의 텍스트를 가진 리스트입니다."},
            # {"role": "user", "content": "리스트 안의 텍스트는 title과 content로 이루어져 있습니다."},
            # {"role": "user", "content": "각 텍스트 마다 title과 content를 종합 및 요약해 주제를 정하게 됩니다."},

            # 주제 분석 방법
            {"role": "user", "content": "텍스트를 읽고 현재 이 커뮤니티의 분위기를 요약해주세요."},
            {"role": "user", "content": "다음부터 나오는 명령들은 위에서 진행한 키워드 요약이 아닌 내용 요약으로 진행해 주세요. "},
            {"role": "user", "content": "가장 대표적인 감정, 분위기로 단어 4개로 요약해주세요"},
            {"role": "user", "content": "요약한 결과에 대한 이유를 작성해야합니다."},
            {"role": "user", "content": "응답은 trend로 합니다."},
            {"role": "user", "content": "요약된 문장엔 공격적인 단어가 적게 포함되어야 합니다."},

            #답변 제공
            {"role": "assistant", "content": f"답변의 형식은 다음을 꼭 지켜주시길 바랍니다."},
            {"role": "assistant", "content": f"\
                mood : 분석한 커뮤니티의 분위기를 요약해서 표시하는 곳입니다.\
                mood_reason : 글의 요약을 통해 유추한 결과를 자세히 서술하는 곳\
            "}
        ]
    )


    result = response.choices[0].message.content
    print(result)


#테스트용 실행
# path = os.path.abspath(os.path.dirname(__file__))
# gpt_research_trends()
get_research_mood()
# mood(context=mood_context)

# trend(context=trend_context)