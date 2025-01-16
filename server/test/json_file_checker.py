import json
from pprint import pprint

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

    new_data = []

    with open("./../src/model/local_database/feed.json", 'r',  encoding='utf-8' )as f:
        data_list.extend(json.load(f))


        for data in data_list:
            if data['fclass'] == "long":
                data["raw_body"] = data['body']
                data['body'] = "개편 이전의 테스트 용도의 본문 내용 ( 실제 내용과 다름 )"
            else:
                data["raw_body"] = ""

            new_data.append(data)


    with open("./../src/model/local_database/feed.json", 'w',  encoding='utf-8' )as f:
        json.dump(new_data, f, ensure_ascii=False, indent=4)


main()