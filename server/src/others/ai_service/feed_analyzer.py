from others.ai_service.agents import ConverterAgent, FinderAgent, AnalyzerAgent
from others.data_domain import Feed, Comment
from others.ai_service.ai_inventory import AIWordBag, ModifierWord, AITagBag
from others.object_storage_connector import HTMLEXtractor, ObjectStorageConnection
from pprint import pprint

class FeedAnalyzer:
    def __init__(self, model_setting):
        self.__model_setting = model_setting
        self.__word_bag = AIWordBag()
        self.__tag_bag = AITagBag()
        pass
    
    def pipeline_when_feed_created(self, feed:Feed, data_payload_body=None):
        
        # 1. 피드에서 단어 골라내기
        # 2. 골라낸 단어랑 같이 컨버터에 넣기
        # 3. 컨버팅된 데이터와 강도를 함께 feed에 넣고 반환
        
        # 4. 게시글을 분석기에 넣기
        # 5. 4.에서 나온 태그들을 준비
        # 6. AIRecommander에서 bias를 찾아서 거기다가 Tag 넣어주기(중복 X)
        
        words = self._word_finder(body=feed.body, word_bag=self.__word_bag)
        
        dict_words = []
        
        for word in words:
            dict_words.append(word.to_dict())
        
        body_content = ""
        
        if feed.fclass == "short":
            body_content = feed.body
            
            result = self._convert_feed(body_content=body_content, words=dict_words)
            #self._analyze_feed(feed=feed, tag_bag=self.__tag_bag)
            
            # 피드 데이터 넣어주기
            feed.reworked_body = result['변환문']
            feed.level = result['강도']
            
        else:
            pprint(data_payload_body)
            body_content = HTMLEXtractor().remove_img_src_data_in_html(html_data=data_payload_body)
            pprint(body_content)
            result = self._convert_feed(body_content=body_content, words=dict_words)
            #self._analyze_feed(feed=feed, tag_bag=self.__tag_bag)
            # 피드 데이터 넣어주기
            feed.p_body = result['변환문']
            # 미리보기를 위해 이것도 만들어 넣어줘야됨
            feed.reworked_body = ObjectStorageConnection().extract_body_n_image(raw_data=result['변환문'])
            feed.level = result['강도']
        
        return  feed
    
    # 새로운 댓글이 생기면 동작하는 파이프라인
    def pipeline_when_comment_created(self, comment:Comment):
        # 1. 코멘트에서 단어 골라내기
        # 2. 골라낸 단어랑 같이 컨버터에 넣기
        # 3. 컨버팅된 데이터와 강도를 함께 Comment에 넣고 반환
        
        # 4.  분석기에 넣기
        # 5. 4.에서 나온 태그들을 준비
        # 6. AIRecommander에서 bias를 찾아서 거기다가 Tag 넣어주기(중복 X)
        
        words = self._word_finder(body=comment.body, word_bag=self.__word_bag)
        
        dict_words = []
        
        for word in words:
            dict_words.append(word.to_dict())
        
        body_content = comment.body
                
        result = self._convert_feed(body_content=body_content, words=dict_words)
        #self._analyze_feed(feed=feed, tag_bag=self.__tag_bag)
                
        # Comment 데이터에 넣어주기
        comment.reworked_body = result['변환문']
        comment.level = result['강도']
        
        return comment
    
    
    # 게시글 분석
    # 전성훈이가 들고오면 여기다가 집어넣으면됨
    # agent 만들고
    def _analyze_feed(self, feed:Feed, tag_bag:AITagBag) -> Feed:
        agent = AnalyzerAgent(model_setting=self.__model_setting)

        result = agent.extract_proper_tag(context=feed.body)

        new_tags = result['tags']

        result_tag = []

        # 태그를 찾아서 가방에 넣기
        for new_tag in new_tags:
            modifier_word:ModifierWord= tag_bag.add_new_tag(tag=new_tag)
            result_tag.append(modifier_word)

        return feed
        
    # 게시글 컨버터
    # 워드 백이 들어가야함
    def _convert_feed(self, body_content, words:list) -> Feed:
        
        # 에이전트 소환
        agent = ConverterAgent(model_setting=self.__model_setting)
        
        # 문장 새로 만들기
        result = agent.convert_feed_data(words=words, context=body_content)
        
        
        return result
        
    # 단어 찾기
    def _word_finder(self, body:str, word_bag:AIWordBag) -> Feed:
        # 에이전트 소환
        agent = FinderAgent(model_setting=self.__model_setting)
        
        # 문장 새로 만들기
        result = agent.extract_proper_noun(context=body)
        
        new_words = result['context']['words']
        # 단어 가방에 집어넣으면 끝
        
        result_word = []
        
        # 단어 찾아서 가방에 넣기
        for new_word in new_words:
            modifier_word:ModifierWord= word_bag.add_new_word(word=new_word)
            result_word.append(modifier_word)
        
        # 찾아낸 단어 리턴
        return result_word
    

