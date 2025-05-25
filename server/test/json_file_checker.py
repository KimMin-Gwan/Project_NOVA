import json
from pprint import pprint
from random import randint, sample

def main():
    data_list = []
    #dict_data = {
        #"uid" : "",
        #"uname" : "",
        #"age" : "",
        #"email" : "",
        #"gender" : "m",
        #"credit" : 0,
        #"solo_bid" : "",
        #"group_bid" : "",
        #"password" : "sample122",
        #"alert" : [],
        #"like" : [],
        #"my_feed" : [],
        #"my_comment" : [],
        #"active_feed" : []
    #}
    
    new_data= []
    
    options = ["게임", "저챗", "음악", "그림", "스포츠", "시참", "기타"]

    with open("./before.json", 'r', encoding='utf-8') as f:
        data_list = json.load(f)

        for data in data_list:
            # 0개에서 3개의 랜덤 옵션을 선택
            num_tags = randint(0, 3)
            data['tags'] = sample(options, num_tags)
            new_data.append(data)

    with open("./result.json", 'w', encoding='utf-8') as f:
        json.dump(new_data, f, ensure_ascii=False, indent=4)


main()