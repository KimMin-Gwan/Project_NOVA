import pandas as pd
from model.local_database_model import *
import  datetime 
# 검색엔진이 해야하는일

# 1. 키워드를 통한 피드 검색
# 2. 특정 피드 다음으로 제시할 피드 검색
# 3. 피드 분석 및 최신화
# 4. 추천 피드 제공

# 아래는 검색 엔진
class SearchEngine:
    def __init__(self, database:Local_Database):
        self.__feed_algorithm= FeedAlgorithm(database=database)
        self.__search_manager = SearchManager(database=database,self.__feed_algorithm)
        self.__recommand_manager = RecommandManager(database=database,self.__feed_algorithm)
        self.db=database
    def try_serach_feed(self, target_type="hashtag", target = "", num_feed=10 ):

        result = None

        if target_type == "hashtag":   
            result = self.__serach_manager.search_feed_with_hashtag(hashtag=target)
        elif target_type == "feed":
            result = self.__serach_manager.search_feed_with_fid(fid=target)
        elif target_type == "user":
            result = self.__serach_manager.search_feed_with_user(user=target)
        elif target_type == "string":
            result = self.__serach_manager.search_feed_with_string(string=target)
            
        return result

    def try_get_hashtags(self, num_hashtag,target_type="default", user=None, bias=None):
        result = []

        if target_type == "default":
            result = self.__recommand_manager.get_best_hashtags(num_hashtag=num_hashtag)
        elif target_type == "all":
            result = self.__recommand_manager.get_recommand_hashtags(user, bias, num_hashtag)

        return result

    def try_recommand_feed(self, num_hashtag,target_type="default", feed=None, user=None, bias=None):
        result = []

        if target_type == "short":
            
            result = self.__recommand_manager.get_next_feeds(feed, user, num_hashtag)
        elif target_type == "best":
            result = self.__recommand_manager.get_recommand_hashtags(user, bias, num_hashtag)

        return result 
"""
case 1) 첫 page에서 HASH TAG로 좋아요 순으로 보여줘야함
    -get_all_feed() 모든 피드를 가져오고
    -
    -NUM_OF_FEED 갯수만큼 return 해야함
    -이때 날짜는 1주일 1달 3달 6달 1년 2년 .....첫날짜 까지 계속해서 늘려감
    -
"""

