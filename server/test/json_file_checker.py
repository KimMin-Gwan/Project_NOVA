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
    uid = "9113-ganp-ga49"
    
    long = 0
    short = 0

    with open("./../src/model/local_database/feed.json", 'r',  encoding='utf-8' )as f:
        data_list.extend(json.load(f))

        for data in data_list:
            if data['uid'] == uid:
                if data['fclass'] == "long":
                    long += 1
                else:
                    short += 1
                    
    print("long : ", long)
    print("short : ", short)


    #with open("./../src/model/local_database/user.json", 'w',  encoding='utf-8' )as f:
        #json.dump(new_data, f, ensure_ascii=False, indent=4)


main()