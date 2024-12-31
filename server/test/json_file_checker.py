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
            dict_data = {}

            dict_data['fid'] = data['fid']
            dict_data['uid'] = data['uid']
            dict_data['body'] = data['body']
            dict_data['fclass'] = "short"
            dict_data['display'] = 4
            dict_data['date'] = data['date']
            dict_data['nickname'] =data['nickname']
            dict_data['star'] = data['star']
            dict_data['image'] = data['image']
            dict_data['hashtag'] = data['hashtag']
            dict_data['cid'] = []
            dict_data['iid'] = ""
            new_data.append(dict_data)


    with open("./../src/model/local_database/feed.json", 'w',  encoding='utf-8' )as f:
        json.dump(new_data, f, ensure_ascii=False, indent=4)


main()