class FeedAlgorithm:
    def __init__(self, database:Local_Database):
        self.__now_all_feed=[]
        self.__database=database 
        self.__find_feed=[]
        self.__batch_size=[7,31,91,180,360,720]  #그이후는 시작일짜로 ...
        self.__date_format = "%Y/%m/%d-%H:%M:%S"
    def get_all_feed(self):
        self.__now_all_feed=self.__database.get_all_data(target="fid")
    
    

    
    #start_index는 이전에 내가 return해준index - num_of_feed , 그래야 이어서 돌려줌 
    def get_feed_hashtag_with_times(self,start_index, hashtag:str,num_of_feed=10) :   #맨처음 화면에서 HashTag누르면 실행되는곳, 최신순으로 알맞는 데이터 return 해준다.
        feed_data=[]
        #그냥 HashTag , FEED ID -> Table 있으면 SELECT * FROM FEED ID where HASHTAG = hashtag 
        #이 데이터로 FEED INDEX 가져오면 참좋은데 
        
        self.get_all_feed()  #실행되면 update   
        for item in self.__now_all_feed:
            if hashtag not in item["hashtag"] :
                continue
            else:
                feed_data.append(item)
                
        if start_index<=num_of_feed:
            return (feed_data[start_index:0:-1] ,0)  #FEED_DATA (list)  , INDEX(0)  
        else:
            return (feed_data[start_index:start_index-num_of_feed:-1],start_index-num_of_feed)
    
    
    
    
    
    def get_feed_hashtag_with_likes(self,hashtag:str,num_of_feed=10):  #가장 첫 page에서 hash tag눌렀을때 보여줘야할곳 
        feed_data=[]
        self.get_all_feed()
        now_batch_index=0
        now_time=datetime.now()
        while True:
            if(now_batch_index==len(self.__batch_size)):
                #끝까지 갔는데도 안나오면 그냥 return하자
                #혹시라도 While문 계속 돌수도 있으니까
                feed_data=sorted(feed_data,key = lambda x : x[1], reverse=True)
                break
            
            for item in self.__now_all_feed:
                if hashtag not in item["hashtag"]:  #해쉬태그 없으면 pass
                    continue
                #날짜 형식  안맞는거같아서 바꾸공
                post_date =datetime.datetime.strptime(item["date"],self.__date_fromat)
                #차이나는 만큼 
                delta_days=now_time-post_date

                if delta_days<self.__batch_size[now_batch_index]:
                    like_between_day=item["star"]/(delta_days+1)  #같은 시간이면 divided 0 임
                    feed_data.append(like_between_day)
                    
                if len(feed_data)>=num_of_feed:
                    feed_data=sorted(feed_data,key = lambda x : x[1], reverse=True)[:num_of_feed]
                    break
                else:
                    now_batch_index+=1
        return feed_data
    
    
    def get_feed_with_fid(self,fid,num_of_feed=1) :  #더보기 기능?
        self.get_all_feed()
        feed_data=[]
        for item in self.__now_all_feed:
            if fid == item["fid"]:
                feed_data.append(item)
                break
        return feed_data
    
    
    
    
    def get_feed_with_user(self,uid,num_of_feed=10):  #유저가 작성한 최신순으로
        self.get_all_feed()
        feed_data=[]
        feed_num=0
        for item in reversed(self.__now_all_feed):
            if uid==item["uid"]:
                feed_data.append(item)
                feed_num+=1
            if feed_num==num_of_feed:
                break
        return feed뭔지모르겠
    
    
    
    def get_feed_with_string(self,string,num_of_feeds=10) :  #본문 내용 검색
        self.get_all_feed()
        feed_data=[]
        feed_num=0
        for item in reversed(self.__now_all_feed):
            if string in item["body"]:
                feed_data.append(item)
                feed_num+=1
            if feed_num==num_of_feeds:
                break
        return feed_data
    
    
    
    def get_like_feed(self):  #????뭔지모르겠
        pass





class SearchManager:
    def __init__(self, database,feed_algorithm : FeedAlgorithm):
        self.__database = database
        self.__feed_algorithm=feed_algorithm
        
        
    #type likes, time
    def search_feed_with_hashtag(self, hashtag,search_type="likes", num_feed=10) -> list:
        
        #hash tag로 찾는건데
        #1. 해쉬태그로 좋아요많은순으로
        #2. 해쉬태그로 최신순으로
        #3. 
        if search_type=="likes":
            return self.__feed_algorithm.get_feed_hashtag_with_likes(hashtag,num_feed)  #list만 return
        elif search_type=="time":
            return self.__feed_algorithm.get_feed_hashtag_with_times(여기에 몇번 index까지 했는지,hashtag,num_feed)   #list, index

    def search_feed_with_fid(self, fid, num_feed=10) -> list:   #feed id로 return해주는거 더보기 같음  아마num=1이 맞는거같은데
        return  self.__feed_algorithm.get_feed_with_fid(fid,num_feed)

    def search_feed_with_user(self, user, num_feed=10) -> list:   #User가 작성한 피드 돌려주는거? 
        return  self.__feed_algorithm.get_feed_with_user(user,num_feed)

    def search_feed_with_string(self, string, num_feed=10) -> list:   #본문 내용을 가지고 찾는거같음
        return self.__feed_algorithm.get_feed_with_string(string,num_feed)
    
    
    
    
    
class RecommandManager:
    def __init__(self, database,feed_algorithm):
        self.__database = database
        self.__feed_algorithm = feed_algorithm
    def get_best_hashtags(self, num_hashtag=10) -> list:
        return 

    def get_next_feeds(self, feed, user, num_feed=1) -> list:
        return 

    def get_recommand_hashtags(self, user, bias, num_hashtag=4) -> list:
        return 

    def get_best_feeds(self, num_feed=10) -> list: 
        return 



