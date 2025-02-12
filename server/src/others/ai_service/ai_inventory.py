import pandas as pd
from bintrees import AVLTree
from bs4 import Tag
from pandas.core.internals.construction import to_arrays


# 인벤토리 -> 가방 원형
class Inventory:
    def __init__(self):
        self._bag = pd.DataFrame()
        self._tree = AVLTree()
        
class ModifierWord:
    def __init__(self, word="", meaning=[]):
        self.word:str = word
        self.meaning:list = meaning
        self.num_meaning = len(self.meaning)
        
    # dict_data
    def to_dict(self):
        return {
            'word' : self.word,
            'meaning' : self.meaning,
        }
    
    # json 파일 뜯어서 만들 때 쓰는거
    def make_with_dict(self, dict_data:dict):
        return ModifierWord(word=dict_data['word'], meaning=dict_data['meaning'])

class ModifierTag:
    def __init__(self, tag=""):
        self.tag:str = tag

    def to_dict(self):
        return {
            'tag' : self.tag
        }

    def make_with_dict(self, dict_data:dict):
        return ModifierTag(tag=dict_data['tag'])


# AI 단어 가방
class AIWordBag(Inventory):
    def __init__(self):
        super().__init__()
        self._word_tree = AVLTree()
        
    # 초기에 세팅하기
    def __init_inventory(self):
        pass
    
    # 추가
    def add_new_word(self, word:str):
        target_word:ModifierWord = self._word_tree.get(key=word)
        # 없으면 추가할 것
        if not target_word:
            target_word = ModifierWord(word=word)
            self._word_tree.insert(key=word, value=target_word)
        # 단어 데이터 리턴
        return target_word
        
    # 검색
    def search_word(self, word:str):
        result = self._word_tree.get(key=word)
        return result
    
    # 수정
    def modifiy_word(self, word:str, meaning:list):
        target_word:ModifierWord = self._word_tree.get(key=word)
        if not target_word:
            self._word_tree.insert(key=word, value=ModifierWord(word=word, meaning=meaning))
        else:
            target_word.meaning.extend(meaning)
        return
        

# AI 태그 가방
class AITagBag(Inventory):
    def __init__(self):
        super().__init__()
        self._tag_tree = AVLTree()

    def __init_inventory(self):
        pass

    def add_new_tag(self, tag:str):
        target_tag:ModifierTag = self._tag_tree.get(key=tag)
        if not target_tag:
            target_tag = ModifierTag(tag)
            self._tag_tree.insert(key=tag, value=target_tag)

        return target_tag

    def search_tag(self, tag:str):
        result = self._tag_tree.get(key=tag)
        return result

    def modify_tag(self, tag:str, meaning:list):
        target_tag:ModifierTag = self._tag_tree.get(key=tag)
        if not target_tag:
            self._tag_tree.insert(key=tag, value=ModifierTag(tag=tag))
        return




