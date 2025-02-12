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

    with open("./../src/model/local_database/feed.json", 'r',  encoding='utf-8' )as f:
        data_list.extend(json.load(f))

        for data in data_list:
            data['reworked_body'] = ''
            data['level'] = 0
            new_data.append(data)
        

    with open("./../src/model/local_database/feed.json", 'w',  encoding='utf-8' )as f:
        json.dump(new_data, f, ensure_ascii=False, indent=4)


main()