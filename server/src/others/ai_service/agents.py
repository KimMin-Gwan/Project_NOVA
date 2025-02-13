# 반환되는 데이터에서 원문 데이터를 제외할 것 (돈나감)
from pprint import pprint

import json
from openai import OpenAI

# 기반 키 파라미터
class KeyParam:
    def __init__(self):
        self.set_role()
        self._content = ""
        
    # 바꿀일이 있으면 사용할 것
    def set_role(self, role="assistant"):
        self._role = role
        return
        
    # contnet 초기화
    def _init_content(self, content):
        self._content = content
        return
    
    # content에 핵심 본문 추가(context 추가)
    def set_context(self, context):
        self._content = self._content + context
        return
    
    # 전송에 사용될 dict 데이터 키 파라미터 (답변 내용)
    def get_dict_key_param(self):
        return [{"role":self._role, "content":self._content}]

# 근본 에이전트
class BaseAgent():
    def __init__(self, model_setting):
        self._client = OpenAI(api_key=model_setting.api_key)
        self._model_v = model_setting.model_v
        self._response_format={ "type" : "json_object" }
        self.__system_role = {"role": "system", "content": "You are a helpful assistant designed to output JSON."}
        self._message = []
        self._message.append(self.__system_role)
    
    # query 전송하기(json 버전으로 받기)
    def _make_response_as_json(self, query_data:KeyParam) -> dict:
        self._message.extend(query_data.get_dict_key_param())
        
        response = self._client.chat.completions.create(
            model=self._model_v,
            response_format=self._response_format,
            messages=self._message
        )
        result = response.choices[0].message.content
        return json.loads(result)
        
    # message 초기 세팅
    def _init_message_setting(self, init_query:list):
        self._message.extend(init_query)
        return

class AnalyzerAgent(BaseAgent):
    
    class AnalyizerKeyParam(KeyParam):
        def __init__(self):
            super().__init__()
            self._init_content(content="context를 분석하는 Agent입니다. context:")
            
    def __init__(self, model_setting):
        super().__init__(model_setting=model_setting)
        self.__set_analyzer_prompt()
        self._init_message_setting(init_query=self._analyzer_prompt)
        self.__key_param = self.AnalyizerKeyParam()

    # 주문사항
    def __set_analyzer_prompt(self):
        self._analyzer_prompt = [
            #주문사항
            {"role": "user", "content": "주어진 문장에서 태그를 추출합니다."},
            {"role": "user", "content": "태그는 문장 전체 또는 각 단어에서 추출합니다."},
            {"role": "user", "content": "태그는 문맥에서 가장 중요한걸로 추출합니다."},
            {"role": "user", "content": "고유명사는 중요한 태그일 가능성이 있습니다."},
            {"role": "user", "content": "응답에 최소 1개 이상의 태그가 있어야 합니다."},
            {"role": "user", "content": "모든 태그는 명사입니다."},
            {"role": "user", "content": "응답은 tags로 합니다."},
            {"role": "user", "content": "응답은 tags는 list 입니다."},
        ]

    def extract_proper_tag(self, context):
        self.__key_param.set_context(context)
        return self._make_response_as_json(query_data=self.__key_param)

# 고유명사 찾아내는 Agent
class FinderAgent(BaseAgent):
    
    class FinderKeyParam(KeyParam):
        def __init__(self):
            super().__init__()
            self._init_content(content="context에 포함될 고유명사들을 출력합니다. context:")
        
        # 단일 속성에는 list가 아닌 string으로 넣엏야함
        def set_context(self, context):
            self._content = f"context에 포함될 고유명사들을 출력합니다. context:{context}"
            return           
            
    def __init__(self, model_setting):
        super().__init__(model_setting)
        self.__set_converter_prompt()
        self._init_message_setting(init_query=self._finder_prompt)
        self.__key_param = self.FinderKeyParam()
    
    # 주문사항
    def __set_converter_prompt(self):
        self._finder_prompt = [
            {"role": "user", "content": "문장에서 고유명사를 찾아냅니다."},
            {"role": "user", "content": "의미를 알 수 없는 단어를 고유명사로 취급합니다."},
            {"role": "user", "content": "고유명사가 아닌 경우 응답에 포함하지 않습니다."},
            {"role": "user", "content": "응답은 context로 합니다."},
            {"role": "user", "content": "context에는 input, words가 있습니다."},
            {"role": "user", "content": "words는 list입니다."},
            #{"role": "user", "content": "고유명사가 영어인 경우 알파벳을 모두 분리합니다. "},
            #{"role": "user", "content": "context에는 input, word와 index가 있습니다."},
            #{"role": "user", "content": "input은 입력받은 문장 word는 고유명사 index는 위치입니다."},
            #{"role": "user", "content": "title과 content에서 고유명사의 index 위치를 찾습니다."},
        ]
        return
    
    # 단어 추출
    def extract_proper_noun(self, context):
        self.__key_param.set_context(context=context)
        return self._make_response_as_json(query_data=self.__key_param)
        
        
