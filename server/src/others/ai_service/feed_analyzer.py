from others.ai_service.agents import ConverterAgent, FinderAgent, AnalyzerAgent
from others.data_domain import Feed
from others.ai_service.ai_inventory import AIWordBag, ModifierWord, AITagBag
from wheel.cli import tags_f

from src.others.ai_service.ai_inventory import AITagBag


class FeedAnalyzer:
    def __init__(self, model_setting):
        self.__model_setting = model_setting
        pass
    
    # 게시글 분석
    # 전성훈이가 들고오면 여기다가 집어넣으면됨
    # agent 만들고
    def _analyze_feed(self, feed:Feed, tag_bag:AITagBag) -> Feed:
        body = feed.body
        agent = AnalyzerAgent(model_setting=self.__model_setting)

        result = agent.analyze_feed_data(context=feed.body)

        new_tags = result['context']['tags']

        result_tag = []

        # 태그를 찾아서 가방에 넣기
        for new_tag in new_tags:
            modifier_word:ModifierWord= tag_bag.add_new_tag(tag=new_tag)
            result_tag.append(modifier_word)

        return feed
        
    # 게시글 컨버터
    # 워드 백이 들어가야함
    def _convert_feed(self, feed:Feed) -> Feed:
        
        # 에이전트 소환
        agent = ConverterAgent(model_setting=self.__model_setting)
        
        # 문장 새로 만들기
        result = agent.convert_feed_data(context=feed.body)
        
        # 피드 데이터 넣어주기
        feed.reworked_body = result['변환문']
        feed.level = result['강도']
        
        return feed
        
    # 단어 찾기
    def _word_finder(self, feed:Feed, word_bag:AIWordBag) -> Feed:
        # 에이전트 소환
        agent = FinderAgent(model_setting=self.__model_setting)
        
        # 문장 새로 만들기
        result = agent.extract_proper_noun(context=feed.body)
        
        new_words = result['context']['words']
        # 단어 가방에 집어넣으면 끝
        
        result_word = []
        
        # 단어 찾아서 가방에 넣기
        for new_word in new_words:
            modifier_word:ModifierWord= word_bag.add_new_word(word=new_word)
            result_word.append(modifier_word)
        
        # 찾아낸 단어 리턴
        return result_word
    