# 컨버터 Agent
class ConverterAgent(BaseAgent):
    
    class ConverterKeyParam(KeyParam):
        def __init__(self):
            super().__init__()
            
        # 단일 속성에는 list가 아닌 string으로 넣엏야함
        def set_context(self, context):
            self._content = f"context에 포함된 내용을 변환하여 응답합니다. context:{context}"
            return           
        
    def __init__(self, model_setting):
        super().__init__(model_setting)
        self.__set_converter_prompt()
        self._init_message_setting(init_query=self._converter_prompt)
        self.__key_param = self.ConverterKeyParam()
    
    # 주문사항
    def __set_converter_prompt(self):
        self._converter_prompt = [
            #주문사항
            {"role": "user", "content": "비속어를 유사한 의미의 단어로 교체합니다."},
            {"role": "user", "content": "반말을 모두 존댓말로 교체합니다."},
            {"role": "user", "content": "텍스트에서 전달하고자 하는 의도 또는 의미가 변형되면 안됩니다."},
            {"role": "user", "content": "텍스트의 분위기 또한 파악하여 의미가 변형되지 않도록 해야합니다."},
            {"role": "user", "content": "텍스트는 content로 이루어져 있습니다"},
            {"role": "user", "content": "응답은 '변환문'과 강도로 합니다."},        
            {"role": "user", "content": "응답의 변환문은 content로 구성되어야 합니다."},
        
            {"role": "user", "content": "강도는 비속어 또는 욕설이 포함된 경우 2, 비속어는 포함되나 않으나 욕설이 없이 작성된 경우 1, 비속어 또는 욕설이 사용되지 않고 작성 된 경우 0을 반환합니다"}, #작동이 애매함
            {"role": "user", "content": '고유명사는 변환하지 않습니다.'},
            # {"role": "user", "content": '둘 이상의 단어가 합쳐진 단어가 있습니다. 이는 고유명사가 아닙니다.'}, #이상한 단어 분리해서 알아보라고 해보려고 한건데 안되는듯
            # {"role": "user", "content": '둘 이상의 단어가 합쳐진 단어는 해당 단어를 분해하여 어떤 단어가 사용됐는지 파악해 의미가 변하지 않도록 변환합니다.'},
            # {"role": "user", "content": '변환된 문장엔 일베용어가 사용되어선 안됩니다'}, #이거 정리해서 다 알려줘야 되나..?
            {"role": "user", "content": "변환된 문장엔 공격적인 단어가 적게 포함되어야 합니다."},
        ]
        return
    
    def _set_word_content(self, words_bag:list):
        words = []
        for single_word in words_bag:
            words.append(single_word['word'])
        
        additional_prompt = [
            # 02/12 추가 워드백 사용하기
            {"role": "user", "content": f"words:{words}, words 단어를 word_bag 맞게 변환합니다. word_bag:{words_bag} "},
            {"role": "user", "content": "word를 meaning에 맞게 변환합니다."},
        ]
        
        self._message.extend(additional_prompt)
        return
    
    # 컨버팅 시작
    def convert_feed_data(self, words:list, context) -> dict:
        self._set_word_content(words_bag = words)
        self.__key_param.set_context(context=context)
        return self._make_response_as_json(query_data=self.__key_param)
    
    
# 무드 메이커
class MoodMakerAgent(BaseAgent):
    
    class MoodMakerKeyParam(KeyParam):
        def __init__(self):
            super().__init__()
            
        def set_context(self, context):
            self._content = [
                f"context에 포함된 내용을 변환하여 응답합니다. context:{context}",
                "응답의 형식은 다음을 지켜주십시오",
                f"원문 : {context}, mood : 요약해서 나온 mood 결과, mood_reason : 글의 요약을 통해 유추한 결과"
            ]
            return
        
        def get_dict_key_param(self):
            key_param = []
            for content in self._content:
                key_param.append({"role":self._role, "content":content})
            return key_param
            
    def __init__(self, model_setting):
        super().__init__(model_setting)
        self.__set_converter_prompt()
        self._init_message_setting(init_query=self._converter_prompt)
        self.__key_param = self.MoodMakerKeyParam()
    
    # 주문사항
    def __set_converter_prompt(self):
        self._converter_prompt = [
            #주문사항
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
            
        ]
        return
    
    # 컨버팅 시작
    def try_search_mood(self, context):
        self.__key_param.set_context(context=context)
        return self._make_response_as_json(query_data=self.__key_param)
    
    
# 트렌드 메이커
class TrendMakerAgent(BaseAgent):
    
    class TrendMakerKeyParam(KeyParam):
        def __init__(self):
            super().__init__()
            
        def set_context(self, context):
            self._content = [
                f"context에 포함된 내용을 요약하여 응답합니다. context:{context}",
                f"원문 : {context}\
                    trend : [\
                        main_topic : 글을 요약해서 얻은 메인 주제 키워드\
                        sub_topic : 글을 요약해 얻은 서브 주제들\
                    ]\
                    trend_reason : 글의 요약을 통해 유추한 결과를 자세히 서술하는 곳\
                "
            ]
            return
        
        def get_dict_key_param(self):
            key_param = []
            for content in self._content:
                key_param.append({"role":self.__role, "content":content})
            return key_param
            
    def __init__(self, model_setting):
        super().__init__(model_setting)
        self.__set_converter_prompt()
        self._init_message_setting(init_query=self._converter_prompt)
        self.__key_param = self.TrendMakerKeyParam()
    
    # 주문사항
    def __set_converter_prompt(self):
        self._converter_prompt = [
            #주문사항
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
        ]
        return
    
    # 컨버팅 시작
    def try_search_trend(self, context):
        self.__key_param.set_context(context=context)
        return self._make_response_as_json(query_data=self.__key_param)
    